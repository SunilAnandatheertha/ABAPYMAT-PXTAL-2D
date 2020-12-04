from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup
import os
import visualization
import time
import numpy as np
#-----------------------------------------------------------------
executeOnCaeStartup()
Mdb()
#-----------------------------------------------------------------
# model and basic element dimensions
Model_origin_x = 0.
Model_origin_y = 0.

Model_enddim_x = 100.0
Model_enddim_y = 6.0
Model_enddim_z = 1.0 # Assuming unit thickness
#-----------------------------------------------------------------
# some identifier variables defined
ODB_ID            = 3
ODB_FileName_list = ['sunil', 'haha', 'Job-1', 'Job-2']
TotalNumFrames    = [18, 0, 18, 14]

NumPartitions_x_list = [24, 0, 17, 2]
NumPartitions_y_list = [02, 0, 01, 2]

NumPartitions_x = NumPartitions_x_list[ODB_ID]
NumPartitions_y = NumPartitions_y_list[ODB_ID]

factorUSED = 1
ElementSize   = (Model_enddim_y/NumPartitions_y)/factorUSED
#-----------------------------------------------------------------
# generate variable values needed to re-create element set names
Num_DatumPlanes_x = NumPartitions_x - 1
Num_DatumPlanes_y = NumPartitions_y - 1
#--------------------------------------------------------
# should the elemental results at centrouids be extracted? If extracted, they will be written to file
Extract_S11_ELCEN = 1
Extract_S22_ELCEN = 1
Extract_S12_ELCEN = 1
#--------------------------------------------------------
# defining filenames
RandomNumber_START_MATLAB_OUTPUT = str(4847864798)
RandomNumber_END_MATLAB_OUTPUT   = str(9948322254)
#--------------------------------------------------------
S11_contour_label_max_MPa = 1000
S11_contour_label_min_MPa = 0

S22_contour_label_max_MPa = 100
S22_contour_label_min_MPa = -100

S12_contour_label_max_MPa = 100
S12_contour_label_min_MPa = -100

Print_S11_Contours_File = 1
#--------------------------------------------------------
# frame incerements needed
# texture id value
# Elements per grain value
# elemebnt type value
frincr = 1
TEXIDVALUE  = '01'
EPGValue    = '001'
ElementType = 'CPS4'
#-----------------------------------------------------------------
#  VIEWPORT - 1
VP_num              = 1
VP_name             = 'Viewport: ' + str(VP_num)
VP_ODB_PathName     = 'C:/Temp/CalibrationModels/Cal_100ng/'
VP_ODB_FileName     = ODB_FileName_list[ODB_ID] + '.odb'
VP_ODB_FullPathName = VP_ODB_PathName + VP_ODB_FileName

MVPport = session.Viewport(name = VP_name, origin = (0.0, 0.0), width = 150, height = 100)
SESS_VP = session.viewports[VP_name]
SESS_VP.makeCurrent()
SESS_VP.maximize()
SESS_VP.partDisplay.geometryOptions.setValues(referenceRepresentation = ON)
SESS_VP.setValues(displayedObject = None)

Associate_ODB = session.openOdb(name = VP_ODB_FullPathName)
SESS_VP.setValues(displayedObject = Associate_ODB)
#-----------------------------------------------------------------
# Display contour plot
SESS_VP.odbDisplay.display.setValues(plotState = (CONTOURS_ON_DEF, ))
# put the first frame on scree
SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = 0)
# adjust fonts and display styles
session.graphicsOptions.setValues(backgroundStyle = SOLID)
session.graphicsOptions.setValues(backgroundColor = '#FFFFFF')
SESS_VP.viewportAnnotationOptions.setValues(legendFont = '-*-verdana-medium-r-normal-*-*-160-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(titleFont  = '-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(stateFont  = '-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(legendBox  = OFF)
SESS_VP.viewportAnnotationOptions.setValues(legendNumberFormat  = FIXED)
SESS_VP.viewportAnnotationOptions.setValues(legendDecimalPlaces = 1)

# Set the contour display to the variable of interest
#SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (COMPONENT, 'S11'  ), )
SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (INVARIANT, 'Mises'), )
#-----------------------------------------------------------------
# partname and set names
thispartname = 'PARTNAME-1'
NodeSetName_1  = 'FULLEDGE_X-'
NodeSetName_2  = 'FULLEDGE_X+'
#-----------------------------------------------------------------
# define path for acquiring reaction forces
NumNodes_NodeSetName_1 = len(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName_1].nodes)
Nodes_For_Path_1       = np.zeros(NumNodes_NodeSetName_1, dtype = int)
count = 0
for NthNode in range(0, NumNodes_NodeSetName_1, 1):
	Nodes_For_Path_1[count] = int(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName_1].nodes[NthNode].label)
	count = count + 1
