#!/usr/bin/env python

import sounddevice as sd
import os

def usableAudioDevices():
    usable = {}

    devs = sd.query_devices()
    for d in range(len(devs)):
        dev = devs[d]
        if "USB" in dev["name"] and dev["default_samplerate"] == 44100:
            usable[d] = dev["name"]

    return usable


def usableVideoDevices():
    return [(int(f.name[-1:]), 30) for f in filter(lambda f: "video" in f.name, os.scandir("/dev"))]

    


