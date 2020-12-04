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
RESULTDATAROOTFILENAME1 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_TSteps____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

RESULTDATAROOTFILENAME2 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_RFX____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT

RESULTDATAROOTFILENAME3 = str(NumPartitions_x*NumPartitions_y) + 'Ng_' + str(NumPartitions_x) + 'x_'+ str(NumPartitions_y) + 'y_'+ 'TEXID' + TEXIDVALUE + '_' + 'EBG' + EPGValue + '_' + ElementType + '____DATA_RFY____' + '_id1_' + RandomNumber_START_MATLAB_OUTPUT + '_id2_' + RandomNumber_END_MATLAB_OUTPUT
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
session.graphicsOptions.setValues(backgroundColor='#FFFFFF')
SESS_VP.viewportAnnotationOptions.setValues(legendFont = '-*-verdana-medium-r-normal-*-*-160-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(titleFont  = '-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(stateFont  = '-*-verdana-medium-r-normal-*-*-140-*-*-p-*-*-*')
SESS_VP.viewportAnnotationOptions.setValues(legendBox = OFF)
SESS_VP.viewportAnnotationOptions.setValues(legendNumberFormat = FIXED)
SESS_VP.viewportAnnotationOptions.setValues(legendDecimalPlaces = 1)

# Set the contour display to the variable of interest
#SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (COMPONENT, 'S11'  ), )
SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'S', outputPosition = INTEGRATION_POINT, refinement = (INVARIANT, 'Mises'), )
#-----------------------------------------------------------------
# partname and set names
thispartname = 'PARTNAME-1'
NodeSetName  = 'FULLEDGE_X-'
#-----------------------------------------------------------------
NumNodes_NodeSetName = len(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName].nodes)
Nodes_For_Path       = np.zeros(NumNodes_NodeSetName, dtype = int)
count = 0
for NthNode in range(0, NumNodes_NodeSetName, 1):
	Nodes_For_Path[count] = int(Associate_ODB.rootAssembly.instances[thispartname].nodeSets[NodeSetName].nodes[NthNode].label)
	count = count + 1
session.Path(name = 'path_x-', type = NODE_LIST, expression = ((thispartname, tuple(Nodes_For_Path)), ))
#-----------------------------------------------------------------
# lets add some fun
pausetimeseconds = 0.2
#-----------------------------------------------------------------
# select the path as a node list
PathName         = session.paths['path_x-']
#-----------------------------------------------------------------
# initialize variables
TimeInstances      = range(0, TotalNumFrames[ODB_ID], frincr)
TimeSTEPValues     = range(0, TotalNumFrames[ODB_ID], frincr)

ReactionForces_x   = np.zeros(len(range(0, TotalNumFrames[ODB_ID], frincr)), dtype = 'float')
ReactionForces_y   = np.zeros(len(range(0, TotalNumFrames[ODB_ID], frincr)), dtype = 'float')

RF_X_time_Data     = np.zeros((NumNodes_NodeSetName, len(TimeInstances)))
RF_X_time_Data_SUM = np.zeros(len(TimeInstances))

RF_Y_time_Data     = np.zeros((NumNodes_NodeSetName, len(TimeInstances)))
RF_Y_time_Data_SUM = np.zeros(len(TimeInstances))
#-----------------------------------------------------------------
# loop over frames to find out the reaction forces X on all nodes belonging to this node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Reaction force - 1
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'RF', outputPosition = NODAL, refinement = (COMPONENT, 'RF1'))
	print 'Extracting reaction forces X for nodes on path: ' + PathName.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'newdata', path = PathName, includeIntersections = True, 
			 projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
			 projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of reaction force
		RF_X_time_Data[nthnode, fr] = xy[nthnode][colpos]
		#print xy
	RF_X_time_Data_SUM[fr] =  np.sum(RF_X_time_Data[:, fr])
#-----------------------------------------------------------------
# loop over frames to find out the reaction forces Y on all nodes belonging to this node path
for fr in range(0, TotalNumFrames[ODB_ID], frincr):
	SESS_VP.odbDisplay.setFrame(step = 'Step-1', frame = fr)
	# Reaction force - 2
	SESS_VP.odbDisplay.setPrimaryVariable(variableLabel = 'RF', outputPosition = NODAL, refinement = (COMPONENT, 'RF2'))
	print 'Extracting reaction forces Y for nodes on path: ' + PathName.name + '... FRAME:   ' + str(fr)
	time.sleep(pausetimeseconds/5)
	xy = session.XYDataFromPath(name = 'newdata', path = PathName, includeIntersections = True, 
			 projectOntoMesh = False, pathStyle = PATH_POINTS, numIntervals = 10, 
			 projectionTolerance = 0, shape = UNDEFORMED, labelType = TRUE_DISTANCE)
	for nthnode in range(0, NumNodes_NodeSetName, 1):
		#colpos = 0 # value of y-coordinate of the node, i.e. distance from the first node which is taken at 0 by default
		colpos = 1 # value of reaction force
		RF_Y_time_Data[nthnode, fr] = xy[nthnode][colpos]
		#print xy
	RF_Y_time_Data_SUM[fr] =  np.sum(RF_Y_time_Data[:, fr])
#--------------------------------------------------------
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
print STEPINFO
#--------------------------------------------------------
# Write TimeStepData to file
outputFile = open(RESULTDATAROOTFILENAME1 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(TimeSTEPValues[fr]) + '\n')
outputFile.close()

# Write RF-X to file
outputFile = open(RESULTDATAROOTFILENAME2 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(RF_X_time_Data_SUM[fr]) + '\n')
outputFile.close()

# Write RF-Y to file
outputFile = open(RESULTDATAROOTFILENAME3 + '.txt', 'w')
for fr in range(0, TotalNumFrames[ODB_ID], frincr):	outputFile.write(str(TimeSTEPValues[fr]) + '\n')
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