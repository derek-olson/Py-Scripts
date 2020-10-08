import arcpy
import sklearn
import os
import sys
import geopandas as gpd
import numpy as np
import pandas as pd
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# TODO: figure out how to install libraries on to computer

# Inputs
Input_Shapefile = r"\\166.2.126.25\teui1\4_Derek\AWS_POC\Zonal_Statistics_Random_Forest_Classification_Python_Test\Data\Segments\Dixie_segments_refData_2.shp"  #arcpy.GetParameterAsText(0)
Shape_Unique_ID = "FID_Model" #arcpy.GetParameterAsText(1)
Response_Field = "L1" #arcpy.GetParameterAsText(2)
Zonal_Stats = r"\\166.2.126.25\teui1\4_Derek\AWS_POC\Zonal_Statistics_Random_Forest_Classification_Python_Test\Data\OutTables\ZonalStats.csv" #arcpy.GetParameterAsText(3)
Stats_Unique_ID = "FID_Model"#arcpy.GetParameterAsText(4)
Raster_List = ""#arcpy.GetParameterAsText(5)
Prediction_Type = 'Categorical' #arcpy.GetParameterAsText(6)
Output_Shapefile = ""#arcpy.GetParameterAsText(7)

print("****************************************")
print("Printing Input Variables")
print("featureInput: {0}".format(Input_Shapefile))
print("featureIDField: {0}".format(Shape_Unique_ID))
print("ResponseField: {0}".format(Response_Field))
print("ZonalStats: {0}".format(Zonal_Stats))
print("ZonalUniqueIDField: {0}".format(Stats_Unique_ID))

#  get the start time
program_start_time = time.time()

desc = arcpy.Describe(Input_Shapefile)

#if desc.shapeType == "Polygon":
#    print("polygons chosen")
#    # determine if correct data exists
#    try:
#        if Shape_Unique_ID is None:
#            print('Shape Unique ID is None')
#    except NameError:
#        print('Shape Unique ID is not defined')
#    else:
#        print("Shape Unique ID is defined and has a value")
#
#    try:
#        if Response_Field is None:
#            print('Response Field is None')
#    except NameError:
#        print('Response Field is not defined')
#    else:
#        print("Response Field is defined and has a value")
#
#    try:
#        if Zonal_Stats is None:
#            print('Zonal_Stats is None')
#    except NameError:
#        print('Zonal Stats are not defined')
#    else:
#        print("Zonal_Stats is defined and has a value")
#
#    try:
#        if Stats_Unique_ID is None:
#            print('Stats Unique ID is None')
#    except NameError:
#        print('Stats Unique ID field is not defined')
#    else:
#        print("Stats Unique ID field is defined and has a value")
#
#    try:
#        if Output_Shapefile is None:
#            print('Output Shapefile is None')
#    except NameError:
#        print('Output Shapefile is not defined')
#    else:
#        print("Output Shapefile is defined and has a value")

# get a list of the zonal stats field names
#def list_fields(dataset):
#    fields = arcpy.ListFields(dataset)
#    return fields
#
#shape_fields = list_fields(Input_Shapefile)

# use geopandas to read in the data
in_shape = gpd.read_file(Input_Shapefile)
in_stats = pd.read_csv(Zonal_Stats)

# test table lengths
in_shape_table = pd.DataFrame(in_shape)
in_shape_length = len(in_shape_table.index)
in_stats_length = len(in_stats.index)

if in_shape_length > in_stats_length:
    print('More features than zonal stats rows')
    #sys.exit()
elif in_shape_length < in_stats_length:
    print('Fewer features than zonal stats rows')
    #sys.exit()
elif in_shape_length == in_stats_length:
    print('Zones and stats have same length')

# test that unique ID fields are the same
shape_id_list = in_shape_table[Shape_Unique_ID].tolist()
shape_id_list.sort()
zone_id_list = in_stats[Stats_Unique_ID].tolist()
zone_id_list.sort()

if shape_id_list == zone_id_list:
    print("The zone id list and the zonal stat id list are identical")
else:
    print("The zone id list and the zonal stat id list are not identical")
    #sys.exit()

# join the zonal stats to the polygons
# arcpy join - use if geopandas doesn't work
#joined_table = arcpy.AddJoin_management(Input_Shapefile, Shape_Unique_ID, Zonal_Stats, Stats_Unique_ID)

