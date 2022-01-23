#AF funtion, initiate stg and camera object first

import AutoFocusMicroSpheres
from AutoFocusMicroSpheres import AutoFocusMicroSpheres
import AFonSingles
from AFonSingles import AFonSingles
import numpy as np

class CombinedAFMaster:
    
    def __init__(self, cam, stg):
        self.focus = AutoFocusMicroSpheres(cam)
        self.focussingles = AFonSingles(cam)
        self.stg = stg

    def main(self, roundOneStartZVal, roundOneEndZVal, numSweepsFirstRound, numSweepsConvolution):
        
        
        print ("Round one starting Z val: ",roundOneStartZVal)
        print ("Round one ending Z val: ", roundOneEndZVal)

        print("starting cell")
        Zs = np.linspace(roundOneStartZVal,roundOneEndZVal,numSweepsFirstRound)
        autofocusZ = self.focus.Autofocus(Zs, self.stg)
        Zss=Zs
        print("Round 1 Brightest Z value at: " , Zss[autofocusZ])
        print("Image number: ", autofocusZ+1 , "out of ", numSweepsFirstRound, " z-sweeps")



        #Now singles algorithm

        print()
        print("Starting Final Convolution Round")

        finalstartsweep = Zss[autofocusZ] - .05
        finalendsweep = Zss[autofocusZ] + .05

        print ("Convolution Round starting Z val: ",finalstartsweep)
        print ("Convolution Round ending Z val: ", finalendsweep)

        Zs4=np.linspace(finalstartsweep,finalendsweep,numSweepsConvolution)
        zVals, pics= self.focussingles.MakeImageSweepForAF(Zs4, self.stg)

        #now that zsweep is done and images are saved do AF thing to find most in focus
        #returns the value of the z coordinate most in focus

        zValinFocus = self.focussingles.main(pics, zVals)

        print("Final in Focus Value: ", zValinFocus)

        #move stage to the in focus place
        self.stg.MoveToZ(zValinFocus)
