# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 11:54:14 2018

@author: derekolson
"""

import arcpy
from arcpy import env
import os
import geopandas

env.workspace = r"C:\Users\derekolson\Downloads\FireSevDates\FireSevDates"

fcNames = list()
fcList = list()

for root, dirs, files, in os.walk(r"C:\Users\derekolson\Downloads\FireSevDates\FireSevDates"):
    for file in files:
        if file.endswith(".shp"):
            print(os.path.join(root,file))
            fileName = os.path.join(root,file)
            fcList.append(fileName)
            fcNames.append(file)
            
            
arcpy.Merge_management(fcList, "F:/Fires/firesMerged.shp")

arcpy.Dissolve_management("F:/Fires/firesMerged.shp", "F:/Fires/firesMerged_dissolved.shp", ["Year", "StartMonth", "StartDay"], "", "MULTI_PART", "DISSOLVE_LINES")

