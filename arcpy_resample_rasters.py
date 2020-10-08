import arcpy, os
from arcpy import env
from arcpy.sa import *
import subprocess
arcpy.CheckOutExtension("Spatial")
Dir = "K:/Nebraska/Data/Imagery/Clipped_Imagery/"
arcpy.env.workspace = Dir
arcpy.env.snapRaster = "//166.2.126.25/R2_VegMaps/Nebraska/Mapping/Riparian/ValleyBottomPredict2.R.img"
arcpy.env.extent = "//166.2.126.25/R2_VegMaps/Nebraska/Mapping/Riparian/ValleyBottomPredict2.R.img"
arcpy.env.overwriteOutput=True

def DereksRescale(inRaster, outRaster):
                  #convert to numpy array
                  #rescale in numpy
                # convert back to arcpy raster
                # return your outraster
                  

def iansResampFunk(inRaster, outRaster, pixelType, res):
    call = 'C:/Program Files (x86)/FWTools2.4.7/bin/gdalwarp -multi -ot '+pixelType+' -tr '+str(res)+' '+str(res) + ' '
    call += '"'+inRaster + '" "' + outRaster + '"'
    print call
    call = subprocess.Popen(call)
    call.wait()
    
#65535
rasts = arcpy.ListRasters("*_clip.tif")
print rasts
for rast in rasts:
    print rast
  
    rastFileName = os.path.splitext(rast)[0]
    resampOutFile = rastFileName + "_rip.tif"
    copyOutFile = rastFileName + "_copy.tif"
    gdal_calc.py -A 
##    my_raster = arcpy.Raster(rast)
##    my_raster = my_raster[*] * 10000
##    my_raster.save(copyOutFile)

    iansResampFunk(Dir + rast, Dir + resampOutFile, 'Int16', 10)

   
    
