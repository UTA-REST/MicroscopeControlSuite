from PIL import Image
import numpy as np
import pylab as plt
from scipy import  fft
import imageio
import scipy
from scipy.signal import argrelextrema
from scipy.optimize import curve_fit
import os



def NullFilter(XSize, YSize):
    return no.ones(size=(XSize*2,YSize*2))

def FourierFilter(XSize, YSize, passLow=20,passHigh=100,smoothHigh=10,smoothLow=5):
    XX, YY=np.meshgrid(range(-int(YSize/2),int(YSize/2)),range(-int(XSize/2),int(XSize/2)))
    RR=np.sqrt(XX**2+YY**2)

    FilterFunction = lambda R:0.5+np.tanh((R-passLow)/smoothLow)-np.tanh((R-passHigh)/smoothHigh)
    TheFilter=FilterFunction(RR)
    return TheFilter


    


class MicroscopeImage():
    
    Filter=None
    
    AllData=[]
    Image=[]
    FImage=[]
    
    XROI=[]
    YROI=[]
    
    Offset=0    # background level
    XCenter=0   # center of brightness in X 
    YCenter=0   # center of brightness in Y

    def __init__(self, data,CalcParams=True,XROI=-1,YROI=-1):
        self.AllData=data
        if(XROI==-1):
            self.XROI=[0,len(data)]
        else:
            self.XROI=[XROI[0],XROI[1]]
        if(YROI==-1):
            self.YROI=[0,len(data[0])]
        else:
            self.YROI=[YROI[0],YROI[1]]

        self.Image=data[self.XROI[0]:self.XROI[1],self.YROI[0]:self.YROI[1]]
        self.Filter=FourierFilter(len(self.Image),len(self.Image[0]))
        thefft=fft.fftshift(fft.fft2(self.Image))
        FilteredFFT=self.Filter*thefft
        self.FImage=np.abs(fft.ifft2(fft.ifftshift(FilteredFFT)))
        self.GetImageParams()
        

    def GetImageParams(self):
        def ToFit(x,p1,p2,p3,p4):
            return(p1+p2*np.exp(-(x-p3)**2/(2*p4**2)))

        XProj=np.sum(self.Image,axis=0)
        YProj=np.sum(self.Image,axis=1)

        self.Offset=(XProj[0]+XProj[-1]+YProj[0]+YProj[-1])/4

        XProj_offset=XProj-self.Offset
        YProj_offset=YProj-self.Offset

        self.XCenter=sum(XProj_offset*range(len(XProj_offset)))/sum(XProj_offset)
        self.YCenter=sum(YProj_offset*range(len(YProj_offset)))/sum(YProj_offset)

        # comment these out for speed - can restore if we ever need them
        #self.XRMS=np.sqrt(sum(XProj_offset*(range(len(XProj_offset))-self.XCenter)**2)/sum(XProj_offset))
        #self.YRMS=np.sqrt(sum(YProj_offset*(range(len(YProj_offset))-self.YCenter)**2)/sum(YProj_offset))

        
    # Get an image cropped to the center of brightness with half-width ImWidth    
    def GetCroppedImage(self,ImWidth):
            
        XStart=self.XCenter
        YStart=self.YCenter
        
        if(XStart-ImWidth<0):
            XStart=ImWidth
        if(YStart-ImWidth<0):
            YStart=ImWidth
    
        if((len(self.Image)-XStart)<ImWidth):
            XStart=len(self.Image)-ImWidth
        if((len(self.Image[0])-YStart)<ImWidth):
            YStart=len(self.Image[0])-ImWidth
        
        return self.Image[int(YStart-ImWidth):int(YStart+ImWidth),int(XStart-ImWidth):int(XStart+ImWidth)]
    
    # Get an FImage cropped to the center of brightness with half-width ImWidth    
    def GetCroppedFImage(self,ImWidth):
        
        XStart=self.XCenter
        YStart=self.YCenter
        
        if(XStart-ImWidth<0):
            XStart=ImWidth
        if(YStart-ImWidth<0):
            YStart=ImWidth
    
        if((len(self.Image)-XStart)<ImWidth):
            XStart=len(self.Image)-ImWidth
        if((len(self.Image[0])-YStart)<ImWidth):
            YStart=len(self.Image[0])-ImWidth
        
        return self.FImage[int(YStart-ImWidth):int(YStart+ImWidth),int(XStart-ImWidth):int(XStart+ImWidth)]
            
    
class SequenceSettings:
    def __int__(self):
        True

    WindowSig1=4
    WindowSig2=8
    ExtremaSearchFirst=10
    ExtremaSearchLast=10
    ROI=[[0,512],[0,512]]
    imtype='txt'
    TopN=40
    ExclR=10
    
