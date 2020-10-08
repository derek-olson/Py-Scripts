import arcpy, os


## Processing variables 
workspace = r"I:\GMUG\tiles" 
allRasters = []
walk = arcpy.da.Walk(workspace, topdown = True, datatype = "RasterDataset", type = "TIF")

for dirpath, dirnames, filenames in walk:
    for filename in filenames:
        allRasters.append(os.path.join(dirpath,filename))
