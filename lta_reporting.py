# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 12:15:58 2019

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
import numpy as np
###############################################################################################################################################
## zonal statistics
###############################################################################################################################################
# Set the path to the continuous rasters 
cont_rast_path = ""

# Load segments
zones = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Results_20180717/sc_draft_ltas_20180730.shp"

# set the ouput directory location
cont_out_path = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats/"

# Set the segments unique ID field
unique_field = 'FID'

def zonal_stats(zones, unique_field, raster_path, out_path):
    arcpy.env.workspace = cont_raster_path
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

zonal_stats(zones, unique_field, cont_raster_path, cont_out_path)
###############################################################################################################################################
## tabulate areas
###############################################################################################################################################
# Set the path to the continuous rasters 
them_rast_path = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/thematic/"

# make a list of the class fields in the order they correspond with the input rasters
classFields = ["GROUPVEG", "LABEL","LABEL","LABEL","LABEL","LABEL","LABEL","NEW_CLASS","LABEL","WUICLASS10"]

# Load segments
segments = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Results_20180717/sc_draft_ltas_20180730.shp"

# set the unique zone field 
zoneField = "FID"

# set the ouput directory location
them_out_path = "//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/thematic/dbfs/"

def tabulate_area(zones, zone_field, raster_path, class_fields, out_path):  
    arcpy.env.workspace = raster_path
    rast_list = arcpy.ListRasters()
    for rast, class_field in zip(rast_list, class_fields):
        out_rast_name = rast.split(".")[0]
        out_table_name = them_out_path + out_rast_name + ".dbf"
        TabulateArea(zones, zone_field, rast, class_field, out_table_name )

tabulate_area(segments, zoneField, them_rast_path, classFields, them_out_path)

# function to convert square meters to acres
def calc_acres(in_path, out_path):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if file.endswith(".dbf"):
                    print(file)
                    tempTable = DBF(os.path.join(root, file))
                    data = DataFrame(iter(tempTable))
                    df = data.iloc[:,0:]
                    for column in df.columns[1:]:
                        df.loc[:,column] /= 4046.86 
                        out_name = file.split('.')[0]
                        df.to_csv(path_or_buf = out_path + out_name + '_acres.csv', sep = ',')
        

calc_acres(them_out_path[:-1], them_out_path)

# function to calculate percentages
def calc_percent(in_path, out_path):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if file.endswith(".csv"):
                df = pd.read_csv(os.path.join(root,file))
                data = df.iloc[:,2:]
                divisors = data.apply(np.sum, axis = 1)
                for column in data.columns[0:]:
                    df.loc[:,column] /= divisors
                    df.loc[:,column] *= 100
                    out_name = file.split('.')[0]
                    df.to_csv(path_or_buf = out_path + out_name + '_pct.csv', sep = ',')
        
calc_percent(them_out_path[:-1], them_out_path)
    
###############################################################################################################################################
## extract all rasters to aoi
###############################################################################################################################################

###############################################################################################################################################
## make maps
###############################################################################################################################################

