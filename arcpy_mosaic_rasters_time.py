# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 08:19:56 2018

@author: dolson
"""
###################################################################################################################################
# Import Libraries
###################################################################################################################################
import arcpy
import time
# import psutil

###################################################################################################################################
# Mosaic Images
###################################################################################################################################
# Get the start time
start_time = time.time()

# set the workspace
arcpy.env.workspace = r"\\166.2.126.25\teui1\4_Derek\Region_8_Topographic_Derivatives\AR\AR_DEMs"

# Set location of rasters to mosaic
path = r"\\166.2.126.25\teui1\4_Derek\Region_8_Topographic_Derivatives\AR\AR_DEMs"

# Get a list of the rasters to mosaic
rasterList = arcpy.ListRasters("*", "TIF")

# set the out raster name
outRas = "AR_mosaic.img"

# Mosaic the rasters
arcpy.MosaicToNewRaster_management(input_rasters = rasterList, output_location = path, raster_dataset_name_with_extension = outRas, pixel_type = "32_BIT_Float", cellsize= "1", number_of_bands= "1")

# Get the total time in minutes and seconds
end_time = time.time()
time_minutes = (end_time - start_time) / 60
print(time_minutes, "minutes")
print("--- %s seconds ---" % (time.time() - start_time))

# ###################################################################################################################################
# # Clip to HT admin bound
# ###################################################################################################################################
# # Get the start time
# start_time2 = time.time()
#
# # Get the raster to be clipped
# clipRas = path + outRas
#
# # Get the admin bound
# clipShp = "F:/HT_LTA_Development/Imagery/Landsat/AdminBound/AdminBound.shp"
#
# # Set the output image name
# clipOut = clipRas.split(".")[0] + "adminBound.img"
#
# # Clip the image
# arcpy.Clip_management(clipRas, "#" , clipOut, clipShp, "#", "ClippingGeometry", "NO_MAINTAIN_EXTENT")
#
# # Get the total time in minutes and seconds
# end_time2 = time.time()
# time_minutes = (end_time2 - start_time2) / 60
# print(time_minutes, "minutes")
# print("--- %s seconds ---" % (time.time() - start_time2))
#
# ###################################################################################################################################
# # mosaic with gdal
# ###################################################################################################################################
# # Import libraries
# import gdal, glob, os, subprocess, time
# from subprocess import call
#
# # Get the start time
# start_time = time.time()
#
# outNameList = list()
# fileList = list()
# for root, dirs, files in os.walk('F:/HT_LTA_Development/Imagery/Landsat/ToMosaic'):
#     for file in files:
#         if file.endswith('.tif'):
#             fileName = os.path.join(root, file)
#             fileList.append(fileName)
#
#
# driver = gdal.GetDriverByName("VRT")
#
# vrt_options = gdal.BuildVRTOptions(resampleAlg='nearest', addAlpha=False)
# vrt = gdal.BuildVRT('F:/HT_LTA_Development/Imagery/Landsat/ToMosaic/temp.vrt', glob.glob("F:/HT_LTA_Development/Imagery/Landsat/ToMosaic/*.img"), options = vrt_options)
#
# gdal.Info(vrt)
#
# driver.CreateCopy('E:/Data/HT_Landsat_Mosaic_Data_from_GEE/temp4.vrt', vrt)
# gdalTranslate = r'C:\OSGeo4W64\bin\gdal_translate.exe'
# vrt = "F:/HT_LTA_Development/Imagery/Landsat/ToMosaic/temp.vrt"
# dst = "F:/HT_LTA_Development/Imagery/Landsat/ToMosaic/gdalMosaic.tif"
# cmd = "-ot int16 -outsize 30 30"
#
#
# def youCanQuoteMe(item):
#     return "\"" + item + "\""
#
#
# fullCmd = ' '.join([gdalTranslate, youCanQuoteMe(vrt), youCanQuoteMe(dst)])
#
# subprocess.call(fullCmd)
#
# # Get the total time in minutes and seconds
# end_time = time.time()
# time_minutes = (end_time - start_time) / 60
# print(time_minutes, "minutes")
# print("--- %s seconds ---" % (time.time() - start_time))
#
# # Write times to text file
# text_file = open("F:/HT_LTA_Development/Imagery/Landsat/ToMosaic/Raster_Mosaic_Time.txt", "w")
# text_file.write("Mosaic Time: %s" % time_minutes)
# text_file.close()






