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
from abaqus import getInput
from math import sqrt
#number = float(getInput('Enter:'))
#print sqrt(number)
######################################################################
# ----------- Define constants  ------------
# Model origin MUST be 0,0
Model_origin_x = 0.
Model_origin_y = 0.

Model_enddim_x = 1
Model_enddim_y = 1

# anti - prime numbers: 
# 1, 2, 4, 6, 12, 24, 36, 48, 60, 120, 180
# 240, 360, 720, 840, 1260, 1680, 2520, 5040

TOTAL_NO_GRAINS = 1

NumPartitions_x = 1
NumPartitions_y = 1
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
Time_Step1_total_time   = 1.0
Time_Step1_initial_incr = 0.005
Time_Step1_minimum_incr = 1.01e-05
Time_Step1_maximum_incr = Time_Step1_total_time
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#ElementSize      = Model_enddim_y/NumPartitions_y
ElementSize       = 1
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#_______________________
MeshControlOption = 1 # Choose from the below
# MeshControlOption 1: QUAD Free, medial axis, minimize the mesh transitions yes
# MeshControlOption 2: QUAD Free, medial axis, minimize the mesh transitions no
# MeshControlOption 3: QUAD Free, advancing front
# MeshControlOption 4: QUAD Structured, minimize mesh transiion yes

# MeshControlOption 5: QUAD DOMINATED Free, medial axis
# MeshControlOption 6: QUAD DOMINATED Free, advancing front

