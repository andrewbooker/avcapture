#!/usr/bin/env python

import threading
import keyboard
import os
import datetime
import time
import sys
from utils.video import RecordVideo
from utils.audio import RecordAudio

now = time.time()
newPath = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d/%H_%M_%S")
fnBase = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d_%H%M%S")
fqp = os.path.join(sys.argv[1], newPath)

if not os.path.exists(fqp):
    os.makedirs(fqp)

shouldStop = threading.Event()

video = [(0, 30), (1, 30)]
audio = [4]

recorders = []
for v in video:
	recorders.append(RecordVideo(os.path.join(fqp, "video%d_%s.avi" % (v[0], fnBase)), v[0], v[1]))

for a in audio:
	recorders.append(RecordAudio(os.path.join(fqp, "audio%d_%s.wav" % (a, fnBase)), a))

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
