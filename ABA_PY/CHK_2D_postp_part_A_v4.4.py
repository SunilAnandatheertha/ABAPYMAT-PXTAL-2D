"""
	COMPLETE DESCRIPTION HERE
"""
#-----------------------------------------------------------------
#1. Seperate this file for calibration models
#	MAKE THE PYTHON PRE, MATLAB AND PYTHON POST and SPYDER pipelines ready for calibrations
#	Set up the required folders
#	Set up the excel file where to store the file numbers and model numbers

#2. Seperate this file for residual stress induce model

#3. Seperate this file for residual stress induce and relaxation model
#-----------------------------------------------------------------
# ANYTHING TO AID DEVELOPEMENT GOES HERE

# Snippet: to get strain atv centroids and SOLUTION DEPENDENT VARIABLES AT THE CENTROIDAL POSITIONS

# Strain = lastFrame.fieldOutputs['LE'].getSubset(region=polyI)
# Strain = myOdb.steps['Step-1'].frames[1].fieldOutputs['LE'   ].getSubset(region=polyI, position=CENTROID)
# p01    = myOdb.steps['Step-1'].frames[1].fieldOutputs['SDV7' ].getSubset(region=polyI, position=CENTROID)
#-----------------------------------------------------------------
# Compatibility listing
# 1. CPS4, CPS4R
#-----------------------------------------------------------------
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
# GET USER REQUIREMENTS FOR UPPER CAPPING AND LOWER CAPPING THE CONTOUR DISPLAY LEGEND LEVELS
from abaqus import getInputs
fields = (('Model_origin_x:', '0'),
          ('Model_origin_y:', '0'),
	      ('Model_enddim_x:', '100'),
		  ('Model_enddim_y:', '6'),
		  ('Model_enddim_z:', '1'),
		 )
Model_origin_x, Model_origin_y, Model_enddim_x,\
 Model_enddim_y, Model_enddim_z, \
 =  getInputs(fields = fields, label = 'Specify Checkerboard model dimsnions:', dialogTitle = 'Keep origin at (0, 0) for now', )
