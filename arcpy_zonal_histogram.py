# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 13:33:41 2018

@author: derekolson
"""
from dbfread import DBF
import pandas as pd
from pandas import DataFrame
import os, time
import arcpy
from arcpy import env
from arcpy.sa import *
env.workspace = "//166.2.126.25//teui1/4_Derek/Zonal_Histogram"

start_time = time.time()

raster = '//166.2.126.25//teui1/4_Derek/Zonal_Histogram/ndvi.img'
zonfield = 'Value'

for root, dirs, files, in os.walk('//166.2.126.25//teui1/4_Derek/Zonal_Histogram'):
    for file in files:
        if file.endswith('r.img'):
            zoneRas = root+'/'+file
            print(zoneRas)
            outName = file.split('.')[0] + '_histogram.dbf'
            print(outName)
            outTable =    root+'/'+outName
            print(outTable)
            outZonHisto = ZonalHistogram(zoneRas, zonfield, raster, outTable)
            

end_time = time.time()
time_minutes = (end_time - start_time) / 60
            
# Read in the DBF files and convert to pandas dataframe            
table = DBF('//166.2.126.25//teui1/4_Derek/Zonal_Histogram/Segments_Raster_histogram.dbf')
df = DataFrame(iter(table))


# Add the frequencies found
# Divide the frequency for each bin by the total frequency
# Divide 100 by the total frequency
# Multiply the numerator of each fraction in step 3 by the quotient in step 4
# Sum the results cumulatively. That is, add the first two numbers, the first three and so on until you have added them all. These are the percentiles for upper number in each bin

# Format the data
# Get quantile
 
df.quantile(.25)