session.Path(name = 'path_x-', type = NODE_LIST, expression = ((thispartname, tuple(Nodes_For_Path_1)), ))

# define path for acquiring nodal displacements at displacemed edge
NumNodes_NodeSetName_2 = len(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName_2].nodes)
Nodes_For_Path_2       = np.zeros(NumNodes_NodeSetName_2, dtype = int)
count = 0
for NthNode in range(0, NumNodes_NodeSetName_2, 1):
	Nodes_For_Path_2[count] = int(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName_2].nodes[NthNode].label)
	count = count + 1
session.Path(name = 'path_x+', type = NODE_LIST, expression = ((thispartname, tuple(Nodes_For_Path_2)), ))
#-----------------------------------------------------------------
# lets add some fun
pausetimeseconds = 0.2
#-----------------------------------------------------------------
# select the path as a node list
PathName_xminus         = session.paths['path_x-']
PathName_xplus          = session.paths['path_x+']
#-----------------------------------------------------------------
# initialize variables
TimeInstances      = range(0, TotalNumFrames[ODB_ID], frincr)
TimeSTEPValues     = range(0, TotalNumFrames[ODB_ID], frincr)

ReactionForces_x   = np.zeros(len(range(0, TotalNumFrames[ODB_ID], frincr)), dtype = 'float')
ReactionForces_y   = np.zeros(len(range(0, TotalNumFrames[ODB_ID], frincr)), dtype = 'float')

RF_X_time_Data     = np.zeros((NumNodes_NodeSetName_1, len(TimeInstances)))
RF_X_time_Data_SUM = np.zeros(len(TimeInstances))
RF_Y_time_Data     = np.zeros((NumNodes_NodeSetName_1, len(TimeInstances)))
RF_Y_time_Data_SUM = np.zeros(len(TimeInstances))

U_X_time_Data      = np.zeros((NumNodes_NodeSetName_2, len(TimeInstances)))
U_X_time_Data_SUM  = np.zeros(len(TimeInstances))
U_X_time_Data_AVG  = np.zeros(1)
U_Y_time_Data      = np.zeros((NumNodes_NodeSetName_2, len(TimeInstances)))
U_Y_time_Data_SUM  = np.zeros(len(TimeInstances))
U_Y_time_Data_AVG  = np.zeros(1)
#-----------------------------------------------------------------
# loop over frames to find out the reaction forces X on all nodes belonging to the node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Reaction force - 1
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'RF', outputPosition = NODAL, refinement = (COMPONENT, 'RF1'))
	print 'Extracting reaction forces X for nodes on path: ' + PathName_xminus.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'newdata', path = PathName_xminus, includeIntersections = True, 
			 projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
			 projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName_1, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of reaction force
		RF_X_time_Data[nthnode, fr] = xy[nthnode][colpos]
	RF_X_time_Data_SUM[fr] =  np.sum(RF_X_time_Data[:, fr])

# loop over frames to find out the reaction forces Y on all nodes belonging to the node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Reaction force - 2
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'RF', outputPosition = NODAL, refinement = (COMPONENT, 'RF2'))
	print 'Extracting reaction forces Y for nodes on path: ' + PathName_xminus.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'newdata', path = PathName_xminus, includeIntersections = True, 
			 projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
			 projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName_1, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of reaction force
		RF_Y_time_Data[nthnode, fr] = xy[nthnode][colpos]
	RF_Y_time_Data_SUM[fr] =  np.sum(RF_Y_time_Data[:, fr])
