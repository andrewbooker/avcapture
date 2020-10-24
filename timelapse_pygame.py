#!/usr/bin/env python

import time
import datetime
import pygame
import pygame.camera
import threading
import readchar
import sys

shouldStop = threading.Event()

class Timelapse():
    def __init__(self):
        pygame.init()
        pygame.camera.init()
        print("starting camera")
        self.camera = pygame.camera.Camera("/dev/video0", (1600,1200), "RGB")
        self.camera.start()
        print("camera initialised")

    def __del__(self):
        self.camera.stop()
        pygame.camera.quit()
        pygame.quit()

    def start(self, shouldStop):
        while not shouldStop.is_set():
            img = self.camera.get_image()            
            f = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H%M%S")
            pygame.image.save(img, "/home/abooker/Pictures/timelapse/%s.jpg" % f)          
            time.sleep(1.0)

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
del timelapse
