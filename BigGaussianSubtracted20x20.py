""" Input: a directory with txt data files from a big image sweep, in order.
Subtracts an optimized gaussian from each image based on an initial guess,
removes noise from image and ignores outlier molecules for the gaussian fit.
Output: big image"""

import scipy.optimize as opt
import numpy as np
import pylab as plt
import os

def FrequencyFilterFunction(Shape,FreqCut,FreqCutWidth):
    Filter=lambda x: (0.5+np.tanh((x-FreqCut)/FreqCutWidth)/2.)
    vars=np.arange(0,0.5,0.01)
    Freqs = np.fft.fftfreq(Shape)
    FilterArray=np.zeros([Shape,Shape])
    for i in range(0,Shape):
        for j in range(0,Shape):
            Freq2D=(Freqs[i]**2+Freqs[j]**2)**0.5
            FilterArray[i,j]=Filter(Freq2D)
    return FilterArray

def FFT_Filter(ImageArray, FilterArray):
    FFTed = np.fft.fft2(ImageArray)
    FilteredSlideFFT = FFTed*FilterArray
    return np.abs(np.fft.ifft2(FilteredSlideFFT))

def twoD_Gaussian(xdata_tuple, amplitude, xo, yo, sigma_x, sigma_y, theta, offset):
    (x, y) = xdata_tuple
    xo = float(xo)
    yo = float(yo)
    a = (np.cos(theta)**2)/(2*sigma_x**2) + (np.sin(theta)**2)/(2*sigma_y**2)
    b = -(np.sin(2*theta))/(4*sigma_x**2) + (np.sin(2*theta))/(4*sigma_y**2)
    c = (np.sin(theta)**2)/(2*sigma_x**2) + (np.cos(theta)**2)/(2*sigma_y**2)
    g = offset + amplitude*np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo)
                            + c*((y-yo)**2)))
    return g.ravel()

def ignoreOutLiersFit(image,size):
    # Create x and y indices/meshgrid

    x = np.linspace(0, size-1, size)
    y = np.linspace(0, size-1, size)
    x, y = np.meshgrid(x, y)

    image0 = image.reshape(size*size)
    #redefine super bright pixels just for gaussian fit
    max = np.amax(image0)

    # subtract 25% of max from max
    maxMinusAmount = max - .25 * max
    redefine = maxMinusAmount - .05*maxMinusAmount
    num=0
    for p in image0:
        num+=1
        if p>maxMinusAmount:
            image0[num-1]=maxMinusAmount
        else:
            continue

    # using these values as our initial parameter guess for our gaussian
    initial_guess = (288, 304, 262.19578626, -74, -76, 9, 1954)

    # standard deviation of x and y is usually between 50-90 for working images, and is like 3 for nonworking
    popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), image0, method='trf', p0=initial_guess, maxfev=5000, f_scale=1)

    return popt

def applyFilter(image):
    #image size
    size = 512
    # Create x and y indices/mesh grid
    x = np.linspace(0, size - 1, size)
    y = np.linspace(0, size - 1, size)
    x, y = np.meshgrid(x, y)

    image1 = image.reshape(size * size)

    # using these values as our initial parameter guess for our gaussian
    initial_guess = (288, 304, 262.19578626, -74, -76, 9, 1954)

    # standard deviation of x and y is usually between 50-90 for working images, and is like 3 for nonworking
    popt, pcov = opt.curve_fit(twoD_Gaussian, (x, y), image1, method='trf', p0=initial_guess, maxfev=5000, f_scale=1)

    """ if the standard deviation is small, you probably have a random super bright outlier molecule.
     ignore it for the fit. else, continue"""
    if (abs(popt[4]) < 10):
        print("outlier")
        image11 = image1
        popt2 = ignoreOutLiersFit(image11, size)
        popt = popt2

    '''if its running very very slowly, print these parameters and redefine initial_guess above as the 
    parameters for the first image. What is happening is the curvefit needs to take to many 
    guesses to find the right gaussian, so find the right parameters for one image in the sweep and use
     that for initial guess'''
    #print(popt)

    # use this new set of parameters to make a new 2d gaussian and subtract it from our data
    gaussian_fitted = twoD_Gaussian((x, y), *popt)
    imagesubtracted = image1 - gaussian_fitted
    imagesubtracted = imagesubtracted.reshape(size, size)

    # had .05 at first
    freCut = .4
    frcutwidth = .01
    # shape is shape of image
    FrequencyFilter = FrequencyFilterFunction(size, freCut, frcutwidth)

    fffilter = FFT_Filter(imagesubtracted, FrequencyFilter)

    image2 = imagesubtracted - fffilter
    image2 = image2.reshape(size, size)

    # crop image around gaussian (170,340 is center 1/3 of image where gaussian is)
    image2 = image2[170:340, 200:370]

    return image2

