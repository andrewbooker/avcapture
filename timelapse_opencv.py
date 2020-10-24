#!/usr/bin/env python

import time
import datetime
import cv2
import threading
import readchar
import sys

shouldStop = threading.Event()

class Timelapse():
    def __init__(self):
        print("starting camera")
        self.camera = cv2.VideoCapture(0);
        self.camera.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y', 'U', 'Y', 'V'))
        #self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
        #self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        while not self.camera.isOpened():
            time.sleep(0.1)
        print("camera initialised")

    def __del__(self):
        if self.camera is not None:
            self.camera.release()

    def start(self, shouldStop):
        while not shouldStop.is_set():
            ret, img = self.camera.read()
            f = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H%M%S")
            try:
                cv2.imwrite("/home/abooker/Pictures/timelapse/%s.bmp" % f, img)
            except:
                sys.stdout.write("%s: could not save image\r\n" % f)
            time.sleep(1.0)

        self.camera.release()
        self.camera = None


timelapse = Timelapse()
th = threading.Thread(target=timelapse.start, args=(shouldStop,), daemon=True)
th.start()
print("Started. Press 'q' to exit")
while not shouldStop.is_set():
    c = readchar.readchar()
    if c == "q":
        shouldStop.set()
        done = True

th.join()
