import arcpy
import os

arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/R8/DOQ"
filePath = arcpy.env.workspace

rasterList = arcpy.ListRasters("*", "ALL")

for name in rasterList:
    desc = arcpy.Describe(filePath + "//" + name)
    print name
    print desc.bandCount