#-----------------------------------------------------------------
# loop over frames to find out the nodal displkacements U1 and calculate their averages on all nodes belonging to the node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Nodal displacement U1
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'U', outputPosition = NODAL, refinement = (COMPONENT, 'U1'), )
	print 'Extracting nodal displacements U1 for nodes on path: ' + PathName_xplus.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'sss', path = PathName_xplus, includeIntersections = True, 
		     projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
		     projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName_2, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of nodal displacemebt U1
		U_X_time_Data[nthnode, fr] = xy[nthnode][colpos]
	U_X_time_Data_SUM[fr] =  np.sum(U_X_time_Data[:, fr])
U_X_time_Data_AVG = U_X_time_Data_SUM/NumNodes_NodeSetName_2

# loop over frames to find out the nodal displkacements U2 and calculate their averages on all nodes belonging to the node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Nodal displacement U2
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'U', outputPosition = NODAL, refinement = (COMPONENT, 'U2'), )
	print 'Extracting nodal displacements U2 for nodes on path: ' + PathName_xplus.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'sss', path = PathName_xplus, includeIntersections = True, 
		     projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
		     projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName_2, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of nodal displacemebt U2
		U_Y_time_Data[nthnode, fr] = xy[nthnode][colpos]
	U_Y_time_Data_SUM[fr] =  np.sum(U_Y_time_Data[:, fr])
U_Y_time_Data_AVG = U_Y_time_Data_SUM/NumNodes_NodeSetName_2
#-----------------------------------------------------------------
# Calculate stress and total applied strain
stress_xx      = RF_X_time_Data_SUM / (Model_enddim_y * Model_enddim_z)
stress_xx =  [abs(ele) for ele in stress_xx]
totalstrain_xx = U_X_time_Data_AVG  / Model_enddim_x
#-----------------------------------------------------------------
# Get the actual time step values
STEPNAME = 'Step-1'
ThisStep = Associate_ODB.steps[STEPNAME]
STEPINFO = np.zeros((len(TimeInstances),2))
count = 0
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	ThisStepFrame = ThisStep.frames[fr]
	TimeSTEPValues[fr] = ThisStep.frames[fr].frameValue
	STEPINFO[count, 0] = count
	STEPINFO[count, 1] = TimeSTEPValues[fr]
	count = count + 1
# print STEPINFO
#-----------------------------------------------------------------
# find out the number of time steps
ALL_STEPS = Associate_ODB.steps.values()
print 'there are ' + '___' + str(len(ALL_STEPS)) + '___' + 'Time steps in this model'
#-----------------------------------------------------------------
# select the first time step
TIME_STEP_OF_INTEREST = 0 # this is to be later iterated upon if there are more than 1 time steps
THISSTEP              = ALL_STEPS[TIME_STEP_OF_INTEREST]
#-----------------------------------------------------------------
fr           = 10

frame        = THISSTEP.frames[fr]
displacement = frame.fieldOutputs['U']
stress       = frame.fieldOutputs['S']
myInstance   = Associate_ODB.rootAssembly.instances[thispartname]
elmnum       = 0
#-----------------------------------------------------------------
################################################################################################################################################################
################################################################################################################################################################
## GET THE VALUES OF FIELD VARIABLES AT EVERY ELEMENT CENTROID SORTED FOR GRAINS
# python dictionaries are used to store the values
# Following are the critical variables which are populated
# DICT-1: FIELDVARIBLE_ELEM_CENTROID: This contains actual values of field variable at centroid of every elem of every grain
# DICT-2: MAP_Grain_ElementsinGrain_FIELDVARIBLENAME: This maps the basic statistics of field variable values to the grainname
## HERE ENDS THE DESCRIPTION

