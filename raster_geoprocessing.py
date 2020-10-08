#-------------------------------------------------------------------------------
# Name:        Raster Geoprocessing
# Purpose:
#
# Author:      derekolson
#
# Created:     11/05/2018
# Copyright:   (c) derekolson 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()

#IMPORT LIBRARIES
from osgeo import _gdal,
import osr
import ogr
import shutil, os, subprocess, sys, string, random, math, time, itertools, urllib
import scipy, numpy
import arcpy
import gdal

#reproject = TRUE
#resample = TRUE
#clip = TRUE

#INDICATE THE LOCATION OF THE RASTERS TO PROCESS
path = ("//166.2.126.25/teui1/4_Dan/BridgerTeton/Rasters")
gdal.AllRegister()
#INDICATE THE OUTPUT CELL RESOLUTION FOR ALL RASTERS
res = 30

#DEFINE THE PROJECTION TO USE FOR ALL RASTERS
projection =

#REPROJECT ALL RASTERS IF THIER PROJECTIONS DIFFERFROM THE SPECIFIED PROJECTION

#get EPSG
ds=gdal.Open(path)
prj=ds.GetProjection()
print prj

srs=osr.SpatialReference(wkt=prj)
if srs.IsProjected:
    print srs.GetAttrValue('projcs')
print srs.GetAttrValue('geogcs')

#reads the WKT representation of the file's spatial reference, then parses the string to extract the EPSG
epsg = int(gdal.Info(input, format='json')['coordinateSystem']['wkt'].rsplit('"EPSG","', 1)[-1].split('"')[0])

#or

#path = r"H:\workspace\TEUI\BridgerTeton"
d = gdal.Open(path)
proj = osr.SpatialReference(wkt=d.getProjection())
proj.AutoIdentifyEPSG()
print(proj.GetAttrValue('AUTHORITY', 1))

#Reproject rasters
def reproject_raster (raster, \pixel spacing= , epsg_from=, epsg_to= ):

#IF RASTERS ARE DIFFERENT EXTENTS, CLIP TO SMALLEST EXTENT

#determine raster extents

#determine smallest extent


##arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/R8/Segments/Area5"
##
##fcs = arcpy.ListFeatureClasses()
##print(fcs)
##
##dsc = arcpy.Describe("//166.2.126.25/teui1/4_Derek/R8/Alabama_NFs/ExtractArea4.shp")
##
##cs = dsc.spatialReference
##
##for fc in fcs:
##    arcpy.DefineProjection_management(fc, cs)


##Reproject rasters
    ## Get current raster projection


##Resample rasters

##Clip rasters

###Determine smallest extent
