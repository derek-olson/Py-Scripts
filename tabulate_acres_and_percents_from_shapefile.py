# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 14:04:27 2018

@author: derekolson
"""
# import libraries
import geopandas as gpd
import numpy as np
import pandas as pd
from dbfread import DBF
from pandas import DataFrame

# function to convert square meters to acres
def calc_acres(in_path, out_path, shp_dbf, begin_col, end_col):
    if shp_dbf == 'shp':
        # this reads in a shapefile using geopandas
        data = gpd.read_file(in_path)
        # subset the data you are interested in
        df = data.iloc[:,begin_col:end_col]
        for column in df.columns[0:]:
            #print(tempFrame[column])
            df.loc[:,column] /= 4046.86 
            #print(tempFrame[column])
            df.to_csv(path_or_buf = out_path, sep = ',')
    elif shp_dbf == 'dbf':
        tempTable = DBF(in_path)
        tempFrame = DataFrame(iter(tempTable))
        df = tempFrame.iloc[:,begin_col:end_col]
        for column in df.columns[0:]:
            #print(tempFrame[column])
            df.loc[:,column] /= 4046.86 
            #print(tempFrame[column])
            df.to_csv(path_or_buf = out_path, sep = ',')
        

# input your in and out paths
in_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/Tabulate_Area_VCMQ.dbf'
out_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/Tabulate_Area_VCMQ_Acres.csv'
shp_dbf = 'dbf'
begin_col = 3
end_col = 27

calc_acres(in_path, out_path, shp_dbf, begin_col, end_col)

# function to calculate percentages
def calc_percent(in_path, out_path):
    df = pd.read_csv(in_path)
    divisors = df.apply(np.sum, axis = 1)
    for column in df.columns[0:]:
        df.loc[:,column] /= divisors
        df.loc[:,column] *= 100
        df.to_csv(path_or_buf = out_path, sep = ',')
        
# input your in and out paths
in_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/Tabulate_Area_VCMQ_Acres.csv'
out_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Layers_for_zonal_stats/Tabulate_Area_VCMQ_Acres_PCT.csv' 

calc_percent(in_path, out_path)

   
# function to find the max pct and return the index
def find_max(in_path, out_path):
    pcts = pd.read_csv(in_path)
    transpose = pcts.T    
    max_list = list()    
    for column in transpose.columns:
        series = transpose[column]
        print(series)
        max_list.append(series.idxmax())        
        pd.DataFrame(max_list).to_csv(path_or_buf = out_path, sep = ',')

# input your in and out paths
in_path = 'E:/Ecological_Integrity/Bridger_Teton_LTA_Mapping/Data/geology/geology_pct.csv'   
out_path = 'E:/Ecological_Integrity/Bridger_Teton_LTA_Mapping/Data/geology/max_percent.csv' 

find_max(in_path, out_path)