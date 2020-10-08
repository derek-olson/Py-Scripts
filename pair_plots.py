# -*- coding: utf-8 -*-
"""
Created on Mon Oct  8 09:18:34 2018

@author: derekolson
"""

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import scale
from collections import Counter

#%matplotlib inline
#rcParams['figure.figsize'] = 5, 4
sb.set_style('whitegrid')

data = pd.read_csv(r"F:\TNC_Fire_Scar_Analysis\FireScars\FireScars.csv")
df = data.loc[:,['cosAspect', 'elevation', 'sinAspect', 'slope', 'MeanFRI']]
sb.pairplot(df)

print(df.corr())

dfScaled = scale(df)
pd.DataFrame.head(dfScaled, 5)
print(dfScaled)
x = pd.DataFrame(dfScaled)
x.columns = ['cosAspect', 'elevation', 'sinAspect', 'slope', 'MeanFRI']

from statsmodels.stats.outliers_influence import variance_inflation_factor
def calculate_vif_(X, thresh=2.5):
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

calculate_vif_(x, thresh=2.5)


sb.