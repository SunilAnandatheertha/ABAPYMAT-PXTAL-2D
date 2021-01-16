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
# Define constants
# Model origin MUST be 0,0
Modelinfo01 = (('Model_origin_x [allways 0]', '0'),
               ('Model_origin_y [allways 0]', '0'),
               ('Model_enddim_x', '120.0'),
	           ('Model_enddim_y', '5.0'),
               ('XtalMat_start_x','35'),
	     	  )
Model_origin_x, Model_origin_y, Model_enddim_x, Model_enddim_y, XtalMat_start_x\
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
SPACER_left_Mat_end_y   = Model_origin_y
SPACER_left_Mat_size_x  = SPACER_left_Mat_end_x - SPACER_left_Mat_start_x
SPACER_left_Mat_size_y  = Model_origin_y

XtalMat_start_x = float(XtalMat_start_x)
XtalMat_start_y = Model_origin_y
XtalMat_end_x   = Model_enddim_x - XtalMat_start_x
XtalMat_end_y   = Model_origin_y
XtalMat_size_x  = XtalMat_end_x - XtalMat_start_x
XtalMat_size_y  = Model_origin_y

SPACER_right_Mat_start_x = XtalMat_end_x
SPACER_right_Mat_start_y = Model_origin_y
SPACER_right_Mat_end_x   = Model_origin_x + Model_enddim_x
SPACER_right_Mat_end_x   = Model_origin_y
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
# ------------------------------------------------------------
# LOCATION - A
Modelinfo05bAS = (('A1.T: Sub-Domain start, mm', '0.00'), ('A2.T: Sub-Domain start    ', '0.06'), ('A3.T: Sub-Domain start    ', '0.15'), ('A4.T: Sub-Domain start    ', '0.25'),
                  ('A5.T: Sub-Domain start    ', '0.40'), ('A6.T: Sub-Domain start    ', '0.75'), ('A7.T: Sub-Domain start    ', '1.20'),
                  ('dummy', '::::'),
                  ('A7.B: Sub-Domain start    ', '2.50'), ('A6.B: Sub-Domain start    ', '3.80'), ('A5.B: Sub-Domain start    ', '4.25'), ('A4.B: Sub-Domain start    ', '4.60'),
                  ('A3.B: Sub-Domain start    ', '4.75'), ('A2.B: Sub-Domain start    ', '4.85'), ('A1.B: Sub-Domain start    ', '4.94'),
                 )
