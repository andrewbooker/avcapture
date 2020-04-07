#!/usr/bin/env python

import cv2
import os

class RecordVideo():
	def __init__(self, fqfn, deviceIdx):
		self.fn = fqfn
		self.deviceIdx = deviceIdx
	
	def start(self, shouldStop):
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		cap = cv2.VideoCapture(self.deviceIdx)
		out = cv2.VideoWriter(self.fn, fourcc, 30.0, (640, 480))

		while cap.isOpened() and not shouldStop.is_set():
			ret, frame = cap.read()
			if ret==True:
				out.write(frame)
			else:
				break
				
		print("stopping video %d" % self.deviceIdx)
		out.release()
		cap.release()
		
		
		
import threading
import keyboard
shouldStop = threading.Event()


recorders = []
recorders.append(RecordVideo(os.path.join(".", "video0.avi"), 0))
recorders.append(RecordVideo(os.path.join(".", "video1.avi"), 1))

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