class Sequence:
    
    Images=[]
    Found=[]
    FXSize=0
    FYSize=0
    XSize=0
    YSize=0
    
    def __init__(self, imagepaths,settings=SequenceSettings()):
        self.Images.clear()
        self.settings=settings
        for impath in imagepaths:
            try:
                if(self.settings.imtype=='txt'):
                    data=np.loadtxt(impath)
                elif(self.settings.imtype=='tif'):
                    im = Image.open(impath)
                    data=np.array(im)
            except:
                print("failed to load image at " + impath)
                continue
            self.Images.append(MicroscopeImage(data,True,XROI=self.settings.ROI[0],YROI=self.settings.ROI[1]))   
            #print("loaded image at " + impath)
            
        self.Images=np.array(self.Images)
        self.FXSize=len(self.Images[0].FImage)
        self.FYSize=len(self.Images[0].FImage[0])
        self.XSize=len(self.Images[0].Image)
        self.YSize=len(self.Images[0].Image[0])
                
        self.Found=self.FindExtrema(range(0,self.settings.ExtremaSearchFirst),range(int(len(self.Images)-self.settings.ExtremaSearchLast),len(self.Images)),self.settings.TopN,self.settings.ExclR)
                
            
    
    def MakeGif(self,outpath,Filtered=True,vmin=1500, vmax=12000,cmap='afmhot',dpi=150,therange=[0,-1,0,-1],dur=250):

        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")
        print("Image.py filtered", Filtered)
        for i in range(0,len(self.Images)):
            if(Filtered):
                dat_to_save=self.Images[i].FImage[therange[0]:therange[1]][therange[2]:therange[3]]
            else:
                dat_to_save=self.Images[i].Image[therange[0]:therange[1]][therange[2]:therange[3]]
            
            plt.imsave("./tmp/im_"+str(i).zfill(3)+".png",dat_to_save, vmin=vmin,vmax=vmax,cmap=cmap,dpi=dpi)
            
        #Make the gif
        files=sorted(os.listdir("./tmp"))

        with imageio.get_writer(outpath, mode='I',duration=dur,loop=10000) as writer:
            for filename in files:
                image = imageio.imread("tmp/"+filename)
                writer.append_data(image)

        #for filename in set(files):
            #os.remove("tmp/"+filename)

            
            
    def GetImageSeq(self, indices, Filtered=True):
        ReturnVec=[]
        for i in indices:
            if(Filtered):
                dat=self.Images[i].FImage
            else:
                dat=self.Images[i].Image
            ReturnVec.append(dat)
        return np.array(ReturnVec)
            
    def GetSummedImage(self,ImRange,Filtered=True):
        return sum(self.GetImageSeq(ImRange,Filtered))
        
    def FindExtrema(self,SigRange, BGRange, TopN=40,ExclR=10,Filtered=True):
        FGTotal=sum(self.GetImageSeq(SigRange,Filtered))/len(SigRange)
        BGTotal=sum(self.GetImageSeq(BGRange,Filtered))/len(BGRange)

        extrema=argrelextrema(FGTotal, np.greater)
        Heights=FGTotal[extrema]
        HighestArgs=(-Heights).argsort()
        Found=[]
        index=0
        ExclR2=ExclR**2
        while(len(Found)<TopN and index<len(HighestArgs)):
            Keep=True
            TryCoord=np.array([extrema[1][HighestArgs[index]], extrema[0][HighestArgs[index]]])
            for i in range(0,len(Found)):
                if(sum((TryCoord-Found[i])**2)<ExclR2):
                    Keep=False
                    continue
                if((TryCoord[0]<ExclR) or (TryCoord[1]<ExclR) or (TryCoord[0]>(len(FGTotal)-ExclR)) or (TryCoord[1]>(len(FGTotal[0])-ExclR))):
                    Keep=False
                    continue                                                              
            if(Keep):
                Found.append(TryCoord)
            index=index+1            
        return np.array(Found)
    

    def gaus(self,X,Y,meanX,meanY,sig):
        return (2*3.142*sig**2)**-1*np.exp(-((X-meanX)**2+(Y-meanY)**2)/(2*sig**2))

    def GetWindow(self,spot,sig1=4,sig2=8):
        XSize=self.FXSize
        YSize=self.FYSize
        XX,YY=np.meshgrid(range(0,YSize), range(0,XSize))
        return(self.gaus(XX,YY,self.Found[spot][0],self.Found[spot][1],sig1)-self.gaus(XX,YY,self.Found[spot][0],self.Found[spot][1],sig2))
        
    def GetTimeSeq(self,spot):
        window=self.GetWindow(spot,self.settings.WindowSig1,self.settings.WindowSig2)
        brightnesstrace=[]
        for frame in self.Images:
            brightnesstrace.append(sum(sum(frame.Image*window)))
        return brightnesstrace
    
                
    def StepMetric(self,intensities,scanwindow=5):
        StepHeight=[]
        StepConfidence=[]
        Locs=range(scanwindow,len(intensities)-scanwindow)
        for i in range(scanwindow,len(intensities)-scanwindow):
            before=intensities[i-scanwindow:i]
            after=intensities[i:i+scanwindow]
            StepHeight.append(np.average(before)-np.average(after))
            StepConfidence.append((np.average(before)-np.average(after))/(np.sqrt(np.std(before)*np.std(after))))
            if(np.isnan(StepHeight[-1])):
                StepHeight[-1]=0
        return Locs,StepHeight,StepConfidence
    
    def GetMaxStepHeightDistn(self):
        stepheights=[]
        steppos=[]
        for spot in range(0,len(self.Found)):
            brightnesstrace=self.GetTimeSeq(spot)
            Locs, Steps,Conf=self.StepMetric(brightnesstrace)
            pos=Locs[np.argmax(Steps)]
            height=np.max(Steps)
            stepheights.append(height)
            steppos.append(pos)
        return steppos, stepheights