# MeshControlOption 7: TRI free, use mapped meshing where appropriate yes
# MeshControlOption 8: TRI structured
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
#_______________________
ElementTypeOption = 1 # Choose from the below
# ElementTypeOption 01: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_default --- HGC_default
# ElementTypeOption 02: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_default --- HGC_enhanced
# ElementTypeOption 03: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_yes     --- HGC_default
# ElementTypeOption 04: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_yes     --- HGC_enhanced
# ElementTypeOption 05: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_no      --- HGC_default
# ElementTypeOption 06: LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_no      --- HGC_enhanced
#................................
# ElementTypeOption 07: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_default --- HGC_default
# ElementTypeOption 08: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_default --- HGC_enhanced
# ElementTypeOption 09: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_yes     --- HGC_default
# ElementTypeOption 10: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_yes     --- HGC_enhanced
# ElementTypeOption 11: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_no      --- HGC_default
# ElementTypeOption 12: LINEAR Quad --- RI_yes --- 2ndOA_yes --- DC_no      --- HGC_enhanced
#................................
# ElementTypeOption 13: LINEAR Quad --- RI_no
#................................
# ElementTypeOption 14: LINEAR tri --- 2ndOA_no --- DC_default
# ElementTypeOption 15: LINEAR tri --- 2ndOA_no --- DC_yes
#................................
# ElementTypeOption 16: LINEAR tri --- 2ndOA_yes --- DC_default
# ElementTypeOption 17: LINEAR tri --- 2ndOA_yes --- DC_yes
# ElementTypeOption 18: LINEAR tri --- 2ndOA_yes --- DC_no
#................................
# ElementTypeOption 19: QUADRATIC Quad --- RI_yes
# ElementTypeOption 20: QUADRATIC Quad --- RI_no
#................................
# ElementTypeOption 21: QUADRATIC tri --- MF_yes --- 2ndOA_no --- DC_default
# ElementTypeOption 22: QUADRATIC tri --- MF_yes --- 2ndOA_no --- DC_yes
# ElementTypeOption 23: QUADRATIC tri --- MF_yes --- 2ndOA_no --- DC_no
#................................
# ElementTypeOption 24: QUADRATIC tri --- MF_yes --- 2ndOA_yes --- DC_default
# ElementTypeOption 25: QUADRATIC tri --- MF_yes --- 2ndOA_yes --- DC_yes
# ElementTypeOption 26: QUADRATIC tri --- MF_yes --- 2ndOA_yes --- DC_no
#................................
# ElementTypeOption 27: QUADRATIC tri --- MF_no
######################################################################
DClengthRatio     = 0.100000001490116 # Dont change this for now.
#................................
# Set the total applied strain value
TotalStrain_x = 0.08;
######################################################################
# Calculate constants
Num_DatumPlanes_x   = NumPartitions_x - 1
Num_DatumPlanes_y   = NumPartitions_y - 1
Model_size_x        = Model_enddim_x  - Model_origin_x
Model_size_y        = Model_enddim_y  - Model_origin_y
dat_plane_x_incr    = Model_size_x    / (Num_DatumPlanes_x + 1)
dat_plane_y_incr    = Model_size_y    / (Num_DatumPlanes_y + 1)
FirstGrain_centre_x = Model_origin_x  + dat_plane_x_incr/2
FirstGrain_centre_y = Model_origin_y  + dat_plane_y_incr/2
modelcentre_x       = (Model_origin_x + Model_size_x)/2
modelcentre_y       = (Model_origin_y + Model_size_y)/2
# --------- left edge
LE_centre_x         = Model_origin_x
LE_centre_y         = (Model_origin_y + Model_enddim_y)/2
# --------- right edge
RE_centre_x         = Model_enddim_x
RE_centre_y         = LE_centre_y
# --------- bottom edge
BE_centre_x         = (Model_origin_x + Model_enddim_x)/2
BE_centre_y         = Model_origin_y
# --------- top edge
TE_centre_x         = (Model_origin_x + Model_enddim_x)/2
TE_centre_y         = Model_enddim_y
RE_Displacement     = TotalStrain_x   * Model_size_x
######################################################################
# simplify inputs stage 2
model = mdb.models['Model-1']
######################################################################
# make part
model.ConstrainedSketch(name = '__profile__', sheetSize = 1.0)
model.sketches['__profile__'].rectangle(point1 = (Model_origin_x, Model_origin_y), point2 = (Model_enddim_x, Model_enddim_y))
model.Part(dimensionality = TWO_D_PLANAR, name = 'partname', type = DEFORMABLE_BODY)
model.parts['partname'].BaseShell(sketch = mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
######################################################################
# simplify inputs stage 2
part  = model.parts['partname']
######################################################################
# Switch context
session.viewports['Viewport: 1'].setValues(displayedObject = part)
######################################################################
# import external modules
import numpy as np
######################################################################
# Create base sets
part.Set(faces    = part.faces.findAt(((modelcentre_x, modelcentre_y, 0.),)), name = 'FullFace')
part.Set(edges    = part.edges.findAt(((LE_centre_x, LE_centre_y,0.),)), name = 'FullEdge_x-')
part.Set(edges    = part.edges.findAt(((RE_centre_x, RE_centre_y,0.),)), name = 'FullEdge_x+')
part.Set(edges    = part.edges.findAt(((BE_centre_x, BE_centre_y,0.),)), name = 'FullEdge_y-')
part.Set(edges    = part.edges.findAt(((TE_centre_x, TE_centre_y,0.),)), name = 'FullEdge_y+')
part.Set(vertices = part.vertices.findAt(((Model_origin_x, Model_origin_y,0.),)), name = 'FullVertex_BL')
######################################################################
# define datum planes
count = 0
DatumPlaneIDs_y = []
for ii in range(1, Num_DatumPlanes_y + 1):
    if ii == 1:
		thisoffset = dat_plane_y_incr
		#print thisoffset
		count = count+1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = XZPLANE)
		DatumPlaneIDs_y.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_y_'+str(count))
		print 'I am making XZ datum plane number' + str(ii)
    else:
		thisoffset = thisoffset+dat_plane_y_incr
		#print thisoffset
		count = count+1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = XZPLANE)
		DatumPlaneIDs_y.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_y_'+str(count))
		print 'I am making XZ datum plane number' + str(ii)
