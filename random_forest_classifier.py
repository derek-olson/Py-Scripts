# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 12:49:07 2018

@author: derekolson
"""
import os
import arcpy
from arcpy.sa import *
import numpy as np
import geopandas as gpd
import pandas as pd
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
#from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestRegressor
#from sklearn.ensemble import BaggingRegressor
#import matplotlib.pyplot as plt
#import seaborn as sn
import time
from dbfread import DBF

# Read in data
#refPoints from parameters
refPoints = gpd.read_file("//166.2.126.25/teui1/4_Derek/GEE_Development/Dixie_NF/RefPoints_forPrimatives.shp")

#polygons from parameters
#polygons = gpd.read_file("//166.2.126.25/teui1/4_Derek/GEE_Development/Dixie_NF/Segments.shp")

#zonalStats from parameters
#zStats = pd.read_csv("//166.2.126.25/teui1/4_Derek/GEE_Development/Dixie_NF/ZonalStats.csv")

###############################################################################################################################################
## Run Zonal statistics with arcpy
# Get start time
zonal_start_time = time.time()

###############################################################################################################################################
# Array zonal stats stuff
#shpOut = "//166.2.126.25/teui1/4_Derek/GEE_Development/Dixie_NF/Dixie_segments_refData_2.img"
#convert shapefile to raster then to numpy array
#shpToRas = arcpy.PolygonToRaster_conversion (shp, 'FID_Model', shpOut, "CELL_CENTER", "FID_Model", 30)
#shpArray = arcpy.RasterToNumPyArray (shpToRas, {lower_left_corner}, {ncols}, {nrows}, {nodata_to_value})
#arcpy.env.outputCoordinateSystem = shp
#arcpy.env.cellSize = 30
###############################################################################################################################################
# Load segments
shp = "//166.2.126.25/teui1/4_Derek/GEE_Development/Dixie_NF/Dixie_segments_refData_2.shp"

# Set the location of your imagery
arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/Imagery"

# set the ouput directory location
outRoot = "//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/OutTables/"

# Set the segments unique ID field
uid = 'FID_Model'

#Run zonal stats
rastList = arcpy.ListRasters("*", "IMG")
for rast in rastList:
    print(rast)
    d = arcpy.Describe(rast)
    nBands = d.bandCount
    outRasName = rast.split(".")[0]
    print(outRasName)
    if nBands > 1:
        for band in range(1, nBands+1):
            print(band)
            outTableName = outRoot + outRasName + "_band" + str(band) + ".dbf"
            print(outTableName)
            # Check to ensure that the band names are "Layer_n" and not "Band_n"
            bandRas = arcpy.Raster("{}\\Layer_{}".format(rast, band))
            print(bandRas)
            ZonalStatisticsAsTable(shp, uid, bandRas, outTableName, 'DATA', 'MEAN_STD')
    else:
        print("single band")
        outTableName = outRoot + outRasName + ".dbf"
        print(outTableName)
        ZonalStatisticsAsTable(shp, uid, bandRas, outTableName, 'DATA', 'MEAN_STD')

# merge dataframes and name columns
appended_data = pd.DataFrame()
for root, dirs, files in os.walk(outRoot[0:-1]):
    for file in files:
        if file.endswith(".dbf"):
            print(file)
            # convert the dbf to pandas dataframe
            tempTable = DBF(os.path.join(root, file))
            tempFrame = DataFrame(iter(tempTable))
            # subset the columns
            df = tempFrame.iloc[:,[0,3,4]]
            print(df)
            #rename columns
            fileName = file.split(".")[0]
            print(fileName)
            df.columns = [uid, fileName + "_mean", fileName + "_sd"]
            print(df)
            #appended_data = pd.concat([appended_data, df], axis=1)
            if appended_data.empty == True:
                appended_data = df
            else:
                appended_data = appended_data.merge(df, left_on = uid, right_on = uid, how= 'inner')
         
#appended_data = pd.concat(appended_data, axis=1)
appended_data.to_csv(outRoot + 'appended.csv')            

# get total time
zonal_end_time = time.time()
zonal_time_minutes = (zonal_end_time - zonal_start_time) / 60
print(zonal_time_minutes)
print("--- %s seconds ---" % (time.time() - zonal_start_time))

###############################################################################################################################################
# Spatial Join the points to the polygons
rf_start_time = time.time()

refData = gpd.sjoin(refPoints, polygons)

# Get the unique ID field and the reference field
refData = refData[['FID_Model', 'final']]

# Create a dictionary of the reference classes
labels = refData['final'].tolist()
refSet = set(labels)
nLabels = range(0,len(refSet))
labelDict = dict(zip(nLabels, refSet))

# Encode the labels
le = preprocessing.LabelEncoder()
le.fit(labels)
encodedLabels = le.transform(labels)
print(encodedLabels)
# Join the reference data to the zonal stats
X = pd.merge(refData, zStats, how='inner', left_on='FID_Model', right_on='FID')

#create the training and testing data 
y = X[['final']]
X = X.drop(['FID_Model','FID', 'final'], axis=1)

# Split the data
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.25, random_state = 42)

# Create Random Forest Classifier
RFmodel = RandomForestClassifier(n_estimators=500, random_state=0)

# Train the model
classModel = RFmodel.fit(np.array(train_X), np.array(train_y).ravel()) 
print(classModel.feature_importances_)
oob_error = 1 - classModel.oob_score_
print(oob_error)
# Evalute the model on the testing data
score = classModel.score(test_X, test_y)
print(score)

# Join the polygons to the zonal stats
predict_X = pd.merge(polygons[['FID_Model']], zStats, how='inner', left_on='FID_Model', right_on='FID')
predict_X = np.array(predict_X.drop(['FID_Model','FID'], axis=1))

# Apply the model to the polygons
modelPredict = pd.DataFrame(classModel.predict(predict_X))
modelPredictProb = pd.DataFrame(classModel.predict_proba(predict_X))

rf_end_time = time.time()
rf_time_minutes = (zonal_end_time - rf_start_time) / 60
print(zonal_time_minutes)
print("--- %s seconds ---" % (time.time() - rf_time))





