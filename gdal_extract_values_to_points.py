# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 14:19:25 2018

@author: derekolson
"""
## import libraries
from osgeo import ogr
from osgeo import gdal
import numpy as np
import pandas as pd
import os
import struct
import geopandas

## get point shapefile
shpSource = r"F:\TNC_Fire_Scar_Analysis\FireScars\FireScarData_regressionTesting_completeData.shp"
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
rastNames = list()
rastList = list()
for root, dirs, files in os.walk(r"H:\Personal\Personal\DensityPlotAnalysis\Imagery"):
    for file in files:
        if file.endswith(".img"):
           print(os.path.join(root, file))
           fileName = os.path.join(root, file)
           rastList.append(fileName)
           rastNames.append(file)

## extract values to points
# initiate empty list 
vals = list()
lyr = shpFile.GetLayer()

# get a list of features to iterate through
feats = list()
for feat in lyr:
    feats.append(feat)
    

# may need to set the driver name
for rast in rastList:
    tempRas = gdal.Open(rast)
    geoTrans = tempRas.GetGeoTransform()
    rasterBands = tempRas.RasterCount
    print("raster:", rast)
    
    for band in range (rasterBands):
        band += 1
        print("Getting Band", band)
        tempBand = tempRas.GetRasterBand(band)
        x = list()
              
        for feat in feats:
            print(feat)
            geom = feat.GetGeometryRef()
            id = feat.GetField('OBJECTID')
            mx,my = geom.GetX(), geom.GetY()
            px = int((mx - geoTrans[0])/geoTrans[1])
            py = int((my - geoTrans[3])/geoTrans[5])
            structval = tempBand.ReadRaster(px, py, 1,1, buf_type=gdal.GDT_Float32)
            result = struct.unpack('f', structval)[0]
            x.append(result)
            
        vals.append(x)
   
print('vals:', vals)
print('finish')

## reformat extracted data - fix this to accomodate band names as well
tempDF = pd.DataFrame(vals)
dataFrame = pd.DataFrame.transpose(tempDF)

rastNameList = list()
for rast in rastNames:
    rasts = rast.split('.')[0]
    rastNameList.append(rasts)
    
data = pd.DataFrame(dataFrame.values, columns = rastNameList)
print(data)

## add a new field to pandas dataframe
numIDS = len(feats)+1
id = range(1,numIDS)
data['id'] = pd.Series(id, index = data.index)

## get the response field with the explanatory variables
ptAtts = geopandas.read_file(shpSource)

## merge extracted values with existing values and convert from geopandas to pandas
joinDF = ptAtts.merge(data, left_on='OBJECTID', right_on='id')
df = pd.DataFrame(joinDF)
dfAnalysis = df.iloc[:,[10, 11, 13,14,15,16,17,18,19,20,29,30,31,32,33,34,35,23,24,25,26,27]]

#mFRI = df.filter(items=['MeanFRI'])

dfLength = len(dfAnalysis.columns)
y = dfAnalysis.iloc[:,dfLength-1]
X = dfAnalysis.iloc[:,0:dfLength-2]

import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import scipy as sp
from statsmodels.stats.outliers_influence import variance_inflation_factor    
import seaborn as sb

dfAnalysis = sm.tools.tools.add_constant(dfAnalysis)
print(dfAnalysis.corr())
sb.pairplot(dfAnalysis)
# Fit regression model (using the natural log of one of the regressors)
results = smf.ols(formula='MeanFRI ~ HLI_ALL_EC + Insol + CWD_1900_1 + AET_1900_1 + cosAspect + Daily_Average_Temperature + elevation + mean_annual_precip + sinAspect + slope', data = dfAnalysis).fit()
residuals = results.resid
exogVars = results.model.exog
# Inspect the results 
print(results.summary())

## Q-Q plot
## Input array. Should be 1-dimensional
def qqPlot(array):
    modelFit = smf.ols(formula='MeanFRI ~ HLI_ALL_EC + Insol + CWD_1900_1 + AET_1900_1 + cosAspect + Daily_Average_Temperature + elevation + mean_annual_precip + sinAspect + slope', data = dfAnalysis).fit()
    residuals = modelFit.resid
    fig = sm.qqplot(residuals)
    plt.show()

qqPlot(residuals)


#fig, ax = plt.subplots(figsize=(6,2.5))
#_, (__, ___, r) = sp.stats.probplot(residuals, plot=ax, fit=True)


def calculate_vif_(X, thresh=5.0):
    variables =  list(range(X.shape[1]))
    dropped=True
    while dropped:
        dropped=False
        vif = [variance_inflation_factor(X.iloc[:,variables].values, ix) for ix in range(X.iloc[:,variables].shape[1])]
        print(vif)

        maxloc = vif.index(max(vif))
        print(max(vif))
        if max(vif) > thresh:
            print('dropping \'' + X.iloc[:,variables].columns[maxloc] + '\' at index: ' + str(maxloc))
            del variables[maxloc]
            dropped=True

    print('Remaining variables:')
    print(X.columns[variables])
    return X.iloc[:,variables]

calculate_vif_(X, thresh=5.0)