######################################################################
# define datum planes
count = 0
DatumPlaneIDs_x = []
for ii in range(1, Num_DatumPlanes_x + 1):
    if ii == 1:
		thisoffset = dat_plane_x_incr
		#print thisoffset
		count  = count + 1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = YZPLANE)
		DatumPlaneIDs_x.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_x_'+str(count))
		print 'I am making YZ datum plane number' + str(ii)
    else:
		thisoffset = thisoffset+dat_plane_x_incr
		#print thisoffset
		count = count + 1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = YZPLANE)
		DatumPlaneIDs_x.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_x_'+str(count))
		print 'I am making YZ datum plane number' + str(ii)
######################################################################
# partition using datum planes parallel to xz planes
# create set names
for ii in range(1, Num_DatumPlanes_y + 1):
	TheID = DatumPlaneIDs_y[ii-1]
	xloc = FirstGrain_centre_x
	yloc = FirstGrain_centre_y + (ii-1)*dat_plane_y_incr
	#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
	part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))

# partition using datum planes parallel to yz planes
partitioncount = 1
for jj in range(1, Num_DatumPlanes_y + 2):
	for ii in range(1, Num_DatumPlanes_x + 1):
		TheID_x = DatumPlaneIDs_x[ii-1]
		xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
		yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
		#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
		part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID_x], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
		setname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
		part.Set(faces = part.faces.findAt(((xloc, yloc, 0.),)), name = setname)
		print 'Creating partion number' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_partitions'
		partitioncount = partitioncount + 1

for jj in range(1, Num_DatumPlanes_y + 2):
	ii = Num_DatumPlanes_x + 1
	xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
	yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
	#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
	setname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
	part.Set(faces = part.faces.findAt(((xloc, yloc, 0.),)), name = setname)
	print 'Creating partion number' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_partitions'
	partitioncount = partitioncount + 1
######################################################################
# Create materials
# Create sections
# Assign sections
partitioncount = 1
for jj in range(1, Num_DatumPlanes_y + 2):
	for ii in range(1, Num_DatumPlanes_x + 1):
		# create materials
		matsetname = 'Mat_Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
		model.Material(name = matsetname)
		model.materials[matsetname].UserMaterial(mechanicalConstants = (0.0, ))
		# create section
		secsetname = 'Sec_Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
		model.HomogeneousSolidSection(material = matsetname, name = secsetname, thickness = None)
		# assign section
		grainsetname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
		part.SectionAssignment(offset = 0.0, offsetField = '', offsetType = MIDDLE_SURFACE, region = 
			part.sets[grainsetname], sectionName = secsetname, thicknessAssignment = FROM_SECTION)
		print 'Creating material, section and assigning section to grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
		partitioncount = partitioncount + 1
for jj in range(1, Num_DatumPlanes_y + 2):
	ii = Num_DatumPlanes_x + 1
	# create materials
	matsetname = 'Mat_Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
	model.Material(name = matsetname)
	model.materials[matsetname].UserMaterial(mechanicalConstants = (0.0, ))
	# create section
	secsetname = 'Sec_Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
	model.HomogeneousSolidSection(material = matsetname, name = secsetname, thickness = None)
	# assign section
	grainsetname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
	part.SectionAssignment(offset = 0.0, offsetField = '', offsetType = MIDDLE_SURFACE, region = 
		part.sets[grainsetname], sectionName = secsetname, thicknessAssignment = FROM_SECTION)
	print 'Creating material, section and assigning section to grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
	partitioncount = partitioncount + 1
######################################################################
# Create assembly
model.rootAssembly.DatumCsysByDefault(CARTESIAN)
model.rootAssembly.Instance(dependent=ON, name='partname-1', part=mdb.models['Model-1'].parts['partname'])
######################################################################
# Create time steps
model.StaticStep(initialInc=Time_Step1_initial_incr, maxInc=Time_Step1_maximum_incr, minInc=Time_Step1_minimum_incr, 
    name='Step-1', nlgeom=ON, previous='Initial', timePeriod=Time_Step1_total_time)
######################################################################
model = mdb.models['Model-1']
######################################################################
# Apply displacement boundary conditions
# for the constrained edge
model.DisplacementBC(amplitude = UNSET, createStepName = 'Initial', distributionType = UNIFORM, fieldName = '', localCsys = None, name = 
    'BC_constrained_x-', region = model.rootAssembly.instances['partname-1'].sets['FullEdge_x-'], u1 = SET, u2=SET, ur3=SET)
