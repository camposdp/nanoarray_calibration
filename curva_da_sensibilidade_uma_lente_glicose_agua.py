
import numpy as np
from scipy import ndimage
import preprocessing as pp
import os
import matplotlib.pyplot as plt

def getMetrics(data):
    #load image frames

    #pp.plotGray(data[0]) #plot first frame
    
    #define interval to crop
    interval = [200,1500]
    intervalY = [150,1600]
    #average frames and crop it
    img=pp.prepareImage(data,interval,intervalY)
    
    #plot cropped image in gray scale:
    #pp.plotGray(img)
    
    #Plot histogram to find the background values
    Nbits = 12 #camera resolution = 12 bits
    #max value to plot, to see the whole scale, xmax = x**Nbits - 1
    #pp.plotHistogram(img,Nbits,xmax=600)
    
    #After inspecting the image we got the background threshold
    threshold = 300
    #So we get a binary mask:
    bin_mask = pp.getBinaryMask(img, threshold)
    
    #Apply a dilate opperation to get pixels in the bondaries:
    nI = 2 #number of iteration for dilation
    bin_mask_erod = ndimage.binary_erosion(bin_mask,iterations=nI)    
    bin_mask_dil = ndimage.binary_dilation(bin_mask_erod,iterations=nI*6)
    #Let's see the mask!
    pp.plotGray(bin_mask_dil)
    
    #Just for fun let's plot the histogram again with the mask applied:  
    img_noBG = img*bin_mask_dil    
    #pp.plotHistogram(img_noBG,Nbits,xmax=2**Nbits-1)
    
    #If you don't want to dilate just use:
    #img_noBG  = img*bin_mask    
    
    #Number of lines and columns in the image
    N=[5,3]
    #find peaks, some parameters are optional:
    #findPositions(binary_mask,N,dt=200,ht=20,L=80,showPeaks = 'False')
    #dt = distance between peaks
    #ht = height of peaks
    #L = half-size of the square around the ROI
    x, y = pp.findPositions(bin_mask_dil,N,dt=150,ht=1,L=100,W=100,showPeaks = 'False')
    
    #let's see the result:
    #pp.plotxyPeaks(img_noBG,x,y)
    
    #now let's average the values from the ROIS
    #define the half-size of the ROI (default = 30)
    #if you want to see all ROIs, set plotROI = 'True'
    #valmax = pp.maxROI(img_noBG,x,y,N,Nbits,roiSz=35,plotROI='False') 
    #valsum = pp.sumROI(img_noBG,x,y,N,Nbits,roiSz=35,plotROI='False') 
    #n= 10 #top 10 pixels
    #valtop = pp.topROI(img_noBG,x,y,N,Nbits,n,roiSz=35,plotROI='False')
    #ptop = 50
    #pbot = 5
    
    threshold_apply = 50
    bin_mask_apply = pp.getBinaryMask(img, threshold_apply)
    nI = 1 #number of iteration for dilation
    bin_mask_erod_apply = ndimage.binary_erosion(bin_mask_apply,iterations=nI*1)    
    bin_mask_dil_apply = ndimage.binary_dilation(bin_mask_erod_apply,iterations=nI*2) 
    img_noBG_apply = img*bin_mask_dil_apply    
    #print(np.max(img_noBG_apply))
    valper = pp.averageROI(img_noBG_apply,x,y,N,Nbits,roiSz=20,plotROI='False')
    #valper = pp.percentileROI(img_noBG_apply,x,y,N,Nbits,10,80,roiSz=70,plotROI='False',plotBOX='False')
    #valper=pp.topROI(img_noBG_apply,x,y,N,Nbits,10,roiSz=70,plotROI='False')
    #pp.plotGray(img_noBG_apply)
    #Save the file
    return valper


path = os.getcwd()
#folder = '\\data_raw_alternado'
folder = '\\data_glicose_uma_lente'
prefix_glic = 'GLIC_0_'
prefix_h2o = '0_'
name = '001187'
sufix = '.npy'

file_h2o = '\\'+prefix_h2o+name+sufix
data_h2o=np.load(path+folder+file_h2o)

file_glic = '\\'+prefix_glic+name+sufix
data_glic=np.load(path+folder+file_glic)



glic_arr=np.array(getMetrics(data_glic))   
h2o_arr=np.array(getMetrics(data_h2o))   
  

    
ri = [1.3329,1.3379,1.3444,1.3462,1.3594,1.3774]
ri2 = np.flip(ri)

    




fig, ax = plt.subplots()
dif_indiv = glic_arr-h2o_arr
plt.plot(dif_indiv,'o-')
#plt.plot(ri2,dif_mean2,'o-')

#plt.plot(dif_mean,'o-')
#plt.plot(dif_mean2,'o-')
plt.show()