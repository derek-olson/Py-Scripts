# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 10:05:08 2019

@author: derekolson
"""

#Modify SDDraft example
#The following script creates a map service definition draft (.sddraft) file for a map. 
#It then enables feature access on the map service by modifying the service definition draft file 
#using the xml.dom.minidom standard Python library. The modified service definition file is then 
#published to ArcGIS Server. Finally, the script calls the Manage Map Server Cache Tiles tool to create 
#map service cache tiles.

import arcpy, os, sys
import xml.dom.minidom as DOM

arcpy.env.overwriteOutput = True

indir = "//usda.net/fs/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro/" 

for root, dirs, files in os.walk(indir):
    for file in files:
        if file.endswith(".aprx"):
            serviceName = file.split('.')[0]
            sddraft_filename = serviceName + ".sddraft"
            print(sddraft_filename)

            # Update these variables
            tempPath = "//usda.net/fs/FS/Reference/GeoTool/wo_nfs_rsac/TCA_AGOL_Services_Data/TCA_Data_2019_11_14/arcpro2/"
            path2APRX = os.path.join(root,file)
            print(path2APRX)
            
            # Make sure this server url is added as publisher ags connection to the project
            # Else use the ags connection file itself
            targetServer = "C:/Users/derekolson/Documents/ArcGIS/Projects/MyProject/arcgis on ntcfsxnfsx0236_6080.ags"
            
            # All paths are built by joining names to the tempPath
            SDdraftPath = os.path.join(tempPath, sddraft_filename)
            newSDdraftPath = os.path.join(tempPath, serviceName+"updatedDraft.sddraft")
            SDPath = os.path.join(tempPath, serviceName + ".sd")
            
            aprx = arcpy.mp.ArcGISProject(path2APRX)
            m = aprx.listMaps()[0]
            
            # Create MapServiceDraft and set service properties
            sddraft = arcpy.sharing.CreateSharingDraft('STANDALONE_SERVER', 'MAP_SERVICE', serviceName, m)
            sddraft.targetServer = targetServer
            sddraft.copyDataToServer = False
            sddraft.serverFolder = "TCA_LTAs_2019"
            sddraft.exportToSDDraft(SDdraftPath)
            
            # Read the contents of the original SDDraft into an xml parser
            doc = DOM.parse(SDdraftPath)
            
            # The following code modifies the SDDraft from a new MapService with caching capabilities
            # to a FeatureService with Map, Create and Query capabilities.
            typeNames = doc.getElementsByTagName('TypeName')
            for typeName in typeNames:
                if typeName.firstChild.data == "FeatureServer":
                    extention = typeName.parentNode
                    for extElement in extention.childNodes:
                        if extElement.tagName == 'Enabled':
                            extElement.firstChild.data = 'true'
            
            # Turn off caching
            configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
            propArray = configProps.firstChild
            propSets = propArray.childNodes
            for propSet in propSets:
                keyValues = propSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'Key':
                        if keyValue.firstChild.data == "isCached":
                            keyValue.nextSibling.firstChild.data = "false"
            
            # Turn on feature access capabilities
            configProps = doc.getElementsByTagName('Info')[0]
            propArray = configProps.firstChild
            propSets = propArray.childNodes
            for propSet in propSets:
                keyValues = propSet.childNodes
                for keyValue in keyValues:
                    if keyValue.tagName == 'Key':
                        if keyValue.firstChild.data == "WebCapabilities":
                            keyValue.nextSibling.firstChild.data = "Map,Query,Data"
                            
            # Modify keep cache, false by default
            configProps = doc.getElementsByTagName('KeepExistingMapCache')[0]
            configProps.firstChild.data = "true"
                            
            # Write the new draft to disk
            f = open(newSDdraftPath, 'w')
            doc.writexml(f)
            f.close()
            
            try:
                # Stage the service
                arcpy.StageService_server(newSDdraftPath, SDPath)
                warnings = arcpy.GetMessages(1)
                print(warnings)
                print("Staged service")
            
                # Upload the service
                arcpy.UploadServiceDefinition_server(SDPath, server_con)
                print("Uploaded service")
            
                # Manage Map server Cache Tiles
                # For cache, use multiple scales seperated by semicolon (;) 
                # For example "591657527.591555;295828763.795777" 
                arcpy.server.ManageMapServerCacheTiles(targetServer + os.sep + serviceName + ".MapServer", "591657527.591555",
                "RECREATE_ALL_TILES")
                
            except Exception as stage_exception:
                print("Analyzer errors encountered - {}".format(str(stage_exception)))
            
            except arcpy.ExecuteError:
                print(arcpy.GetMessages(2))