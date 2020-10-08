# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 14:27:03 2019

@author: derekolson
"""

import arcpy
import os

# Set output file names
outdir = "//usda.net/fs/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro2/"
service = "Abiotic_Agents"
sddraft_filename = service + ".sddraft"
sddraft_output_filename = os.path.join(outdir, sddraft_filename)

# Reference map to publish
aprx = arcpy.mp.ArcGISProject("//usda.net/fs/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro/abiotic_agents.aprx")
m = aprx.listMaps("Map")[0]

# Create MapServiceDraft and set service properties
service_draft = arcpy.sharing.CreateSharingDraft("STANDALONE_SERVER", "MAP_SERVICE", service, m)
service_draft.targetServer = "C:/Users/derekolson/Documents/ArcGIS/Projects/MyProject/arcgis on ntcfsxnfsx0236_6080.ags"

# Create Service Definition Draft file
service_draft.exportToSDDraft(sddraft_output_filename)

# Stage Service
sd_filename = service + ".sd"
sd_output_filename = os.path.join(outdir, sd_filename)
arcpy.StageService_server(sddraft_output_filename, sd_output_filename)

# Share to portal
print("Uploading Service Definition...")
arcpy.UploadServiceDefinition_server(sd_output_filename, "C:/Users/derekolson/Documents/ArcGIS/Projects/MyProject/arcgis on ntcfsxnfsx0236_6080.ags")

print("Successfully Uploaded service.")