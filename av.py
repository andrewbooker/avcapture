#!/usr/bin/env python

import threading
import datetime
import time
import getpass
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
username = getpass.getuser()
fqp = os.path.join(baseDir, pathBase, pathTime)

if not os.path.exists(fqp):
    os.makedirs(fqp)

video = usableVideoDevices()
audio = UsbAudioDevices().keys()

recorders = []
audioFiles = []
videoFiles = []
for v in video:
    vf = os.path.join(fqp, "video%d_%s.avi" % (v[0], fnBase))
    videoFiles.append(vf)
    recorders.append(RecordVideo(vf, v[0], v[1]))

for a in audio:
    af = os.path.join(fqp, "audio%d_%s.wav" % (a, fnBase))
    audioFiles.append(af)
    recorders.append(RecordAudio(af, a))

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
zipDir = os.path.join(baseDir, pathBase)
ZipFiles().create(zipDir)

from utils.saveToMedia import CopyToMedia
media = CopyToMedia()
media.save("%s.zip" % zipDir, "/media/%s" % username)

if len(videoFiles) == 1:
    mp4 = os.path.join(baseDir, "%s.mp4" % fnBase)
    cmdInVideo = "ffmpeg -i %s" % videoFiles[0]
    cmdInAudio = " ".join(["-i %s" % f for f in audioFiles])
    cmdAudioMix = "-filter_complex \"amix=inputs=%d\"" % len(audioFiles)
    cmdOut = "-b:a 192k -y %s" % mp4
    os.system(" ".join([cmdInVideo, cmdInAudio, cmdAudioMix, cmdOut]))
    media.save(mp4, "/media/%s" % username)

print("done")


