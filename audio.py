#!/usr/bin/env python

#pip install soundfile
#pip install sounddevice
#pip install numpy

import queue
import sounddevice as sd
import soundfile as sf
import numpy
import sys

class Callback():
    def __init__(self):
        self.q = queue.Queue()

    def make(self):
        def handle(indata, frames, time, status):
            if status:
                print(status, sys.stderr)

            self.q.put(indata.copy())

        return handle

class RecordAudio():
    def __init__(self, fqfn, deviceIdx):
        self.fqfn = fqfn
        self.deviceIdx = deviceIdx
        self.cb = Callback()

    def start(self, shouldStop):
        with sf.SoundFile(self.fqfn, mode="x", samplerate=44100, channels=1, subtype="PCM_24") as file:
            with sd.InputStream(samplerate=44100, device=self.deviceIdx, channels=1, callback=self.cb.make()):
                while not shouldStop.is_set():
                    file.write(self.cb.q.get())

                print("stopping audio %s" % self.deviceIdx)

deviceIdx = 4

import threading
import keyboard
import os

shouldStop = threading.Event()


recorders = []
recorders.append(RecordAudio(os.path.join(".", "audio0.wav"), deviceIdx))

threads = [threading.Thread(target=r.start, args=(shouldStop,), daemon=True) for r in recorders]

print ("Starting recording. Press 'q' to stop.")
for t in threads:
	t.start()

keyboard.wait("q")
print ("stopping...")
shouldStop.set()

for t in threads:
	t.join()
print("done")
