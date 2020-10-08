import arcpy

arcpy.env.workspace = "//166.2.126.25/teui1/4_Derek/R8/Segments/Area5"

fcs = arcpy.ListFeatureClasses()
print(fcs)

dsc = arcpy.Describe("//166.2.126.25/teui1/4_Derek/R8/Alabama_NFs/ExtractArea4.shp")

cs = dsc.spatialReference

for fc in fcs:
    arcpy.DefineProjection_management(fc, cs)