######################################################################
# Apply displacement boundary conditions
# for the pulled/pushed edge
model.DisplacementBC(amplitude = UNSET, createStepName = 'Step-1', distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name = 
    'BC_displaced_x_+', region = model.rootAssembly.instances['partname-1'].sets['FullEdge_x+'] , u1 = RE_Displacement, u2 = UNSET, ur3 = UNSET)
######################################################################
# Set element type
# Assign mesh controls
# set element seed length - global
partitioncount = 1
for jj in range(1, Num_DatumPlanes_y + 2):
	for ii in range(1, Num_DatumPlanes_x + 1):
		TheID_x = DatumPlaneIDs_x[ii-1]
		xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
		yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
		# Set element type
		if ElementTypeOption == 1:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 2:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=ENHANCED, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 3:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 4:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=ENHANCED, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 5:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=DEFAULT, distortionControl=OFF), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 6:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=ENHANCED, distortionControl=OFF), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 7:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 8:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=ENHANCED, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 9:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 10:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=ENHANCED, distortionControl=ON,lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 11:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=DEFAULT, distortionControl=OFF), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 12:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=ENHANCED, distortionControl=OFF), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 13:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 14:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
				hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 15:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
				elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
				distortionControl=ON, lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 16:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 17:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=ON, 
				lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 18:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=OFF)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 19:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 20:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 21:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 22:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=ON, 
				lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 23:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=OFF)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 24:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=DEFAULT)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 25:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=ON, 
				lengthRatio=DClengthRatio, elemDeletion=ON)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 26:
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
				elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=OFF)), 
				regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
		elif ElementTypeOption == 27: # ElementTypeOption 27: QUADRATIC tri --- MF_no
			part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6, 
				elemLibrary=STANDARD)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	    # Assign mesh controls
		if MeshControlOption == 1:   part.setMeshControls(algorithm     = MEDIAL_AXIS    , regions = part.faces.findAt(((xloc, yloc, 0.),)))
		elif MeshControlOption == 2: part.setMeshControls(minTransition = OFF            , regions = part.faces.findAt(((xloc, yloc, 0.),)))
		elif MeshControlOption == 3: part.setMeshControls(elemShape     = QUAD           , regions = part.faces.findAt(((xloc, yloc, 0.),)))
		elif MeshControlOption == 4: part.setMeshControls(minTransition = ON             , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = STRUCTURED)
		elif MeshControlOption == 5: part.setMeshControls(elemShape     = QUAD_DOMINATED , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = FREE)
		elif MeshControlOption == 6: part.setMeshControls(algorithm     = ADVANCING_FRONT, regions = part.faces.findAt(((xloc, yloc, 0.),)))
		elif MeshControlOption == 7: part.setMeshControls(elemShape     = TRI            , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = FREE)
		elif MeshControlOption == 8: part.setMeshControls(elemShape=TRI                  , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = STRUCTURED)
		
		print 'Setting element type and mesh controls for grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
		partitioncount = partitioncount + 1
