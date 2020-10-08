import arcpy, os, subprocess
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
Zones = "//166.2.126.25/R4_VegMaps/Uinta_Wasatch_Cache\Mapping/01_Veg_Type/GA3_Uintas/Segments/UWC_GA3_Uintas_Segments.shp"
ZoneField = "FID_Model"
work = "//166.2.126.25/R4_VegMaps/Uinta_Wasatch_Cache/Mapping/ZonalStats/DataLayers/L8_10mResample"
outTableName =  work + "/UWC_Zonal_Stats.txt"
TemplateScript = "//166.2.126.25/R4_VegMaps/VegMapping_Tools/Derek_VegMap/Template_ZonalStats.R"
arcpy.env.workspace = work
arcpy.env.overwriteOutput = True

rasts = arcpy.ListRasters("*.img")
print rasts
for rast in rasts:
    rastFileName = os.path.splitext(rast)[0]
    arcpy.env.workspace = work + "/" + rast
    subRasts = arcpy.ListRasters()
    i = 1
    for subRast in subRasts:
        rastName = work + '/' + rastFileName + '.img/Layer_' + str(i)
        outName = work + '/' + rastFileName + '_' + str(i) + '.dbf'
        ZonalStats = ZonalStatisticsAsTable(Zones, ZoneField, rastName, outName, "NODATA", "MEAN_STD")
        i = i + 1

#########################################################
#Find R executable
#########################################################        
RnameArray = []
path = r"C:\Program Files\R"
for files in os.walk(path):
	for name in files:
		for n in name:
			if n == "Rscript.exe":
				scriptPath = files[0] + "\Rscript.exe"
				RnameArray.append(scriptPath)

if len(RnameArray)<1:
	path = r"C:\Program Files (x86)\R"
	for files in os.walk(path):
		for name in files:
			for n in name:
				if n == "Rscript.exe":
					scriptPath = files[0] + "\Rscript.exe"
					RnameArray.append(scriptPath)
				

Rexe = " "
for i in RnameArray:
	if i.split("\\")[5]=="x64":
		Rexe = i
		break

if Rexe == " ":
	Rexe = RnameArray[0]
print Rexe
#########################################################
#Get header
#########################################################

ScriptLines = []
ScriptLines.append('workspace = "' + work + '"\n')
ScriptLines.append('PrimaryKey = "' + ZoneField + '"\n')
ScriptLines.append('outTableName = "' + outTableName + '"\n')

#########################################################
#write R script
#########################################################
newRscript = os.path.splitext(outTableName)[0] + '.R'
Lines = open(TemplateScript,'r').readlines()
OutputScript = open(newRscript,'w')
OutputScript.writelines(ScriptLines)
OutputScript.writelines(Lines)
OutputScript.close()

#########################################################
#Run R script
#########################################################
call = subprocess.Popen(Rexe + ' --save "' + newRscript + '"')
call.wait()
