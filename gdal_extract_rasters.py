# -*- coding: utf-8 -*-
"""
Created on Fri Sep 21 11:28:50 2018

@author: derekolson
"""

## import libraries
import os, sys
import numpy 
from osgeo import ogr
from osgeo import gdal

## get point shapefile
shpSource = r"F:\CONUS_datasets\CONUS_boundary\fishnet_conus_10_10.shp"
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName(driverName)

if drv is None:
    print("%s driver not available.\n" % driverName)
else:
    print ("%s driver IS available.\n" % driverName)


shpFile = ogr.Open(shpSource, 0)
print(shpFile)

# get field names in shapefile
layer = shpFile.GetLayer(0)
layerDef = layer.GetLayerDefn()
for i in range(layerDef.GetFieldCount()):
    print(layerDef.GetFieldDefn(i).GetName())

## get rasters
dem = r"F:\CONUS_datasets\NED\ned_conus.img"
inRas = gdal.Open(dem)  
rasExtent = gdal.Info(dem)
print(rasExtent)

# Get raster georeference info
transform = inRas.GetGeoTransform()
xOrigin = transform[0]
yOrigin = transform[3]
pixelWidth = transform[1]
pixelHeight = transform[5]


xmin = -2354694
xmax = 2256456
ymin = 311984
ymax = 3165705

# Specify offset and rows and columns to read
arrayWidth = int((xmax - xmin)/pixelWidth)+1
arrayHeight = int((ymax - ymin)/pixelWidth)+1
tileSize = 1000

xRange = range(0,arrayWidth, tileSize)
yRange = range(0,arrayHeight, tileSize)

for x in xRange:
    xBegin = x    
    xEnd = x+tileSize-1
    if xBegin > arrayWidth:
        xEnd = arrayWidth
    
    for y in yRange:
        yBegin = y
        yEnd = y+tileSize-1
        if yEnd > arrayHeight:
            yEnd = arrayHeight
        #print(xBegin,xEnd,yBegin,yEnd)
        #read in raster by chunk
        rasToArray = inRas.ReadAsArray(xBegin, yBegin, tileSize, tileSize)
        #print(rasToArray)
        if numpy.all(rasToArray == rasToArray[0]):
            pass
        else:
            #print(xBegin,xEnd,yBegin,yEnd)
            #print(rasToArray)
            outRas = dem.split('.')[0]+str(x)+str(y)+'.tif'
            gdal.DEMProcessing(outRas, rasToArray, "TPI")
            #Create memory target raster
            #target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, 1, gdal.GDT_Byte)
            #target_ds.SetGeoTransform((xmin, pixelWidth, 0,ymax, 0, pixelHeight,))


        
        
        
        # Create memory target raster
        #target_ds = gdal.GetDriverByName('MEM').Create('', xcount, ycount, 1, gdal.GDT_Byte)
        #target_ds.SetGeoTransform((xmin, pixelWidth, 0,ymax, 0, pixelHeight,))
        