# join with geopandas
joined_table = in_shape_table.merge(in_stats, how='inner', left_on=Shape_Unique_ID, right_on=Stats_Unique_ID)

# subset the data
zstat_fields = list(in_stats.columns.values)
zstat_fields.insert(0, Response_Field)
analysis_table = joined_table[zstat_fields]

# Get the unique ID field and the reference field
X = analysis_table[analysis_table.L1.notnull()]

# Create a dictionary of the reference classes
labels = X[Response_Field].tolist()
refSet = set(labels)
nLabels = range(0, len(refSet))
labelDict = dict(zip(nLabels, refSet))

# Encode the labels
le = preprocessing.LabelEncoder()
le.fit(labels)
encodedLabels = le.transform(labels)
print(encodedLabels)

#create the training and testing data
y = X[Response_Field]
X = X.drop([Shape_Unique_ID, Stats_Unique_ID, Response_Field], axis=1)

# Split the data
train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.25, random_state = 42)

# get the data type
if data_type == 'categorical':

    # Create Random Forest Classifier
    RFmodel = RandomForestClassifier(n_estimators=500, random_state=0)
    
    # Train the model
    classModel = RFmodel.fit(np.array(train_X), np.array(train_y).ravel())
    print(classModel.feature_importances_)
    oob_error = 1 - classModel.oob_score_
    print(oob_error)
    
    # Evaluate the model on the testing data
    score = classModel.score(test_X, test_y)
    print(score)
    
    # Join the polygons to the zonal stats
    predict_X = pd.merge(in_shape_table[[Shape_Unique_ID]], in_stats, how='inner', left_on=Shape_Unique_ID, right_on=Stats_Unique_ID)
    predict_X = np.array(predict_X.drop([Shape_Unique_ID, Stats_Unique_ID], axis=1))
    
    # Apply the model to the polygons
    modelPredict = pd.DataFrame(classModel.predict(predict_X))
    modelPredictProb = pd.DataFrame(classModel.predict_proba(predict_X))

elif data_type == 'continuous':

    # Create Random Forest Classifier
    RFmodel = RandomForestClassifier(n_estimators=500, random_state=0)
    
    # Train the model
    classModel = RFmodel.fit(np.array(train_X), np.array(train_y).ravel())
    print(classModel.feature_importances_)
    oob_error = 1 - classModel.oob_score_
    print(oob_error)
    
    # Evaluate the model on the testing data
    score = classModel.score(test_X, test_y)
    print(score)
    
    # Join the polygons to the zonal stats
    predict_X = pd.merge(in_shape_table[[Shape_Unique_ID]], in_stats, how='inner', left_on=Shape_Unique_ID, right_on=Stats_Unique_ID)
    predict_X = np.array(predict_X.drop([Shape_Unique_ID, Stats_Unique_ID], axis=1))
    
    # Apply the model to the polygons
    modelPredict = pd.DataFrame(classModel.predict(predict_X))
    modelPredictProb = pd.DataFrame(classModel.predict_proba(predict_X))
# if desc == "Point":
#     print('Running point based Random Forest')
#
#     # determine if correct data exists
#     try:
#         if Shape_Unique_ID is None:
#             print('Shape Unique ID is None')
#     except NameError:
#         print('Shape Unique ID is not defined')
#     else:
#         print("Shape Unique ID is defined and has a value")
#
#     try:
#         if Response_Field is None:
#             print('Response Field is None')
#     except NameError:
#         print('Response Field is not defined')
#     else:
#         print("Response Field is defined and has a value")
#
#     try:
#         if Zonal_Stats is None:
#             print('Zonal_Stats is None')
#     except NameError:
#         print('Zonal Stats are not defined')
#     else:
#         print("Zonal_Stats is defined and has a value")
#
#     try:
#         if Stats_Unique_ID is None:
#             print('Stats Unique ID is None')
#     except NameError:
#         print('Stats Unique ID field is not defined')
#     else:
#         print("Stats Unique ID field is defined and has a value")
#
#     try:
#         if Output_Shapefile is None:
#             print('Output Shapefile is None')
#     except NameError:
#         print('Output Shapefile is not defined')
#     else:
#         print("Output Shapefile is defined and has a value")





program_end_time = time.time()
program_time_minutes = (program_end_time - program_start_time) / 60
print(program_time_minutes)