files = []
file_list = os.listdir(r"/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/concentrationsweep13_28BigPlot")
dirname = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/concentrationsweep13_28BigPlot'
for name in file_list:
    files.append(os.path.join(dirname, name))
files = np.asarray(files)
combinedfullImg = []
combinedfullImg = np.asarray(combinedfullImg)
combinedxImg = []
combinedxImg = np.asarray(combinedxImg)
# combine the first two images
# (0 for first round, then 20 and 20+1)
newimage = np.loadtxt(files[0])
newimage = np.asarray(newimage)
newimage = applyFilter(newimage)

secondimage = np.loadtxt(files[1])
secondimage = np.asarray(secondimage)
secondimage = applyFilter(secondimage)

combinedxImg = np.concatenate((newimage, secondimage), 1)
# combine the next 18 or 8 images
# (range 2-10 for 8 more photos)
for x in range(2, 20):
    newimage = np.loadtxt(files[x])
    newimage = np.asarray(newimage)
    newimage = applyFilter(newimage)

    combinedxImg = np.concatenate((combinedxImg, newimage), 1)
combinedfullImg = combinedxImg
# now for the rest (range of 19 bc we have 19 more to add after the first one has been added)
for i in range(1, 20):
    combinedxImg = []
    combinedxImg = np.asarray(combinedxImg)
    # combine the first two images
    # (0 for first round, then 10 and 10+1)
    newimage = np.loadtxt(files[i * 20])
    newimage = np.asarray(newimage)
    newimage = applyFilter(newimage)

    secondimage = np.loadtxt(files[i * 20 + 1])
    secondimage = np.asarray(secondimage)
    secondimage = applyFilter(secondimage)

    combinedxImg = np.concatenate((newimage, secondimage), 1)
    # combine the next 18 or 8 images
    # (range 2-20)
    for x in range(i * 20 + 2, i * 20 + 20):
        newimage = np.loadtxt(files[x])
        newimage = np.asarray(newimage)
        newimage = applyFilter(newimage)
        combinedxImg = np.concatenate((combinedxImg, newimage), 1)
    combinedfullImg = np.concatenate((combinedfullImg, combinedxImg), 0)

pic = np.array(combinedfullImg)
x_label_list = ['0.01', '0.02','0.03','0.04', '0.05','0.06', '0.07','0.08', '0.09', '0.1','0.11', '0.12','0.13','0.14', '0.15','0.16', '0.17','0.18', '0.19', '0.2']
y_label_list = ['0.2','0.19','0.18','0.17','0.16', '0.15','0.14', '0.13','0.12', '0.11','0.1','0.09','0.08','0.07','0.06', '0.05','0.04', '0.03','0.02', '0.01', '0.00']

fig = plt.figure()
plt.imshow(pic,cmap="gray")
plt.clim(0, 70)
plt.xticks(ticks=[170,2*170,3*170,4*170,5*170,6*170,7*170,8*170,9*170,10*170,11*170,12*170,13*170,14*170,15*170,16*170,17*170,18*170,19*170,20*170], labels=x_label_list)

plt.yticks(ticks=[0, 170,2*170,3*170,4*170,5*170,6*170,7*170,8*170,9*170,10*170, 11* 170,12*170,13*170,14*170,15*170,16*170,17*170,18*170,19*170,20*170], labels=y_label_list)
plt.title('Single Molecule Flourecence over O.2mm^2')
plt.ylabel("Distance (mm)")
plt.xlabel("Distance (mm)")
plt.savefig('/Users/oliviaseidel/Desktop/20by20f_scale1.png',format="png", dpi=1200)
plt.show()
