#!/usr/bin/env python

import cv2

class RecordVideo():
	def __init__(self, fqfn, deviceIdx, fps):
		self.fn = fqfn
		self.deviceIdx = deviceIdx
		self.fps = fps
	
	def start(self, shouldStop):
		fourcc = cv2.VideoWriter_fourcc(*'XVID')
		cap = cv2.VideoCapture(self.deviceIdx)
		out = cv2.VideoWriter(self.fn, fourcc, float(self.fps), (640, 480))

		while cap.isOpened() and not shouldStop.is_set():
			ret, frame = cap.read()
			if ret==True:
				out.write(frame)
			else:
				break
				
		print("stopping video %d" % self.deviceIdx)
		out.release()
		cap.release()