# DICTIONARY -- 1
# initialize dictionaries-1 for the model for S11, S22 and S12. 
# dict Key holds grain number. Values include stress values
TotalNumberOfGrains = NumPartitions_x * NumPartitions_y
S11_ELEM_CENTROID   = dict.fromkeys(range(TotalNumberOfGrains))
S22_ELEM_CENTROID   = dict.fromkeys(range(TotalNumberOfGrains))
S12_ELEM_CENTROID   = dict.fromkeys(range(TotalNumberOfGrains))
grainnum = 0
# DICTIONARY -- 2
# Data format of the dictionary-2
# key: python_GrainIndex
# key value 01: Grain number
# key value 02: Grain name
# key value 03: 
# key value 04: 
# key value 05: 
# key value 06: 
# key value 07: 
# key value 08: 
# key value 09: 
# key value 10: 
# key value 11: 
MAP_Grain_ElementsinGrain_DF = {'python_GrainIndex': ['GNum', 'Gname', 'NE_G', 'S11EG_max', 'S11Eg_min', 'S11Eg_mean', 'S11Eg_std']}
# Where,
# GNum:       01. Grain number
# Gname:      02. Grain name
# NE_G:       03. NumberOfElementsInthisGrain
# S11Eg_max:  04. max      of S11 amongst all elements belonging to the grain g of all grains G
# S11Eg_min:  05. min      of S11 amongst all elements belonging to the grain g of all grains G
# S11Eg_mean: 06. mean     of S11 amongst all elements belonging to the grain g of all grains G
# S11Eg_std:  07. std.dev. of S11 amongst all elements belonging to the grain g of all grains G
# Same format applies to all other field variables requested, unless explicitly described
max(thisgrainelements_S11), min(thisgrainelements_S11), np.mean(thisgrainelements_S11), np.std(thisgrainelements_S11)

MAP_Grain_ElementsinGrain_S11 = dict.fromkeys(range(TotalNumberOfGrains))
MAP_Grain_ElementsinGrain_S22 = dict.fromkeys(range(TotalNumberOfGrains))
MAP_Grain_ElementsinGrain_S12 = dict.fromkeys(range(TotalNumberOfGrains))
#-----------------------------------------------------------------
# extract, store and write elemental stress values @ element centroid
ElementType = stress.values[0].baseElementType
yaddfactor  = [1, 2][Num_DatumPlanes_y >= 1] # this is if else::::: [value_false, value_true][<test>]

if Extract_S11_ELCEN == 1:
	print 'Extracting individual S11 @ element centroid for every element of every grain'
	for jj in range(1, Num_DatumPlanes_y + yaddfactor):
		for ii in range(1, Num_DatumPlanes_x + 2):
			print 'processing stresses for individual elements in grain number _____' + str(grainnum)
			print '\n'
			# recreate 'element set name' of all elements in a (ii, jj) grain
			ElemSetName = 'GRAIN_NX_' + str(ii) + '_NY_' + str(jj)
			# iterate over all  elements belonging to this grain
			thisgrainelements_S11 = range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1)
			for elem in range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1):
				# extract S11 for this element at its centroid and store its value in key's values in dict S11_ELEM_CENTROID
				thisgrainelements_S11[elem] = stress.getSubset(region = myInstance.elementSets[ElemSetName].elements[elem],position = CENTROID, elementType = ElementType).values[0].data[0]
			S11_ELEM_CENTROID[grainnum] = thisgrainelements_S11
			# Extract this grain details
			GrainName                   = ElemSetName
			NumberOfElementsInthisGrain = len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements)
			MAP_Grain_ElementsinGrain_S11[grainnum] = [grainnum+1, GrainName, NumberOfElementsInthisGrain, max(thisgrainelements_S11), min(thisgrainelements_S11), np.mean(thisgrainelements_S11), np.std(thisgrainelements_S11)]
			# go to next grain
			grainnum = grainnum + 1
else:
	print 'NOT Extracting individual S11 @ element centroid for every element of every grain'

