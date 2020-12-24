"""
This code defines parameters deciding pipeline start and branching

Pipeline start:
(1) Generation of abaqus models (2) Generate the slurm file (3) Post-processing of ODB data
(4) Post-processing of generated sta file (5) Data assimilations (6) Prepare result
presentations in terms of visualization

Pipeline internal branchings:
[1] in model generation @1 element type selection @2 WRITE HERE
[2] in post-processing
"""
#-----------------------------------------------------------------------------
import os
#-----------------------------------------------------------------------------
# this cell describes the different pipelines in ABAPYMAT for Python-ABAQUS & Python perspective
# IDs 01 to 10 are reserved for pre-processing
# IDs 11 to 20 are reserved for post-processing
#    -    -    -    -    -    -    -    -
# Descriptions of current pre-processing possibilities
# (pre-process ID: 01) - Generate checkerboard model
# (pre-process ID: 02) - Build 2D voronoi tessellation model using MATLAB output
#    -    -    -    -    -    -    -    -
# Descriptions of current pre-processing possibilities
# (post-process ID: 11) - Analyze results of checkerboard model made from process ID: 01
#-----------------------------------------------------------------------------
processIDinfo = (('PRE : Generate checkerboard model', '01'),
                 ('PRE : Build 2D voronoi tessellation model', '02'),
	             ('POST: Analyze chk model results from process ID: 01', '11'),
		         ('Which pipeline ?..', '11'),
	     	    )
ignore1, ignore2, ignore3, processID_UserInput\
 =  getInputs(fields = processIDinfo, label = 'All but last values show possibilities', dialogTitle = 'Level 0 solution metadata', )
del processIDinfo
del ignore1
del ignore2
del ignore3

processID = int(processID_UserInput)
if processID==1:
    py_PRE_processing_filepath     = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter6\\Abaqus Python Scripts\\' + ''
    py_PRE_processing_filename     = 'CHK_2D_prep_V1.0' + '.py'
    py_PRE_processing_fileFULLpath = py_PRE_processing_filepath + py_PRE_processing_filename
    execfile(py_PRE_processing_fileFULLpath)
elif processID==11:
    py_POST_processing_filepath     = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter6\\Abaqus Python Scripts\\' + ''
    py_POST_processing_filename     = 'CHK_2D_postp_v4.3' + '.py'
    py_POST_processing_fileFULLpath = py_POST_processing_filepath + py_POST_processing_filename
    execfile(py_POST_processing_fileFULLpath)
#-----------------------------------------------------------------------------
# define the post-processing filename dictionary
#odb_filename = {1: ['CB-24-2-1-cps4-i-ti1-tr3', 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter7\\ABAQUS_CAL_DATA_FILES\\CBd1'],
#               }
#-----------------------------------------------------------------------------
#path = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter6\\Abaqus Python Scripts\\' + 'PRE_ExecuteDefinitions.py'
#path = os.path.expanduser(path)
#execfile(path)
#-----------------------------------------------------------------------------
#if EXECID >= 5 and EXECID <= 9:
#    # POST PROCESSING
#    if postfilekey == 1:
#        py_POSTprocessing_filename = py_post_filename[postfilekey][0]+py_post_filename[postfilekey][1]+py_post_filename[postfilekey][2]
#    elif postfilekey == 2:
#        writehere = 'writehere'

#if py_post_filename.keys()[0]==1:
#    path = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter6\\Abaqus Python Scripts\\' + py_POSTprocessing_filename
#    path = py_POSTprocessing_fileFULLpath
#    path = os.path.expanduser(path)
#    execfile(path)
#-----------------------------------------------------------------------------
#model_dimensions = {Model_origin_x: 0.,
#                    Model_origin_y: 0.,
#                    Model_enddim_x: 100.0,
#                    Model_enddim_y: 6.0,
#                    Model_enddim_z: 1.0}
#-----------------------------------------------------------------------------
