######################################################################
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
######################################################################
import sys
######################################################################
import numpy as np
######################################################################
# Set viewport background to solid black
session.graphicsOptions.setValues(backgroundStyle = SOLID)
session.graphicsOptions.setValues(backgroundColor = '#000000')
######################################################################
# Define constants
# Model origin MUST be 0,0
Modelinfo01 = (('Model_origin_x [allways 0]', '0'),
               ('Model_origin_y [allways 0]', '0'),
               ('Model_enddim_x', '120.0'),
	           ('Model_enddim_y', '5.0'),
               ('XtalMat_start_x','35'),
               ('Xtal_ResStr_Start_x', '40')
	     	  )
Model_origin_x, Model_origin_y, Model_enddim_x, Model_enddim_y, XtalMat_start_x, Xtal_ResStr_Start_x\
 =  getInputs(fields = Modelinfo01, label = 'Model position and size', dialogTitle = 'Modelinfo01: Location and size', )
Model_origin_x  = float(Model_origin_x)
Model_origin_y  = float(Model_origin_y)
Model_enddim_x  = float(Model_enddim_x)
Model_enddim_y  = float(Model_enddim_y)
del(Modelinfo01)
# Calculate the centres of the overall finite elemebnt model
Model_size_x    = Model_enddim_x - Model_origin_x
Model_size_y    = Model_enddim_y - Model_origin_y
# calculate important locations of thew left spacer material
SPACER_left_Mat_start_x = Model_origin_x
SPACER_left_Mat_start_y = Model_origin_y
SPACER_left_Mat_end_x   = float(XtalMat_start_x)
SPACER_left_Mat_end_y   = Model_origin_y + Model_size_y
SPACER_left_Mat_size_x  = SPACER_left_Mat_end_x - SPACER_left_Mat_start_x
SPACER_left_Mat_size_y  = Model_origin_y
# calculate important locaytions in the xtal mater8ial
XtalMat_start_x         = float(XtalMat_start_x)
XtalMat_start_y         = Model_origin_y

Xtal_ResStr_Start_x     = float(Xtal_ResStr_Start_x)
Xtal_ResStr_Start_y     = Model_origin_y
Xtal_ResStr_End_x       = Model_enddim_x - Xtal_ResStr_Start_x
Xtal_ResStr_End_y       = Model_size_y

XtalMat_end_x   = Model_enddim_x - XtalMat_start_x
XtalMat_end_y   = Model_origin_y + Model_size_y
XtalMat_size_x  = XtalMat_end_x - XtalMat_start_x
XtalMat_size_y  = Model_origin_y
# calcualte important locations in the right spacer material
SPACER_right_Mat_start_x = XtalMat_end_x
SPACER_right_Mat_start_y = Model_origin_y
SPACER_right_Mat_end_x   = Model_origin_x + Model_enddim_x
SPACER_right_Mat_end_y   = Model_origin_y + Model_size_y
SPACER_right_Mat_size_x  = SPACER_right_Mat_end_x - SPACER_right_Mat_start_x
SPACER_right_Mat_size_y  = Model_enddim_y
######################################################################
# user inputs for partitionng the finite elemnebt model
Modelinfo02 = (('NumXTALPartitions_x', '20'),
               ('NumXTALPartitions_y #Ignore', '25'),
               ('NumXTALPartitions_total #ignore', '500'),
               ('NumSPACERPartitions_x', '15'),
               ('NumSPACERPartitions_y', '5'),
	     	  )
NumXTALPartitions_x, NumXTALPartitions_y, NumXTALPartitions_total,\
NumSPACERPartitions_x, NumSPACERPartitions_y,\
 =  getInputs(fields = Modelinfo02, label = 'CHK grain structure info', dialogTitle = 'Modelinfo02: Partitioning details', )
NumXTALPartitions_x     = int(NumXTALPartitions_x)
NumXTALPartitions_y     = int(NumXTALPartitions_y)
NumXTALPartitions_total = int(NumXTALPartitions_total)
NumSPACERPartitions_x   = int(NumSPACERPartitions_x)
NumSPACERPartitions_y   = int(NumSPACERPartitions_y)
del(Modelinfo02)
######################################################################
# calciulate total number of datum planes needed for xtaland spacer partitioning
Num_XTAL_DatumPlanes_x = NumXTALPartitions_x - 1
Num_XTAL_DatumPlanes_y = NumXTALPartitions_y - 1

Num_SPACER_DatumPlanes_x = NumSPACERPartitions_x - 1
Num_SPACER_DatumPlanes_y = NumSPACERPartitions_y - 1
######################################################################
# get user inputs for time stepping
Modelinfo03 = (('Time_Step_RSG_total_time', '1'),
               ('Time_Step_RSG_initial_incr', '0.005'),
               ('Time_Step_RSG_minimum_incr', '1.01e-05'),
               ('Time_Step_RSG_maximum_incr', '0.01'),
               ('Time_Step_EQUI_total_time', '1'),
               ('Time_Step_EQUI_initial_incr', '0.005'),
               ('Time_Step_EQUI_minimum_incr', '1.01e-05'),
               ('Time_Step_EQUI_maximum_incr', '0.01'),
	     	  )
Time_Step_RSG_total_time, Time_Step_RSG_initial_incr, Time_Step_RSG_minimum_incr, Time_Step_RSG_maximum_incr,\
Time_Step_EQUI_total_time, Time_Step_EQUI_initial_incr, Time_Step_EQUI_minimum_incr, Time_Step_EQUI_maximum_incr,\
 =  getInputs(fields = Modelinfo03, label = 'Time stepping info in sec', dialogTitle = 'Modelinfo03', )

Time_Step_RSG_total_time   = float(Time_Step_RSG_total_time)
Time_Step_RSG_initial_incr = float(Time_Step_RSG_initial_incr)
Time_Step_RSG_minimum_incr = float(Time_Step_RSG_minimum_incr)
Time_Step_RSG_maximum_incr = float(Time_Step_RSG_maximum_incr)

Time_Step_EQUI_total_time   = float(Time_Step_EQUI_total_time)
Time_Step_EQUI_initial_incr = float(Time_Step_EQUI_initial_incr)
Time_Step_EQUI_minimum_incr = float(Time_Step_EQUI_minimum_incr)
Time_Step_EQUI_maximum_incr = float(Time_Step_EQUI_maximum_incr)
del(Modelinfo03)
######################################################################
# get finite element information user inputs
Modelinfo04 = (('XTAL_ElementFactor #ignore', '1'),
               ('ElementTypeFlagID: -1:CPS4R/CPS3-,-2:CPS8/CPS6M-,-3:CPS4/CPS3-,-4:CPS8R/CPS6M-,-5:CPS8R/CPS6-', '4'),
               ('ElementShapeFlagID: [1:Quad.Str],[2:Quad.Free],[3:Tri.Str],[4:Tri.Free],[5:Quad.Dom]', '4'),
               ('SPACER_MESHING_MORPHED? (0:no / 1:yes)', '1'),
               ('SPACER_ElementFactor #ignore', '1'),
               ('ElementTypeFlagID: [1:CPS4R/CPS3],[2:CPS8/CPS6M],[3:CPS4/CPS3],[4:CPS8R/CPS6M],[5:CPS8R/CPS6]', '4'),
               ('ElementShapeFlagID: [1:Quad.Str],[2:Quad.Free],[3:Tri.Str],[4:Tri.Free],[5:Quad.Dom]', '4'),
	     	  )

XTAL_ElementFactor, XTAL_ElementTypeFlagID, XTAL_ElementShapeFlagID,\
SPACER_MESHING_MORPHED_FlagID, SPACER_ElementFactor, SPACER_ElementTypeFlagID, SPACER_ElementShapeFlagID\
=  getInputs(fields = Modelinfo04, label = 'Enter element details', dialogTitle = 'Modelinfo04: FE details', )

XTAL_ElementFactor             = float(XTAL_ElementFactor)
XTAL_ElementTypeFlagID         = int(XTAL_ElementTypeFlagID)
XTAL_ElementShapeFlagID        = int(XTAL_ElementShapeFlagID)

