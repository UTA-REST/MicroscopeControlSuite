from camera import Camera
import subprocess
import numpy as np

class CamHam:
    def __init__(self,exposure=1, CCDMode='Normal'):
        self.exposure=exposure
        self.CCDMode=CCDMode

    def Snap(self, N):
        returnvec=[]
        for ni in range(0,N):
            subprocess.run("python hamsnap.py " + str(self.exposure) + " " + self.CCDMode)
            try:
                returnvec.append(np.loadtxt("out_snap.txt"))
            except:
                print("Problem with camera! No image acquired")
        return returnvec
