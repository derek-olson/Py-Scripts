# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 11:59:17 2018

@author: derekolson
"""

import pandas as pd
import seaborn as sb

file = "//166.2.126.25/R2_VegMaps/ArapahoeRoosevelt/Activity_2/Extract/20180821/20181102_accuracy_assessment_FigureExample.csv"

data = pd.read_csv(file)
df = data.dropna()

df['CC_Type_1'] = "Modeled_CC"
df['CC_Type_2'] = "PI_CC"
df.columns = ["SPATIAL_ID", "Modeled_CC", "PI_CC", 'CC_Type_1', 'CC_Type_2']

df2 = df.iloc[:,[1,3]]
df2.columns = ['CC', 'CC_Type']
df3 = df.iloc[:,[2,4]]
df3.columns = ['CC', 'CC_Type']
dfOut = df2.append(df3)


sb. set()
sb.jointplot('Modeled_CC', "PI_CC", df, kind ='kde')

sb.jointplot('Modeled_CC', "PI_CC", df, kind ='reg')

sb.jointplot('Modeled_CC', "PI_CC", df, kind ='hex')


sb.violinplot(x="CC", y="CC_Type", data=dfOut)

sb.kdeplot(df.Modeled_CC, shade=True)
sb.kdeplot(df.PI_CC, shade=True)
