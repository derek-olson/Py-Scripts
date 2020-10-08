import arcpy, os
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
boundPoly = "//166.2.126.25/teui1/4_Derek/R6/Kfac/R6Predictors/asp_clip_clip.tif"
arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/R6/Kfac/R6Predictors"
arcpy.env.snapRaster = "//166.2.126.25/teui1/4_Derek/R6/Kfac/R6Predictors/dem.img"
arcpy.env.overwriteOutput=True
##arcpy.env.nodata = "MINIMUM"


rasts = arcpy.ListRasters()
print rasts
for rast in rasts:
    rastFileName = os.path.splitext(rast)[0]
    clipOutFile = rastFileName + "_clip.tif"
    Clip = ExtractByMask(arcpy.env.workspace + "\\" + rast, boundPoly)
    outClip = Clip.save(arcpy.env.workspace + "\\" + clipOutFile)
    
   
    
