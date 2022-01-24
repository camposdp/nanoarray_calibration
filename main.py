
import numpy as np
from scipy import ndimage
import preprocessing as pp

if __name__ == "__main__":
    #load image frames
    
    file_name = '0_H20_15h10'
    
    data = np.load(file_name+'.npy')
    #pp.plotGray(data[0]) #plot first frame
    
    #define interval to crop
    interval = [400,1500]
    #average frames and crop it
    img=pp.prepareImage(data,interval)
    
    #plot cropped image in gray scale:
    #pp.plotGray(img)
    
    #Plot histogram to find the background values
    Nbits = 12 #camera resolution = 12 bits
    #max value to plot, to see the whole scale, xmax = x**Nbits - 1
    #pp.plotHistogram(img,Nbits,xmax=600)
    
    #After inspecting the image we got the background threshold
    threshold = 430
    #So we get a binary mask:
    bin_mask = pp.getBinaryMask(img, threshold)
    
    #Apply a dilate opperation to get pixels in the bondaries:
    nI = 2 #number of iteration for dilation    
    bin_mask_dil = ndimage.binary_dilation(bin_mask,iterations=nI)
    #Let's see the mask!
    #pp.plotGray(bin_mask_dil)
    
    #Just for fun let's plot the histogram again with the mask applied:  
    img_noBG = img*bin_mask_dil    
    #pp.plotHistogram(img_noBG,Nbits,xmax=2**Nbits-1)
    
    #If you don't want to dilate just use:
    #img_noBG  = img*bin_mask    
    
    #Number of lines and columns in the image
    N=[6,3]
    #find peaks, some parameters are optional:
    #findPositions(binary_mask,N,dt=200,ht=20,L=80,showPeaks = 'False')
    #dt = distance between peaks
    #ht = height of peaks
    #L = half-size of the square around the ROI
    x, y = pp.findPositions(bin_mask_dil,N,showPeaks = 'False')
    
    #let's see the result:
    pp.plotxyPeaks(img_noBG,x,y)
    
    #now let's average the values from the ROIS
    #define the half-size of the ROI (default = 30)
    #if you want to see all ROIs, set plotROI = 'True'
    mean_values = pp.averageROI(img_noBG,x,y,N,Nbits,roiSz=35,plotROI='False') 
    
    #Save the file
    ext = '_medias'
    np.save(file_name+ext+'.npy',mean_values)
    
    
    
    
    
    
    
