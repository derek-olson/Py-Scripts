
##import arcpy
##from arcpy.sa import *
##arcpy.CheckOutExtension('Spatial')
##import os

#### Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
#### The following inputs are layers or table views: 
####
##arcpy.env.workspace = "//166.2.126.25/teui1/4_Ryan/R9/Superior_NF/Deliverables/10k"
##outpath = "//166.2.126.25/teui1/4_Ryan/R9/Superior_NF/Deliverables/10k"
##rasts = arcpy.ListRasters()
##print rasts
##
##
##for rast in rasts: 
##    rastFileName = os.path.splitext(rast)[0]
##    print rastFileName
##    outname = rastFileName + "_10k.img"
##    print outname
##    ras = Raster(rast)
##    rastOut = ras * 10000
##    rastOut.save(outpath + outname)




import arcpy
from arcpy.sa import *
arcpy.CheckOutExtension('Spatial')
import os

arcpy.env.workspace = "//166.2.126.25/teui1/4_Ryan/R9/Superior_NF/Deliverables/Convert_2_int"

rasts = arcpy.ListRasters()
print rasts


for rast in rasts: 
    rastFileName = os.path.splitext(rast)[0]
    print rastFileName
    outname = rastFileName + "_16bit.img"
    print outname
    arcpy.CopyRaster_management(
	in_raster = rast,
	out_rasterdataset= outname,
	config_keyword="",
	background_value="",
	nodata_value="",
	onebit_to_eightbit="NONE",
	colormap_to_RGB="NONE",
	pixel_type="16_BIT_SIGNED",
	scale_pixel_value="NONE",
	RGB_to_Colormap="NONE",
	format="IMAGINE Image",
	transform="Transform")
