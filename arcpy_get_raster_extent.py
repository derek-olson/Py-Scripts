import arcpy
import os

arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/R6/Kfac/R6Predictors"
filePath = arcpy.env.workspace

rasterList = arcpy.ListRasters("*_clip_clip_clip.tif", "ALL")

for name in rasterList:
    desc = arcpy.Describe(filePath + "//" + name)
    print name
    print desc.extent
