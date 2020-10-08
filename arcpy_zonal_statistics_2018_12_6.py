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
import pandas as pd
from pandas import DataFrame
import time
from dbfread import DBF

###############################################################################################################################################
## Run Zonal statistics with arcpy
###############################################################################################################################################
# Get start time
zonal_start_time = time.time()

# Load segments
zones = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Results_20180717/sc_draft_ltas_20180730.shp"

# Set the location of your imagery
raster_path = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats"

# set the ouput directory location
out_path = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats/"

# Set the segments unique ID field
unique_field = 'FID'

def zonal_stats(zone, unique_field, raster_path, out_path):
    arcpy.env.workspace = raster_path
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
                outTableName = out_path + outRasName + "_band" + str(band) + ".dbf"
                print(outTableName)
                # Check to ensure that the band names are "Layer_n" and not "Band_n"
                bandRas = arcpy.Raster("{}\\Layer_{}".format(rast, band))
                print(bandRas)
                ZonalStatisticsAsTable(zones, unique_field, bandRas, outTableName, 'DATA', 'MEAN_STD')
        else:
            print("single band")
            outTableName = out_path + outRasName + ".dbf"
            print(outTableName)
            ZonalStatisticsAsTable(zones, unique_field, rast, outTableName, 'DATA', 'MEAN_STD')
    
    # merge dataframes and name columns
    ZonalStats = pd.DataFrame()
    for root, dirs, files in os.walk(out_path[0:-1]):
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
                df.columns = [unique_field, fileName + "_mean", fileName + "_sd"]
                print(df)
                #ZonalStats = pd.concat([ZonalStats, df], axis=1)
                if ZonalStats.empty == True:
                    ZonalStats = df
                else:
                    ZonalStats = ZonalStats.merge(df, left_on = unique_field, right_on = unique_field, how= 'inner')
             
    #ZonalStats = pd.concat(ZonalStats, axis=1)
    ZonalStats.to_csv(out_path + 'ZonalStats.csv')            

zonal_stats(zones, unique_field, raster_path, out_path)

# get total time
zonal_end_time = time.time()
zonal_time_minutes = (zonal_end_time - zonal_start_time) / 60
print(zonal_time_minutes)
print("--- %s seconds ---" % (time.time() - zonal_start_time))

# Write times to text file
#text_file = open("E:/Data/Zonal_Stats_RF_Times.txt", "w")
#text_file.write("Zonal Stats Time: %s" % zonal_time_minutes)


    
    