Model_origin_x = float(Model_origin_x)
Model_origin_y = float(Model_origin_y)
Model_enddim_x = float(Model_enddim_x)
Model_enddim_y = float(Model_enddim_y)
Model_enddim_z = float(Model_enddim_z)
del fields
#-----------------------------------------------------------------
# Acquire level 0 solution metadata
odbinfo = (('Location', 'B'),
           ('Calibration iteration number(as: 00n, 0mn, mno', '009'),
           ('ODB_FileName (enter without the .odb):', 'Loc_B_009'),
           ('# of frames:', '16'),
	       ('# of grains along x:', '24'),
		   ('# of grains along y:', '4'),
		   ('Element factor used:', '1'),
		   ('SolutionInstance_metadata_Num (keep unchanged for now)', '1'),
		   ('SolutionInstance_folder_path', 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter7\\ABAQUS_CAL_DATA_FILES\\LocationB\\'),
		  )
Cal_Location, Calib_Iteration_Num, This_ODB_FILENAME, NumOfFrames, NumGrains_X,\
 NumGrains_Y, Elem_Factor_Used, SolInst_metadata_Num, SolInst_folder_path\
 =  getInputs(fields = odbinfo, label = 'Specify details of solution file', dialogTitle = 'Level 0 solution metadata', )

del odbinfo
MODEL_INFORMATION = {1:['ODBfilename', This_ODB_FILENAME, 'frames', NumOfFrames, 'Ngx', NumGrains_X, 'Ngy', NumGrains_Y, 'ElemFacUSED', Elem_Factor_Used],
					 2:[SolInst_folder_path],}
# only enter odd number IDs for ODB_ID, i.e. only line number containing meta-data and not folder address
ODB_ID          = 1

ODB_FileName    = MODEL_INFORMATION[ODB_ID][1]
TotalNumFrames  = int(MODEL_INFORMATION[ODB_ID][3])

NumPartitions_x = int(MODEL_INFORMATION[ODB_ID][5])
NumPartitions_y = int(MODEL_INFORMATION[ODB_ID][7])

factorUSED      = float(MODEL_INFORMATION[ODB_ID][9])
ElementSize     = (Model_enddim_y/NumPartitions_y)/factorUSED

# frame incerements needed
# texture id value
# Elements per grain value
# elemebnt type value
frincr      = 1
TEXIDVALUE  = '02'
EPGValue    = '003'
ElementType = 'CPS4'
#-----------------------------------------------------------------
# generate variable values needed to re-create element set names
Num_DatumPlanes_x = NumPartitions_x - 1
Num_DatumPlanes_y = NumPartitions_y - 1
#--------------------------------------------------------
# should the elemental results at centrouids be extracted? If extracted, they will be written to file
Extract_S11_ELCEN = 0
Extract_S22_ELCEN = 0
Extract_S12_ELCEN = 0
#--------------------------------------------------------
# defining filenames
import random
RandomNumber_START_MATLAB_OUTPUT = str(random.randint(10, 99))
RandomNumber_END_MATLAB_OUTPUT   = str(random.randint(10, 99))
#--------------------------------------------------------
# GET USER REQUIREMENTS FOR UPPER CAPPING AND LOWER CAPPING THE CONTOUR DISPLAY LEGEND LEVELS
from abaqus import getInputs
fields = (('S11_contour_label_max_MPa:', '+0500'),
          ('S11_contour_label_min_MPa:', '+0000'),
	      ('S22_contour_label_max_MPa:', '+0100'),
		  ('S22_contour_label_min_MPa:', '-0100'),
		  ('S12_contour_label_max_MPa:', '+0050'),
		  ('S12_contour_label_min_MPa:', '-0050'),
		  )
S11_contour_label_max_MPa, S11_contour_label_min_MPa,\
 S22_contour_label_max_MPa, S22_contour_label_min_MPa,\
 S12_contour_label_max_MPa, S12_contour_label_min_MPa, \
 =  getInputs(fields = fields, label = 'Specify UPPER AND LOWER CAPPING LEVELS FOR CONTOUR LEGEND:', dialogTitle = 'Legend limits: STRESS', )
S11_contour_label_max_MPa = float(S11_contour_label_max_MPa)
S11_contour_label_min_MPa = float(S11_contour_label_min_MPa)
S22_contour_label_max_MPa = float(S22_contour_label_max_MPa)
S22_contour_label_min_MPa = float(S22_contour_label_min_MPa)
S12_contour_label_max_MPa = float(S12_contour_label_max_MPa)
S12_contour_label_min_MPa = float(S12_contour_label_min_MPa)
del fields
#--------------------------------------------------------
# PRINT FLAGS TO SPECIFY WHTHER IMAGES ARE TO BE PRINTED TO PNG FILES
fields = (('Print_S11_Contours_File:', '0'), ('Print_S22_Contours_File:', '0'),
		  ('Print_S12_Contours_File:', '0'),
          )
Print_S11_Contours_File, Print_S22_Contours_File,\
 Print_S12_Contours_File,\
 = getInputs(fields = fields, label = 'Enter 1(print) and 0(dont print)', dialogTitle = 'Set print to .png file requirements', )
Print_S11_Contours_File = float(Print_S11_Contours_File)
del fields
#-----------------------------------------------------------------
#  VIEWPORT - 1
VP_num              = 1
VP_name             = 'Viewport: ' + str(VP_num)
#VP_ODB_PathName     = 'C:/Temp/CalibrationModels/Cal_100ng/'
VP_ODB_PathName     = MODEL_INFORMATION[ODB_ID+1][0]
#VP_ODB_FileName     = ODB_FileName + '.odb'
VP_ODB_FileName     = MODEL_INFORMATION[ODB_ID][1]
VP_ODB_FullPathName = VP_ODB_PathName + VP_ODB_FileName + '.odb'
VP_UpGraded_ODB_FullPathName = VP_ODB_PathName + VP_ODB_FileName + '_UpGraded' + '.odb'


MVPport = session.Viewport(name = VP_name, origin = (0.0, 0.0), width = 150, height = 100)
SESS_VP = session.viewports[VP_name]
SESS_VP.makeCurrent()
SESS_VP.maximize()
SESS_VP.partDisplay.geometryOptions.setValues(referenceRepresentation = ON)
SESS_VP.setValues(displayedObject = None)

import os.path
import odbAccess
import visualization
import abaqus
