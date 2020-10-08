# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 17:34:47 2018

@author: derekolson
"""
###############################################################################
## Import libraries
###############################################################################
import numpy as np
import gdal
import time
start_time = time.time()
###############################################################################
## Load rasters
###############################################################################
segments = gdal.Open('//166.2.126.25/teui1/4_Derek/Zonal_Histogram/segments.img')
ndvi = gdal.Open('//166.2.126.25/teui1/4_Derek/Zonal_Histogram/ndvi.img')

###############################################################################
## Create arrays
###############################################################################
seg_array = np.array(segments.GetRasterBand(1).ReadAsArray())#.flatten()
ndvi_array = np.array(ndvi.GetRasterBand(1).ReadAsArray())#.flatten()
stack = np.array([seg_array,ndvi_array])
###############################################################################
## Create Lists
###############################################################################
seg_list = seg_array.tolist()
ndvi_list = ndvi_array.tolist()

###############################################################################
## Get unique values
###############################################################################
seg_unique = np.unique(seg_array)

###############################################################################
## create dictionaries
###############################################################################
   
R = dict(zip([seg_unique[i] for i in range(seg_unique.shape[0])],[np.nonzero(seg_array==seg_unique[i]) for i in range(seg_unique.shape[0])]))
M = dict(zip(R.keys(),[np.mean(ndvi_array[R[i]]) for i in R.keys()]))

end_time = time.time()
total_time = (end_time - start_time)/60
print(total_time)