if Extract_S22_ELCEN==1:
	print 'Extracting individual S22 @ element centroid for every element of every grain'
	for jj in range(1, Num_DatumPlanes_y + yaddfactor):
		for ii in range(1, Num_DatumPlanes_x + 2):
			print 'processing stresses for individual elements in grain number _____' + str(grainnum)
			print '\n'
			# recreate 'element set name' of all elements in a (ii, jj) grain
			ElemSetName = 'GRAIN_NX_' + str(ii) + '_NY_' + str(jj)
			# iterate over all  elements belonging to this grain
			thisgrainelements_S22 = range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1)
			for elem in range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1):
				# extract S11 for this element at its centroid and store its value in key's values in dict S11_ELEM_CENTROID
				thisgrainelements_S22[elem] = stress.getSubset(region = myInstance.elementSets[ElemSetName].elements[elem],position = CENTROID, elementType = ElementType).values[0].data[1]
			S22_ELEM_CENTROID[grainnum] = thisgrainelements_S22
			# Extract this grain details
			GrainName                   = ElemSetName
			NumberOfElementsInthisGrain = len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements)
			MAP_Grain_ElementsinGrain_S22[grainnum] = [grainnum+1, GrainName, NumberOfElementsInthisGrain, max(thisgrainelements_S11), min(thisgrainelements_S11), np.mean(thisgrainelements_S11), np.std(thisgrainelements_S11)]
			# go to next grain
			grainnum = grainnum + 1
else:
	print 'NOT Extracting individual S22 @ element centroid for every element of every grain'

if Extract_S12_ELCEN==1:
	print 'Extracting individual S12 @ element centroid for every element of every grain'
	for jj in range(1, Num_DatumPlanes_y + yaddfactor):
		for ii in range(1, Num_DatumPlanes_x + 2):
			print 'processing stresses for individual elements in grain number _____' + str(grainnum)
			print '\n'
			# recreate 'element set name' of all elements in a (ii, jj) grain
			ElemSetName = 'GRAIN_NX_' + str(ii) + '_NY_' + str(jj)
			# iterate over all  elements belonging to this grain
			thisgrainelements_S12 = range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1)
			for elem in range(0, len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements), 1):
				# extract S11 for this element at its centroid and store its value in key's values in dict S11_ELEM_CENTROID
				thisgrainelements_S12[elem] = stress.getSubset(region = myInstance.elementSets[ElemSetName].elements[elem],position = CENTROID, elementType = ElementType).values[0].data[3]
			S12_ELEM_CENTROID[grainnum] = thisgrainelements_S12
			# Extract this grain details
			GrainName                   = ElemSetName
			NumberOfElementsInthisGrain = len(Associate_ODB.rootAssembly.instances[thispartname].elementSets[ElemSetName].elements)
			MAP_Grain_ElementsinGrain_S22[grainnum] = [grainnum+1, GrainName, NumberOfElementsInthisGrain, max(thisgrainelements_S11), min(thisgrainelements_S11), np.mean(thisgrainelements_S11), np.std(thisgrainelements_S11)]
			# go to next grain
			grainnum = grainnum + 1
else:
	print 'NOT Extracting individual S12 @ element centroid for every element of every grain'
#-----------------------------------------------------------------
# Write individual S11 @ element centroid for every element of every grain to file
# Ignore 1st row in written file
# From second row to last row, each row represents grain number in the following format
# G06 G07 G08 G09 G10
# G01 G02 G03 G04 G05
# Every column in a row is the stress at the centroid at every element in the grain
# Res_Data_Root_Filename_9: Stress xx - every element centroid
Res_Data_Root_Filename_9 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_Stress_11_ElemWise_AT_CENTROID____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT
if Extract_S11_ELCEN==1:
	S11filename = Res_Data_Root_Filename_9 + '.txt'
	S11file = open(S11filename, "w")
	print 'Writing individual S11 @ element centroid for every element of every grain to file'
	for k, v in S11_ELEM_CENTROID.items():
		thestringa = str(v)
		thestringb = thestringa.replace('[', '')
		thestringc = thestringb.replace(']', '')
		S11file.write(thestringc + '\n')
	del thestringa
	del thestringb
	del thestringc
	S11file.close()
else:
	print 'NOT writing individual S11 @ element centroid for every element of every grain to file'