SPACER_MESHING_MORPHED_FlagID  = int(SPACER_MESHING_MORPHED_FlagID)
SPACER_ElementFactor           = float(SPACER_ElementFactor)
SPACER_ElementTypeFlagID       = int(SPACER_ElementTypeFlagID)
SPACER_ElementShapeFlagID      = int(SPACER_ElementShapeFlagID)
del(Modelinfo04)
######################################################################
# calculate finite element size
XTAL_ElementSize   = (Model_enddim_y/NumXTALPartitions_y)/XTAL_ElementFactor
######################################################################
# GET SAMPLE LOCATION
Modelinfo05a = (('Sample_Location (A/B/C)', 'B'), )
Sample_Location =  getInputs(fields = Modelinfo05a, label = 'Enter Boun. Cond. details', dialogTitle = 'Modelinfo05: Boundary conditions', )
del(Modelinfo05a)
######################################################################
# buyild sub-domain indices numpy array
SubDom_IND_B = np.arange(0, 16)
SubDom_IND_A = np.arange(0, 14)
SubDom_IND_C = np.arange(0, 16)
######################################################################
# Load up default values for the sub-domain depth location bounds
# LOCATION - B: sub-domain start
Modelinfo05bBS = (('B1.T: Sub-Domain start, mm', '0.00'),
                  ('B2.T: Sub-Domain start    ', '0.06'),
                  ('B3.T: Sub-Domain start    ', '0.13'),
                  ('B4.T: Sub-Domain start    ', '0.25'),
                  ('B5.T: Sub-Domain start    ', '0.40'),
                  ('B6.T: Sub-Domain start    ', '0.60'),
                  ('B7.T: Sub-Domain start    ', '0.95'),
                  ('B8.T: Sub-Domain start    ', '1.30'),
                  ('dummy', '::::'),
                  ('B8.B: Sub-Domain start, mm', '2.50'),
                  ('B7.B: Sub-Domain start    ', '3.70'),
                  ('B6.B: Sub-Domain start    ', '4.05'),
                  ('B5.B: Sub-Domain start    ', '4.40'),
                  ('B4.B: Sub-Domain start    ', '4.60'),
                  ('B3.B: Sub-Domain start    ', '4.75'),
                  ('B2.B: Sub-Domain start    ', '4.87'),
                  ('B1.B: Sub-Domain start    ', '4.94'),
                 )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    B1T_start, B2T_start, B3T_start, B4T_start, B5T_start, B6T_start, B7T_start, B8T_start, dummy,\
    B8B_start, B7B_start, B6B_start, B5B_start, B4B_start, B3B_start, B2B_start, B1B_start\
     =  getInputs(fields = Modelinfo05bBS,\
                  label = 'Enter depth wise sub-domain TE location (mm) @ Loc B',\
                  dialogTitle = 'ModInfo05b_B_S:dim.@B1..B8@TE', )
    SD_Loc_B_TOP_Start = np.array([B1T_start, B2T_start, B3T_start, B4T_start, B5T_start, B6T_start, B7T_start, B8T_start])
    SD_Loc_B_BOT_Start = np.array([B8B_start, B7B_start, B6B_start, B5B_start, B4B_start, B3B_start, B2B_start, B1B_start])
    SD_Loc_B_TOP_Start = SD_Loc_B_TOP_Start.astype(np.float)
    SD_Loc_B_BOT_Start = SD_Loc_B_BOT_Start.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_B_Start     = np.concatenate((SD_Loc_B_TOP_Start, SD_Loc_B_BOT_Start), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_Start    = SD_Loc_B_Start
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bBS)
# LOCATION - B: sub-domain end
Modelinfo05bBE = (('B1.T: Sub-Domain end, mm', '0.06'),
                  ('B2.T: Sub-Domain end'    , '0.13'),
                  ('B3.T: Sub-Domain end'    , '0.25'),
                  ('B4.T: Sub-Domain end'    , '0.40'),
                  ('B5.T: Sub-Domain end'    , '0.60'),
                  ('B6.T: Sub-Domain end'    , '0.95'),
                  ('B7.T: Sub-Domain end'    , '1.30'),
                  ('B8.T: Sub-Domain end'    , '2.50'),
                  ('dummy', '::::'),
                  ('B8.B: Sub-Domain end, mm', '3.70'),
                  ('B7.B: Sub-Domain end    ', '4.05'),
                  ('B6.B: Sub-Domain end    ', '4.40'),
                  ('B5.B: Sub-Domain end    ', '4.60'),
                  ('B4.B: Sub-Domain end    ', '4.75'),
                  ('B3.B: Sub-Domain end    ', '4.87'),
                  ('B2.B: Sub-Domain end    ', '4.94'),
                  ('B1.B: Sub-Domain end    ', '5.00'),
 	     	     )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    B1T_end, B2T_end, B3T_end, B4T_end, B5T_end, B6T_end, B7T_end, B8T_end, dummy,\
    B8B_end, B7B_end, B6B_end, B5B_end, B4B_end, B3B_end, B2B_end, B1B_end\
     =  getInputs(fields = Modelinfo05bBE,\
                  label = 'Enter depth wise sub-domain bottom edge locations (mm) @ Loc B',\
                  dialogTitle = 'ModInfo05b_B_E:dim.@B1..B8@BE', )
    SD_Loc_B_TOP_End = np.array([B1T_end, B2T_end, B3T_end, B4T_end, B5T_end, B6T_end, B7T_end, B8T_end])
    SD_Loc_B_BOT_End = np.array([B8B_end, B7B_end, B6B_end, B5B_end, B4B_end, B3B_end, B2B_end, B1B_end])
    SD_Loc_B_TOP_End = SD_Loc_B_TOP_End.astype(np.float)
    SD_Loc_B_BOT_End = SD_Loc_B_BOT_End.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_B_End     = np.concatenate((SD_Loc_B_TOP_End, SD_Loc_B_BOT_End), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_End    = SD_Loc_B_End
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bBE)
# ------------------------------------------------------------
# LOCATION - A: sub-domain start
Modelinfo05bAS = (('A1.T: Sub-Domain start, mm', '0.00'),
                  ('A2.T: Sub-Domain start    ', '0.06'),
                  ('A3.T: Sub-Domain start    ', '0.15'),
                  ('A4.T: Sub-Domain start    ', '0.25'),
                  ('A5.T: Sub-Domain start    ', '0.40'),
                  ('A6.T: Sub-Domain start    ', '0.75'),
                  ('A7.T: Sub-Domain start    ', '1.20'),
                  ('dummy', '::::'),
                  ('A7.B: Sub-Domain start    ', '2.50'),
                  ('A6.B: Sub-Domain start    ', '3.80'),
                  ('A5.B: Sub-Domain start    ', '4.25'),
                  ('A4.B: Sub-Domain start    ', '4.60'),
                  ('A3.B: Sub-Domain start    ', '4.75'),
                  ('A2.B: Sub-Domain start    ', '4.85'),
                  ('A1.B: Sub-Domain start    ', '4.94'),
                 )
if Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    A1T_start, A2T_start, A3T_start, A4T_start, A5T_start, A6T_start, A7T_start, dummy,\
    A7B_start, A6B_start, A5B_start, A4B_start, A3B_start, A2B_start, A1B_start\
     =  getInputs(fields = Modelinfo05bAS,\
                  label = 'Enter depth wise sub-domain TE location (mm) @ Loc A',\
                  dialogTitle = 'ModInfo05b_A_S:dim.@A1..A7@TE', )
    SD_Loc_A_TOP_Start = np.array([A1T_start, A2T_start, A3T_start, A4T_start, A5T_start, A6T_start, A7T_start])
    SD_Loc_A_BOT_Start = np.array([A7B_start, A6B_start, A5B_start, A4B_start, A3B_start, A2B_start, A1B_start])
    SD_Loc_A_TOP_Start = SD_Loc_A_TOP_Start.astype(np.float)
    SD_Loc_A_BOT_Start = SD_Loc_A_BOT_Start.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_A_Start     = np.concatenate((SD_Loc_A_TOP_Start, SD_Loc_A_BOT_Start), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_Start    = SD_Loc_A_Start
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bAS)
# LOCATION - A: sub-domain end
Modelinfo05bAE = (('A1.T: Sub-Domain end, mm', '0.06'),
                  ('A2.T: Sub-Domain end'    , '0.15'),
                  ('A3.T: Sub-Domain end'    , '0.25'),
                  ('A4.T: Sub-Domain end'    , '0.40'),
                  ('A5.T: Sub-Domain end'    , '0.75'),
                  ('A6.T: Sub-Domain end'    , '1.20'),
                  ('A7.T: Sub-Domain end'    , '2.50'),
                  ('Adummy', '::::'),
                  ('A7.B: Sub-Domain end    ', '3.80'),
                  ('A6.B: Sub-Domain end    ', '4.25'),
                  ('A5.B: Sub-Domain end    ', '4.60'),
                  ('A4.B: Sub-Domain end    ', '4.75'),
                  ('A3.B: Sub-Domain end    ', '4.85'),
                  ('A2.B: Sub-Domain end    ', '4.94'),
                  ('A1.B: Sub-Domain end    ', '5.00'),
 	     	     )
if Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    A1T_end, A2T_end, A3T_end, A4T_end, A5T_end, A6T_end, A7T_end, dummy,\
    A7C_end, A6C_end, A5C_end, A4C_end, A3C_end, A2C_end, A1C_end\
     =  getInputs(fields = Modelinfo05bAE,\
                  label = 'Enter depth wise sub-domain bottom edge locations (mm) @ Loc A',\
                  dialogTitle = 'ModInfo05b_A_E:dim.@A1..A7@BE', )
    SD_Loc_A_TOP_End = np.array([A1T_end, A2T_end, A3T_end, A4T_end, A5T_end, A6T_end, A7T_end])
    SD_Loc_A_BOT_End = np.array([A7C_end, A6C_end, A5C_end, A4C_end, A3C_end, A2C_end, A1C_end])
    SD_Loc_A_TOP_End = SD_Loc_A_TOP_End.astype(np.float)
    SD_Loc_A_BOT_End = SD_Loc_A_BOT_End.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_A_End     = np.concatenate((SD_Loc_A_TOP_End, SD_Loc_A_BOT_End), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_End    = SD_Loc_A_End
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bAE)
# ------------------------------------------------------------
# LOCATION - C: sub-domain start
Modelinfo05bCS = (('C1.T: Sub-Domain start, mm', '0.00'),
                  ('C2.T: Sub-Domain start    ', '0.06'),
                  ('C3.T: Sub-Domain start    ', '0.15'),
                  ('C4.T: Sub-Domain start    ', '0.25'),
                  ('C5.T: Sub-Domain start    ', '0.50'),
                  ('C6.T: Sub-Domain start    ', '0.70'),
                  ('C7.T: Sub-Domain start    ', '1.30'),
                  ('C8.T: Sub-Domain start    ', '1.80'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain start, mm', '2.50'),
                  ('C7.B: Sub-Domain start    ', '3.20'),
                  ('C6.B: Sub-Domain start    ', '3.70'),
                  ('C5.B: Sub-Domain start    ', '4.30'),
                  ('C4.B: Sub-Domain start    ', '4.50'),
                  ('C3.B: Sub-Domain start    ', '4.75'),
                  ('C2.B: Sub-Domain start    ', '4.85'),
                  ('C1.B: Sub-Domain start    ', '4.94'),
                 )
if Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    C1T_start, C2T_start, C3T_start, C4T_start, C5T_start, C6T_start, C7T_start, C8T_start, dummy,\
    C8B_start, C7B_start, C6B_start, C5B_start, C4B_start, C3B_start, C2B_start, C1B_start\
     =  getInputs(fields = Modelinfo05bCS,\
                  label = 'Enter depth wise sub-domain TE location (mm) @ Loc C',\
                  dialogTitle = 'ModInfo05b_C_S:dim.@C1..C8@TE', )
    SD_Loc_C_TOP_Start = np.array([C1T_start, C2T_start, C3T_start, C4T_start, C5T_start, C6T_start, C7T_start, C8T_start])
    SD_Loc_C_BOT_Start = np.array([C8B_start, C7B_start, C6B_start, C5B_start, C4B_start, C3B_start, C2B_start, C1B_start])
    SD_Loc_C_TOP_Start = SD_Loc_C_TOP_Start.astype(np.float)
    SD_Loc_C_BOT_Start = SD_Loc_C_BOT_Start.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_C_Start     = np.concatenate((SD_Loc_C_TOP_Start, SD_Loc_C_BOT_Start), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_Start    = SD_Loc_C_Start
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bCS)
# LOCATION - C: sub-domain end
Modelinfo05bCE = (('C1.T: Sub-Domain end, mm', '0.06'),
                  ('C2.T: Sub-Domain end'    , '0.15'),
                  ('C3.T: Sub-Domain end'    , '0.25'),
                  ('C4.T: Sub-Domain end'    , '0.50'),
                  ('C5.T: Sub-Domain end'    , '0.70'),
                  ('C6.T: Sub-Domain end'    , '1.30'),
                  ('C7.T: Sub-Domain end'    , '1.80'),
                  ('C8.T: Sub-Domain end'    , '2.50'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain end, mm', '3.20'),
                  ('C7.B: Sub-Domain end    ', '3.70'),
                  ('C6.B: Sub-Domain end    ', '4.30'),
                  ('C5.B: Sub-Domain end    ', '4.50'),
                  ('C4.B: Sub-Domain end    ', '4.75'),
                  ('C3.B: Sub-Domain end    ', '4.85'),
                  ('C2.B: Sub-Domain end    ', '4.94'),
                  ('C1.B: Sub-Domain end    ', '5.00'),
 	     	     )
if Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    C1T_end, C2T_end, C3T_end, C4T_end, C5T_end, C6T_end, C7T_end, C8T_end, dummy,\
    C8C_end, C7C_end, C6C_end, C5C_end, C4C_end, C3C_end, C2C_end, C1C_end\
     =  getInputs(fields = Modelinfo05bCE,\
                  label = 'Enter depth wise sub-domain bottom edge locations (mm) @ Loc C',\
                  dialogTitle = 'ModInfo05b_C_E:dim.@C1..C8@BE', )
    SD_Loc_C_TOP_End = np.array([C1T_end, C2T_end, C3T_end, C4T_end, C5T_end, C6T_end, C7T_end, C8T_end])
    SD_Loc_C_BOT_End = np.array([C8C_end, C7C_end, C6C_end, C5C_end, C4C_end, C3C_end, C2C_end, C1C_end])
    SD_Loc_C_TOP_End = SD_Loc_C_TOP_End.astype(np.float)
    SD_Loc_C_BOT_End = SD_Loc_C_BOT_End.astype(np.float)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_Loc_C_End     = np.concatenate((SD_Loc_C_TOP_End, SD_Loc_C_BOT_End), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SubDomain_End    = SD_Loc_C_End
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05bCE)
######################################################################
# use a single sub-domain indices array
# delete old arrays particvulatr to indivdual locations
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    SubDom_IND = SubDom_IND_B;
    del(SubDom_IND_B)
elif Sample_Location[0] in ['B', 'A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    SubDom_IND = SubDom_IND_A;
    del(SubDom_IND_A)
elif Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    SubDom_IND = SubDom_IND_C;
    del(SubDom_IND_C)
######################################################################
# Load up default values for location B
Modelinfo05cB = (('epsilon_topedge_depth_loc_1 @B1T.TE', '-0.040'),
                 ('epsilon_topedge_depth_loc_2 @B2T.TE', '-0.035'),
                 ('epsilon_topedge_depth_loc_3 @B3T.TE', '-0.030'),
                 ('epsilon_topedge_depth_loc_4 @B4T.TE', '-0.020'),
                 ('epsilon_topedge_depth_loc_5 @B5T.TE', '-0.010'),
                 ('epsilon_topedge_depth_loc_6 @B6T.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @B7T.TE', ''),
                 ('epsilon_topedge_depth_loc_8 @B8T.TE', ''),
                 ('dummy', ':::'),
                 ('epsilon_topedge_depth_loc_8 @B8B.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @B7B.TE', ''),
                 ('epsilon_topedge_depth_loc_6 @B6B.TE', ''),
                 ('epsilon_topedge_depth_loc_5 @B5B.TE', '0.010'),
                 ('epsilon_topedge_depth_loc_4 @B4B.TE', '0.020'),
                 ('epsilon_topedge_depth_loc_3 @B3B.TE', '0.030'),
                 ('epsilon_topedge_depth_loc_2 @B2B.TE', '0.035'),
                 ('epsilon_topedge_depth_loc_1 @B1B.TE', '0.040'),
 	     	    )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    eps01, eps02, eps03, eps04, eps05, eps06, eps07, eps08, dummy,\
    eps09, eps10, eps11, eps12, eps13, eps14, eps15, eps16\
     =  getInputs(fields = Modelinfo05cB,\
                  label = 'Enter depth wise strain for B subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_B:eps.@B1..B8@TB', )
    SD_eps_BT_TE = np.array([eps01, eps02, eps03, eps04, eps05, eps06, eps07, eps08])
    SD_eps_BB_TE = np.array([eps09, eps10, eps11, eps12, eps13, eps14, eps15, eps16])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_eps_B_TE = np.concatenate((SD_eps_BT_TE, SD_eps_BB_TE), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05cB)
# Load up default valuyes for location A
Modelinfo05cA = (('epsilon_topedge_depth_loc_1 @A1T.TE', '-0.040'),
                 ('epsilon_topedge_depth_loc_2 @A2T.TE', '-0.035'),
                 ('epsilon_topedge_depth_loc_3 @A3T.TE', '-0.030'),
                 ('epsilon_topedge_depth_loc_4 @A4T.TE', '-0.020'),
                 ('epsilon_topedge_depth_loc_5 @A5T.TE', '-0.010'),
                 ('epsilon_topedge_depth_loc_6 @A6T.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @A7T.TE', ''),
                 ('dummy', ':::'),
                 ('epsilon_topedge_depth_loc_7 @A7B.TE', ''),
                 ('epsilon_topedge_depth_loc_6 @A6B.TE', ''),
                 ('epsilon_topedge_depth_loc_5 @A5B.TE', '0.010'),
                 ('epsilon_topedge_depth_loc_4 @A4B.TE', '0.020'),
                 ('epsilon_topedge_depth_loc_3 @A3B.TE', '0.030'),
                 ('epsilon_topedge_depth_loc_2 @A2B.TE', '0.035'),
                 ('epsilon_topedge_depth_loc_1 @A1B.TE', '0.040'),
 	     	    )
if Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    eps01, eps02, eps03, eps04, eps05, eps06, eps07, dummy,\
    eps08, eps09, eps10, eps11, eps12, eps13, eps14\
     =  getInputs(fields = Modelinfo05cA,\
                  label = 'Enter depth wise strain for A subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_A:eps.@A1..A7@TB', )
    SD_eps_AT_TE = np.array([eps01, eps02, eps03, eps04, eps05, eps06, eps07])
    SD_eps_AB_TE = np.array([eps08, eps09, eps10, eps11, eps12, eps13, eps14])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_eps_A_TE = np.concatenate((SD_eps_AT_TE, SD_eps_AB_TE), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05cA)
# Load up default valuyes for location C
Modelinfo05cC = (('epsilon_topedge_depth_loc_1 @C1T.TE', '-0.040'),
                 ('epsilon_topedge_depth_loc_2 @C2T.TE', '-0.035'),
                 ('epsilon_topedge_depth_loc_3 @C3T.TE', '-0.030'),
                 ('epsilon_topedge_depth_loc_4 @C4T.TE', '-0.020'),
                 ('epsilon_topedge_depth_loc_5 @C5T.TE', '-0.010'),
                 ('epsilon_topedge_depth_loc_6 @C6T.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @C7T.TE', ''),
                 ('epsilon_topedge_depth_loc_8 @C8T.TE', ''),
	     	     ('dummy', ':::'),
                 ('epsilon_topedge_depth_loc_8 @C8B.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @C7B.TE', ''),
                 ('epsilon_topedge_depth_loc_6 @C6B.TE', ''),
                 ('epsilon_topedge_depth_loc_5 @C5B.TE', '0.010'),
                 ('epsilon_topedge_depth_loc_4 @C4B.TE', '0.020'),
                 ('epsilon_topedge_depth_loc_3 @C3B.TE', '0.030'),
                 ('epsilon_topedge_depth_loc_2 @C2B.TE', '0.035'),
                 ('epsilon_topedge_depth_loc_1 @C1B.TE', '0.040'),
	     	    )
if Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    eps01, eps02, eps03, eps04, eps05, eps06, eps07, eps08, dummy,\
    eps09, eps10, eps11, eps12, eps13, eps14, eps15, eps16\
     =  getInputs(fields = Modelinfo05cC,\
                  label = 'Enter depth wise strain for C subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_C:eps.@C1..C8@TB', )
    SD_eps_CT_TE = np.array([eps01, eps02, eps03, eps04, eps05, eps06, eps07, eps08])
    SD_eps_CB_TE = np.array([eps09, eps10, eps11, eps12, eps13, eps14, eps15, eps16])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_eps_C_TE = np.concatenate((SD_eps_CT_TE, SD_eps_CB_TE), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    del(Modelinfo05cC)
######################################################################
# BUild a single sub-domain applied strain array
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    SD_eps_TE = SD_eps_B_TE;
    SD_eps_TE_VAL = np.ones(16, dtype = 'int')
    del(SD_eps_B_TE)
elif Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    SD_eps_TE = SD_eps_A_TE;
    SD_eps_TE_VAL = np.ones(14, dtype = 'int')
    del(SD_eps_A_TE)
elif Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    SD_eps_TE = SD_eps_C_TE;
    SD_eps_TE_VAL = np.ones(16, dtype = 'int')
    del(SD_eps_C_TE)
######################################################################
SD_eps_TE_flo = np.zeros(SD_eps_TE.shape[0])
for count in SubDom_IND:
    if not SD_eps_TE[count]:
        SD_eps_TE_VAL[count] = 0
        SD_eps_TE_flo[count] = 0
    else:
        SD_eps_TE_flo[count] = float(SD_eps_TE[count])
SD_eps_TE = SD_eps_TE_flo
del SD_eps_TE_flo
######################################################################
# VARIABLE SUMMARY - 1
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# Depending on the location specified, the following
# variable will have appropriate data for that location
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# VARIABLE 01: SubDomain_Start
    # Contains the top edge location of every sub-domain of tht central XTAL region
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# VARIABLE 02: SubDomain_End
    # Contains the bot edge location of every sub-domain of tht central XTAL region
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# VARIABLE 03: SubDom_IND
    # Contains the sub-domain number starting from 0 for topmost and all the way
    # to the opposite end on the bending sample
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# VARIABLE 04: SD_eps_TE_VAL
    # These are like flag values. 0 indicates that the top edge at the location
    # is to be left free without any boundary condition!
    # ONly those with 1 should be applied with a boundary condition
#  -  -  -  -  -  -  -  -  -  -  -  -  -  -
# VARIABLE 05: SD_eps_TE
    # Sub-domain strain values to be used. These are @ top edge of the
    # corresponding sub-domains
    # +ve values indicate tensile strain and compressive otherwise
######################################################################
# build XTAL sub-domains names
NumXTALSubDomains = len(SubDomain_End)
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    NamesXTALSubDomains = ['B1T','B2T', 'B3T', 'B4T', 'B5T', 'B6T', 'B7T', 'B8T', 'B8B', 'B7B', 'B6B', 'B5B', 'B4B', 'B3B', 'B2B', 'B1B']
elif Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    NamesXTALSubDomains = ['A1T','A2T', 'A3T', 'A4T', 'A5T', 'A6T', 'A7T', 'A7B', 'A6B', 'A5B', 'A4B', 'A3B', 'A2B', 'A1B']
elif Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    NamesXTALSubDomains = ['C1T','C2T', 'C3T', 'C4T', 'C5T', 'C6T', 'C7T', 'C8T', 'C8B', 'C7B', 'C6B', 'C5B', 'C4B', 'C3B', 'C2B', 'C1B']
######################################################################
# user input for the cae file name
Modelinfo06    = (('CAE_File_name', 'RS_Loc_B_0'),
	     	     )
CAE_File_name, =  getInputs(fields = Modelinfo06, label = 'Enter CAE file name', dialogTitle = 'Modelinfo06: filenames', )
CAE_File_name  = str(CAE_File_name)
del(Modelinfo06)
######################################################################
# Calculate the centre of the entire model
modelcentre_x   = (Model_origin_x + Model_size_x)/2
modelcentre_y   = (Model_origin_y + Model_size_y)/2
#------------------
# Centre of the left spacer material
SPACER_left_centre_x    = (SPACER_left_Mat_start_x + SPACER_left_Mat_end_x)/2
SPACER_left_centre_y    = (SPACER_left_Mat_start_y + SPACER_left_Mat_end_y)/2
# Datum plane increments for the left side spcer
SPACER_left_dat_plane_x_incr = SPACER_left_Mat_size_x / (Num_SPACER_DatumPlanes_x + 1)
SPACER_left_dat_plane_y_incr = SPACER_left_Mat_size_y / (Num_SPACER_DatumPlanes_y + 1)
# First partition center for the left side spacer
SPACER_left_1st_partition_centre_x = SPACER_left_Mat_start_x + SPACER_left_dat_plane_x_incr/2
SPACER_left_1st_partition_centre_y = SPACER_left_Mat_start_y + SPACER_left_dat_plane_y_incr/2
#------------------
BW_LeftSpacer_XTAL_centre_x = (SPACER_left_Mat_end_x + Xtal_ResStr_Start_x)/2
BW_LeftSpacer_XTAL_centre_y = (SPACER_left_Mat_end_y + Xtal_ResStr_Start_y)/2
#------------------
# Centre of the XTAL
XTAL_Mat_centre_x    = (XtalMat_start_x + XtalMat_end_x)/2
XTAL_Mat_centre_y    = (XtalMat_start_y + XtalMat_end_y)/2
# Datum plane increments for the left side
XTAL_dat_plane_x_incr = XtalMat_size_x / (Num_XTAL_DatumPlanes_x + 1)
XTAL_dat_plane_y_incr = XtalMat_size_y / (Num_XTAL_DatumPlanes_y + 1)
# First grain centre in the central XTAL region
FirstGrain_centre_x = XtalMat_start_x + XTAL_dat_plane_x_incr/2
FirstGrain_centre_y = XtalMat_start_y + XTAL_dat_plane_y_incr/2
#------------------
BW_XTAL_rightspacer_centre_x = (Xtal_ResStr_End_x + SPACER_right_Mat_start_x)/2
BW_XTAL_rightspacer_centre_y = (Xtal_ResStr_End_y + SPACER_right_Mat_start_y)/2
#------------------
# Centre of the right spacer material
SPACER_right_centre_x    = (SPACER_right_Mat_start_x + SPACER_right_Mat_end_x)/2
SPACER_right_centre_y    = (SPACER_right_Mat_start_y + SPACER_right_Mat_end_y)/2
# Datum plane increments for the right side spcer
SPACER_right_dat_plane_x_incr = SPACER_right_Mat_size_x / (Num_SPACER_DatumPlanes_x + 1)
SPACER_right_dat_plane_y_incr = SPACER_right_Mat_size_y / (Num_SPACER_DatumPlanes_y + 1)
# First partition center for the right side spacer
SPACER_right_1st_partition_centre_x = SPACER_right_Mat_start_x + SPACER_right_dat_plane_x_incr/2
SPACER_right_1st_partition_centre_y = SPACER_right_Mat_start_y + SPACER_right_dat_plane_y_incr/2
######################################################################
# left edge
MLE_centre_x = Model_origin_x
MLE_centre_y = (Model_origin_y + Model_enddim_y)/2
# right edge
MRE_centre_x = Model_enddim_x
MRE_centre_y = MLE_centre_y
# bottom edge
MBE_centre_x = (Model_origin_x + Model_enddim_x)/2
MBE_centre_y = Model_origin_y
# top edge
MTE_centre_x = (Model_origin_x + Model_enddim_x)/2
MTE_centre_y = Model_enddim_y
######################################################################
# simplify inputs stage 2
model = mdb.models['Model-1']
######################################################################
# make part
model.ConstrainedSketch(name='__profile__', sheetSize = 1.0)
model.sketches['__profile__'].rectangle(point1 = (Model_origin_x, Model_origin_y), point2 = (Model_enddim_x, Model_enddim_y))
model.Part(dimensionality=TWO_D_PLANAR, name='partname', type=DEFORMABLE_BODY)
model.parts['partname'].BaseShell(sketch=mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
######################################################################
# simplify inputs stage 2
part  = model.parts['partname']
######################################################################
# Switch context
session.viewports['Viewport: 1'].setValues(displayedObject = part)
######################################################################
# Create base sets
part.Set(faces    = part.faces.findAt(((modelcentre_x, modelcentre_y, 0.),))    , name = 'FullFace')
part.Set(edges    = part.edges.findAt(((MLE_centre_x, MLE_centre_y,0.),))       , name = 'FullEdge_x-')
part.Set(edges    = part.edges.findAt(((MRE_centre_x, MRE_centre_y,0.),))       , name = 'FullEdge_x+')
part.Set(edges    = part.edges.findAt(((MBE_centre_x, MBE_centre_y,0.),))       , name = 'FullEdge_y-')
part.Set(edges    = part.edges.findAt(((MTE_centre_x, MTE_centre_y,0.),))       , name = 'FullEdge_y+')
part.Set(vertices = part.vertices.findAt(((Model_origin_x, Model_origin_y,0.),)), name = 'FullVertex_BL')
######################################################################
# Define left spacer to central XTAL domain transision datum plane
DatumPlaneIDs_y = []
DPinfo = part.DatumPlaneByPrincipalPlane(offset = XtalMat_start_x, principalPlane = YZPLANE)
DatumPlaneIDs_y.append(DPinfo.id)
part.features.changeKey(fromName = 'Datum plane-1', toName = 'DatPl-LS:Xtal transition')
######################################################################
# Partition main domain into left spacer and XTAL domains
Dat_Pln_COUNT = len(DatumPlaneIDs_y)-1
TheID = DatumPlaneIDs_y[Dat_Pln_COUNT]
xloc  = modelcentre_x
yloc  = modelcentre_y
part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
#part.DatumPointByCoordinate(coords = (SPACER_left_centre_x, SPACER_left_centre_y, 0.0))
######################################################################
# Define right spacer to central XTAL domain transision datum plane
DPinfo = part.DatumPlaneByPrincipalPlane(offset = XtalMat_end_x, principalPlane = YZPLANE)
DatumPlaneIDs_y.append(DPinfo.id)
part.features.changeKey(fromName = 'Datum plane-1', toName = 'DatPl-Xtal:RS transition')
######################################################################
# Partition main domain into XTAL and right spacer domains
Dat_Pln_COUNT = len(DatumPlaneIDs_y)-1
TheID = DatumPlaneIDs_y[Dat_Pln_COUNT]
xloc  = modelcentre_x
yloc  = modelcentre_y
part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
#part.DatumPointByCoordinate(coords = (SPACER_right_centre_x, SPACER_right_centre_y, 0.0))
######################################################################
## Define central XTAL domain start datum plane
#DPinfo = part.DatumPlaneByPrincipalPlane(offset = Xtal_ResStr_Start_x, principalPlane = YZPLANE)
#DatumPlaneIDs_y.append(DPinfo.id)
#part.features.changeKey(fromName = 'Datum plane-1', toName = 'DatPl-LS:Xtal boundary')
######################################################################
## Partition main domain into XTAL and right spacer domains
#Dat_Pln_COUNT = len(DatumPlaneIDs_y)-1
#TheID = DatumPlaneIDs_y[Dat_Pln_COUNT]
#xloc  = modelcentre_x
#yloc  = modelcentre_y
#part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
#part.DatumPointByCoordinate(coords = (BW_LeftSpacer_XTAL_centre_x, BW_LeftSpacer_XTAL_centre_y, 0.0))
######################################################################
## Define central XTAL domain end datum plane
#DPinfo = part.DatumPlaneByPrincipalPlane(offset = Xtal_ResStr_End_x, principalPlane = YZPLANE)
#DatumPlaneIDs_y.append(DPinfo.id)
#part.features.changeKey(fromName = 'Datum plane-1', toName = 'DatPl-Xtal:RS boundary')
######################################################################
## Partition main domain into XTAL and right spacer domains
#Dat_Pln_COUNT = len(DatumPlaneIDs_y)-1
#TheID = DatumPlaneIDs_y[Dat_Pln_COUNT]
#xloc  = modelcentre_x
#yloc  = modelcentre_y
#part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
#part.DatumPointByCoordinate(coords = (BW_XTAL_rightspacer_centre_x, BW_XTAL_rightspacer_centre_y, 0.0))
######################################################################
#part.DatumPointByCoordinate(coords = (XTAL_Mat_centre_x, XTAL_Mat_centre_y, 0.0))
######################################################################
# Determine locations of all vertical edges of the models
# LEft most edge is Edge00 and then proceeds to the right as Edge01 and so on
Edge00 = [MLE_centre_x, modelcentre_y, 0.]
Edge01 = [XtalMat_start_x, modelcentre_y, 0.]
Edge02 = [Xtal_ResStr_Start_x, modelcentre_y, 0.]
Edge03 = [XtalMat_end_x, modelcentre_y, 0.]
Edge04 = [Xtal_ResStr_End_x, modelcentre_y, 0.]
Edge05 = [MRE_centre_x, modelcentre_y, 0.]
# Build the VEdges array
VEdges = [Edge00, Edge01, Edge02, Edge03, Edge04, Edge05]
######################################################################
# VARIABLE SUMMARY - 2
# VARIABLE 01: modelcentre_x: x location of the entire model centre. similarly y
# VARIABLE 02: SPACER_left_centre_x: x location of the centre of the left spacer. similarly y
# VARIABLE 03: BW_LeftSpacer_XTAL_centre_x: x location of the centre of the region between the left spacer's right boundary and the
    # XTAL's residual stress left region boundary. similarly y
# VARIABLE 04: XTAL_Mat_centre_x: x location of the centre of the XTAL domain. similarly y
# VARIABLE 05: BW_XTAL_rightspacer_centre_x: x location of the centre of the region between the XTAL's residual stress region right
    # boundary and the right spacer's left boundary. similarly y
# VARIABLE 06: SPACER_right_centre_x: x location of the centre of the right spacer. similarly y

# VARIABLE 07: SPACER_left_dat_plane_x_incr: Increments of the datum planes inside the left spacer domain
# VARIABLE 08a: XTAL_dat_plane_x_incr: Increments of the vertical datum planes in the XTAL domain
# VARIABLE 08b: XTAL_dat_plane_y_incr: Increments of the horizontal datum planes in the XTAL domain
# VARIABLE 09: SPACER_right_dat_plane_x_incr: Increments of the datum planes inside the right spacer domain

# VARIABLE 10: SPACER_left_1st_partition_centre_x: x location of the first partition in the left spacer. similarly y
# VARIABLE 11: FirstGrain_centre_x: x location of the first grain in the XTAL domain. similarly y
# VARIABLE 12: SPACER_right_1st_partition_centre_x: x location of the first partition in the right spacer. similarly y

# VARIABLE 13: VEdges: Contains the x,y,z of centres of all vertical edges of the level-0 partitioned edges
######################################################################
# Create all the datum planes parallel to peened surface at the top edges of the sub-domains in the central XTAL domain.
# Of course, skip the top side peened surface.
# Bot side peened surface will be skipped any way bcz "SubDomain_Start" is being used
# Peened surface is parallel to XZ plane
for XZDatPlnCount in range(1, NumXTALSubDomains):# Start with 1 to skip DPlane @ top peened surface
    DPinfo = part.DatumPlaneByPrincipalPlane(offset = 5-SubDomain_Start[XZDatPlnCount], principalPlane = XZPLANE)
    DatumPlaneIDs_y.append(DPinfo.id)
    part.features.changeKey(fromName='Datum plane-1', toName='DP_XTAL_y_'+str(XZDatPlnCount))
######################################################################
# Reset the sub-domain start and end positions to match the coordinatre system being used
SubDomain_Start = 5.0 - SubDomain_Start
SubDomain_End   = 5.0 - SubDomain_End
######################################################################
## Partition the XTAL-left domain into its constitutent sub-domains and name them accordingly
## same naming convention is used as in CHK model used for calibration, but has
## the string "location + ID + T/B" attached before grain name
## For example, grain 2,13 in B2.Top has the name "XTAL_B2T_Mat_Grain_Nx_2_Ny_13"
#DatPlnIDloc  = 1
#for SDcountY in range(NumXTALSubDomains-1):
#    DatPlnIDloc = DatPlnIDloc + 1
#    SD_center_x = BW_LeftSpacer_XTAL_centre_x
#    SD_center_y = (SubDomain_Start[SDcountY] + SubDomain_End[SDcountY])/2
#    #part.DatumPointByCoordinate(coords = (SD_center_x, SD_center_y, 0.0))
#    DPID = DatumPlaneIDs_y[DatPlnIDloc]
#    part.PartitionFaceByDatumPlane(datumPlane = part.datums[DPID], faces = part.faces.findAt(((SD_center_x, SD_center_y, 0.), ), ))
######################################################################
# Partition the XTAL domain into its constitutent sub-domains and name them accordingly
# same naming convention is used as in CHK model used for calibration, but has
# the string "location + ID + T/B" attached before grain name
# For example, grain 2,13 in B2.Top has the name "XTAL_B2T_Mat_Grain_Nx_2_Ny_13"
DatPlnIDloc  = 1
for SDcountY in range(NumXTALSubDomains-1):
    DatPlnIDloc = DatPlnIDloc + 1
    SD_center_x = XTAL_Mat_centre_x
    SD_center_y = (SubDomain_Start[SDcountY] + SubDomain_End[SDcountY])/2
    #part.DatumPointByCoordinate(coords = (SD_center_x, SD_center_y, 0.0))
    DPID = DatumPlaneIDs_y[DatPlnIDloc]
    part.PartitionFaceByDatumPlane(datumPlane = part.datums[DPID], faces = part.faces.findAt(((SD_center_x, SD_center_y, 0.), ), ))
######################################################################
## Partition the XTAL-right domain into its constitutent sub-domains and name them accordingly
## same naming convention is used as in CHK model used for calibration, but has
## the string "location + ID + T/B" attached before grain name
## For example, grain 2,13 in B2.Top has the name "XTAL_B2T_Mat_Grain_Nx_2_Ny_13"
#DatPlnIDloc  = 3
#for SDcountY in range(NumXTALSubDomains-1):
#    DatPlnIDloc = DatPlnIDloc + 1
#    SD_center_x = BW_XTAL_rightspacer_centre_x
#    SD_center_y = (SubDomain_Start[SDcountY] + SubDomain_End[SDcountY])/2
#    #part.DatumPointByCoordinate(coords = (SD_center_x, SD_center_y, 0.0))
#    DPID = DatumPlaneIDs_y[DatPlnIDloc]
#    part.PartitionFaceByDatumPlane(datumPlane = part.datums[DPID], faces = part.faces.findAt(((SD_center_x, SD_center_y, 0.), ), ))
######################################################################
# calculate the x-axis locations of the subdomains in XTAL domain
XTAL_Grains_XLOCS = np.arange(XtalMat_start_x, XtalMat_end_x, XTAL_dat_plane_x_incr) + XTAL_dat_plane_x_incr/2
######################################################################
# Create all the datum planes normal to peened surface in the sub-domains in the central XTAL domain.
# Of course, skip the XTAL start and XTAL end
xincr = XTAL_dat_plane_x_incr
XTAL_dat_plane_x_incr_values = range(1, NumXTALPartitions_x+1)
for planenumx in range(1, NumXTALPartitions_x):
    xcoord = XTAL_Grains_XLOCS[planenumx]
    XTAL_dat_plane_x_incr_values[planenumx-1] = XtalMat_start_x + xincr
    DPinfo = part.DatumPlaneByPrincipalPlane(offset = SPACER_left_Mat_end_x + xincr, principalPlane = YZPLANE)
    xincr = xincr + XTAL_dat_plane_x_incr
    DatumPlaneIDs_y.append(DPinfo.id)
    part.features.changeKey(fromName='Datum plane-1', toName='DP_XTAL_x_'+str(planenumx))
######################################################################
## Place a datum point at the centre of every sub-domain partition
#xincr = XTAL_dat_plane_x_incr
#for pointnumx in range(NumXTALPartitions_x):
#    xcoord = XTAL_Grains_XLOCS[pointnumx]
#    for pointnumy in range(NumXTALSubDomains):
#        ycoord = (SubDomain_Start[pointnumy] + SubDomain_End[pointnumy])/2
#        part.DatumPointByCoordinate(coords = (xcoord, ycoord, 0.0))
######################################################################
# Partition the XTAL domain into sub-domains
DatPlnIDloc_y_start = 1
if NumXTALPartitions_x>1:
    DAT_plane_IND_Start = DatumPlaneIDs_y[DatPlnIDloc_y_start + (NumXTALSubDomains-1) + 1]
else:
    DAT_plane_IND_Start = DatumPlaneIDs_y[DatPlnIDloc_y_start + (NumXTALSubDomains-1)]
DAT_plane_IND_End   = DatumPlaneIDs_y[len(DatumPlaneIDs_y)-1]

ThisPlaneID = DAT_plane_IND_Start
xincr       = XTAL_dat_plane_x_incr

#DatPlaneID_Count = DatPlnIDloc_y_start + (NumXTALSubDomains-1) + 1
# Calcualte the centres of XTAL subdomains along x and y axes and create sets for subdomains
for pointnumx in range(NumXTALPartitions_x):
    SD_centre_xcoord = XTAL_Grains_XLOCS[pointnumx]
    for pointnumy in range(NumXTALSubDomains):
        SD_centre_ycoord = (SubDomain_Start[pointnumy] + SubDomain_End[pointnumy])/2
        #part.DatumPointByCoordinate(coords = (SD_centre_xcoord, SD_centre_ycoord, 0.0))
        if pointnumx<(len(range(NumXTALPartitions_x))-1):
            part.PartitionFaceByDatumPlane(datumPlane = part.datums[ThisPlaneID], faces = part.faces.findAt(((SD_centre_xcoord, SD_centre_ycoord, 0.), ), ))
        setname = 'XSD_c_' + str(pointnumx) + '_r_' + str(pointnumy)# C: Column along model length, R: Row along model depth
        part.Set(faces = part.faces.findAt(((SD_centre_xcoord, SD_centre_ycoord, 0.),)), name = setname)
    ThisPlaneID = ThisPlaneID + 1
######################################################################
# STORE ALL THE SET NAMES OF THE XTAL IN ONE ARRAY
XTAL_AllSetNames = range(NumXTALPartitions_x)
for pointnumx in range(NumXTALPartitions_x):
    EachColSetNames = range(NumXTALSubDomains)
    for pointnumy in range(NumXTALSubDomains):
        setname = 'XSD_c_' + str(pointnumx) + '_r_' + str(pointnumy)# C: Column along model length, R: Row along model depth
        EachColSetNames[pointnumy] = setname
    XTAL_AllSetNames[pointnumx] = EachColSetNames
######################################################################
# Store the centre locations of all thew sub-domains
AllSubDomain_centre_X = range(NumXTALPartitions_x)
AllSubDomain_centre_Y = range(NumXTALPartitions_x)
for pointnumx in range(NumXTALPartitions_x):
    EachSubDomain_centre_X = range(NumXTALSubDomains)
    EachSubDomain_centre_Y = range(NumXTALSubDomains)
    SD_centre_xcoord = XTAL_Grains_XLOCS[pointnumx]
    for pointnumy in range(NumXTALSubDomains):
        EachSubDomain_centre_X[pointnumy] = SD_centre_xcoord
        EachSubDomain_centre_Y[pointnumy] = (SubDomain_Start[pointnumy] + SubDomain_End[pointnumy])/2
    AllSubDomain_centre_X[pointnumx] = EachSubDomain_centre_X
    AllSubDomain_centre_Y[pointnumx] = EachSubDomain_centre_Y
######################################################################
# Load up default values for location B: number of grains in each subdomain below the peened surface
Modelinfo08B = (('N_Grains_Y_loc_1 @B1T.. all > 0', '3'),
                ('N_Grains_Y_loc_2 @B2T'          , '3'),
                ('N_Grains_Y_loc_3 @B3T'          , '3'),
                ('N_Grains_Y_loc_4 @B4T'          , '3'),
                ('N_Grains_Y_loc_5 @B5T'          , '3'),
                ('N_Grains_Y_loc_6 @B6T'          , '3'),
                ('N_Grains_Y_loc_7 @B7T'          , '3'),
                ('N_Grains_Y_loc_8 @B8T'          , '4'),
                ('dummy', ':::'),
                ('N_Grains_Y_loc_8 @B8B'          , '4'),
                ('N_Grains_Y_loc_7 @B7B'          , '3'),
                ('N_Grains_Y_loc_6 @B6B'          , '3'),
                ('N_Grains_Y_loc_5 @B5B'          , '3'),
                ('N_Grains_Y_loc_4 @B4B'          , '3'),
                ('N_Grains_Y_loc_3 @B3B'          , '3'),
                ('N_Grains_Y_loc_2 @B2B'          , '3'),
                ('N_Grains_Y_loc_1 @B1B'          , '3'),
 	     	   )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07, NGY08, dummy,\
    NGY09, NGY10, NGY11, NGY12, NGY13, NGY14, NGY15, NGY16\
     =  getInputs(fields = Modelinfo08B,\
                  label = 'Enter depth wise N-Grains for B subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_B:NGY.@B1..B8@TB', )
    SD_NGY_BT = np.array([NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07, NGY08])
    SD_NGY_BB = np.array([NGY09, NGY10, NGY11, NGY12, NGY13, NGY14, NGY15, NGY16])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_NGY_B  = np.concatenate((SD_NGY_BT, SD_NGY_BB), axis = 1)
    SD_NGY    = SD_NGY_B
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load up default valuyes for location A: Number of grains in each subdomain below the peened surface
Modelinfo08A = (('N_Grains_Y_loc_1 @A1T.. all > 0', '3'),
                ('N_Grains_Y_loc_2 @A2T'          , '3'),
                ('N_Grains_Y_loc_3 @A3T'          , '3'),
                ('N_Grains_Y_loc_4 @A4T'          , '3'),
                ('N_Grains_Y_loc_5 @A5T'          , '4'),
                ('N_Grains_Y_loc_6 @A6T'          , '4'),
                ('N_Grains_Y_loc_7 @A7T'          , '5'),
                ('dummy', ':::'),
                ('N_Grains_Y_loc_7 @A7B'          , '5'),
                ('N_Grains_Y_loc_6 @A6B'          , '4'),
                ('N_Grains_Y_loc_5 @A5B'          , '4'),
                ('N_Grains_Y_loc_4 @A4B'          , '3'),
                ('N_Grains_Y_loc_3 @A3B'          , '3'),
                ('N_Grains_Y_loc_2 @A2B'          , '3'),
                ('N_Grains_Y_loc_1 @A1B'          , '3'),
 	     	   )
if Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07, dummy,\
    NGY08, NGY09, NGY10, NGY11, NGY12, NGY13, NGY14\
     =  getInputs(fields = Modelinfo08A,\
                  label = 'Enter depth wise N-Grains for A subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_A:NGY.@A1..A7@TB', )
    SD_NGY_AT = np.array([NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07])
    SD_NGY_AB = np.array([NGY08, NGY09, NGY10, NGY11, NGY12, NGY13, NGY14])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_NGY_A  = np.concatenate((SD_NGY_AT, SD_NGY_AB), axis = 1)
    SD_NGY    = SD_NGY_A
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load up default valuyes for location C: number of grains in each sub-domain below the peeened surface
Modelinfo08C = (('N_Grains_Y_loc_1 @C1T.. all > 0', '3'),
                ('N_Grains_Y_loc_2 @C2T'          , '3'),
                ('N_Grains_Y_loc_3 @C3T'          , '3'),
                ('N_Grains_Y_loc_4 @C4T'          , '4'),
                ('N_Grains_Y_loc_5 @C5T'          , '4'),
                ('N_Grains_Y_loc_6 @C6T'          , '4'),
                ('N_Grains_Y_loc_7 @C7T'          , '5'),
                ('N_Grains_Y_loc_8 @C8T'          , '5'),
	     	    ('dummy', ':::'),
                ('N_Grains_Y_loc_8 @C8B'          , '5'),
                ('N_Grains_Y_loc_7 @C7B'          , '5'),
                ('N_Grains_Y_loc_6 @C6B'          , '4'),
                ('N_Grains_Y_loc_5 @C5B'          , '4'),
                ('N_Grains_Y_loc_4 @C4B'          , '4'),
                ('N_Grains_Y_loc_3 @C3B'          , '3'),
                ('N_Grains_Y_loc_2 @C2B'          , '3'),
                ('N_Grains_Y_loc_1 @C1B'          , '3'),
	     	   )
if Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07, NGY08, dummy,\
    NGY09, NGY10, NGY11, NGY12, NGY13, NGY14, NGY15, NGY16\
     =  getInputs(fields = Modelinfo08C,\
                  label = 'Enter depth wise N-Grains for C subdomains ('' if edge is free)',\
                  dialogTitle = 'ModInfo05c_C:NGY.@C1..C8@TB', )
    SD_NGY_CT = np.array([NGY01, NGY02, NGY03, NGY04, NGY05, NGY06, NGY07, NGY08])
    SD_NGY_CB = np.array([NGY09, NGY10, NGY11, NGY12, NGY13, NGY14, NGY15, NGY16])
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    SD_NGY_C  = np.concatenate((SD_NGY_CT, SD_NGY_CB), axis = 1)
    SD_NGY    = SD_NGY_C
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
######################################################################
# SEEDING THE HORIZONTAL EDGES
# Location B: edge seed size in mm
Modelinfo09B = (('TopEdge.SeedSize.AllGrains_in_Loc: @B1T. all > 0', '0.010'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B2T'         , '0.014'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B3T'         , '0.030'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B4T'         , '0.044'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B5T'         , '0.067'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B6T'         , '0.087'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B7T'         , '0.087'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @B8T'         , '0.160'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B8T'         , '0.200'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B8B'         , '0.160'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B7B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B6B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B5B'         , '0.073'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B4B'         , '0.044'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B3B'         , '0.030'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B2B'         , '0.014'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @B1B'         , '0.010'),
 	     	   )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07, TESS_NGY08, dummy1,\
    BESS_NGY09, dummy2, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15, BESS_NGY16, BESS_NGY17\
     = getInputs(fields = Modelinfo09B,label = 'Enter top-edge element-seed-size for grains in mm',dialogTitle = 'Modelinfo09B:TESS_NGY.@B1..B8@TB', )
    SD_allG_TESS_NGY_BT = np.array([TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07, TESS_NGY08])
    SD_allG_BESS_NGY_BB = np.array([BESS_NGY09, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15, BESS_NGY16, BESS_NGY16])
    SD_allG_BESS_NGY_B  = np.concatenate((SD_allG_TESS_NGY_BT, SD_allG_BESS_NGY_BB), axis = 1)
    Modelinfo09Ba = (('Enter multiplication factor', '3'), )
    MultFactor = getInputs(fields = Modelinfo09Ba, label = 'Multiplication factor for previous values', dialogTitle = 'Modelinfo09Ba: Multiplication factor', )
    MultFactor = float(MultFactor[0])
    SD_allG_BESS_NGY_B  = MultFactor*np.asfarray(SD_allG_BESS_NGY_B)
# Location A: edge seed size in mm
Modelinfo09A = (('TopEdge.SeedSize.AllGrains_in_Loc: @A1T. all > 0', '0.010'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A2T'         , '0.014'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A3T'         , '0.030'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A4T'         , '0.044'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A5T'         , '0.067'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A6T'         , '0.087'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @A7T'         , '0.087'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A7T'         , '0.200'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A7B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A6B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A5B'         , '0.073'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A4B'         , '0.044'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A3B'         , '0.030'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A2B'         , '0.014'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @A1B'         , '0.010'),
 	     	   )
if Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07, dummy1,\
    BESS_NGY08, dummy2, BESS_NGY09, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15\
     = getInputs(fields = Modelinfo09A,label = 'Enter top-edge element-seed-size for grains in mm',dialogTitle = 'Modelinfo09a:TESS_NGY.@A1..A8@TB', )
    SD_allG_TESS_NGY_AT = np.array([TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07])
    SD_allG_BESS_NGY_AB = np.array([BESS_NGY08, BESS_NGY09, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15])
    SD_allG_BESS_NGY_A  = np.concatenate((SD_allG_TESS_NGY_AT, SD_allG_BESS_NGY_AB), axis = 1)
    Modelinfo09Aa = (('Enter multiplication factor', '3'), )
    MultFactor = getInputs(fields = Modelinfo09Aa, label = 'Multiplication factor for previous values', dialogTitle = 'Modelinfo09Aa: Multiplication factor', )
    MultFactor = float(MultFactor[0])
    SD_allG_BESS_NGY_A  = MultFactor*np.asfarray(SD_allG_BESS_NGY_A)
# Location C: edge seed size in mm
Modelinfo09C = (('TopEdge.SeedSize.AllGrains_in_Loc: @C1T. all > 0', '0.010'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C2T'         , '0.014'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C3T'         , '0.030'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C4T'         , '0.044'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C5T'         , '0.067'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C6T'         , '0.087'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C7T'         , '0.087'),
                ('TopEdge.SeedSize.AllGrains_in_Loc: @C8T'         , '0.160'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C8T'         , '0.200'),
                ('dummy', ':::'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C8B'         , '0.160'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C7B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C6B'         , '0.087'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C5B'         , '0.073'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C4B'         , '0.044'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C3B'         , '0.030'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C2B'         , '0.014'),
                ('BotEdge.SeedSize.AllGrains_in_Loc: @C1B'         , '0.010'),
 	     	   )
if Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07, TESS_NGY08, dummy1,\
    BESS_NGY09, dummy2, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15, BESS_NGY16, BESS_NGY17\
     = getInputs(fields = Modelinfo09C,label = 'Enter top-edge element-seed-size for grains in mm',dialogTitle = 'Modelinfo09C:TESS_NGY.@C1..C8@TB', )
    SD_allG_TESS_NGY_CT = np.array([TESS_NGY01, TESS_NGY02, TESS_NGY03, TESS_NGY04, TESS_NGY05, TESS_NGY06, TESS_NGY07, TESS_NGY08])
    SD_allG_BESS_NGY_CB = np.array([BESS_NGY09, BESS_NGY10, BESS_NGY11, BESS_NGY12, BESS_NGY13, BESS_NGY14, BESS_NGY15, BESS_NGY16, BESS_NGY16])
    SD_allG_BESS_NGY_C  = np.concatenate((SD_allG_TESS_NGY_CT, SD_allG_BESS_NGY_CB), axis = 1)
    Modelinfo09Ca = (('Enter multiplication factor', '3'), )
    MultFactor = getInputs(fields = Modelinfo09Ca, label = 'Multiplication factor for previous values', dialogTitle = 'Modelinfo09Ca: Multiplication factor', )
    MultFactor = float(MultFactor[0])
    SD_allG_BESS_NGY_C  = MultFactor*np.asfarray(SD_allG_BESS_NGY_C)
######################################################################
# SEEDING THE VERTICAL EDGES
# Location B: edge seed size entered in the form of number of edge seed partitions
Modelinfo09BV = (('VertEdge.SeedSize.AllGrains_in_Loc: @B1T. all > 0', '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B2T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B3T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B4T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B5T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B6T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B7T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B8T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B8B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B7B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B6B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B5B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B4B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B3B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B2B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @B1B'         , '2'),
  	     	    )
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07, VESS_NGY08,\
    VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14, VESS_NGY15, VESS_NGY16\
     = getInputs(fields = Modelinfo09BV,label = 'Enter vert-edge element-seed-NUMBER for grains',dialogTitle = 'Modelinfo09BV:VESN_NGY.@B1..B8@VE', )
    SD_allG_VESS_NGY_BT = np.array([VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07, VESS_NGY08])
    SD_allG_VESS_NGY_BB = np.array([VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14, VESS_NGY15, VESS_NGY16])
    SD_allG_VESS_NGY_B  = np.concatenate((SD_allG_VESS_NGY_BT, SD_allG_VESS_NGY_BB), axis = 1)
# Location A: edge seed size entered in the form of number of edge seed partitions
Modelinfo09AV = (('VertEdge.SeedSize.AllGrains_in_Loc: @A1T. all > 0', '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A2T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A3T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A4T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A5T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A6T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A7T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A7B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A6B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A5B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A4B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A3B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A2B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @A1B'         , '2'),
  	     	    )
if Sample_Location[0] in ['B', 'A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07,\
    VESS_NGY08, VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14\
     = getInputs(fields = Modelinfo09AV,label = 'Enter vert-edge element-seed-NUMBER for grains',dialogTitle = 'Modelinfo09AV:VESN_NGY.@A1..A7@VE', )
    SD_allG_VESS_NGY_AT = np.array([VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07])
    SD_allG_VESS_NGY_AB = np.array([VESS_NGY08, VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14])
    SD_allG_VESS_NGY_A  = np.concatenate((SD_allG_VESS_NGY_AT, SD_allG_VESS_NGY_AB), axis = 1)
# Location C: edge seed size entered in the form of number of edge seed partitions
Modelinfo09CV = (('VertEdge.SeedSize.AllGrains_in_Loc: @C1T. all > 0', '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C2T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C3T'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C4T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C5T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C6T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C7T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C8T'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C8B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C7B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C6B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C5B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C4B'         , '1'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C3B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C2B'         , '2'),
                 ('VertEdge.SeedSize.AllGrains_in_Loc: @C1B'         , '2'),
  	     	    )
if Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07, VESS_NGY08,\
    VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14, VESS_NGY15, VESS_NGY16\
     = getInputs(fields = Modelinfo09CV,label = 'Enter vert-edge element-seed-NUMBER for grains',dialogTitle = 'Modelinfo09CV:VESN_NGY.@C1..C8@VE', )
    SD_allG_VESS_NGY_CT = np.array([VESS_NGY01, VESS_NGY02, VESS_NGY03, VESS_NGY04, VESS_NGY05, VESS_NGY06, VESS_NGY07, VESS_NGY08])
    SD_allG_VESS_NGY_CB = np.array([VESS_NGY09, VESS_NGY10, VESS_NGY11, VESS_NGY12, VESS_NGY13, VESS_NGY14, VESS_NGY15, VESS_NGY16])
    SD_allG_VESS_NGY_C  = np.concatenate((SD_allG_VESS_NGY_CT, SD_allG_VESS_NGY_CB), axis = 1)
######################################################################
# Calculate the total number of top edges to be seeded in one x partition of the XTAL
NTopEdg_in_half__XTL_parti_X = np.sum(np.asarray(SD_NGY[0:int(len(SD_NGY)/2)], dtype = 'int'))
# - - - - - -
# Calculate the total number of bot edges to be seeded in one x partition of the XTAL
NBotEdg_in_half__XTL_parti_X = np.sum(np.asarray(SD_NGY[0:int(len(SD_NGY)/2)], dtype = 'int'))+1
# - - - - - -
# Initialize the matrix to store seed values of all top edges in the XTAL domain
TE_Seed_SizeData  = np.zeros(shape = (NTopEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
TE_Seed_EdgeLoc_X = np.zeros(shape = (NTopEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
TE_Seed_EdgeLoc_Y = np.zeros(shape = (NTopEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
# Access: TE_Seed_SizeData[0][1], CE_Seed_SizeData[0][3]
# - - - - - -
# Initialize the matrix to store seed values of all model centre edges in the XTAL domain
CE_Seed_SizeData  = np.zeros(shape = (1, NumXTALPartitions_x))
CE_Seed_EdgeLoc_X = np.zeros(shape = (1, NumXTALPartitions_x))
CE_Seed_EdgeLoc_Y = np.zeros(shape = (1, NumXTALPartitions_x))
# Access: CE_Seed_SizeData[0][1], CE_Seed_SizeData[0][3]
# - - - - - -
# Initialize the matrix to store seed values of all bot edges in the XTAL domain
BE_Seed_SizeData  = np.zeros(shape = (NBotEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
BE_Seed_EdgeLoc_X = np.zeros(shape = (NBotEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
BE_Seed_EdgeLoc_Y = np.zeros(shape = (NBotEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
# - - - - - -
# Initialize the matrix to store seed values of top and bot edges in the XTAL domain.
# Bot and top data will then be extracted from this
# These matrices themselves to be deleted after use to save memory
Seed_EdgeLoc_Y    = np.zeros(shape = (NTopEdg_in_half__XTL_parti_X+NBotEdg_in_half__XTL_parti_X, NumXTALPartitions_x))
Seed_EdgeLoc_X    = Seed_EdgeLoc_Y
##################################################
# build the x-location of centres of top edges of all grains in NTopEdg_in_half__XTL_parti_X
xincr = XTAL_dat_plane_x_incr
XTAL_dat_plane_x_incr_values = range(1, NumXTALPartitions_x+1)
for planenumx in range(1, NumXTALPartitions_x):
    xcoord = XTAL_Grains_XLOCS[planenumx]
    XTAL_dat_plane_x_incr_values[planenumx-1] = XtalMat_start_x + xincr
    xincr = xincr + XTAL_dat_plane_x_incr
TE_Seed_EdgeLoc_X = XTAL_dat_plane_x_incr_values
for pcount in range(len(XTAL_dat_plane_x_incr_values)):
    if pcount<len(XTAL_dat_plane_x_incr_values)-1:
        TE_Seed_EdgeLoc_X[pcount] = TE_Seed_EdgeLoc_X[pcount] - XTAL_dat_plane_x_incr/2
    elif pcount==len(XTAL_dat_plane_x_incr_values)-1:
        TE_Seed_EdgeLoc_X[pcount] = TE_Seed_EdgeLoc_X[pcount-1] + XTAL_dat_plane_x_incr
#--------------------
# build the y-location of centres of top edges of all grains in NTopEdg_in_half__XTL_parti_X and NBotEdg_in_half__XTL_parti_X combined
TotalNumGrains    = int(np.sum(np.asfarray(SD_NGY)))
TotalNumSeedEdges = int(TotalNumGrains + 1)
#--------------------
######################################################################
# Construct thickness of each sub-domains
SubDomain_Thickness = np.round(np.round(SubDomain_Start,2) - np.round(SubDomain_End,2), 2)
######################################################################
# Do decimal point house keeping
SubDomain_Start = np.round(SubDomain_Start, 2)
SubDomain_End   = np.round(SubDomain_End, 2)
######################################################################
# build the array "Hor_seed_size" having the horizontal edge seed lengths for relevant edges for all grains in 1 set
# of a any single vertical partition of the XTAL domain
Seed_EdgeLoc_Ytemp = range(1,TotalNumSeedEdges+1)
GrainCount_y = 0 # Count for the grains along y-axis
EdgeCount    = 0
Hor_seed_size = []
for ypos in range(NumXTALSubDomains):
    # SUB-DOMAIN
    ThisSD_TE_Start  = SubDomain_Start[ypos]
    ThisSD_TE_End    = SubDomain_End[ypos]
    ThisSD_thickness = SubDomain_Thickness[ypos]
    # GRAIN
    NoGrains             = int(SD_NGY[ypos])
    ThisGrainThickness   = ThisSD_thickness/NoGrains
    GrainTE_Locations    = np.arange(ThisSD_TE_Start, ThisSD_TE_End, -ThisGrainThickness)
    GrainBE_Locations    = GrainTE_Locations - ThisGrainThickness
    for SD_grain_count in range(NoGrains):
        if GrainCount_y <= TotalNumGrains/2:
            Seed_EdgeLoc_Ytemp[GrainCount_y] = GrainTE_Locations[SD_grain_count]
            Hor_seed_size.append(SD_allG_BESS_NGY_B[ypos])
            GrainCount_y = GrainCount_y + 1
        elif GrainCount_y == TotalNumGrains/2:
            Seed_EdgeLoc_Ytemp[GrainCount_y] = modelcentre_y
            Hor_seed_size.append(SD_allG_BESS_NGY_B[ypos])
            GrainCount_y = GrainCount_y + 1
        elif GrainCount_y == TotalNumGrains/2+1:
            Seed_EdgeLoc_Ytemp[GrainCount_y]   = GrainTE_Locations[SD_grain_count]
            Seed_EdgeLoc_Ytemp[GrainCount_y+1] = GrainBE_Locations[SD_grain_count]
            Hor_seed_size.append(SD_allG_BESS_NGY_B[ypos+1])
            GrainCount_y = GrainCount_y + 1
            Hor_seed_size.append(SD_allG_BESS_NGY_B[ypos+1])
            GrainCount_y = GrainCount_y + 1
        elif GrainCount_y > TotalNumGrains/2+1:
            Seed_EdgeLoc_Ytemp[GrainCount_y] = GrainBE_Locations[SD_grain_count]
            Hor_seed_size.append(SD_allG_BESS_NGY_B[ypos])
            GrainCount_y = GrainCount_y + 1
######################################################################
# HORIZONTAL EDGES OF ALL GRAINS
Hor_seed_size = []
# For all top edges
paritioncount = 0
nthgrainnum   = 0
for seedsize in SD_allG_BESS_NGY_B[0:len(SD_allG_BESS_NGY_B)/2-1+1]:
    for graincount in range(int(SD_NGY[paritioncount])):
        Hor_seed_size.append(seedsize)
        nthgrainnum = nthgrainnum + 1
    paritioncount = paritioncount + 1
# for the central edge
Hor_seed_size.append(SD_allG_BESS_NGY_B[len(SD_allG_BESS_NGY_B)/2])
# For all bottom edges
for seedsize in SD_allG_BESS_NGY_B[len(SD_allG_BESS_NGY_B)/2+1:len(SD_allG_BESS_NGY_B)]:
    for graincount in range(int(SD_NGY[paritioncount])):
        Hor_seed_size.append(seedsize)
        nthgrainnum = nthgrainnum + 1
    paritioncount = paritioncount + 1
######################################################################
# VERTICAL EDGES OF ALL GRAINS
SD_allG_VESS_NGY_B
Vert_seed_Num = []
# For all top edges
paritioncount = 0
nthgrainnum   = 0
for seedsize in SD_allG_VESS_NGY_B:
    for graincount in range(int(SD_NGY[paritioncount])):
        Vert_seed_Num.append(seedsize)
        nthgrainnum = nthgrainnum + 1
    paritioncount = paritioncount + 1
######################################################################
Hor_Edges_LOC_X = TE_Seed_EdgeLoc_X
Hor_Edges_LOC_Y = Seed_EdgeLoc_Ytemp

#for xloc in Hor_Edges_LOC_X:
#    for yloc in Hor_Edges_LOC_Y:
#        part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
######################################################################
# Insead of making grains in each of the subdomains, i am making each of the
# subdomains themselves as the grain

# Partition each sub-domain into constituent grains
# Assign set name for each Grain
# Assign material for each grain
# Assign section to mater8ial

PartitionCount = 0 # Overall partition count
GrainCount_x   = 0 # Count for the grains along x-axis
Total_HardeningMatModel_Subdomains = 0
GrainCentres_Y = []
GrainThicknessData = []
for xpos in range(NumXTALPartitions_x):
    ######################################
    #xpos = 1 # For hardcoding and debugging
    GrainCount_y = 0 # Count for the grains along y-axis
    for ypos in range(NumXTALSubDomains):
        #ypos = 2 # For hardcoding and debugging
        # SUB-DOMAIN CALCULATIONS
        # Retrieve the sub-domain partition name
        SDName           = XTAL_AllSetNames[xpos][ypos]
        # Retrieve position of the top edge of this sub-domain.. #ThisSD_TE_Start  = round(SubDomain_Start[ypos], 2) # Forcing 2 digits again
        ThisSD_TE_Start  = SubDomain_Start[ypos]
        # Retrieve position of the bot edge of this sub-domain.. #ThisSD_TE_End    = round(SubDomain_End[ypos], 2)
        ThisSD_TE_End    = SubDomain_End[ypos]
        # Retrieve thickness of this sub-domain.. #ThisSD_thickness = round(SubDomain_Thickness[ypos], 2)
        ThisSD_thickness = SubDomain_Thickness[ypos]
        #-----------
        # GRAIN CALCULATIONS.     # FOR LOCATIONS, ONLY THE Y-COORDINATES ARE NEEDED
        # AS THE X-CCOORDSINATES WILL BE THE SAME AS THAT OF THE MAIN XTAL PARITIONIKNG
        # Retrieve how many grains are needed in this sub-domain
        NoGrains             = int(SD_NGY[ypos])
        # Calculate this grain thickness
        ThisGrainThickness   = ThisSD_thickness/NoGrains
        if GrainCount_x == 0:
            GrainThicknessData.append(ThisGrainThickness)
        # Calculate top edge locations of each grain in this sub-domain
        GrainTE_Locations    = np.arange(ThisSD_TE_Start, ThisSD_TE_End, -ThisGrainThickness)
        # Calculate bot edge locations of each grain in this sub-domain
        GrainBE_Locations    = GrainTE_Locations - ThisGrainThickness
        # Calculate the centre positions of each of the grains
        GrainCentreLocations = (GrainBE_Locations + GrainTE_Locations)/2
        # Calculate the datum plane location needed to partition sub-domain into grains
        if NoGrains>1:
            GrainPartDatPlnLoc = GrainTE_Locations[1:len(GrainTE_Locations)]
        # Retrieve the centre location X-coord of all grains in this sub-domain
        thesesgrainshavecentreX = AllSubDomain_centre_X[xpos][ypos]
        # Loop over each grain in this sub-domain
        datumplaneIDs = range(NoGrains-1)
        NoGrainsRange = range(NoGrains)
        for SD_grain_count in range(NoGrains):
            #SD_grain_count = 1 # For hardcoding and debugging
            # Build the grain name
            ThisGrainName = SDName + '_Grain_Nx_' + str(GrainCount_x + 1) + '_Ny_' + str(GrainCount_y + 1)
            # Retrieve the centre location X-coord & Y-coord of this grain
            thisgraincentreX = thesesgrainshavecentreX
            thisgraincentreY = GrainCentreLocations[SD_grain_count]
            if xpos==0:
                GrainCentres_Y.append(thisgraincentreY)
            # Test visually by printing out datum points at these location. KEEP COMMENTED
            # part.DatumPointByCoordinate(coords = (thisgraincentreX, thisgraincentreY, 0.0))
            # Retrieve location of the datum plane where this sub-domain is to be sub-divided into grains
            if NoGrains>1 and SD_grain_count!=NoGrainsRange[len(NoGrainsRange)-1]:
                DatPlnLoc = GrainPartDatPlnLoc[SD_grain_count]
                # Make the datum plane
                DPinfo = part.DatumPlaneByPrincipalPlane(offset = DatPlnLoc, principalPlane = XZPLANE)
                # Retreieve the datum plane ID
                ThisDP_ID = DPinfo.id
                # Build the datum planbe ID array for probable future use
                datumplaneIDs[SD_grain_count] = ThisDP_ID
                # Make the partition using this datum ID
                part.PartitionFaceByDatumPlane(datumPlane = part.datums[ThisDP_ID], faces = part.faces.findAt(((thisgraincentreX, thisgraincentreY, 0.), ), ))
            #-----------
            # Build set name
            ThisGrainSetName     = 'Set_' + SDName + '_Grain_Nx_' + str(GrainCount_x + 1) + '_Ny_' + str(GrainCount_y + 1)
            # Build material name
            ThisGrainMatName     = 'Mat_' + SDName + '_Grain_Nx_' + str(GrainCount_x + 1) + '_Ny_' + str(GrainCount_y + 1)
            # 8b. Build section name
            ThisGrainSectionName = 'Sec_' + SDName + '_Grain_Nx_' + str(GrainCount_x + 1) + '_Ny_' + str(GrainCount_y + 1)
            #-----------
            # Assign the set
            part.Set(faces = part.faces.findAt(((thisgraincentreX, thisgraincentreY, 0.),)), name = ThisGrainSetName)
            # Create material
            model.Material(name=ThisGrainMatName)
            model.materials[ThisGrainMatName].UserMaterial(mechanicalConstants=(0.0,))
            # Create section
            model.HomogeneousSolidSection(material = ThisGrainMatName, name = ThisGrainSectionName, thickness = None)
            # Assign section to geometry
            part.SectionAssignment(offset = 0.0, offsetField = '', offsetType = MIDDLE_SURFACE, region = part.sets[ThisGrainSetName], sectionName = ThisGrainSectionName, thicknessAssignment = FROM_SECTION)
            # 12. Seed the top edges
            # 13. Seed the left edges
            # 14. Mesh the grain
            #-----------
            # Increment the loop variables
            GrainCount_y   = GrainCount_y + 1
            PartitionCount = PartitionCount + 1
        Total_HardeningMatModel_Subdomains = Total_HardeningMatModel_Subdomains + 1
    GrainCount_x = GrainCount_x + 1
######################################################################
# Create assembly
model.rootAssembly.DatumCsysByDefault(CARTESIAN)
model.rootAssembly.Instance(dependent=ON, name='partname-1', part=mdb.models['Model-1'].parts['partname'])
######################################################################
# Create time steps
model.StaticStep(initialInc=Time_Step_RSG_initial_incr, maxInc=Time_Step_RSG_maximum_incr, minInc=Time_Step_RSG_minimum_incr,
    name='Step-1', nlgeom=ON, previous='Initial', timePeriod=Time_Step_EQUI_total_time)
######################################################################
model = mdb.models['Model-1']
part  = model.parts['partname']
######################################################################
# Get "Hor_seed_size" in float datatype
Hor_seed_size_temp = Hor_seed_size
Hor_seed_size = []
for count in range(len(Hor_Edges_LOC_Y)-1):
    Hor_seed_size.append(float(Hor_seed_size_temp[count]))
######################################################################
# Get user input on Edge Seeding -- Finite element conformity
Modelinfo10A = (('Hor.Edge.Seeding.Constraint', '1'),
                ('1: Free', ':::'),
                ('2: Finer', ':::'),
                ('3: Fixed', ':::'),
	      	   )
Hor_Edge_Seeding_Constraint, dummy1, dummy2,dummy3,\
 =  getInputs(fields = Modelinfo10A, label = 'SEED:to:ELEM conformity@HOR.EDGES', dialogTitle = 'Modelinfo10A: FE seed behaviour', )
Hor_Edge_Seeding_Constraint = int(Hor_Edge_Seeding_Constraint)

# Seed the horizontal edges
Hor_seed_size.append(Hor_seed_size[len(Hor_seed_size)-1])
try:
    count = 0
    for yloc in Hor_Edges_LOC_Y:
        for xloc in Hor_Edges_LOC_X:
            ThisEdgeSize = float(Hor_seed_size[count])
            if Hor_Edge_Seeding_Constraint==1:
                part.seedEdgeBySize(constraint=FREE, deviationFactor=0.1, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), size = ThisEdgeSize)
            elif Hor_Edge_Seeding_Constraint==2:
                part.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), size = ThisEdgeSize)
            elif Hor_Edge_Seeding_Constraint==3:
                part.seedEdgeBySize(constraint=FIXED, deviationFactor=0.1, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), size = ThisEdgeSize)
        count = count + 1
except:
    pass
######################################################################
# Get user input on Edge Seeding -- Finite element conformity
Modelinfo10B = (('Vert.Edge.Seeding.Constraint', '1'),
                ('1: Free', ':::'),
                ('2: Finer', ':::'),
                ('3: Fixed', ':::'),
	     	   )
Vert_Edge_Seeding_Constraint, dummy1, dummy2,dummy3,\
 =  getInputs(fields = Modelinfo10B, label = 'SEED:to:ELEM conformity@VERT.EDGES', dialogTitle = 'Modelinfo10B: FE seed behaviour', )
Vert_Edge_Seeding_Constraint = int(Vert_Edge_Seeding_Constraint)
# identify the locations of the centres of vertical edges of all the grains
VertEdge_centres_Y = GrainCentres_Y
VertEdge_centres_X = []
GrainCentres_X = Hor_Edges_LOC_X
for locx in GrainCentres_X:
    VertEdge_centres_X.append(locx - XTAL_dat_plane_x_incr/2)
VertEdge_centres_X.append(VertEdge_centres_X[len(VertEdge_centres_X)-1] + XTAL_dat_plane_x_incr)
# Seed the horizontal edges
for xloc in VertEdge_centres_X:
    count = 0
    for yloc in VertEdge_centres_Y:
        ThisEdgeNumSeeds = int(Vert_seed_Num[count])
        if Vert_Edge_Seeding_Constraint==1:
            part.seedEdgeByNumber(constraint=FREE, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), number = ThisEdgeNumSeeds)
        elif Vert_Edge_Seeding_Constraint==2:
            part.seedEdgeByNumber(constraint=FINER, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), number = ThisEdgeNumSeeds)
        elif Vert_Edge_Seeding_Constraint==3:
            part.seedEdgeByNumber(constraint=FIXED, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), number = ThisEdgeNumSeeds)
        count = count+1
######################################################################
#HES = np.zeros((len(Hor_Edges_LOC_Y), len(Hor_Edges_LOC_X)), dtype = 'float')
#HES_y = np.zeros((len(Hor_Edges_LOC_Y), len(Hor_Edges_LOC_X)), dtype = 'float')
#HES_x = np.zeros((len(Hor_Edges_LOC_Y), len(Hor_Edges_LOC_X)), dtype = 'float')
#for row in range(len(Hor_Edges_LOC_Y)-1):
#    for col in range(len(Hor_Edges_LOC_X)-1):
#        HES_y[row][col] = Hor_Edges_LOC_Y[row]
#        HES_x[row][col] = Hor_Edges_LOC_X[col]
#        HES[row][col] = float(Hor_seed_size[row])

#for row in range(len(Hor_Edges_LOC_Y)-1):
#    for col in range(len(Hor_Edges_LOC_X)):
#        ThisEdgeSize = float(HES[row][col])
#        xloc = HES_x[row][col]
#        yloc = HES_y[row][col]
#        part.seedEdgeBySize(constraint=FINER, deviationFactor=0.1, edges = model.rootAssembly.instances['partname-1'].edges.findAt(((xloc, yloc, 0.), ), ), size = ThisEdgeSize)
######################################################################
######################################################################
######################################################################
######################################################################
######################################################################
# Assign element element information to each grain
GrainCentres_X = Hor_Edges_LOC_X
GrainCentres_Y

for xloc in GrainCentres_X:
    print 'xloc = ' + str(xloc)
    for yloc in GrainCentres_Y:
        #-------------------------------
        if XTAL_ElementTypeFlagID==1:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS4R, elemLibrary = STANDARD, secondOrderAccuracy = OFF,hourglassControl = ENHANCED, distortionControl = DEFAULT), ElemType(elemCode = CPS3, elemLibrary = STANDARD)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif XTAL_ElementTypeFlagID==2:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8 , elemLibrary = STANDARD), ElemType(elemCode = CPS6M,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif XTAL_ElementTypeFlagID==3:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS4 , elemLibrary = STANDARD), ElemType(elemCode = CPS3 ,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif XTAL_ElementTypeFlagID==4:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8R, elemLibrary = STANDARD), ElemType(elemCode = CPS6M,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif XTAL_ElementTypeFlagID==5:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8R, elemLibrary = STANDARD), ElemType(elemCode = CPS6 ,elemLibrary = STANDARD)), regions = (part.faces.findAt(((xloc,yloc,0.),)),))
        #-------------------------------
        if XTAL_ElementShapeFlagID == 1:
            part.setMeshControls(elemShape=QUAD, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=STRUCTURED)
        elif XTAL_ElementShapeFlagID == 2:
            part.setMeshControls(elemShape=QUAD, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=FREE)
        elif XTAL_ElementShapeFlagID == 3:
            part.setMeshControls(elemShape=TRI, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=STRUCTURED)
        elif XTAL_ElementShapeFlagID == 4:
            part.setMeshControls(elemShape=TRI, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=FREE)
        elif XTAL_ElementShapeFlagID == 5:
            part.setMeshControls(elemShape=QUAD_DOMINATED, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=FREE)
# generate the finite element mesh
for xloc in GrainCentres_X:
    print 'xloc = ' + str(xloc)
    for yloc in GrainCentres_Y:
        part.generateMesh(regions = part.faces.findAt(((xloc, yloc, 0.),)))
######################################################################
# print out the total number of nodes and elements in the XTAL domain
mdb.models['Model-1'].rootAssembly.regenerate()
instance        = model.rootAssembly.instances['partname-1']
TotalNumOfNodes = len(instance.nodes)
TotalNumOfElem  = len(instance.elements)

print('There are %d Elements --- %d Nodes --- in this XTAL domain'% (TotalNumOfElem, TotalNumOfNodes))
######################################################################
######################################################################
