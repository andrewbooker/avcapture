#!/usr/bin/env python

#pip install opencv-python


import datetime
import pygame
import pygame.camera
import time
import sys
import os

outDir = sys.argv[1]
req = int(sys.argv[2]) if len(sys.argv) > 2 else 10
tsDir = os.path.join(outDir, datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H%M%S"))
os.mkdir(tsDir)


pygame.init()
pygame.camera.init()
cams = pygame.camera.list_cameras()
if len(cams) > 0:
    print("starting camera")
    camera = pygame.camera.Camera(cams[0], (1920,1080), "RGB")
    camera.start()
    print("camera initialised")

    f = 0
    while f < req:
        img = camera.get_image()
        pygame.image.save(img, os.path.join(tsDir, "%04d.bmp" % f))
        f += 1
        time.sleep(1)

    print("stopping camera")
    camera.stop()
pygame.camera.quit()
pygame.quit()

