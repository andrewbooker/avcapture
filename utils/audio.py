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
        
        device = sd.query_devices()[deviceIdx]
        self.channels = int(device["max_input_channels"])
        self.sampleRate = int(device["default_samplerate"])
        print("%d channels at %d on %s" % (self.channels, self.sampleRate, device["name"]))

    def start(self, shouldStop):
        cb = Callback()
        with sf.SoundFile(self.fqfn, mode="x", samplerate=self.sampleRate, channels=self.channels, subtype="PCM_24") as file:
            with sd.InputStream(samplerate=self.sampleRate, device=self.deviceIdx, channels=self.channels, callback=cb.make()):
                while not shouldStop.is_set():
                    file.write(cb.q.get())

                print("stopping audio %s" % self.deviceIdx)

