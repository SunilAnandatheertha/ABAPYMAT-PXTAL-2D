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
# Define constants
# Model origin MUST be 0,0
Modelinfo01 = (('Model_origin_x', '0'),
               ('Model_origin_y', '0'),
               ('Model_enddim_x', '100.0'),
	           ('Model_enddim_y', '6.0'),
	     	  )
Model_origin_x, Model_origin_y, Model_enddim_x, Model_enddim_y,\
 =  getInputs(fields = Modelinfo01, label = 'Model position and size', dialogTitle = 'Modelinfo01: Location and size', )
Model_origin_x = float(Model_origin_x)
Model_origin_y = float(Model_origin_y)
Model_enddim_x = float(Model_enddim_x)
Model_enddim_y = float(Model_enddim_y)
#Model_origin_x = 0.
#Model_origin_y = 0.
#Model_enddim_x = 100.0
#Model_enddim_y = 6.0
######################################################################
# anti - prime numbers:
# 1, 2, 4, 6, 12, 24, 36, 48, 60, 120, 180
# 240, 360, 720, 840, 1260, 1680, 2520, 5040
Modelinfo02 = (('NumPartitions_x', '96'),
               ('NumPartitions_y', '2'),
               ('NumPartitions_total', '192'),
	     	  )
NumPartitions_x, NumPartitions_y, NumPartitions_total,\
 =  getInputs(fields = Modelinfo02, label = 'CHK grain structure info', dialogTitle = 'Modelinfo02: Partitioning details', )
NumPartitions_x     = int(NumPartitions_x)
NumPartitions_y     = int(NumPartitions_y)
NumPartitions_total = int(NumPartitions_total)
#NumPartitions_x  = 48
#NumPartitions_y  = 4
######################################################################
Num_DatumPlanes_x = NumPartitions_x - 1
Num_DatumPlanes_y = NumPartitions_y - 1
######################################################################
Modelinfo03 = (('Time_Step1_total_time', '1'),
               ('Time_Step1_initial_incr', '0.005'),
               ('Time_Step1_minimum_incr', '1.01e-05'),
               ('Time_Step1_maximum_incr', '0.05'),
	     	  )
Time_Step1_total_time, Time_Step1_initial_incr, Time_Step1_minimum_incr, Time_Step1_maximum_incr,\
 =  getInputs(fields = Modelinfo03, label = 'Time stepping details', dialogTitle = 'Modelinfo03', )
Time_Step1_total_time   = float(Time_Step1_total_time)
Time_Step1_initial_incr = float(Time_Step1_initial_incr)
Time_Step1_minimum_incr = float(Time_Step1_minimum_incr)
Time_Step1_maximum_incr = float(Time_Step1_maximum_incr)
#Time_Step1_total_time   = 1.0
#Time_Step1_initial_incr = 0.005
#Time_Step1_minimum_incr = 1.01e-05
#Time_Step1_maximum_incr = Time_Step1_total_time
######################################################################
Modelinfo04 = (('ElementFactor', '1'),
               ('ElementTypeFlagID: 1: CPS4R-or-CPS3...2: CPS8-or-CPS6M...3: CPS4-or-CPS3...4: CPS8R-or-CPS6M...5: CPS8R-or-CPS6', '5'),
               ('ElementShapeFlagID: 1: Quad-structured...2: Quad-free...3: Tri-Structured...4: Tri-Free', '4'),
	     	  )
factor, ElementTypeFlagID, ElementShapeFlagID,\
=  getInputs(fields = Modelinfo04, label = 'Enter element details', dialogTitle = 'Modelinfo04: FE details', )
factor             = float(factor)
ElementTypeFlagID  = int(ElementTypeFlagID)
ElementShapeFlagID = int(ElementShapeFlagID)
#factor = 1
#ElementTypeFlagID  = 5 #1: CPS4R-or-CPS3\\\\\2: CPS8-or-CPS6M\\\\\3: CPS4-or-CPS3\\\\\4: CPS8R-or-CPS6M\\\\\5: CPS8R-or-CPS6
#ElementShapeFlagID = 4 #1: Quad-structured\\\\\2: Quad-free\\\\\3: Tri-Structured\\\\\4: Tri-Free
ElementSize   = (Model_enddim_y/NumPartitions_y)/factor
######################################################################
Modelinfo05 = (('TotalStrain_x', '0.04'),
	     	  )
