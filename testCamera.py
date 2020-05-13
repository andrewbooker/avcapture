#!/usr/bin/env python

import cv2
import time

class ShowCamera():
    def __init__(self, deviceIdx):
        self.deviceIdx = deviceIdx
        self.camera = cv2.VideoCapture(deviceIdx)
        while not self.camera.isOpened():
            time.sleep(0.1)
            
    def start(self):
        print("starting camera... (press ESC to quit)")
        while self.camera.isOpened():
            ret, frame = self.camera.read()
            if not ret or cv2.waitKey(1) == 27:
                break

            cv2.imshow("Camera %d" % self.deviceIdx, frame)

        print("stopping camera")


ShowCamera(0).start()
