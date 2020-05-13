
import os

class CopyToMedia():
    def save(self, toCopy, mediaDir):
        subDirs = [f.name for f in filter(lambda f: f.is_dir(), os.scandir(mediaDir))]
        if len(subDirs) == 0:
            print("No media found in", mediaDir)
            return

        ontoMedia = os.path.join(mediaDir, subDirs[0])
        print("copying", toCopy, "onto", ontoMedia)
        os.system("cp '%s' '%s'" % (toCopy, ontoMedia))
        print("copied")


