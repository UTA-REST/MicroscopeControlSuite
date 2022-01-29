from matplotlib import pyplot
from skimage import io
import os
import numpy as np
import skimage.io
import skimage.color
import skimage.filters
from matplotlib.pyplot import cm
import scipy.signal
import time

class AFonSingles:
    def __init__(self, cam):
       self.cam = cam

    #saves the zsweep to the AF directory
    def MakeImageSweepForAF(self, Zs, stg, showthem=True):

        # Put the images in this array
        pics=[]
        zVals=[]


        for i in range(0,len(Zs)):

            # Move stage
            stg.MoveToZ(Zs[i])

            #Snap a pic
            pics.append(self.cam.Snap(1)[0])
            zVals.append(Zs[i])

            print(Zs[i])
            time.sleep(1)

        return zVals, pics

    #scipy signals convolve 2d
    #this makes sure it is in greyscale (some of the pics have weird extra things)
    
    def processImage(self, image):
    #image=np.loadtxt(image, delimiter= ' ',dtype=float)
    
        return image

    #creates your kernel and applys it!
    def convolve2D(self, image, kernel,  strides=1):
        # Cross Correlation, flips all of the entrys in the kernal
        kernel = np.flipud(np.fliplr(kernel))

        # Gather Shapes of Kernel that are passed when the kernel is created, the Image shape
        xKernShape = kernel.shape[0]
        yKernShape = kernel.shape[1]
        xImgShape = image.shape[0]
        yImgShape = image.shape[1]

        # Shape of Output Convolution
        xOutput = int(((xImgShape - xKernShape + 2 ) / strides) + 1)
        yOutput = int(((yImgShape - yKernShape + 2 ) / strides) + 1)
        output = np.zeros((xOutput, yOutput))

        # Iterate through image with the kernel and do the kernel thing
        for y in range(image.shape[1]):
            # Exit Convolution
            if y > image.shape[1] - yKernShape:
                break
            # Only Convolve if y has gone down by the specified Strides, strides are set in calling this funct
            if y % strides == 0:
                for x in range(image.shape[0]):
                    # Goes to next row once kernel is out of bounds (you hit end of row)
                    if x > image.shape[0] - xKernShape:
                        break
                    try:
                        # Only Convolve if x has moved by the specified Strides
                        if x % strides == 0:
                            output[x, y] = (kernel * image[x: x + xKernShape, y: y + yKernShape]).sum()
                    except:
                        break
        return output

    def threshold(self, image1):
        # load the image
        image = skimage.io.imread(image1)

        # convert the image to grayscale
        gray_image = skimage.color.rgb2gray(image)

        # blur the image to denoise
        blurred_image = skimage.filters.gaussian(gray_image, sigma=1.0)

        # create a mask based on the threshold
        t = 0.9
        #returns false for all pixel values below the 90% threshold,
        # returns true and shows the ones above 90
        binary_mask = blurred_image > t

        #Do some fancy things to read bianary image and return the number of white pixels
        indices = binary_mask.astype(np.uint8)  # converts to an unsigned byte
        indices *= 255
        #cv2.imshow('Indices', indices)
        numWhitePixels=(indices == 255).sum()

        return numWhitePixels


    def makekernel(self):

        sumkernelval = 0
        array = []
        subarray = []

        for l in range(0, 3):
            for i in range(0, 11):
                subarray.append(-.25)
                sumkernelval += -.25
            array.append(subarray)
            subarray = []
        subarray = []
        for l in range(0, 1):
            for i in range(0, 3):
                subarray.append(-.25)
                sumkernelval += -.25
            for i in range(0, 1):
                subarray.append(0)
                sumkernelval += 0
            for i in range(0, 4):
                subarray.append(1)
                sumkernelval += 1
            for i in range(0, 3):
                subarray.append(-.25)
                sumkernelval += -.25
            array.append(subarray)
        subarray = []
        for l in range(0, 4):
            for i in range(0, 3):
                subarray.append(-.25)
                sumkernelval += -.25

            for i in range(0, 5):
                subarray.append(1)
                sumkernelval += 1
            for i in range(0, 3):
                subarray.append(-.25)
                sumkernelval += -.25
            array.append(subarray)
            subarray = []
        for l in range(0, 3):
            for i in range(0, 11):
                subarray.append(-.25)
                sumkernelval += -.25

            array.append(subarray)
            subarray = []


        array = np.asarray(array)
        kernel = np.array(array)
        return kernel

    def main(self, pics, zVals):

        numWhitePixelsArr = []
        for image in pics:
            #pass the .txt file that cam.snap returns from the made directory
            image = self.processImage(image)
            #kernel = self.makekernel()
            kernel = [[-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25,  0.0,    1.,    1.,    1.,    1.,   -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25,  1.,    1. ,   1.,    1.,    1.,   -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25,  1.,    1.,    1.,    1.,    1.,   -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25,  1.,    1.,    1.,    1.,    1.,   -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25,  1.,    1.,    1.,    1.,    1.,   -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25],
                     [-0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25, -0.25]]

            #output = convolve2D(image, kernel, strides=1)
            output = scipy.signal.convolve2d(image, kernel,
                                  mode='same', boundary='fill')

            pyplot.imsave("onePic.jpg", output, cmap=cm.gray)
            numWhitePixels = self.threshold('onePic.jpg')
            numWhitePixelsArr.append(numWhitePixels)

        numWhitePixelsArr = np.asarray(numWhitePixelsArr)
        print(numWhitePixelsArr)
        maxValIndex = max_index = np.argmax(numWhitePixelsArr, axis=0)
        #the maxvalindex is the index to find in array that saves the z position, return or print that, then go there
        
        zValinFocus = zVals[maxValIndex]

        return zValinFocus