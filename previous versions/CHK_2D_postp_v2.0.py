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

NumPartitions_x = 24
NumPartitions_y = 2

factorUSED = 1
ElementSize   = (Model_enddim_y/NumPartitions_y)/factorUSED
#-----------------------------------------------------------------
# some identifier variables defined
ODB_ID            = 0
ODB_FileName_list = ['sunil', 'haha']
TotalNumFrames    = [18, 0]
#--------------------------------------------------------
# defining filenames
RandomNumber_START_MATLAB_OUTPUT = str(4847864798)
RandomNumber_END_MATLAB_OUTPUT   = str(9948322254)
#--------------------------------------------------------
# frame incerements needed
# texture id value
# Elements per grain value
# elemebnt type value
frincr = 1
TEXIDVALUE = '01'
EPGValue   = '001'
ElementType = 'CPS4'
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
# loop over frames for Stresses (S)
#pausetimeseconds = 0.2
#for fr in range(0, TotalNumFrames[ODB_ID], frincr):
#	# Get the first frame
#	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
#	# pause for some time to allow user to see the frame
#	time.sleep(pausetimeseconds)

#odbPath = "sunil.odb"
#odb = visualization.openOdb(path = odbPath)

#myViewport = session.Viewport(name = 'this is the name of the viewport', origin = (00,00), width = 250, height = 150)
#myViewport.setValues(displayedObject = odb)

#session.printToFile('haha', PNG, (myViewport, ))

#session.viewports[session.currentViewportName].odbDisplay.setFrame(step = 'Step-1', frame = 17)
#-----------------------------------------------------------------
Python script for stress-strain graph
This commit is a python script to read stress-strain data files which are output by 'CHK_2D_postp_v2.0.py'