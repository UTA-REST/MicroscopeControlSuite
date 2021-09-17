#!/usr/bin/env python 

from hamamatsu.dcam import dcam, Stream, copy_frame, ECCDMode
import numpy as np
import sys
import os

returnvec=[]

if os.path.exists("out_snap.txt"):   
    os.remove("out_snap.txt")
with dcam:
    camera = dcam[0]
    with camera:
        print(camera.info)
        print(camera['image_width'].value, camera['image_height'].value)

        # Simple acquisition example
        camera["exposure_time"] = float(sys.argv[1])
        
        if(sys.argv[2]=='Normal'):
            camera['ccd_mode']=ECCDMode.NORMALCCD
        elif(sys.argv[2]=='EMCCD'):
            camera['ccd_mode']=ECCDMode.EMCCD
        camera['readout_speed'] = 1



        with Stream(camera, 1) as stream:
                camera.start()

                for i, frame_buffer in enumerate(stream):
                    frame = copy_frame(frame_buffer)
                    np.savetxt('out_snap.txt',frame)
                    print(f"acquired frame #%d/%d: %s", i+1)
                print("finished acquisition")