if Sample_Location[0] in ['B', 'A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
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
Modelinfo05bAE = (('A1.T: Sub-Domain end, mm', '0.06'), ('A2.T: Sub-Domain end'    , '0.15'), ('A3.T: Sub-Domain end'    , '0.25'), ('A4.T: Sub-Domain end'    , '0.40'),
                  ('A5.T: Sub-Domain end'    , '0.75'), ('A6.T: Sub-Domain end'    , '1.20'), ('A7.T: Sub-Domain end'    , '2.50'),
                  ('Adummy', '::::'),
                  ('A7.B: Sub-Domain end    ', '3.80'), ('A6.B: Sub-Domain end    ', '4.25'), ('A5.B: Sub-Domain end    ', '4.60'), ('A4.B: Sub-Domain end    ', '4.75'),
                  ('A3.B: Sub-Domain end    ', '4.85'), ('A2.B: Sub-Domain end    ', '4.94'), ('A1.B: Sub-Domain end    ', '5.00'),
 	     	     )
if Sample_Location[0] in ['B', 'A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
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
# ------------------------------------------------------------
# LOCATION - C
Modelinfo05bCS = (('C1.T: Sub-Domain start, mm', '0.00'), ('C2.T: Sub-Domain start    ', '0.06'), ('C3.T: Sub-Domain start    ', '0.15'), ('C4.T: Sub-Domain start    ', '0.25'),
                  ('C5.T: Sub-Domain start    ', '0.50'), ('C6.T: Sub-Domain start    ', '0.70'), ('C7.T: Sub-Domain start    ', '1.30'), ('C8.T: Sub-Domain start    ', '1.80'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain start, mm', '2.50'), ('C7.B: Sub-Domain start    ', '3.20'), ('C6.B: Sub-Domain start    ', '3.70'), ('C5.B: Sub-Domain start    ', '4.30'),
                  ('C4.B: Sub-Domain start    ', '4.50'), ('C3.B: Sub-Domain start    ', '4.75'), ('C2.B: Sub-Domain start    ', '4.85'), ('C1.B: Sub-Domain start    ', '4.94'),
                 )
if Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
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
Modelinfo05bCE = (('C1.T: Sub-Domain end, mm', '0.06'), ('C2.T: Sub-Domain end'    , '0.15'), ('C3.T: Sub-Domain end'    , '0.25'), ('C4.T: Sub-Domain end'    , '0.50'),
                  ('C5.T: Sub-Domain end'    , '0.70'), ('C6.T: Sub-Domain end'    , '1.30'), ('C7.T: Sub-Domain end'    , '1.80'), ('C8.T: Sub-Domain end'    , '2.50'),
                  ('dummy', '::::'),
                  ('C8.B: Sub-Domain end, mm', '3.20'), ('C7.B: Sub-Domain end    ', '3.70'), ('C6.B: Sub-Domain end    ', '4.30'), ('C5.B: Sub-Domain end    ', '4.50'),
                  ('C4.B: Sub-Domain end    ', '4.75'), ('C3.B: Sub-Domain end    ', '4.85'), ('C2.B: Sub-Domain end    ', '4.94'), ('C1.B: Sub-Domain end    ', '5.00'),
 	     	     )
if Sample_Location[0] in ['B', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
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

######################################################################
# Load up default values for location B
Modelinfo05cB = (('epsilon_topedge_depth_loc_1 @B1.TE', '0.040'),
                 ('epsilon_topedge_depth_loc_2 @B2.TE', '0.035'),
                 ('epsilon_topedge_depth_loc_3 @B3.TE', '0.030'),
                 ('epsilon_topedge_depth_loc_4 @B4.TE', '0.020'),
                 ('epsilon_topedge_depth_loc_5 @B5.TE', '0.010'),
                 ('epsilon_topedge_depth_loc_6 @B6.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @B7.TE', ''),
                 ('epsilon_topedge_depth_loc_8 @B8.TE', ''),
 	     	    )
# Load up default valuyes for location A
Modelinfo05cA = (('epsilon_topedge_depth_loc_1 @A1.TE', '0.040'),
                 ('epsilon_topedge_depth_loc_2 @A2.TE', '0.035'),
                 ('epsilon_topedge_depth_loc_3 @A3.TE', '0.030'),
                 ('epsilon_topedge_depth_loc_4 @A4.TE', '0.020'),
                 ('epsilon_topedge_depth_loc_5 @A5.TE', '0.010'),
                 ('epsilon_topedge_depth_loc_6 @A6.TE', ''),
                 ('epsilon_topedge_depth_loc_7 @A7.TE', ''),
	     	    )
# Load up default valuyes for location C
Modelinfo05cC = (('epsilon_topedge_depth_loc_1', '0.040'),
                 ('epsilon_topedge_depth_loc_2', '0.035'),
                 ('epsilon_topedge_depth_loc_3', '0.030'),
                 ('epsilon_topedge_depth_loc_4', '0.020'),
                 ('epsilon_topedge_depth_loc_5', '0.010'),
                 ('epsilon_topedge_depth_loc_6', ''),
                 ('epsilon_topedge_depth_loc_7', ''),
                 ('epsilon_topedge_depth_loc_8', ''),
	     	    )
######################################################################
# Ask for user inputs
if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b']:
    epsilon_topedge_depth_loc_1, epsilon_topedge_depth_loc_2, epsilon_topedge_depth_loc_3, epsilon_topedge_depth_loc_4,\
    epsilon_topedge_depth_loc_5, epsilon_topedge_depth_loc_6, epsilon_topedge_depth_loc_7, epsilon_topedge_depth_loc_8\
     =  getInputs(fields = Modelinfo05b,\
                  label = 'Enter depth wise strain @ subdomain TopEdge ('-' if edge is free)',\
                  dialogTitle = 'Modelinfo05: BC @ loc-B @ B1.to.B8 @TopEdge', )
elif Sample_Location[0] in ['A', 'a', 'LocA', 'Loc_A', 'loca', 'loc_a']:
    epsilon_topedge_depth_loc_1, epsilon_topedge_depth_loc_2, epsilon_topedge_depth_loc_3, epsilon_topedge_depth_loc_4,\
    epsilon_topedge_depth_loc_5, epsilon_topedge_depth_loc_6, epsilon_topedge_depth_loc_7\
     =  getInputs(fields = Modelinfo05b,\
                  label = 'Enter depth wise strain @ subdomain TopEdge ('' if edge is free)',\
                  dialogTitle = 'Modelinfo05: BC @ loc-A @ A1.to.A7 @TopEdge', )
elif Sample_Location[0] in ['C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    epsilon_topedge_depth_loc_1, epsilon_topedge_depth_loc_2, epsilon_topedge_depth_loc_3, epsilon_topedge_depth_loc_4,\
    epsilon_topedge_depth_loc_5, epsilon_topedge_depth_loc_6, epsilon_topedge_depth_loc_7, epsilon_topedge_depth_loc_8\
     =  getInputs(fields = Modelinfo05b,\
                  label = 'Enter Boun. Cond. details',\
                  dialogTitle = 'Modelinfo05: Boundary conditions', )
######################################################################
epsilon_topedge_depth_loc_1 = float(epsilon_topedge_depth_loc_1)
epsilon_topedge_depth_loc_2 = float(epsilon_topedge_depth_loc_2)
epsilon_topedge_depth_loc_3 = float(epsilon_topedge_depth_loc_3)
epsilon_topedge_depth_loc_4 = float(epsilon_topedge_depth_loc_4)
epsilon_topedge_depth_loc_5 = float(epsilon_topedge_depth_loc_5)
epsilon_topedge_depth_loc_6 = float(epsilon_topedge_depth_loc_6)
epsilon_topedge_depth_loc_7 = float(epsilon_topedge_depth_loc_7)

if Sample_Location[0] in ['B', 'b', 'LocB', 'Loc_B', 'locb', 'loc_b', 'C', 'c', 'LocC', 'Loc_C', 'locc', 'loc_c']:
    epsilon_topedge_depth_loc_8 = float(epsilon_topedge_depth_loc_8)

ApplyStrain_XTALdepth =
######################################################################
Modelinfo06 = (('CAE_File_name', 'RS_Loc_B_0'),
	     	  )
CAE_File_name,\
 =  getInputs(fields = Modelinfo06, label = 'Enter CAE file name', dialogTitle = 'Modelinfo06: filenames', )
CAE_File_name = str(CAE_File_name)
######################################################################
#Model_origin_x  = float(Model_origin_x)#
#Model_origin_y  = float(Model_origin_y)#
#Model_enddim_x  = float(Model_enddim_x)#
#Model_enddim_y  = float(Model_enddim_y)#

modelcentre_x   = (Model_origin_x + Model_size_x)/2
modelcentre_y   = (Model_origin_y + Model_size_y)/2
#------------------
#SPACER_left_Mat_start_x = Model_origin_x#
#SPACER_left_Mat_start_y = Model_origin_y#
#SPACER_left_Mat_end_x   = float(XtalMat_start_x)#
#SPACER_left_Mat_end_y   = Model_origin_y#
#SPACER_left_Mat_size_x  = SPACER_left_Mat_end_x - SPACER_left_Mat_start_x#
#SPACER_left_Mat_size_y  = Model_origin_y#

SPACER_left_centre_x    = (SPACER_left_Mat_start_x + SPACER_left_Mat_end_x)/2
SPACER_left_centre_y    = (SPACER_left_Mat_start_y + SPACER_left_Mat_end_y)/2

SPACER_left_dat_plane_x_incr = SPACER_left_Mat_size_x / (Num_SPACER_DatumPlanes_x + 1)
SPACER_left_dat_plane_y_incr = SPACER_left_Mat_size_y / (Num_SPACER_DatumPlanes_y + 1)

SPACER_left_1st_partition_centre_x = SPACER_left_Mat_start_x + SPACER_left_dat_plane_x_incr/2
SPACER_left_1st_partition_centre_y = SPACER_left_Mat_start_y + SPACER_left_dat_plane_y_incr/2
#------------------
#XtalMat_start_x = float(XtalMat_start_x)#
#XtalMat_start_y = Model_origin_y#
#XtalMat_end_x   = Model_enddim_x - XtalMat_start_x#
#XtalMat_end_y   = Model_origin_y#
#XtalMat_size_x  = XtalMat_end_x - XtalMat_start_x#
#XtalMat_size_y  = Model_origin_y#
if Sample_Location_Flag_ID.lower in ['b', 'locb', 'loc_b']:

elif Sample_Location_Flag_ID.lower in ['a', 'loca', 'loc_a']:
elif Sample_Location_Flag_ID.lower in ['c', 'locc', 'loc_c']:


XTAL_Mat_centre_x    = (XtalMat_start_x + XtalMat_end_x)/2
XTAL_Mat_centre_y    = (XtalMat_start_y + XtalMat_end_y)/2

XTAL_dat_plane_x_incr = XtalMat_size_x / (Num_XTAL_DatumPlanes_x + 1)
XTAL_dat_plane_y_incr = XtalMat_size_y / (Num_XTAL_DatumPlanes_y + 1)

FirstGrain_centre_x = XtalMat_start_x + XTAL_dat_plane_x_incr/2
FirstGrain_centre_y = XtalMat_start_Y + XTAL_dat_plane_y_incr/2
#------------------
#SPACER_right_Mat_start_x = XtalMat_end_x#
#SPACER_right_Mat_start_y = Model_origin_y#
#SPACER_right_Mat_end_x   = Model_origin_x + Model_enddim_x#
#SPACER_right_Mat_end_y   = Model_origin_y#
#SPACER_right_Mat_size_x  = SPACER_right_Mat_end_x - SPACER_right_Mat_start_x#
#SPACER_right_Mat_size_y  = Model_enddim_y#

SPACER_right_centre_x    = (SPACER_right_Mat_start_x + SPACER_right_Mat_end_x)/2
SPACER_right_centre_y    = (SPACER_right_Mat_start_y + SPACER_right_Mat_end_y)/2

SPACER_right_dat_plane_x_incr = SPACER_right_Mat_size_x / (Num_SPACER_DatumPlanes_x + 1)
SPACER_right_dat_plane_y_incr = SPACER_right_Mat_size_y / (Num_SPACER_DatumPlanes_y + 1)

SPACER_right_1st_partition_centre_x = SPACER_right_Mat_start_x + SPACER_right_dat_plane_x_incr/2
SPACER_right_1st_partition_centre_y = SPACER_right_Mat_start_y + SPACER_right_dat_plane_y_incr/2
#------------------
######################################################################

# left edge
LE_centre_x = Model_origin_x
LE_centre_y = (Model_origin_y + Model_enddim_y)/2
# right edge
RE_centre_x = Model_enddim_x
RE_centre_y = LE_centre_y
# bottom edge
BE_centre_x = (Model_origin_x + Model_enddim_x)/2
BE_centre_y = Model_origin_y
# top edge
TE_centre_x = (Model_origin_x + Model_enddim_x)/2
TE_centre_y = Model_enddim_y

RE_Displacement = TotalStrain_x*Model_size_x
######################################################################
