#---------------------------------------------------------------
import numpy as np
import matplotlib.pyplot as plt
#---------------------------------------------------------------
font = {'family': 'arial',
        'color':  'black',
        'weight': 'normal',
        'size': 12,
        }
#---------------------------------------------------------------
FolderName             = 'C:\\Temp\\CalibrationModels\\Cal_100ng\\'
Rootfilename_001        = '48Ng_24x_2y_TEXID01_EBG001_CPS4____'
IDname_001              = '_4847864798_id2_9948322254.txt'
#Data_RFX_Filename      = Rootfilename_001 + 'DATA_RFX_____id1' + IDname_001
#Data_RFY_Filename      = Rootfilename_001 + 'DATA_RFY_____id1' + IDname_001
#Data_TSteps_Filename   = Rootfilename_001 + 'DATA_TSteps_____id1' + IDname_001
#Data_UX_Filename       = Rootfilename_001 + 'DATA_UXavg_____id1' + IDname_001
#Data_UY_Filename       = Rootfilename_001 + 'DATA_UYavg_____id1' + IDname_001
Data_StressXX_Filename_001 = Rootfilename_001 + 'DATA_Stress_XX_____id1' + IDname_001
Data_StrainXX_Filename_001 = Rootfilename_001 + 'DATA_Strain_XX_____id1' + IDname_001
#---------------------------------------------------------------
#RFX       = np.loadtxt(FolderName + Data_RFX_Filename,    delimiter = ",")
#RFY       = np.loadtxt(FolderName + Data_RFY_Filename,    delimiter = ",")
#TSteps    = np.loadtxt(FolderName + Data_TSteps_Filename, delimiter = ",")
#UX        = np.loadtxt(FolderName + Data_UX_Filename, delimiter = ",")
#UY        = np.loadtxt(FolderName + Data_UY_Filename, delimiter = ",")
Stress_XX_001 = np.loadtxt(FolderName + Data_StressXX_Filename_001, delimiter = ",")
Strain_XX_001 = np.loadtxt(FolderName + Data_StrainXX_Filename_001, delimiter = ",")
#---------------------------------------------------------------
plt.plot(Strain_XX_001, Stress_XX_001, color='blue', linewidth = 1,\
         linestyle = 'solid', marker='o', markersize = 3, label = 'Model-001')
#---------------------------------------------------------------
plt.title('Stress vs. time', fontdict = font)
plt.xlabel('Total strain', fontdict = font)
plt.ylabel('Average induced stress, Sxx (MPa)', fontdict = font)
plt.legend(loc = 'best', frameon = False)
plt.savefig('books_read.png', transparent='true', dpi = 600)
plt.show()
#---------------------------------------------------------------