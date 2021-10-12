from camera import Camera
import subprocess
import numpy as np
import threading
from hamamatsu.dcam import dcam, Stream, copy_frame, ECCDMode
import sys
import time

class CamHamThread:
    def __init__(self,exposure=1, CCDMode='Normal',SensitivityGain=1,BufferLength=10,RunUntil=20000,BufferPath="./buffer/"):
        self.exposure=exposure
        self.CCDMode=CCDMode
        self.BufferLength=BufferLength
        self.SensitivityGain=SensitivityGain
        self.RunUntil=RunUntil
        self.BufferPath=BufferPath
        
        self.ImageID=0
        self.sleeptime=0.05
        self.thr=threading.Thread(target=self.ThreadFunction,args=())
        self.thr.daemon = True
        self.thr.start()
        self.running=True
        time.sleep(5)
        
    def BufferID(self,n=0):
        return (self.ImageID-n)%self.BufferLength

    def ThreadFunction(self):
        with dcam:
            camera = dcam[0]
            with camera:
                camera["exposure_time"] = self.exposure

                if(self.CCDMode=='Normal'):
                    camera['ccd_mode']=ECCDMode.NORMALCCD
                elif(self.CCDMode=='EMCCD'):
                    camera['ccd_mode']=ECCDMode.EMCCD
                camera['readout_speed'] = 1
                camera['sensitivity']=self.SensitivityGain


                with Stream(camera, self.RunUntil) as stream:
                        camera.start()

                        for i, frame_buffer in enumerate(stream):
                            frame = copy_frame(frame_buffer)
                            np.savetxt(self.BufferPath+"buffer"+str(self.BufferID())+'.txt',frame)
                            self.ImageID=self.ImageID+1
                self.running=False
        

    def Snap(self, n):
        if(not self.running):
            print("Camera not running!   Restart it!")
            return False
        returnvec=[]
        for i in range(0,n):
            returnvec.append(self.SnapOne())
        return returnvec
    
    def SnapOne(self,waitforit=True):
        presentbuffer=self.ImageID
        if(waitforit):
            while(self.ImageID==presentbuffer):
                time.sleep(self.sleeptime)
        return np.loadtxt(self.BufferPath+"buffer"+str(self.BufferID())+'.txt')
 
    def GetWholeBuffer(self):
        returnvec=[]
        for i in range(0, self.BufferLength):
            returnvec.append(np.loadtxt(self.BufferPath+"buffer"+str(self.BufferID(i))+'.txt'))
        return returnvec