for jj in range(1, Num_DatumPlanes_y + 2):
	ii = Num_DatumPlanes_x + 1
	xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
	yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
	# Set element type
	if ElementTypeOption == 1:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 2:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=ENHANCED, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 3:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 4:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=ENHANCED, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 5:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=DEFAULT, distortionControl=OFF), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 6:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=ENHANCED, distortionControl=OFF), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 7:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 8:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=ENHANCED, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 9:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=DEFAULT, distortionControl=ON, lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 10:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=ENHANCED, distortionControl=ON,lengthRatio=DClengthRatio), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 11:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=DEFAULT, distortionControl=OFF), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 12:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=ENHANCED, distortionControl=OFF), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 13:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 14:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=ON, 
			hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=DEFAULT)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 15:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			hourglassControl=DEFAULT, distortionControl=DEFAULT), ElemType(
			elemCode=CPS3, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
			distortionControl=ON, lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 16:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 17:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=ON, 
			lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 18:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS4R, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=OFF)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 19:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 20:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 21:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 22:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=ON, 
			lengthRatio=DClengthRatio)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 23:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=OFF, distortionControl=OFF)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 24:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=DEFAULT)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 25:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=ON, 
			lengthRatio=DClengthRatio, elemDeletion=ON)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 26:
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6M, 
			elemLibrary=STANDARD, secondOrderAccuracy=ON, distortionControl=OFF)), 
			regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	elif ElementTypeOption == 27: # ElementTypeOption 27: QUADRATIC tri --- MF_no
		part.setElementType(elemTypes=(ElemType(elemCode=CPS8R, elemLibrary=STANDARD), ElemType(elemCode=CPS6, 
			elemLibrary=STANDARD)), regions=(part.faces.findAt(((xloc, yloc, 0.),)), ))
	# Assign mesh controls
	if   MeshControlOption == 1: part.setMeshControls(algorithm     = MEDIAL_AXIS    , regions = part.faces.findAt(((xloc, yloc, 0.),)))
	elif MeshControlOption == 2: part.setMeshControls(minTransition = OFF            , regions = part.faces.findAt(((xloc, yloc, 0.),)))
	elif MeshControlOption == 3: part.setMeshControls(elemShape     = QUAD           , regions = part.faces.findAt(((xloc, yloc, 0.),)))
	elif MeshControlOption == 4: part.setMeshControls(minTransition = ON             , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = STRUCTURED)
	elif MeshControlOption == 5: part.setMeshControls(elemShape     = QUAD_DOMINATED , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = FREE)
	elif MeshControlOption == 6: part.setMeshControls(algorithm     = ADVANCING_FRONT, regions = part.faces.findAt(((xloc, yloc, 0.),)))
	elif MeshControlOption == 7: part.setMeshControls(elemShape     = TRI            , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = FREE)
	elif MeshControlOption == 8: part.setMeshControls(elemShape     = TRI            , regions = part.faces.findAt(((xloc, yloc, 0.),)), technique = STRUCTURED)
	print 'Setting element type and mesh controls for grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
	partitioncount = partitioncount + 1
	
# set element seed length - global
part.seedPart(deviationFactor = 0.1, minSizeFactor = 0.1, size = ElementSize)
######################################################################
# Mesh the individual faces
TOTAL_NUM_GRAINS = 0
partitioncount = 1
for jj in range(1, Num_DatumPlanes_y + 2):
	for ii in range(1, Num_DatumPlanes_x + 1):
		TheID_x = DatumPlaneIDs_x[ii-1]
		xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
		yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
		part.generateMesh(regions = part.faces.findAt(((xloc, yloc, 0.),)))
		TOTAL_NUM_GRAINS = TOTAL_NUM_GRAINS + 1
		print 'Meshing grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
		partitioncount = partitioncount + 1
for jj in range(1, Num_DatumPlanes_y + 2):
	ii = Num_DatumPlanes_x + 1
	xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
	yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
	part.generateMesh(regions = part.faces.findAt(((xloc, yloc, 0.),)))
	TOTAL_NUM_GRAINS = TOTAL_NUM_GRAINS + 1
	print 'Meshing grain_' + str(partitioncount) + '_of_' + str(TOTAL_NO_GRAINS) + '_grains'
	partitioncount = partitioncount + 1
######################################################################
# Save the CAE files to hard disk
folder1 = 'C:\Temp\CalibrationModels\CalibrationModelCAE_File_Repository\_'
CAEname1 = 'CBmodal' # Check Board Model
CAEname2 = '_' + str(NumPartitions_x*NumPartitions_y)
CAEname3 = '_' + 'Ngx_' + str(NumPartitions_x)
CAEname4 = '_' + 'Ngy_' + str(NumPartitions_y)
CAEname5 = '_' + 'MCO_' + str(MeshControlOption)
CAEname6 = '_' + 'ETO_' + str(ElementTypeOption)
CAEname7 = '_' + 'ETO_' + str(ElementSize)
CAEFILENAME = CAEname1 + CAEname2 + CAEname3 + CAEname4 + CAEname5 + CAEname6 + CAEname7
PathName_FileName = folder1 + CAEFILENAME
import os.path
import sys
if os.path.isfile(PathName_FileName + '.cae'):
	print 'The file with same parameters already exists'
	print 'I am not saving it'
	print 'Please find the file with the following line2 cae and jnl names in the following line 1 folder'
	print 'line 1:   ' + folder1[:-2]
	print 'line 2a:   ' + CAEFILENAME + '.cae'
	print 'line 2b:   ' + CAEFILENAME + '.jnl'
	print 'END OF CHECKERBOARD MODEL GENERATION'
	print '______________________________________'
	print '______________________________________'