TotalStrain_x,\
 =  getInputs(fields = Modelinfo05, label = 'Enter Boun. Cond. details', dialogTitle = 'Modelinfo05: Boundary conditions', )
TotalStrain_x = float(TotalStrain_x)
#TotalStrain_x = 0.04;
######################################################################
Modelinfo06 = (('CAE_File_name', ''),
	     	  )
CAE_File_name,\
 =  getInputs(fields = Modelinfo06, label = 'Enter CAE file name', dialogTitle = 'Modelinfo06: filenames', )
CAE_File_name = str(CAE_File_name)
######################################################################
#mdb.saveAs(pathName = 'C:\Temp\CalibrationModels\Location A\Cal_48ng\Ng_'+str(NumPartitions_x*NumPartitions_y)+'_'+'Ngx_'+str(NumPartitions_x)+'_'+'Ngy_'+str(NumPartitions_y))
######################################################################
# Calculate constants
Model_size_x = Model_enddim_x - Model_origin_x
Model_size_y = Model_enddim_y - Model_origin_y

dat_plane_x_incr = Model_size_x / (Num_DatumPlanes_x + 1)
dat_plane_y_incr = Model_size_y / (Num_DatumPlanes_y + 1)

FirstGrain_centre_x = Model_origin_x + dat_plane_x_incr/2
FirstGrain_centre_y = Model_origin_y + dat_plane_y_incr/2

modelcentre_x = (Model_origin_x + Model_size_x)/2
modelcentre_y = (Model_origin_y + Model_size_y)/2

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
#import external modules
import numpy as np
######################################################################
# Create base sets
part.Set(faces = part.faces.findAt(((modelcentre_x, modelcentre_y, 0.),)), name = 'FullFace')
part.Set(edges = part.edges.findAt(((LE_centre_x, LE_centre_y,0.),)), name = 'FullEdge_x-')
part.Set(edges = part.edges.findAt(((RE_centre_x, RE_centre_y,0.),)), name = 'FullEdge_x+')
part.Set(edges = part.edges.findAt(((BE_centre_x, BE_centre_y,0.),)), name = 'FullEdge_y-')
part.Set(edges = part.edges.findAt(((TE_centre_x, TE_centre_y,0.),)), name = 'FullEdge_y+')
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
    else:
		thisoffset = thisoffset+dat_plane_y_incr
		#print thisoffset
		count = count+1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = XZPLANE)
		DatumPlaneIDs_y.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_y_'+str(count))
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
    else:
		thisoffset = thisoffset+dat_plane_x_incr
		#print thisoffset
		count = count + 1
		DPinfo = part.DatumPlaneByPrincipalPlane(offset = thisoffset, principalPlane = YZPLANE)
		DatumPlaneIDs_x.append(DPinfo.id)
		part.features.changeKey(fromName='Datum plane-1', toName='DP_x_'+str(count))
######################################################################
# partition using datum planes parallel to xz planes
# create set names
for ii in range(1, Num_DatumPlanes_y + 1):
	TheID = DatumPlaneIDs_y[ii-1]
	xloc  = FirstGrain_centre_x
	yloc  = FirstGrain_centre_y + (ii-1)*dat_plane_y_incr
	#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
	part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))

# partition using datum planes parallel to yz planes
for jj in range(1, Num_DatumPlanes_y + 2):
	for ii in range(1, Num_DatumPlanes_x + 1):
		TheID_x = DatumPlaneIDs_x[ii-1]
		xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
		yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
		#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
		part.PartitionFaceByDatumPlane(datumPlane = part.datums[TheID_x], faces = part.faces.findAt(((xloc, yloc, 0.), ), ))
		setname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
		part.Set(faces = part.faces.findAt(((xloc, yloc, 0.),)), name = setname)

for jj in range(1, Num_DatumPlanes_y + 2):
	ii = Num_DatumPlanes_x + 1
	xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
	yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
	#part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
	setname = 'Grain_Nx_' + str(ii) + '_Ny_' + str(jj)
	part.Set(faces = part.faces.findAt(((xloc, yloc, 0.),)), name = setname)
