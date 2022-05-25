"""Compares three concentrations with three points each"""
import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt

#This is the number that it discards images under this value
# (some of the camera images are randomly blanks)
num = -.01e8

#Directory names of the various points for each slide (and name of txt file to use for normalizing)

dir1pt1 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt1/'
dir1pt1NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt1/120.txt'
dir1pt2 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt2/'
dir1pt2NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt2/120.txt'
dir1pt3 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt3/'
dir1pt3NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.1mm/pt3/120.txt'

dir2pt1 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt1/'
dir2pt1NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt1/120.txt'
dir2pt2 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt2/'
dir2pt2NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt2/120.txt'
dir2pt3 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt3/'
dir2pt3NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/0.01mm/pt3/120.txt'

dir3pt1 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt1/'
dir3pt1NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt1/120.txt'
dir3pt2 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt2/'
dir3pt2NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt2/120.txt'
dir3pt3 = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt3/'
dir3pt3NormFile = '/Users/oliviaseidel/Desktop/Everything Grad School/Research/ConcentrationStudies/day3/1mm/pt3/120.txt'


dirname = dir1pt1
dirFile120 = dir1pt1NormFile
data120 = np.loadtxt(dirFile120)
data120 = np.array(data120)
pics120a = np.sum(data120)
files = glob(os.path.join(dirname, '*.txt'))
summedValArr=[]
sum=0
files.sort(key=lambda a: int(''.join(filter(str.isdigit, a))))

for a in files:
    img = np.loadtxt(a)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a = sum - pics120a
    if pics2a < num:
        continue
    else:
        summedValArr.append(pics2a)
dirname1_2 = dir1pt2
dirFile120_2 = dir1pt2NormFile
data120_2 = np.loadtxt(dirFile120_2)
data120_2 = np.array(data120_2)
pics120a_2 = np.sum(data120_2)
files = glob(os.path.join(dirname1_2, '*.txt'))
summedValArr1_2=[]
sum=0
files.sort(key=lambda a2: int(''.join(filter(str.isdigit, a2))))
for a2 in files:
    img = np.loadtxt(a2)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a_2 = sum - pics120a_2
    if pics2a_2 < num:
        continue
    else:
        summedValArr1_2.append(pics2a_2)
dirname1_3 = dir1pt3
dirFile120_3 = dir1pt3NormFile
data120_3 = np.loadtxt(dirFile120_3)
data120_3 = np.array(data120_3)
pics120a_3 = np.sum(data120_3)
files = glob(os.path.join(dirname1_3, '*.txt'))
summedValArr1_3=[]
sum=0
files.sort(key=lambda a3: int(''.join(filter(str.isdigit, a3))))
for a3 in files:
    img = np.loadtxt(a3)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a_3 = sum - pics120a_3
    if pics2a_3 < num:
        continue
    else:
        summedValArr1_3.append(pics2a_3)

dirname2 = dir2pt1
files2 = glob(os.path.join(dirname2, '*.txt'))
dirFile120 = dir2pt1NormFile
data120 = np.loadtxt(dirFile120)
data120 = np.array(data120)
pics120 = np.sum(data120)
summedValArr2=[]
sum=0
files2.sort(key=lambda b: int(''.join(filter(str.isdigit, b))))
summedValArr2=[]
for b in files2:
    img = np.loadtxt(b)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2b = sum - pics120
    if pics2b < num:
        continue
    else:
        summedValArr2.append(pics2b)
dirname2_2 = dir2pt2
dirFile120_2_2 = dir2pt2NormFile
data120_2_2 = np.loadtxt(dirFile120_2_2)
data120_2_2 = np.array(data120_2_2)
pics120a2_2 = np.sum(data120_2_2)
files = glob(os.path.join(dirname2_2, '*.txt'))
summedValArr2_2=[]
sum=0
files.sort(key=lambda a22: int(''.join(filter(str.isdigit, a22))))
for a22 in files:
    img = np.loadtxt(a22)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a2_2 = sum - pics120a2_2
    if pics2a2_2 < num:
        continue
    else:
        summedValArr2_2.append(pics2a2_2)
dirname2_3 = dir2pt3
dirFile120_2_3 = dir2pt3NormFile
data120_2_3 = np.loadtxt(dirFile120_2_3)
data120_2_3 = np.array(data120_2_3)
pics120a2_3 = np.sum(data120_2_3)
files = glob(os.path.join(dirname2_3, '*.txt'))
summedValArr2_3=[]
sum=0
files.sort(key=lambda a23: int(''.join(filter(str.isdigit, a23))))
for a23 in files:
    img = np.loadtxt(a23)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a2_3 = sum - pics120a2_3
    if pics2a2_3 < num:
        continue
    else:
        summedValArr2_3.append(pics2a2_3)


dirname3 = dir3pt1
dirFile120 = dir3pt1NormFile
data120 = np.loadtxt(dirFile120)
data120 = np.array(data120)
pics120b = np.sum(data120)
files3 = glob(os.path.join(dirname3, '*.txt'))
summedValArr3=[]
sum=0
files3.sort(key=lambda c: int(''.join(filter(str.isdigit, c))))
summedValArr3=[]
for c in files3:
    img = np.loadtxt(c)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2c = sum - pics120b
    if pics2c < num:
        continue
    else:
        summedValArr3.append(pics2c)
dirname3_2 = dir3pt2
dirFile120_3_2 = dir3pt2NormFile
data120_3_2 = np.loadtxt(dirFile120_3_2)
data120_3_2 = np.array(data120_3_2)
pics120a3_2 = np.sum(data120_3_2)
files = glob(os.path.join(dirname3_2, '*.txt'))
summedValArr3_2=[]
sum=0
files.sort(key=lambda a32: int(''.join(filter(str.isdigit, a32))))
for a32 in files:
    img = np.loadtxt(a32)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a3_2 = sum - pics120a3_2
    if pics2a3_2 < num:
        continue
    else:
        summedValArr3_2.append(pics2a3_2)
dirname3_3 = dir3pt3
dirFile120_3_3 = dir3pt3NormFile
data120_3_3 = np.loadtxt(dirFile120_3_3)
data120_3_3 = np.array(data120_3_3)
pics120a3_3 = np.sum(data120_3_3)
files = glob(os.path.join(dirname3_3, '*.txt'))
summedValArr3_3=[]
sum=0
files.sort(key=lambda a33: int(''.join(filter(str.isdigit, a33))))
for a33 in files:
    img = np.loadtxt(a33)
    img_arr = np.array(img)
    sum = np.sum(img_arr)
    pics2a3_3 = sum - pics120a3_3
    if pics2a3_3 < num:
        continue
    else:
        summedValArr3_3.append(pics2a3_3)



plt.title("Compare Brightness Different Concentrations Day 2 (04/20)", fontdict = {'fontsize' : 8})
#plt.xlim(0,600)
plt.ylim(0,7e8)

plt.plot(summedValArr3, color="green", label = "1mm")
plt.plot(summedValArr3_2, color="green")
plt.plot(summedValArr3_3, color="green")

plt.plot(summedValArr, color="red",label = "0.1mm")
plt.plot(summedValArr1_2, color="red")
plt.plot(summedValArr1_3, color="red")

plt.plot(summedValArr2, color="blue", label = "0.01mm")
plt.plot(summedValArr2_2, color="blue")
plt.plot(summedValArr2_3, color="blue")

plt.xlabel("Image number")
plt.ylabel("Summed Pixel Brightness")

plt.legend(loc="upper left")
plt.savefig('/Users/oliviaseidel/Desktop/ConcMedHiLoDay3.png',format="png", dpi=1200)
plt.show()



