#!/usr/bin/env python

import threading
import keyboard
import os
from utils.video import RecordVideo

shouldStop = threading.Event()


recorders = []
recorders.append(RecordVideo(os.path.join(".", "video0.avi"), 0, 30))
recorders.append(RecordVideo(os.path.join(".", "video1.avi"), 1, 25))

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