else:
	print '______________________________________'
	print 'Copying the files to grain structure repository'
	mdb.saveAs(PathName_FileName)
	print 'Files____' + CAEFILENAME + '.cae' + '____and____' + CAEFILENAME + '.jnl' '____have been saved in the folder:'
	print folder1[:-2]
	print 'END OF CHECKERBOARD MODEL GENERATION'
	print '______________________________________'

if os.path.isfile(CAEFILENAME + '.cae'):
	print 'The file with same parameters already exists'
	print 'I am not saving it'
	print 'Please find the file with the following line2 cae and jnl names in the following line 1 folder'
	print 'line 1:   ' + os.getcwd()
	print 'line 2a:   ' + CAEFILENAME + '.cae'
	print 'line 2b:   ' + CAEFILENAME + '.jnl'
	print 'END OF CHECKERBOARD MODEL GENERATION'
	print '______________________________________'
else:
	print '______________________________________'
	mdb.saveAs(CAEFILENAME)
	print 'Files____' + CAEFILENAME + '.cae' + '____and____' + CAEFILENAME + '.jnl' '____have been saved in the folder:'
	print os.getcwd()
	print 'END OF CHECKERBOARD MODEL GENERATION'
	print '______________________________________'
######################################################################
mdb.models['Model-1'].rootAssembly.regenerate()
instance = model.rootAssembly.instances['partname-1']
TotalNumOfNodes = len(instance.nodes)
TotalNumOfElem  = len(instance.elements)
FindDOF = 1

#if FindDOF==1:
#	if str(instance.elements[1].type)=='CPS4R' or str(instance.elements[1].type)=='CPS4':
#		Total_DOF = TotalNumOfNodes*4
#	elif str(instance.elements[1].type)=='CPS8R' or str(instance.elements[1].type)=='CPS8':
#		Total_DOF = TotalNumOfNodes*8
#	print('The model has %d Elements -- & -- %d Nodes --- %d Ds.O.F'% (TotalNumOfElem, TotalNumOfNodes, Total_DOF))
#else:
print('The model has %d Elements -- & -- %d Nodes'% (TotalNumOfElem, TotalNumOfNodes))
######################################################################
#mdb.Job(atTime=None, contactPrint=OFF, description='thejobdescription', 
#   echoPrint=OFF, explicitPrecision=SINGLE, getMemoryFromAnalysis=True, 
#    historyPrint=OFF, memory=90, memoryUnits=PERCENTAGE, model='Model-1', 
#    modelPrint=OFF, multiprocessingMode=DEFAULT, name='TheJob123', 
#    nodalOutputPrecision=SINGLE, numCpus=1, numGPUs=0, queue=None, 
#    resultsFormat=ODB, scratch='', type=ANALYSIS, userSubroutine='', waitHours=
#    0, waitMinutes=0)
######################################################################
# HERE I GIVE DETAILS OF PARAMETERS USED FOR CORRESPONDING CALIBRATION ITERATIONS
# ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~
#                  CALIBRATION 01
#_______
# No. of grains     = 120    
# NumPartitions_y   = 7
#_______
# MeshControlOption = 1 # QUAD Free, medial axis, minimize the mesh transitions yes
# ElementTypeOption = 1 # LINEAR Quad --- RI_yes --- 2ndOA_no --- DC_default --- HGC_default
# Element size      = 2
# ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~ + ~
######################################################################