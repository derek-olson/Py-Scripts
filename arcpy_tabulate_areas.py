# -*- coding: utf-8 -*-
"""
Created on Fri May 10 10:09:20 2019

@author: derekolson
"""

def extractRaster(raster, bound, out_path):
    outFileName0 = raster.split('/')[0]
    outExtractByMask = ExtractByMask(raster, bound)
    outExtractByMask.save(out_path + outFileName0 + '_clipped.img')
    
def listFieldUniqueValues(table, field):
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        return sorted({row[0] for row in cursor})

def listRasterFields(bound, raster_path):
    arcpy.env.workspace = raster_path
    rast_list = arcpy.ListRasters()
    field_list = []
    for rast in rast_list:
        fields = arcpy.ListFields(rast)
        for f in fields:
            field_list.append(f.name)
        print(field_list)
    with open(them_out_path+'test.csv','w', newline='') as empty_csv:
        writer = csv.writer(empty_csv)
        writer.writerows(field_list)
        
def tabulate_area(zones, zone_field, raster, class_field, out_path):  
        out_rast_name = raster.split(".")[0]
        out_table_name = them_out_path + out_rast_name + ".dbf"
        TabulateArea(zones, zone_field, rast, class_field, out_table_name )

def tabulate_areas(zones, zone_field, raster_path, class_fields, out_path):  
    arcpy.env.workspace = raster_path
    rast_list = arcpy.ListRasters()
    for rast, class_field in zip(rast_list, class_fields):
        out_rast_name = rast.split(".")[0]
        out_table_name = them_out_path + out_rast_name + ".dbf"
        TabulateArea(zones, zone_field, rast, class_field, out_table_name )    