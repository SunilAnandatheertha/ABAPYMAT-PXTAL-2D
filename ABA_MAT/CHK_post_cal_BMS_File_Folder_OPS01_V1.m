
EXCEL_filepath  = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6';
EXCEL_FN        = 'Post_Cal_Model__Benchmark_Studies_v1.0.xlsx';
EXCEL_filename  = [EXCEL_filepath filesep EXCEL_FN];
EXCEL_sheetname = 'Post-Calib-Benchmark-1';
xlRange_FolderRootNames     = 'O10:O89';
xlRange_SIM_Include_Exclude = 'P10:P89';
[~, SIM_Folder_ROOT_Names, ~]     = xlsread(EXCEL_filename, sheet, xlRange_FolderRootNames);
[SIM_Include_Exclude_FLAGS, ~, ~] = xlsread(EXCEL_filename, sheet, xlRange_SIM_Include_Exclude);

SIM_filepath  = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter7\ABAQUS_POST_CAL_BENCHMARK_STUDIES\LocationB';
SIM_FN        = 'Post_Cal_Model__Benchmark_Studies_v1.0.xlsx';
SIM_filename  = [EXCEL_filepath filesep EXCEL_FN];

SIM_INCLUDE_LIST = find(SIM_Include_Exclude_FLAGS==1);

ORIGINAL_UMAT_FORTRAN_FileName = 'HKumat.f';
ORIGINAL_SLURM_FileName        = 'cpfem.f';
ORIGINAL_MPI_SLURM_FileName    = 'cpfem_mpi.f';

ORIGINAL_UMAT_FORTRAN_FULL_FileName = [SIM_filepath filesep ORIGINAL_UMAT_FORTRAN_FileName];
ORIGINAL_SLURM_FULL_FileName        = [SIM_filepath filesep ORIGINAL_SLURM_FileName];
ORIGINAL_MPI_SLURM_FULL_FileName    = [SIM_filepath filesep ORIGINAL_MPI_SLURM_FileName];

for SIM_flag_index = 1:numel(SIM_INCLUDE_LIST)
    This_Sim_Folder_Name = SIM_Folder_ROOT_Names{SIM_INCLUDE_LIST(SIM_flag_index)};
    % in post_cal_bms_loc_B, "bms" means bench mark studies
    DestinationFolder = [SIM_filepath filesep 'To_upload_to_HPC' filesep 'post_cal_bms_loc_B' filesep This_Sim_Folder_Name];
    mkdir(DestinationFolder)
    FULL_Destination_FORTRAN_Filename = [DestinationFolder filesep ORIGINAL_UMAT_FORTRAN_FileName];
    copyfile(ORIGINAL_UMAT_FORTRAN_FULL_FileName, FULL_Destination_FORTRAN_Filename)
end