from pipython import GCSDevice
from pipython import pitools
import time


class Stage:

    X=None
    Y=None
    Z=None

    __X_Axis=None
    __Y_Axis=None
    __Z_Axis=None

    def __init__(self,XYZStart=(0,0,3.35)):
        Controller = 'E-873'
        self.__X_Axis = GCSDevice(Controller)
        self.__Y_Axis = GCSDevice(Controller)
        self.__Z_Axis = GCSDevice(Controller)

        self.__Z_Axis.ConnectUSB(serialnum='120002962')
        pitools.startup(self.__Z_Axis)
        self.__Z_Axis.SVO( self.__Z_Axis.axes, values=True)
        self.__Z_Axis.FNL(self.__Z_Axis.axes)
        
        self.__X_Axis.ConnectUSB(serialnum='120002968')
        pitools.startup(self.__X_Axis)
        self.__X_Axis.SVO( self.__X_Axis.axes, values=True)
        self.__X_Axis.FNL(self.__X_Axis.axes)
        
        self.__Y_Axis.ConnectUSB(serialnum='120003784')
        pitools.startup(self.__Y_Axis)
        self.__Y_Axis.SVO( self.__Y_Axis.axes, values=True)
        time.sleep(5)

        self.MoveToX(0) 
        self.__Y_Axis.FNL(self.__Y_Axis.axes)
        
        time.sleep(5)
        
        if(XYZStart!=None):
            self.MoveToX( XYZStart[0])
            self.MoveToY( XYZStart[1])
            self.MoveToZ( XYZStart[2])


    def MoveToX(self,x):
        self.__X_Axis.MOV(self.__X_Axis.axes, x)
        self.X=x

    def MoveToY(self,y):
        self.__Y_Axis.MOV(self.__Y_Axis.axes, y)
        self.Y=y

    def MoveToZ(self,z):
        self.__Z_Axis.MOV(self.__Z_Axis.axes, z)
        self.Z=z

    def MoveTo(self,x,y,z):
        self.MoveToX(x)
        self.MoveToY(y)
        self.MoveToZ(z)
        
    def GetAxes(self):
        return(self.__X_Axis, self.__Y_Axis, self.__Z_Axis)
