import os, pandas, sys
from dbfread import DBF
from pandas import DataFrame
import numpy as np

#list files
rastNames = list()
rastList = list()
for root, dirs, files in os.walk(r"E:\Ecological_Integrity\Bridger_Teton_LTA_Mapping\CalculateAcres"):
    for file in files:
        if file.endswith(".dbf"):
           print(os.path.join(root, file))
           fileName = os.path.join(root, file)
           rastList.append(fileName)
           rastNames.append(file)
print(rastNames)
print(rastList)

# read in files and convert to pandas dataframe
# convert values in columns from square meters to acres
for rast in rastList:
    tempTable = DBF(rast)
    tempFrame = DataFrame(iter(tempTable))
    #print(tempFrame)
    for column in tempFrame.columns[0:]:
        #print(tempFrame[column])
        tempFrame.loc[:,column] /= 4046.86 
        #print(tempFrame[column])
        outName = rast.split('.')[0]
        tempFrame.to_csv(path_or_buf = outName+'_acres.csv', sep = ',')
print("done")

# read in files and convert to pandas dataframe
# calculate percentages
for rast in rastList:
    tempTable = DBF(rast)
    tempFrame = DataFrame(iter(tempTable))
    divisors = tempFrame.apply(np.sum, axis = 1)
    print(divisors)
    for column in tempFrame.columns[0:]:
        tempFrame.loc[:,column] /= divisors
        tempFrame.loc[:,column] *= 100
        outName = rast.split('.')[0]
        tempFrame.to_csv(path_or_buf = outName+'_pct.csv', sep = ',')
print("done")