#-----------------------------------------------------------------
# Write individual S22 @ element centroid for every element of every grain to file
# Res_Data_Root_Filename_10: Stress 22 - every element centroid
Res_Data_Root_Filename_10 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_Stress_22_ElemWise_AT_CENTROID____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT
if Extract_S22_ELCEN==1:
	S22filename = Res_Data_Root_Filename_10 + '.txt'
	S22file = open(S22filename, "w")
	print 'Writing individual S22 @ element centroid for every element of every grain to file'
	for k, v in S22_ELEM_CENTROID.items():
		thestringa = str(v)
		thestringb = thestringa.replace('[', '')
		thestringc = thestringb.replace(']', '')
		S22file.write(thestringc + '\n')
	del thestringa
	del thestringb
	del thestringc
	S11file.close()
else:
	print 'NOT writing individual S11 @ element centroid for every element of every grain to file'
#-----------------------------------------------------------------
# Write individual S12 @ element centroid for every element of every grain to file
# Res_Data_Root_Filename_11: Stress 12 - every element centroid
Res_Data_Root_Filename_11 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_Stress_12_ElemWise_AT_CENTROID____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT
if Extract_S12_ELCEN==1:
	S12filename = Res_Data_Root_Filename_11 + '.txt'
	S12file = open(S12filename, "w")
	print 'Writing individual S12 @ element centroid for every element of every grain to file'
	for k, v in S12_ELEM_CENTROID.items():
		thestringa = str(v)
		thestringb = thestringa.replace('[', '')
		thestringc = thestringb.replace(']', '')
		S12file.write(thestringc + '\n')
	del thestringa
	del thestringb
	del thestringc
	S11file.close()
else:
	print 'NOT writing individual S11 @ element centroid for every element of every grain to file'
################################################################################################################################################################
################################################################################################################################################################


#IPN = 1 # Integration point number
#print stress.values[IPN].data

	
# calculate the stresses for each elemenbt in each grain

# calculate the grain averaged stress

# calculate the grain volume averaged stress
#--------------------------------------------------------
# construct file names

# Res_Data_Root_Filename_1: time steps
Res_Data_Root_Filename_1 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_TSteps____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_2: reaction force x
Res_Data_Root_Filename_2 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_RFX____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_3: reaction force y
Res_Data_Root_Filename_3 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_RFY____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_4: UX_avg
Res_Data_Root_Filename_4 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_UXavg____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_5: UY_avg
Res_Data_Root_Filename_5 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_UYavg____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_6: Stress xx
Res_Data_Root_Filename_6 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_Stress_XX____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_7: Strain xx
Res_Data_Root_Filename_7 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_Strain_XX____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

# Res_Data_Root_Filename_8: Stress xx - contour plot image file
Res_Data_Root_Filename_8 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____IMG_Stress_XX_CONTOUR____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT + '__RESFrameNum___'

# Res_Data_Root_Filename_9 : Stress 11 @ centroid of every element in every grain
# Res_Data_Root_Filename_10: Stress 22 @ centroid of every element in every grain
# Res_Data_Root_Filename_11: Stress 12 @ centroid of every element in every grain
# The above three names have already been defined mech before. So use from 'Res_Data_Root_Filename_12' onwards

# Res_Data_Root_Filename_12: Decription
#--------------------------------------------------------
# Write TimeStepData to file
outputFile = open(Res_Data_Root_Filename_1 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(TimeSTEPValues[fr]) + '\n')
outputFile.close()

# Write RF-X to file
outputFile = open(Res_Data_Root_Filename_2 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(RF_X_time_Data_SUM[fr]) + '\n')
outputFile.close()

# Write RF-Y to file
outputFile = open(Res_Data_Root_Filename_3 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(RF_Y_time_Data_SUM[fr]) + '\n')
outputFile.close()

# Res_Data_Root_Filename_4: UX_avg
outputFile = open(Res_Data_Root_Filename_4 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(U_X_time_Data_AVG[fr]) + '\n')
outputFile.close()

# Res_Data_Root_Filename_5: UY_avg
outputFile = open(Res_Data_Root_Filename_5 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(U_Y_time_Data_AVG[fr]) + '\n')
outputFile.close()

