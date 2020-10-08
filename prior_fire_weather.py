# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 15:07:31 2018

@author: derekolson
"""
import ee
ee.Initialize()
import urllib.request
import ogr, os
#import geopandas as gpd

#import the daymet data
daymet = ee.ImageCollection("NASA/ORNL/DAYMET_V3")
#select the max temp band
tmax = daymet.select('tmax')

# create empty lists
fireFileList = list()
fireNameList = list()

# get OGR drivers
inDriver = ogr.GetDriverByName("ESRI Shapefile")
outDriver = ogr.GetDriverByName('GeoJSON')

# loop through each fire
for root, dirs, files in os.walk(r"F:/FireSevDates"):
    for file in files:
        if file.endswith(".shp"):
            print(os.path.join(root,file))
            fileName = os.path.join(root, file)
            # get a list of all file paths
            fireFileList.append(fileName)
            # get a list of all file names
            fireNameList.append(file)
            # get the extent of each fire
            inShapefile = fileName
            inDataSource = inDriver.Open(inShapefile, 0)
            inLayer = inDataSource.GetLayer()
            extent = inLayer.GetExtent()
            print(extent)
            # convert extent into EE Feature
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(extent[0], extent[2])
            ring.AddPoint(extent[1], extent[3])
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            geojson = poly.ExportToJson()
            print(geojson)
            feat = ee.Feature(geojson)
            print(feat)
            # get the fire start date
            
            # filter the DAYMET data
            # ge the begin and end dates
            
            # export the DAYMET data
            # get the out file path
            # get the out file name
            # set the export params
            # get the download URL

import geopandas as gpd
data = "F:/FireSevDates/1986_fireSev_dates/or4495911830019860803_19850717_19870808/or4495911830019860803_19850717_19870808_dnbr6_dates.shp"    
df = gpd.read_file(data)
print(df)
df.columns = [x.lower() for x in df.columns]
df = df[df.year != 0]
print(df)


