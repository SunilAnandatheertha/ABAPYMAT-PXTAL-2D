"""
This code defines parameters deciding pipeline start and branching

Pipeline start:
(1) Generation of abaqus models (2) Generate the slurm file (3) Post-processing of ODB data
(4) Post-processing of generated sta file (5) Data assimilations (6) Prepare result
presentations in terms of visualization

Pipeline branching:
[1] in model generation @1 element type selection @2 WRITE HERE
[2] in post-processing
"""
#-----------------------------------------------------------------------------
import os
#-----------------------------------------------------------------------------
# IDs 1 to 4 are reserved for pre-processing
# IDs 5 to 9 are reserved for post-processing
EXECID = 5
# Descriptions
# (ID: 1) - Post-Process Checkerboard model results
# (ID: 5) - Generate Checkerboard model
#-----------------------------------------------------------------------------
postfilekey = 1
#-----------------------------------------------------------------------------
# define the post-processing filename dictionary
py_post_filename = {1: ['CHK_2D_postp_v4.2.py'],
                  }
#-----------------------------------------------------------------------------
# define the post-processing filename dictionary
odb_filename = {1: [''],
               }
#-----------------------------------------------------------------------------
# filepath of the python post-processing file
if EXECID > 5 and EXECID < 9:
    appendname = py_post_filename[postfilekey] + ''

path = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter6\\Abaqus Python Scripts\\' + appendname
path = os.path.expanduser(path)
execfile(path)
#-----------------------------------------------------------------------------
model_dimensions = {Model_origin_x: 0.,
                    Model_origin_y: 0.,
                    Model_enddim_x: 100.0,
                    Model_enddim_y: 6.0,
                    Model_enddim_z: 1.0}
