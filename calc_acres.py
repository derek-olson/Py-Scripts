# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:34:34 2019

@author: derekolson
"""

# function to convert square meters to acres
def calc_acres(in_path, out_path):
    for root, dirs, files in os.walk(in_path):
        for file in files:
            if file.endswith("_tabulateArea.dbf"):
                print(file)
                tempTable = DBF(os.path.join(root, file))
                data = DataFrame(iter(tempTable))
                df = data.iloc[:,0:]
                for column in df.columns[1:]:
                    df.loc[:,column] /= 4046.86 
                    out_name = file.split('.')[0]
                    df.columns = unqFlds
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