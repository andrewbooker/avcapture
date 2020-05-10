#!/usr/bin/env python

import cv2
import time

class RecordVideo():
    def __init__(self, fqfn, deviceIdx, fps):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.cap = cv2.VideoCapture(deviceIdx)
        self.out = cv2.VideoWriter(fqfn, fourcc, float(fps), (640, 480))
        self.deviceIdx = deviceIdx
        while not self.cap.isOpened():
            time.sleep(0.1)
        print("video initialised on", self.deviceIdx)

    def start(self, shouldStop):
        while self.cap.isOpened() and not shouldStop.is_set():
            ret, frame = self.cap.read()
            if ret == True:
                self.out.write(frame)
            else:
                break

        print("stopping video on", self.deviceIdx)
        self.out.release()
        self.cap.release()


