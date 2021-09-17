from camera import Camera
import subprocess
import numpy as np
import threading
from hamamatsu.dcam import dcam, Stream, copy_frame, ECCDMode
import sys

class CamHamThread:
    def __init__(self,exposure=1, CCDMode='Normal',SensitivityGain=1,BufferLength=10,RunUntil=2000,BufferPath="./buffer/"):
        self.exposure=exposure
        self.CCDMode=CCDMode
        self.BufferLength=BufferLength
        self.SensitivityGain=SensitivityGain
        self.RunUntil=RunUntil
        self.BufferPath=BufferPath
        
        self.ImageID=0
        self.thr=threading.Thread(target=ThreadFunction,args=())
        self.thr.start()
        
    def BufferID(int n=0):
        return (self.ImageID-n)%self.BufferLength

    def ThreadFunction(self):
        with dcam:
            camera = dcam[0]
            with camera:
                camera["exposure_time"] = float(sys.argv[1])

                if(self.CCDMode=='Normal'):
                    camera['ccd_mode']=ECCDMode.NORMALCCD
                elif(self.CCDMode=='EMCCD'):
                    camera['ccd_mode']=ECCDMode.EMCCD
                camera['readout_speed'] = 1
                camera['sensitivity_gain']=self.SensitivityGain


                with Stream(camera, self.RunUntil) as stream:
                        camera.start()

                        for i, frame_buffer in enumerate(stream):
                            frame = copy_frame(frame_buffer)
                            np.savetxt(self.BufferPath+"buffer"+self.BufferID()+'.txt',frame)
                            self.ImageID=self.ImageID+1
   
    def Snap():
        return np.loadtxt(BufferPath+"buffer"+self.BufferID()+'.txt')
    
    def GetWholeBuffer():
        returnvec=[]
        for i in range(0, self.BufferLength):
            returnvec.append(np.loadtxt(self.BufferPath+"buffer"+self.BufferID(i)+'.txt'))
        return returnvec

