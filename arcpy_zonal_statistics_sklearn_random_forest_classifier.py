# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 08:23:53 2018

@author: derekolson
"""

###############################################################################################################################################
## Import libraries
###############################################################################################################################################
import os
import arcpy
from arcpy.sa import *
import numpy as np
import geopandas as gpd
import pandas as pd
from pandas import DataFrame
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import time
from dbfread import DBF

###############################################################################################################################################
## Run Zonal statistics with arcpy
###############################################################################################################################################
# Get start time
zonal_start_time = time.time()

# Load segments
shp = "//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/Segments/Dixie_segments_refData_2.shp"

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
        ZonalStatisticsAsTable(shp, uid, rast, outTableName, 'DATA', 'MEAN_STD')

# merge dataframes and name columns
ZonalStats = pd.DataFrame()
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
            #ZonalStats = pd.concat([ZonalStats, df], axis=1)
            if ZonalStats.empty == True:
                ZonalStats = df
            else:
                ZonalStats = ZonalStats.merge(df, left_on = uid, right_on = uid, how= 'inner')
         
#ZonalStats = pd.concat(ZonalStats, axis=1)
ZonalStats.to_csv(outRoot + 'ZonalStats.csv')            

# get total time
zonal_end_time = time.time()
zonal_time_minutes = (zonal_end_time - zonal_start_time) / 60
print(zonal_time_minutes)
print("--- %s seconds ---" % (time.time() - zonal_start_time))

# Write times to text file
text_file = open("E:/Data/Zonal_Stats_RF_Times.txt", "w")
text_file.write("Zonal Stats Time: %s" % zonal_time_minutes)

###############################################################################################################################################
# Random Forest Modeling with zonal statistics from above
###############################################################################################################################################
# Get the start time for random forest modeling
rf_start_time = time.time()

# Read in data
#refPoints from parameters
refPoints = gpd.read_file("//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/Reference_Data/RefPoints_forPrimatives.shp")

#polygons from parameters
polygons = gpd.read_file("//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/Segments/Dixie_segments_refData_2.shp")

#zonalStats from parameters
zStats = pd.read_csv("//166.2.126.25/teui1/4_Derek/AWS_POC/Zonal_Statistics_Random_Forest_Classification_Python_Test/Data/OutTables/ZonalStats.csv")
colNum = zStats.shape[1]
zStats = zStats.iloc[:,1:colNum]

# Spatial Join the points to the polygons
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
X = pd.merge(refData, zStats, how='inner', left_on='FID_Model', right_on='FID_Model')

#create the training and testing data 
y = X[['final']]
X = X.drop(['FID_Model','FID_Model', 'final'], axis=1)

# Split the data
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size = 0.25, random_state = 42)

# Create Random Forest Classifier
RFmodel = RandomForestClassifier(n_estimators=500, random_state=0)

# Train the model
classModel = RFmodel.fit(np.array(train_X), np.array(train_y).ravel()) 
print(classModel.feature_importances_)
#oob_error = 1 - classModel.oob_score_
#print(oob_error)
# Evalute the model on the testing data
score = classModel.score(test_X, test_y)
print(score)

# Join the polygons to the zonal stats
predict_X = pd.merge(polygons[['FID_Model']], zStats, how='inner', left_on='FID_Model', right_on='FID_Model')
predict_X = np.array(predict_X.drop(['FID_Model','FID_Model'], axis=1))

# Apply the model to the polygons
modelPredict = pd.DataFrame(classModel.predict(predict_X))
modelPredictProb = pd.DataFrame(classModel.predict_proba(predict_X))

# join predictions to the segments and write to output
zonePreds = pd.concat([zStats['FID_Model'], modelPredict], axis=1)
zonePreds.columns = ['FID_Model', 'class']
outPolys = polygons.merge(zonePreds, on= 'FID_Model')
outPolys.to_file(outRoot+'classifiedPolygons.shp')

# Get the total time to run random forest
rf_end_time = time.time()
rf_time_minutes = (rf_end_time - rf_start_time) / 60
print(rf_time_minutes, "minutes")
print("--- %s seconds ---" % (time.time() - rf_start_time))

# Write times to text file and close the file
text_file.write(", Random Forest Time: %s" % rf_time_minutes)
text_file.close()