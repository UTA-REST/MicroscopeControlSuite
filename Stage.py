from pipython import GCSDevice
from pipython import pitools
import scipy
from scipy import optimize
from scipy.interpolate import interp2d
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
        time.sleep(0.5)
        self.__Z_Axis.FNL(self.__Z_Axis.axes)
        time.sleep(2)
        self.__X_Axis.ConnectUSB(serialnum='120002968')
        pitools.startup(self.__X_Axis)
        self.__X_Axis.SVO( self.__X_Axis.axes, values=True)
        time.sleep(2)
        self.__X_Axis.FNL(self.__X_Axis.axes)
        
        self.__Y_Axis.ConnectUSB(serialnum='120003784')
        pitools.startup(self.__Y_Axis)
        self.__Y_Axis.SVO( self.__Y_Axis.axes, values=True)
        time.sleep(10)

        self.MoveToX(0) 
        self.__Y_Axis.FNL(self.__Y_Axis.axes)
        
        time.sleep(10)
        
        if(XYZStart!=None):
            self.MoveToX( XYZStart[0])
            self.MoveToY( XYZStart[1])
            self.MoveToZ( XYZStart[2])

        self.FocalPlane=None

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

    
    def DefineFocalPlane(self,FocalPoints):
        
        xs=FocalPoints[:,0]    
        ys=FocalPoints[:,1]        
        zs=FocalPoints[:,2]        
                 
        # Function of a plane in 2D
        def PlaneFunction(x,y, args):
            return args[0]*x + args[1]*y + args[2]

        # Scalar function to minimize to find best fit plane from focal points
        Minimizefunction = lambda args: sum((zs-PlaneFunction(xs,ys, args))**2)

        # Minimize and find the best fit plane 
        res=optimize.minimize(Minimizefunction,[0,0,0])
        self.FocalPlane= lambda x,y: PlaneFunction(x,y, res.x)
    
    def FocusAt(self,x,y):
        if(self.FocalPlane==None):
            print("No focal plane set! Find focal points and try again")
            return(False) 
        self.MoveToX(x)
        self.MoveToY(y)
        self.MoveToZ(self.FocalPlane(x,y))