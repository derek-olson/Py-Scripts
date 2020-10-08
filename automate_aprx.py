# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:21:21 2019

@author: derekolson
"""

import arcpy
import os
p = arcpy.mp.ArcGISProject("T:/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro/template2.aprx")
#p = arcpy.mp.ArcGISProject('CURRENT')
m = p.listMaps()[0]
l = m.listLayers()[0]
sym = l.symbology
outdir = "T:/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro2/"
symLayer = 'T:/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro/T2_Symbology.lyrx'
fields = [field for field in arcpy.ListFields(l, "nw0*", "Double") if not field.name.endswith('dd')]
for field in fields:
    print(field.name)
    outName = field.name.split("__")[1]
    sym.renderer.fields = "{}".format(field)
    l.symbology = sym
    symbologyFields = "VALUE_FIELD nw0__ozone"+" "+"{}".format(field.name)
    arcpy.management.ApplySymbologyFromLayer(l.name, symLayer, symbologyFields, "MAINTAIN")
    p.saveACopy(outdir+outName+".aprx")

   








