# -*- coding: utf-8 -*-
"""
Created on Thu Oct 11 12:12:29 2018

@author: derekolson
"""
## THIS SCRIPT REQUIRES THAT THE MXD BE IN YOUR RECENT PROJECTS AND YOUR DIRECTORY STRUCTURE TO MATCH EXACTLY
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
#from selenium.webdriver.common.by import By

# open ArcMap
driver = webdriver.Remote(
    command_executor='http://localhost:9999',
    desired_capabilities={
        "debugConnectToRunningApp": 'false',
        "app": r"C:\Program Files (x86)\ArcGIS\Desktop10.5\bin\ArcMap.exe"
    })

# pause script for one minute to let ArcMap open
time.sleep(45)

# open an ArcMap project
arcmap = driver.find_element_by_name("Untitled - ArcMap")
gettingStarted = arcmap.find_element_by_name('ArcMap - Getting Started')
projList = gettingStarted.find_element_by_class_name('SysListView32')
project = projList.find_element_by_name('TEUI_Testing_Template_local')
project.click()
time.sleep(5)
opn = gettingStarted.find_element_by_name('Open')
opn.click()
time.sleep(5)
# navigate to the TEUI Toolbar
teuiTesting = driver.find_element_by_name('TEUI_Testing_Template_local.mxd - ArcMap')
pane = teuiTesting.find_element_by_name('xtpBarTop')
toolbar = pane.find_element_by_name('TEUI Toolbar')

# set the project location
loc = toolbar.find_element_by_name('Set project Location')
loc.click()
time.sleep(15)
selectProject = driver.find_element_by_name('Select Project')
tempProjDir = selectProject.find_element_by_name('G:\\TEUI_Toolkit_Testing\\TempProjectDirectory')
tempProjDir.click()
time.sleep(5)
openDir = selectProject.find_element_by_name('Open')
openDir.click()
time.sleep(5)
# run zonal stats
manageData = toolbar.find_element_by_name('Data')
manageData.click()

# manage data
teuiData = teuiTesting.find_element_by_name('TEUI Data')
addLayerText = teuiData.find_element_by_name('Add Layer')
allButtons = teuiData.find_elements_by_class_name('Button')
addLayerButton = allButtons[4]
addLayerButton.click()

zones = teuiTesting.find_element_by_name('Zones')
combo1 = zones.find_element_by_class_name('ComboBox')
combo1.click()
time.sleep(2)
dirListFeatures = combo1.find_element_by_class_name('ComboLBox')
featuresDir = dirListFeatures.find_element_by_name('G:\\TEUI_Toolkit_Testing')
featuresDir.click()
time.sleep(2)

#TEST IF ALREAD IN THE CORRECT FILE LOCATION

static = zones.find_element_by_class_name('Static')
featList = static.find_element_by_class_name('SysListView32')
features = featList.find_element_by_name('Features')
features.click()
addFeatures = zones.find_element_by_name('Add')
addFeatures.click()
time.sleep(5)

# add non-everlapping features
nonOvLapFeats = static.find_element_by_name('Non_Overlapping_Features')
nonOvLapFeats.click()
time.sleep(2)
addFeatures = zones.find_element_by_name('Add')
addFeatures.click()
time.sleep(2)
level7 = static.find_element_by_name('testingFeatures_level7_withMapUnits.shp')
level7.click()
time.sleep(2)
addFeatures = zones.find_element_by_name('Add')
addFeatures.click()
time.sleep(2)

# select the added features and assign a map unit column
featScrollViewer = teuiData.find_element_by_class_name('ScrollViewer')
featListView = featScrollViewer.find_element_by_class_name('ListView')
featDataItem = featListView.find_element_by_class_name('ListViewItem')
featCheckBox = featDataItem.find_element_by_class_name('CheckBox')
featCheckBox.click()
time.sleep(2)
mapUnitCombo = teuiData.find_element_by_class_name('ComboBox')
mapUnitCombo.click()
groupVeg = teuiData.find_element_by_name('GROUPVEG')
groupVeg.click()

# set raster data
addRasterButton = allButtons[8]
addRasterButton.click()
rasterDialogue = teuiTesting.find_element_by_name('Rasters')
oneLevelUp = teuiTesting.find_element_by_name('Up One Level')
oneLevelUp.click()
oneLevelUp.click()
GxContentsView = rasterDialogue.find_element_by_name('GxContentsView')
tempList = GxContentsView.find_element_by_class_name('SysListView32')
dirLists = tempList.find_element_by_name('Rasters')
dirLists.click()
addRastersDir = rasterDialogue.find_element_by_name('Add')
addRastersDir.click()






































