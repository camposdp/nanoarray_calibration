# nanoarray_calibration
Sensibility calibration of a gold nanohole array using images capture by a CCD camera in optical setup. 


- **opentif**: convert TIF images to NPY.

- **visu_images**: this was the first code I was using to visualize the images, find local maxima and average each array (channel). Requires the image to be in npy format (already imported and converted from TIF to npy). 

- **main**: does the same, but functions are encapsulated in preprocessing framework

- **processBatch**: process images in a batch (duh!)

Codes are not as optimized or generic as I wanted to, but they do the work (for now).  
