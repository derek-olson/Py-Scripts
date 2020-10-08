# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 08:19:56 2018

@author: dolson
"""
###################################################################################################################################
# mosaic with gdal
###################################################################################################################################
# Import libraries
import gdal, glob, subprocess, time
from subprocess import call 

raster_in_path = '//166.2.126.25/teui1/4_Ryan/R8_DEM_pull/lidar_by_state/GA/GA_Georgia_A1_2016/IMG/GA_USGS_1m_all'
vrt_outname = 'dem.vrt'
raster_out_name = 'GA_dem_mosaic.tif'
# Get the start time
start_time = time.time()        

def gdal_mosaic(raster_in_path, vrt_outname, raster_out_name):
    driver = gdal.GetDriverByName("VRT")

    vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear', addAlpha=False)
    vrt = gdal.BuildVRT(raster_in_path + vrt_outname, glob.glob(raster_in_path + '*de.img'), options = vrt_options)

    gdal.Info(vrt)

    driver.CreateCopy(raster_in_path + vrt_outname, vrt)
    gdalTranslate = r'C:\OSGeo4W64\bin\gdal_translate.exe'
    vrt = raster_in_path + vrt_outname
    dst = raster_in_path + raster_out_name
    #cmd = "-ot int16 -outsize 30 30"

    def youCanQuoteMe(item):
        return "\"" + item + "\""

    fullCmd = ' '.join([gdalTranslate, youCanQuoteMe(vrt), youCanQuoteMe(dst)])

    subprocess.call(fullCmd)

gdal_mosaic(raster_in_path, vrt_outname, raster_out_name)

# Get the total time in minutes and seconds
end_time = time.time()
time_minutes = (end_time - start_time) / 60
print(time_minutes, "minutes")
print("--- %s seconds ---" % (time.time() - start_time))



# ###################################################################################################################################
# # clip with gdal
# ###################################################################################################################################
# import ogr, gdal, osr
# from subprocess import call
#
# ## get point shapefile
# shpSource = '//166.2.126.25/teui1/4_Derek/TCA_LTA_Segmentation_Regions_1_2_4_5_8_9/Regions_8_9/R_8_9_LTAs_dissolved_buffer_5miles.shp'
# driverName = "ESRI Shapefile"
# drv = ogr.GetDriverByName(driverName)
#
# if drv is None:
#     print("%s driver not available.\n" % driverName)
# else:
#     print ("%s driver IS available.\n" % driverName)
#
#
# shpFile = ogr.Open(shpSource, 0)
# print(shpFile)
#
# # get field names in shapefile
# #layer = shpFile.GetLayer(0)
# #layerDef = layer.GetLayerDefn()
# #for i in range(layerDef.GetFieldCount()):
# #    print(layerDef.GetFieldDefn(i).GetName())
#
# ## get rasters
# dem = raster_in_path + raster_out_name
# inRas = gdal.Open(dem)
# rasExtent = gdal.Info(dem)
# print(rasExtent)
# prj = inRas.GetProjection()
# srs = osr.SpatialReference(wkt=prj)
#
#
# def youCanQuoteMe(item):
#     return "\"" + item + "\""
#
# gdal_warp = r'C:\OSGeo4W64\bin\gdalwarp.exe'
#
# warpCmd = ' '.join([gdal_warp, '-cutline ' + youCanQuoteMe(shpSource), '-dstalpha', '-of GTIFF', dem, raster_in_path+'dem_clip.tif'])
#
# subprocess.call(warpCmd)



