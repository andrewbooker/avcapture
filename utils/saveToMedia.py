#!/usr/bin/env python

import os
import sys

mediaDir = sys.argv[1]
toCopy = sys.argv[2]

subDirs = [f.name for f in filter(lambda f: f.is_dir(), os.scandir(mediaDir))]
if len(subDirs) == 0:
    print("No media found in", mediaDir)
    exit()

ontoMedia = os.path.join(mediaDir, subDirs[0])
print("copying onto", ontoMedia)
os.system("cp '%s' '%s'" % (toCopy, ontoMedia))
print("done")

