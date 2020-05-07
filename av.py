#!/usr/bin/env python

import threading
import datetime
import time
from utils.video import RecordVideo
from utils.audio import RecordAudio
from utils.availableDevices import *

import os
import sys
parentDir = os.path.dirname(os.getcwd())
sys.path.append(parentDir)
def checkImport(lib):
    if not os.path.exists(os.path.join(parentDir, lib)):
        print("%s library not found." % lib)
        print("please clone github.com/andrewbooker/%s.git into %s" % (lib, parentDir))
        exit()

checkImport("mediautils")
from mediautils.audiodevices import UsbAudioDevices

now = time.time()
pathBase = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d")
pathTime = datetime.datetime.fromtimestamp(now).strftime("%H_%M_%S")
fnBase = datetime.datetime.fromtimestamp(now).strftime("%Y-%m-%d_%H%M%S")

baseDir = sys.argv[1]
username = sys.argv[2]
fqp = os.path.join(baseDir, pathBase, pathTime)

if not os.path.exists(fqp):
    os.makedirs(fqp)

video = usableVideoDevices()
audio = UsbAudioDevices().keys()

recorders = []
for v in video:
	recorders.append(RecordVideo(os.path.join(fqp, "video%d_%s.avi" % (v[0], fnBase)), v[0], v[1]))

for a in audio:
	recorders.append(RecordAudio(os.path.join(fqp, "audio%d_%s.wav" % (a, fnBase)), a))

shouldStop = threading.Event()
threads = [threading.Thread(target=r.start, args=(shouldStop,), daemon=True) for r in recorders]

import readchar
print ("Starting recording. Press 'q' to stop.")
[t.start() for t in threads]
while not shouldStop.is_set():
    c = readchar.readchar()
    if c == "q":
        print("stopping...")
        shouldStop.set()
        [t.join() for t in threads]

from utils.zipfiles import ZipFiles
zipDir = os.path.join(sys.argv[1], pathBase)
ZipFiles().create(zipDir)

from utils.saveToMedia import CopyToMedia
CopyToMedia().save("%s.zip" % zipDir, "/media/%s" % username)

print("done")
    

