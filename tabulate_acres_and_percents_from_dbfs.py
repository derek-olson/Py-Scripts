# -*- coding: utf-8 -*-
"""
Created on Thu Dec 20 17:02:36 2018

@author: derekolson
"""

# import libraries
import pandas as pd
import os
import numpy as np
from dbfread import DBF
from pandas import DataFrame
# get a list of tables to iterate through
path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats'
out_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats/'
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".dbf"):
                print(file)
                # convert the dbf to pandas dataframe
                tempTable = DBF(os.path.join(root, file))
                tempFrame = DataFrame(iter(tempTable))
                file_name = os.path.join(root,file)
                data = tempFrame #pd.read_csv(file_name)
                df = data.iloc[:,1:]
                for column in df.columns[0:]:
                    #print(tempFrame[column])
                    df.loc[:,column] /= 4046.86 
                    #print(tempFrame[column])
                    out_name = file.split('.')[0]
                    df.to_csv(path_or_buf = out_path + out_name + '_acres.csv', sep = ',')
                    
                    
path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats'
out_path = '//166.2.126.25/teui1/4_Derek/Salmon_Challis_LTA_Mapping/Zonal_Stats/'  
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.csv'):
            print(file)
            file_name = os.path.join(root,file)
            data = pd.read_csv(file_name)
            df = data.iloc[:,1:]
            divisors = df.apply(np.sum, axis = 1)
            for column in df.columns[0:]:
                df.loc[:,column] /= divisors
                df.loc[:,column] *= 100
                out_name = file.split('.')[0]
                df.to_csv(path_or_buf = out_path + out_name + '_pct.csv', sep = ',')