######################################################################
# Create materials
# Create sections
# Assign sections
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
# set element seed length - global
part.seedPart(deviationFactor = 0.1, minSizeFactor = 0.1, size = ElementSize)
# Set element type
# Assign mesh controls
# set element seed length - global
# mesh the faces
for jj in range(1, Num_DatumPlanes_y + 2, 1):
    yloc = FirstGrain_centre_y + (jj-1)*dat_plane_y_incr
    #print jj
    for ii in range(1, Num_DatumPlanes_x + 2, 1):
        xloc = FirstGrain_centre_x + (ii-1)*dat_plane_x_incr
        #print ii
        #part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
        if ElementTypeFlagID==1:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS4R, elemLibrary = STANDARD, secondOrderAccuracy = OFF,hourglassControl = ENHANCED, distortionControl = DEFAULT), ElemType(elemCode = CPS3, elemLibrary = STANDARD)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif ElementTypeFlagID==2:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8 , elemLibrary = STANDARD), ElemType(elemCode = CPS6M,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif ElementTypeFlagID==3:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS4 , elemLibrary = STANDARD), ElemType(elemCode = CPS3 ,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif ElementTypeFlagID==4:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8R, elemLibrary = STANDARD), ElemType(elemCode = CPS6M,elemLibrary = STANDARD, secondOrderAccuracy = OFF, distortionControl = DEFAULT)), regions = (part.faces.findAt(((xloc, yloc, 0.),)), ))
        elif ElementTypeFlagID==5:
            part.setElementType(elemTypes = (ElemType(elemCode = CPS8R, elemLibrary = STANDARD), ElemType(elemCode = CPS6 ,elemLibrary = STANDARD)), regions = (part.faces.findAt(((xloc,yloc,0.),)),))
        #part.DatumPointByCoordinate(coords = (xloc, yloc, 0.0))
        if ElementShapeFlagID == 1:
            part.setMeshControls(elemShape=QUAD, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=STRUCTURED)
        elif ElementShapeFlagID == 4:
            part.setMeshControls(elemShape=TRI, regions = part.faces.findAt(((xloc, yloc, 0.),)), technique=FREE)
        part.generateMesh(regions = part.faces.findAt(((xloc, yloc, 0.),)))
######################################################################
# print out the total number of nodes and elements

mdb.models['Model-1'].rootAssembly.regenerate()
instance        = model.rootAssembly.instances['partname-1']
TotalNumOfNodes = len(instance.nodes)
TotalNumOfElem  = len(instance.elements)
usethis         = 0

if usethis==1:
	if str(instance.elements[1].type)=='CPS4R' or str(instance.elements[1].type)=='CPS4':
		Total_DOF = TotalNumOfNodes*4
	elif str(instance.elements[1].type)=='CPS8R' or str(instance.elements[1].type)=='CPS8':
		Total_DOF = TotalNumOfNodes*8

print('%d Elements --- %d Nodes --- '% (TotalNumOfElem, TotalNumOfNodes))
print('%d Elements per Grain --- '% (TotalNumOfElem/(NumPartitions_x*NumPartitions_y)))
print('Grain Length X: %2f'% (Model_size_x/NumPartitions_x))
print('Grain Width  Y: %2f'% (Model_size_y/NumPartitions_y))
print('Grain Aspect Ratio: %2f'% float((Model_size_x/NumPartitions_x)/(Model_size_y/NumPartitions_y)))
######################################################################
#CAE_File_name = '\\CB-24-2-1-cps4--tr1'
######################################################################
CAEFILEpath = 'C:\\Users\\anandats\\OneDrive - Coventry University\\coventry-thesis\\Chapter7\\ABAQUS_CAL_DATA_FILES\\LocationB'
mdb.saveAs(pathName = CAEFILEpath + '\\' + CAE_File_name)
#mdb.saveAs(pathName = 'C:\Temp\CalibrationModels\Location A\Cal_48ng\Ng_'+str(NumPartitions_x*NumPartitions_y)+'_'+'Ngx_'+str(NumPartitions_x)+'_'+'Ngy_'+str(NumPartitions_y))
print('Printing the CAE file: %s'% (CAE_File_name+'.cae'))
