import numpy as np
import time
import pylab
import os
from dcam import *

class CamHamPy:
    
    LastData=[[0,0],[0,0]]
    dcam0=None
    iDevice=0
    
    def __init__(self):
        if Dcamapi.init() is not False:
            dcam = Dcam(self.iDevice)
            if dcam.dev_open() is not False:
                print("Dev open")
                self.dcam0=dcam
            else:
                print('-NG: Dcam.dev_open() fails with error {}'.format(dcam.lasterr()))
        else:
            print('-NG: Dcamapi.init() fails with error {}'.format(Dcamapi.lasterr()))
        if self.dcam0.buf_alloc(1) is not False:
            print("Buffer allocated")
        else:
            print("Problem allocating buffer")
                

    def Snap(self, ExposureTime=0.5,GainMode=0,Sensitivity=1):
        data=self.LastData
        self.dcam0.prop_setvalue(DCAM_IDPROP.EXPOSURETIME,ExposureTime)
        self.dcam0.prop_setvalue(DCAM_IDPROP.DIRECTEMGAIN_MODE,GainMode)
        self.dcam0.prop_setvalue(DCAM_IDPROP.SENSITIVITY,Sensitivity)
        time.sleep(0.1)
        
        if self.dcam0.cap_snapshot() is not False:
            timeout_milisec = int(ExposureTime*2*1000)

            while True:

                if self.dcam0.wait_capevent_frameready(timeout_milisec) is not False:
                    data = self.dcam0.buf_getlastframedata()
                    self.LastData=data
                    break

                dcamerr = self.dcam0.lasterr()
                if dcamerr.is_timeout():
                    print('===: timeout')
                    continue

                print('-NG: Dcam.wait_event() fails with error {}'.format(dcamerr))
                print(' at ' +time.strftime('%I:%M%p on %b %d, %Y'))
                break
        else:
            print('-NG: Dcam.cap_start() fails with error {}'.format(self.dcam0.lasterr()))

           
        return(data)        
    
    def Close(self):
        try:
            self.dcam0.buf_release()
            self.dcam0.dev_close()
        except:
            print("Camera close error... trying to unload API anyway")
        Dcamapi.uninit()
    
    