# Res_Data_Root_Filename_6: Stress xx
outputFile = open(Res_Data_Root_Filename_6 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(stress_xx[fr]) + '\n')
outputFile.close()

# Res_Data_Root_Filename_7: Strain xx
outputFile = open(Res_Data_Root_Filename_7 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(totalstrain_xx[fr]) + '\n')
outputFile.close()
#--------------------------------------------------------
# display S11 contours
SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (COMPONENT, 'S11'), )
# set contour display styles
session.viewports[VP_name].odbDisplay.contourOptions.setValues(numIntervals = 10) # 2 to 24
session.viewports[VP_name].odbDisplay.contourOptions.setValues(contourEdges = OFF)
session.viewports[VP_name].odbDisplay.contourOptions.setValues(contourEdgeThickness = VERY_THIN) # VERY_THIN, THIN, MEDIUM, THICK
session.viewports[VP_name].odbDisplay.contourOptions.setValues(contourEdgeStyle = DASHED) # 
session.viewports[VP_name].odbDisplay.commonOptions.setValues(deformationScaling = UNIFORM) # uniform deformed shape scaling. scaling factor is unity by dafault
session.viewports[VP_name].odbDisplay.commonOptions.setValues(renderStyle = SHADED)
session.viewports[VP_name].odbDisplay.commonOptions.setValues(visibleEdges = FREE) # only show free edges
session.viewports[VP_name].odbDisplay.commonOptions.setValues(edgeLineThickness = MEDIUM) # set model edge line thickness
# set max and min limits for S11 legend
SESS_VP.odbDisplay.contourOptions.setValues(maxAutoCompute = OFF, maxValue = S11_contour_label_max_MPa, minAutoCompute = OFF, minValue = S11_contour_label_min_MPa)
# set off title block
session.viewports[VP_name].viewportAnnotationOptions.setValues(title = OFF)
# loop over frames to display S11 contours
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (COMPONENT, 'S11'), )
	#SESS_VP.setValues(displayedObject = odb)
	if Print_S11_Contours_File == 1:
		if fr < 10:
			thisIMGfilename = Res_Data_Root_Filename_8 + '000'+ str(fr)
		elif fr >= 10 and fr < 100:
			thisIMGfilename = Res_Data_Root_Filename_8 + '00'+ str(fr)
		elif fr >= 100 and fr < 1000:
			thisIMGfilename = Res_Data_Root_Filename_8 + '0'+ str(fr)
		else:
			thisIMGfilename = Res_Data_Root_Filename_8 + str(fr)
		session.printOptions.setValues(reduceColors = True)
		session.printToFile(thisIMGfilename, PNG, (SESS_VP, ))
	else:
		dummy = 0
		del dummy
#--------------------------------------------------------
#to annotate, use the following codes
#t = session.odbs['C:/Temp/CalibrationModels/Cal_100ng/Job-2.odb'].userData.Text(
#    name='texthere', text='Text-1', offset=(20, 50), anchor=(0, 0), 
#    referencePoint=(40, 0), 
#    font='-*-arial-medium-r-normal-*-*-140-*-*-p-*-*-*', box=ON)
#session.viewports['Viewport: 1'].plotAnnotation(annotation=t)
#--------------------------------------------------------
#SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (INVARIANT, 'Mises'), )
#--------------------------------------------------------
# loop over frames for Stresses (S)
#pausetimeseconds = 0.2
#for fr in range(0, TotalNumFrames[ODB_ID], frincr):
#	# Get the first frame
#	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
#	# pause for some time to allow user to see the frame
#	time.sleep(pausetimeseconds)

#odbPath = "sunil.odb"
#odb = visualization.openOdb(path     = odbPath)
#myViewport = session.Viewport(name   = 'this is the name of the viewport', origin = (00,00), width = 250, height = 150)
#myViewport.setValues(displayedObject = odb)
#session.printToFile('haha', PNG, (myViewport, ))
#session.viewports[session.currentViewportName].odbDisplay.setFrame(step = 'Step-1', frame = 17)
#-----------------------------------------------------------------