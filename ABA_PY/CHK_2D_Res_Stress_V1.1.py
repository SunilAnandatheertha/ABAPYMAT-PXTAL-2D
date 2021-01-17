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

Model_size_x    = Model_enddim_x - Model_origin_x
Model_size_y    = Model_enddim_y - Model_origin_y

SPACER_left_Mat_start_x = Model_origin_x
SPACER_left_Mat_start_y = Model_origin_y
SPACER_left_Mat_end_x   = float(XtalMat_start_x)
SPACER_left_Mat_end_y   = Model_origin_y + Model_size_y
SPACER_left_Mat_size_x  = SPACER_left_Mat_end_x - SPACER_left_Mat_start_x
SPACER_left_Mat_size_y  = Model_origin_y

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

SPACER_right_Mat_start_x = XtalMat_end_x
SPACER_right_Mat_start_y = Model_origin_y
SPACER_right_Mat_end_x   = Model_origin_x + Model_enddim_x
SPACER_right_Mat_end_y   = Model_origin_y + Model_size_y
SPACER_right_Mat_size_x  = SPACER_right_Mat_end_x - SPACER_right_Mat_start_x
SPACER_right_Mat_size_y  = Model_enddim_y
######################################################################
Modelinfo02 = (('NumXTALPartitions_x', '20'),
               ('NumXTALPartitions_y', '25'),
               ('NumXTALPartitions_total', '500'),
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
######################################################################
Num_XTAL_DatumPlanes_x = NumXTALPartitions_x - 1
Num_XTAL_DatumPlanes_y = NumXTALPartitions_y - 1

Num_SPACER_DatumPlanes_x = NumSPACERPartitions_x - 1
Num_SPACER_DatumPlanes_y = NumSPACERPartitions_y - 1
######################################################################
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
 =  getInputs(fields = Modelinfo03, label = 'Time stepping details', dialogTitle = 'Modelinfo03', )

Time_Step_RSG_total_time   = float(Time_Step_RSG_total_time)
Time_Step_RSG_initial_incr = float(Time_Step_RSG_initial_incr)
Time_Step_RSG_minimum_incr = float(Time_Step_RSG_minimum_incr)
Time_Step_RSG_maximum_incr = float(Time_Step_RSG_maximum_incr)

Time_Step_EQUI_total_time   = float(Time_Step_EQUI_total_time)
Time_Step_EQUI_initial_incr = float(Time_Step_EQUI_initial_incr)
Time_Step_EQUI_minimum_incr = float(Time_Step_EQUI_minimum_incr)
Time_Step_EQUI_maximum_incr = float(Time_Step_EQUI_maximum_incr)
######################################################################
Modelinfo04 = (('XTAL_ElementFactor', '1'),
               ('ElementTypeFlagID: 1: CPS4R-or-CPS3...2: CPS8-or-CPS6M...3: CPS4-or-CPS3...4: CPS8R-or-CPS6M...5: CPS8R-or-CPS6', '4'),
               ('ElementShapeFlagID: 1: Quad-structured...2: Quad-free...3: Tri-Structured...4: Tri-Free', '4'),
               ('SPACER_MESHING_MORPHED ?(0:no, 1:yes)', '1'),
               ('SPACER_ElementFactor', '1'),
               ('ElementTypeFlagID: 1: CPS4R-or-CPS3...2: CPS8-or-CPS6M...3: CPS4-or-CPS3...4: CPS8R-or-CPS6M...5: CPS8R-or-CPS6', '4'),
               ('ElementShapeFlagID: 1: Quad-structured...2: Quad-free...3: Tri-Structured...4: Tri-Free', '4'),
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

XTAL_ElementSize   = (Model_enddim_y/NumXTALPartitions_y)/XTAL_ElementFactor
######################################################################
# GET SAMPLE LOCATION
Modelinfo05a = (('Sample_Location (A/B/C)', 'B'), )
Sample_Location =  getInputs(fields = Modelinfo05a, label = 'Enter Boun. Cond. details', dialogTitle = 'Modelinfo05: Boundary conditions', )
######################################################################
SubDom_IND_B = np.arange(0, 16)
SubDom_IND_A = np.arange(0, 14)
SubDom_IND_C = np.arange(0, 16)
######################################################################
# Load up default values for the sub-domain depth location bounds
# LOCATION - B
Modelinfo05bBS = (('B1.T: Sub-Domain start, mm', '0.00'), ('B2.T: Sub-Domain start    ', '0.06'), ('B3.T: Sub-Domain start    ', '0.13'), ('B4.T: Sub-Domain start    ', '0.25'),
                  ('B5.T: Sub-Domain start    ', '0.40'), ('B6.T: Sub-Domain start    ', '0.60'), ('B7.T: Sub-Domain start    ', '0.95'), ('B8.T: Sub-Domain start    ', '1.30'),
                  ('dummy', '::::'),
                  ('B8.B: Sub-Domain start, mm', '2.50'), ('B7.B: Sub-Domain start    ', '3.70'), ('B6.B: Sub-Domain start    ', '4.05'), ('B5.B: Sub-Domain start    ', '4.40'),
                  ('B4.B: Sub-Domain start    ', '4.60'), ('B3.B: Sub-Domain start    ', '4.75'), ('B2.B: Sub-Domain start    ', '4.87'), ('B1.B: Sub-Domain start    ', '4.94'),
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
Modelinfo05bBE = (('B1.T: Sub-Domain end, mm', '0.06'), ('B2.T: Sub-Domain end'    , '0.13'), ('B3.T: Sub-Domain end'    , '0.25'), ('B4.T: Sub-Domain end'    , '0.40'),
                  ('B5.T: Sub-Domain end'    , '0.60'), ('B6.T: Sub-Domain end'    , '0.95'), ('B7.T: Sub-Domain end'    , '1.30'), ('B8.T: Sub-Domain end'    , '2.50'),
                  ('dummy', '::::'),
                  ('B8.B: Sub-Domain end, mm', '3.70'), ('B7.B: Sub-Domain end    ', '4.05'), ('B6.B: Sub-Domain end    ', '4.40'), ('B5.B: Sub-Domain end    ', '4.60'),
                  ('B4.B: Sub-Domain end    ', '4.75'), ('B3.B: Sub-Domain end    ', '4.87'), ('B2.B: Sub-Domain end    ', '4.94'), ('B1.B: Sub-Domain end    ', '5.00'),
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
# ------------------------------------------------------------
# LOCATION - A
Modelinfo05bAS = (('A1.T: Sub-Domain start, mm', '0.00'), ('A2.T: Sub-Domain start    ', '0.06'), ('A3.T: Sub-Domain start    ', '0.15'), ('A4.T: Sub-Domain start    ', '0.25'),
                  ('A5.T: Sub-Domain start    ', '0.40'), ('A6.T: Sub-Domain start    ', '0.75'), ('A7.T: Sub-Domain start    ', '1.20'),
                  ('dummy', '::::'),
                  ('A7.B: Sub-Domain start    ', '2.50'), ('A6.B: Sub-Domain start    ', '3.80'), ('A5.B: Sub-Domain start    ', '4.25'), ('A4.B: Sub-Domain start    ', '4.60'),
                  ('A3.B: Sub-Domain start    ', '4.75'), ('A2.B: Sub-Domain start    ', '4.85'), ('A1.B: Sub-Domain start    ', '4.94'),
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
Modelinfo05bAE = (('A1.T: Sub-Domain end, mm', '0.06'), ('A2.T: Sub-Domain end'    , '0.15'), ('A3.T: Sub-Domain end'    , '0.25'), ('A4.T: Sub-Domain end'    , '0.40'),
                  ('A5.T: Sub-Domain end'    , '0.75'), ('A6.T: Sub-Domain end'    , '1.20'), ('A7.T: Sub-Domain end'    , '2.50'),
                  ('Adummy', '::::'),
                  ('A7.B: Sub-Domain end    ', '3.80'), ('A6.B: Sub-Domain end    ', '4.25'), ('A5.B: Sub-Domain end    ', '4.60'), ('A4.B: Sub-Domain end    ', '4.75'),
                  ('A3.B: Sub-Domain end    ', '4.85'), ('A2.B: Sub-Domain end    ', '4.94'), ('A1.B: Sub-Domain end    ', '5.00'),
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
# ------------------------------------------------------------
# LOCATION - C
Modelinfo05bCS = (('C1.T: Sub-Domain start, mm', '0.00'), ('C2.T: Sub-Domain start    ', '0.06'), ('C3.T: Sub-Domain start    ', '0.15'), ('C4.T: Sub-Domain start    ', '0.25'),
                  ('C5.T: Sub-Domain start    ', '0.50'), ('C6.T: Sub-Domain start    ', '0.70'), ('C7.T: Sub-Domain start    ', '1.30'), ('C8.T: Sub-Domain start    ', '1.80'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain start, mm', '2.50'), ('C7.B: Sub-Domain start    ', '3.20'), ('C6.B: Sub-Domain start    ', '3.70'), ('C5.B: Sub-Domain start    ', '4.30'),
                  ('C4.B: Sub-Domain start    ', '4.50'), ('C3.B: Sub-Domain start    ', '4.75'), ('C2.B: Sub-Domain start    ', '4.85'), ('C1.B: Sub-Domain start    ', '4.94'),
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
Modelinfo05bCE = (('C1.T: Sub-Domain end, mm', '0.06'), ('C2.T: Sub-Domain end'    , '0.15'), ('C3.T: Sub-Domain end'    , '0.25'), ('C4.T: Sub-Domain end'    , '0.50'),
                  ('C5.T: Sub-Domain end'    , '0.70'), ('C6.T: Sub-Domain end'    , '1.30'), ('C7.T: Sub-Domain end'    , '1.80'), ('C8.T: Sub-Domain end'    , '2.50'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain end, mm', '3.20'), ('C7.B: Sub-Domain end    ', '3.70'), ('C6.B: Sub-Domain end    ', '4.30'), ('C5.B: Sub-Domain end    ', '4.50'),
                  ('C4.B: Sub-Domain end    ', '4.75'), ('C3.B: Sub-Domain end    ', '4.85'), ('C2.B: Sub-Domain end    ', '4.94'), ('C1.B: Sub-Domain end    ', '5.00'),
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
######################################################################
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    SubDom_IND = SubDom_IND_B;
elif Sample_Location[0] in ['B', 'A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    SubDom_IND = SubDom_IND_A;
elif Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    SubDom_IND = SubDom_IND_C;
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
######################################################################
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    SD_eps_TE = SD_eps_B_TE;
    SD_eps_TE_VAL = np.ones(16, dtype = 'int')
elif Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    SD_eps_TE = SD_eps_A_TE;
    SD_eps_TE_VAL = np.ones(14, dtype = 'int')
elif Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    SD_eps_TE = SD_eps_C_TE;
    SD_eps_TE_VAL = np.ones(16, dtype = 'int')
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
NumXTALSubDomains = len(SubDomain_End)
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    NamesXTALSubDomains = ['B1T','B2T', 'B3T', 'B4T', 'B5T', 'B6T', 'B7T', 'B8T', 'B8B', 'B7B', 'B6B', 'B5B', 'B4B', 'B3B', 'B2B', 'B1B']
elif Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    NamesXTALSubDomains = ['A1T','A2T', 'A3T', 'A4T', 'A5T', 'A6T', 'A7T', 'A7B', 'A6B', 'A5B', 'A4B', 'A3B', 'A2B', 'A1B']
elif Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    NamesXTALSubDomains = ['C1T','C2T', 'C3T', 'C4T', 'C5T', 'C6T', 'C7T', 'C8T', 'C8B', 'C7B', 'C6B', 'C5B', 'C4B', 'C3B', 'C2B', 'C1B']
######################################################################
Modelinfo06    = (('CAE_File_name', 'RS_Loc_B_0'),
	     	     )
CAE_File_name, =  getInputs(fields = Modelinfo06, label = 'Enter CAE file name', dialogTitle = 'Modelinfo06: filenames', )
CAE_File_name  = str(CAE_File_name)
######################################################################
#Calculate the centre of the entire model
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
part.Set(faces = part.faces.findAt(((modelcentre_x, modelcentre_y, 0.),)), name = 'FullFace')
part.Set(edges = part.edges.findAt(((MLE_centre_x, MLE_centre_y,0.),)), name = 'FullEdge_x-')
part.Set(edges = part.edges.findAt(((MRE_centre_x, MRE_centre_y,0.),)), name = 'FullEdge_x+')
part.Set(edges = part.edges.findAt(((MBE_centre_x, MBE_centre_y,0.),)), name = 'FullEdge_y-')
part.Set(edges = part.edges.findAt(((MTE_centre_x, MTE_centre_y,0.),)), name = 'FullEdge_y+')
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
part.DatumPointByCoordinate(coords = (SPACER_left_centre_x, SPACER_left_centre_y, 0.0))
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
part.DatumPointByCoordinate(coords = (SPACER_right_centre_x, SPACER_right_centre_y, 0.0))
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
part.DatumPointByCoordinate(coords = (XTAL_Mat_centre_x, XTAL_Mat_centre_y, 0.0))
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
XTAL_Grains_XLOCS = np.arange(XtalMat_start_x, XtalMat_end_x, XTAL_dat_plane_x_incr) + XTAL_dat_plane_x_incr/2
######################################################################
# Create all the datum planes normal to peened surface in the sub-domains in the central XTAL domain.
# Of course, skip the XTAL start and XTAL end
xincr = XTAL_dat_plane_x_incr
for planenumx in range(1, NumXTALPartitions_x):
    xcoord = XTAL_Grains_XLOCS[planenumx]
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
DAT_plane_IND_Start = DatumPlaneIDs_y[DatPlnIDloc_y_start + (NumXTALSubDomains-1) + 1]
DAT_plane_IND_End   = DatumPlaneIDs_y[len(DatumPlaneIDs_y)-1]

ThisPlaneID = DAT_plane_IND_Start
xincr = XTAL_dat_plane_x_incr

#DatPlaneID_Count = DatPlnIDloc_y_start + (NumXTALSubDomains-1) + 1

for pointnumx in range(NumXTALPartitions_x):
    SD_centre_xcoord = XTAL_Grains_XLOCS[pointnumx]
    for pointnumy in range(NumXTALSubDomains):
        SD_centre_ycoord = (SubDomain_Start[pointnumy] + SubDomain_End[pointnumy])/2
        part.DatumPointByCoordinate(coords = (SD_centre_xcoord, SD_centre_ycoord, 0.0))
        if pointnumx<(len(range(NumXTALPartitions_x))-1):
            part.PartitionFaceByDatumPlane(datumPlane = part.datums[ThisPlaneID], faces = part.faces.findAt(((SD_centre_xcoord, SD_centre_ycoord, 0.), ), ))
        setname = 'XTAL_SubDomain_Nx_' + str(pointnumx) + '_Ny_' + str(pointnumy)
        part.Set(faces = part.faces.findAt(((SD_centre_xcoord, SD_centre_ycoord, 0.),)), name = setname)
    ThisPlaneID = ThisPlaneID + 1
######################################################################
######################################################################
# Load up default values for location B
Modelinfo08B = (('N_Grains_Y_loc_1 @B1T', '3'),
                ('N_Grains_Y_loc_2 @B2T', '3'),
                ('N_Grains_Y_loc_3 @B3T', '3'),
                ('N_Grains_Y_loc_4 @B4T', '3'),
                ('N_Grains_Y_loc_5 @B5T', '4'),
                ('N_Grains_Y_loc_6 @B6T', '4'),
                ('N_Grains_Y_loc_7 @B7T', '4'),
                ('N_Grains_Y_loc_8 @B8T', '5'),
                ('dummy', ':::'),
                ('N_Grains_Y_loc_8 @B8B', '5'),
                ('N_Grains_Y_loc_7 @B7B', '4'),
                ('N_Grains_Y_loc_6 @B6B', '4'),
                ('N_Grains_Y_loc_5 @B5B', '4'),
                ('N_Grains_Y_loc_4 @B4B', '3'),
                ('N_Grains_Y_loc_3 @B3B', '3'),
                ('N_Grains_Y_loc_2 @B2B', '3'),
                ('N_Grains_Y_loc_1 @B1B', '3'),
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
    SD_NGY_B = np.concatenate((SD_NGY_BT, SD_NGY_BB), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load up default valuyes for location A
Modelinfo08A = (('N_Grains_Y_loc_1 @A1T', '3'),
                ('N_Grains_Y_loc_2 @A2T', '3'),
                ('N_Grains_Y_loc_3 @A3T', '3'),
                ('N_Grains_Y_loc_4 @A4T', '3'),
                ('N_Grains_Y_loc_5 @A5T', '4'),
                ('N_Grains_Y_loc_6 @A6T', '4'),
                ('N_Grains_Y_loc_7 @A7T', '5'),
                ('dummy', ':::'),
                ('N_Grains_Y_loc_7 @A7B', '5'),
                ('N_Grains_Y_loc_6 @A6B', '4'),
                ('N_Grains_Y_loc_5 @A5B', '4'),
                ('N_Grains_Y_loc_4 @A4B', '3'),
                ('N_Grains_Y_loc_3 @A3B', '3'),
                ('N_Grains_Y_loc_2 @A2B', '3'),
                ('N_Grains_Y_loc_1 @A1B', '3'),
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
    SD_NGY_A = np.concatenate((SD_NGY_AT, SD_NGY_AB), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Load up default valuyes for location C
Modelinfo08C = (('N_Grains_Y_loc_1 @C1T', '3'),
                ('N_Grains_Y_loc_2 @C2T', '3'),
                ('N_Grains_Y_loc_3 @C3T', '3'),
                ('N_Grains_Y_loc_4 @C4T', '4'),
                ('N_Grains_Y_loc_5 @C5T', '4'),
                ('N_Grains_Y_loc_6 @C6T', '4'),
                ('N_Grains_Y_loc_7 @C7T', '5'),
                ('N_Grains_Y_loc_8 @C8T', '5'),
	     	    ('dummy', ':::'),
                ('N_Grains_Y_loc_8 @C8B', '5'),
                ('N_Grains_Y_loc_7 @C7B', '5'),
                ('N_Grains_Y_loc_6 @C6B', '4'),
                ('N_Grains_Y_loc_5 @C5B', '4'),
                ('N_Grains_Y_loc_4 @C4B', '4'),
                ('N_Grains_Y_loc_3 @C3B', '3'),
                ('N_Grains_Y_loc_2 @C2B', '3'),
                ('N_Grains_Y_loc_1 @C1B', '3'),
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
    SD_NGY_C = np.concatenate((SD_NGY_CT, SD_NGY_CB), axis = 1)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
