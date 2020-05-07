#!/usr/bin/env python

import os

def usableVideoDevices():
    return [(int(f.name[-1:]), 30) for f in filter(lambda f: "video" in f.name, os.scandir("/dev"))]

