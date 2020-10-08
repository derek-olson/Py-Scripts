# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 15:51:07 2018

@author: derekolson
"""

import arcpy
from arcpy.sa import *

arcpy.env = 'C:/Users/derekolson/Downloads/'

rast = 'C:/Users/derekolson/Downloads/SC_Landsat_SR_1984_2018_190_250_lcmsCONUS_mtbs_tdom.tif'

out_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_DSM_Data/'

d = arcpy.Describe(rast)
nBands = d.bandCount
outRasName = rast.split("/")[-1]
outRasName = outRasName.split('.')[0]
for band in range(1, nBands+1):
    bandRas = arcpy.Raster("{}\\Band_{}".format(rast, band))
    #outFocalStat = FocalStatistics(bandRas, NbrRectangle(5, 5, 'CELL'), 'MEAN', 'Data')
    #outFocalStat.save(out_path + outRasName + str(band) + '.img')
    #out_ras = Con(IsNull(bandRas), FocalStatistics(bandRas, NbrRectangle(5,5, "CELL"), "MEAN"), bandRas)
    out_ras = Con(bandRas==0, FocalStatistics(bandRas, NbrRectangle(5,5, "CELL"), "MEAN"), bandRas)
    out_ras.save(out_path + outRasName + str(band) + '.img')