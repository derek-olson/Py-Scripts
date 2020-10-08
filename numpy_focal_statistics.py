# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 12:11:06 2018

@author: derekolson
"""

 import gdal
 import numpy as np
 from scipy import ndimage
 
 rast_source = '//166.2.126.25/teui1/4_Derek/TCA_LTA_Segmentation_Regions_1_2_4_5_8_9/Topography/TopoComposite_with_R6.img'
 
 srs = gdal.Open(rast_source)
 bands = srs.RasterCount

 for band in range(bands):
     band += 1
     tempBand = srs.GetRasterBand(band)
     tempArray =np.array(tempBand.ReadAsArray())
     if np.isnan(tempArray):
         print(True)
         #focal = ndimage.median_filter(tempArray, size = 5)
         #focal = tempArray
     else:
        break
     
     
     

 