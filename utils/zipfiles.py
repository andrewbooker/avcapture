#!/usr/bin/env python

from zipfile import ZipFile, ZIP_DEFLATED
import os


class ZipFiles():
    def create(self, workingDir):
        print ("zipping %s" % workingDir)
        zipName = os.path.basename(workingDir)

        files = {}
        subDirs = filter(lambda f: f.is_dir(), os.scandir(workingDir))
        for d in subDirs:
            files[d.name] = [f.name for f in filter(lambda f: f.is_file(), os.scandir(os.path.join(workingDir, d.name)))]

        os.chdir(workingDir)

        with ZipFile("../%s.zip" % zipName, "w", ZIP_DEFLATED) as zipfile:
            for subDir in files:
                print("writing %s" % subDir)
                [zipfile.write(os.path.join(subDir, f)) for f in files[subDir]]

