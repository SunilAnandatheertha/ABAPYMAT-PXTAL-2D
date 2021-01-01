% next line. If 1, then data already exists. no need to read excel file
% again.

% if in doubt OR of excel read has nnot been done before, use 0. But, it
% will take longer time.

excel_data_extraction_FLAG = 0;

if excel_data_extraction_FLAG == 0
    EXCEL_filepath  = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6';
    EXCEL_FN        = 'Post_Cal_Model__Benchmark_Studies_v1.0.xlsx';
    EXCEL_filename  = [EXCEL_filepath filesep EXCEL_FN];
    EXCEL_sheetname = 'Post-Calib-Benchmark-1';
    xlRange_FolderRootNames     = 'O10:O89';
    xlRange_SIM_Include_Exclude = 'P10:P89';
    xlRange_UMAT_FORMAT_DATA    = 'K10:K89';
    [~, SIM_Folder_ROOT_Names, ~]         = xlsread(EXCEL_filename, EXCEL_sheetname, xlRange_FolderRootNames);
    [SIM_Include_Exclude_FLAGS, ~, ~]     = xlsread(EXCEL_filename, EXCEL_sheetname, xlRange_SIM_Include_Exclude);
    [~, Formatted_UMAT_DATA_FileNames, ~] = xlsread(EXCEL_filename, EXCEL_sheetname, xlRange_UMAT_FORMAT_DATA);
end


SIM_filepath  = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter7\ABAQUS_POST_CAL_BENCHMARK_STUDIES\LocationB';
SIM_filename  = [EXCEL_filepath filesep EXCEL_FN];

SIM_INCLUDE_LIST = find(SIM_Include_Exclude_FLAGS==1);

ORIGINAL_UMAT_FORTRAN_FileName = 'HKumat.f';
ORIGINAL_SLURM_FileName        = 'cpfem.slurm';
ORIGINAL_MPI_SLURM_FileName    = 'cpfem_mpi.slurm';

ORIGINAL_UMAT_FORTRAN_FULL_FileName = [SIM_filepath filesep ORIGINAL_UMAT_FORTRAN_FileName];
ORIGINAL_SLURM_FULL_FileName        = [SIM_filepath filesep ORIGINAL_SLURM_FileName];
ORIGINAL_MPI_SLURM_FULL_FileName    = [SIM_filepath filesep ORIGINAL_MPI_SLURM_FileName];

% in next line: post_cal_bms_loc_B, "bms" means bench mark studies
to_HPC_post_calib_folder_name = [SIM_filepath filesep 'To_upload_to_HPC' filesep 'post_cal_bms_loc_B'];
if exist(to_HPC_post_calib_folder_name, 'dir')==7 % 7: it is a folder
    disp('Folder exists. DELETE it and re-run')
    % rmdir(to_HPC_post_calib_folder_name)
    % mkdir(to_HPC_post_calib_folder_name)
elseif exist(to_HPC_post_calib_folder_name, 'dir')==0 % 0: foolder does no exist
    mkdir(to_HPC_post_calib_folder_name)
    for SIM_flag_index = 1:numel(SIM_INCLUDE_LIST)
        disp(' - - - - - - - - - - - - - - - - - - - - - - - - - ')
        This_Sim_Folder_Name = SIM_Folder_ROOT_Names{SIM_INCLUDE_LIST(SIM_flag_index)};
        DestinationFolder = [to_HPC_post_calib_folder_name filesep This_Sim_Folder_Name];
        mkdir(DestinationFolder)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        disp('Copying UMAT fortran file file')
        FULL_Destination_FORTRAN_Filename = [DestinationFolder filesep ORIGINAL_UMAT_FORTRAN_FileName];
        copyfile(ORIGINAL_UMAT_FORTRAN_FULL_FileName, FULL_Destination_FORTRAN_Filename)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        disp('Copying HPC SLURM file: single')
        FULL_Destination_SLURM_Filename = [DestinationFolder filesep ORIGINAL_SLURM_FileName];
        copyfile(ORIGINAL_SLURM_FULL_FileName, FULL_Destination_SLURM_Filename)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        disp('Copying HPC SLURM file: MPI (parallel processing)')
        FULL_Destination_MPI_SLURM_Filename = [DestinationFolder filesep ORIGINAL_MPI_SLURM_FileName];
        copyfile(ORIGINAL_MPI_SLURM_FULL_FileName, FULL_Destination_MPI_SLURM_Filename)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        disp('Copying CAE and JNL files')
        FULL_Source_CAE_Filename = [SIM_filepath filesep [This_Sim_Folder_Name '.cae']];
        FULL_Destination_CAE_Filename = [DestinationFolder filesep [This_Sim_Folder_Name '.cae']];
        copyfile(FULL_Source_CAE_Filename, FULL_Destination_CAE_Filename)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        FULL_Source_JNL_Filename = [SIM_filepath filesep [This_Sim_Folder_Name '.jnl']];
        FULL_Destination_JNL_Filename = [DestinationFolder filesep [This_Sim_Folder_Name '.jnl']];
        copyfile(FULL_Source_JNL_Filename, FULL_Destination_JNL_Filename)
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        TEXINFO_files_folder = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\UMAT_DATA\TEX_DISTRIBUTION_INFO';
        EANGLES_files_folder = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\UMAT_DATA\EULER_ANGLES';
        UMAT_file_folder     = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\UMAT_DATA\UMAT_FORMAT';
        
        RootFilename      = [Formatted_UMAT_DATA_FileNames{SIM_INCLUDE_LIST(SIM_flag_index)}];
        %LocB__CalIter019__Ng192x96y2__GS1__TM1__UM1__RD1__UP1__OD.io__TxIn1__IDGMDS19__UMATdata
        %LocB__CalIter019__Ng192x16y12__GS1__TM1__UM1__RD1__UP1__OD.io__TxIn4__IDGMDS19__TexDistrData
        RootFilename      = RootFilename(1:end-8);
        
        TEXINFO_Distr_filename   = [RootFilename 'TexDistrData.txt'];
        TEXINFO_TCinfo_filename  = [RootFilename 'TClocTCidnames.txt'];
        TEXINFO_Viz_IMG_filename = [RootFilename(1:end-2) '.tiff'];
        EANGLES_filename         = [RootFilename 'EuAng.txt'];
        UMAT_filename            = [Formatted_UMAT_DATA_FileNames{SIM_INCLUDE_LIST(SIM_flag_index)} '.txt'];
        
        TEXINFO_Distr_filename_shortened   = [This_Sim_Folder_Name '__TEX_distr.txt'];
        TEXINFO_TCinfo_filename_shortened  = [This_Sim_Folder_Name '__TEX_TCinfo.txt'];
        TEXINFO_Viz_IMG_filename_shortened = [This_Sim_Folder_Name '__TEX_IMG.tiff'];
        EANGLES_filename_shortened         = [This_Sim_Folder_Name '__TEX_EA.txt'];
        UMAT_filename_shortened            = [This_Sim_Folder_Name '__UMAT_MatData.txt'];
       
        copyfile([TEXINFO_files_folder filesep TEXINFO_Distr_filename]  , [DestinationFolder filesep TEXINFO_Distr_filename_shortened]  )
        copyfile([TEXINFO_files_folder filesep TEXINFO_TCinfo_filename] , [DestinationFolder filesep TEXINFO_TCinfo_filename_shortened] )
        copyfile([TEXINFO_files_folder filesep TEXINFO_Viz_IMG_filename], [DestinationFolder filesep TEXINFO_Viz_IMG_filename_shortened])
        copyfile([EANGLES_files_folder filesep EANGLES_filename]        , [DestinationFolder filesep EANGLES_filename_shortened])
        copyfile([UMAT_file_folder filesep UMAT_filename]               , [DestinationFolder filesep UMAT_filename_shortened])
        
        SHORT_LONG_FILENAME_MAPPING_FILE          = [This_Sim_Folder_Name '__FileName_MAPPING.txt'];
        SHORT_LONG_FILENAME_MAPPING_FILE_fullPath = [DestinationFolder filesep SHORT_LONG_FILENAME_MAPPING_FILE];
        fid = fopen(SHORT_LONG_FILENAME_MAPPING_FILE_fullPath,'W');
        fprintf(fid, [TEXINFO_Distr_filename_shortened '--' TEXINFO_Distr_filename '\n']);
        fclose(fid);
        fid = fopen(SHORT_LONG_FILENAME_MAPPING_FILE_fullPath,'a');
        fprintf(fid, [TEXINFO_TCinfo_filename_shortened '--' TEXINFO_TCinfo_filename '\n']);
        fprintf(fid, [TEXINFO_Viz_IMG_filename_shortened '--' TEXINFO_Viz_IMG_filename '\n']);
        fprintf(fid, [EANGLES_filename_shortened '--' EANGLES_filename '\n']);
        fprintf(fid, [UMAT_filename_shortened '--' UMAT_filename '\n']);
        fclose(fid);
        % - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        % !!!!!!!!!!Replace dummy MAT DATA with FOMRATTED UMAT MATERIAL DATA IN ALL SIMULATION INPUT FILES!!!!!!!!!!
        disp('Creating the .inp file')
        FULL_Source_INP_Filename = [SIM_filepath filesep [This_Sim_Folder_Name '.inp']];
        RAW_INP_FILE = fileread(FULL_Source_INP_Filename);
        SPLIT_RAW_INP_FILE = regexp(RAW_INP_FILE,'\n','split');
        %$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        % PART 1 -- PRE MATERIAL DATA        
        LeftCap_0_LineNumber                    = 1;                                                  % DONT CHANGE
        RightCap_0_LineNumber                   = find(contains(SPLIT_RAW_INP_FILE, '** MATERIALS')); % DONT CHANGE
        FULL_Destination_INP_Filename_PART_FULL = [DestinationFolder filesep [This_Sim_Folder_Name '_new.inp']];
        fileID                                  = fopen(FULL_Destination_INP_Filename_PART_FULL,'W');
        for LineNumber = LeftCap_0_LineNumber:RightCap_0_LineNumber+1
            fprintf(fileID, [SPLIT_RAW_INP_FILE{LineNumber} '\n']);
        end
        disp('Write part - 1 finished: Model geom and mesh details')
        fclose(fileID);
        % PART 2 -- UMAT MAT DATA
        fprintf('Using TEX from file <<<    %s    >>> \n', UMAT_filename)
        UMAT_filename_full  = [UMAT_file_folder filesep UMAT_filename];
        UMAT_INP_FILE       = fileread(UMAT_filename_full);
        SPLIT_UMAT_INP_FILE = regexp(UMAT_INP_FILE,'\n','split');
        fileID              = fopen(FULL_Destination_INP_Filename_PART_FULL,'a');
        for LineNumber = 1:numel(SPLIT_UMAT_INP_FILE)
            fprintf(fileID, [SPLIT_UMAT_INP_FILE{LineNumber} '\n']);
        end
        disp('Write part - 2 finished: Model UMAT material details')
        fclose(fileID);
        % PART 3 -- POST MATERIAL DATA
        LeftCap_1_LineNumbers = find(contains(SPLIT_RAW_INP_FILE, '** BOUNDARY CONDITIONS')); % DONT CHANGE
        RightCap_1_LineNumber = find(contains(SPLIT_RAW_INP_FILE, '** FIELD OUTPUT'));        % DONT CHANGE
        LeftCap_1_LineNumber  = LeftCap_1_LineNumbers(1)-1;                                   % DONT CHANGE
        RightCap_1_LineNumber = RightCap_1_LineNumber + 1;                                    % DONT CHANGE
        fileID                = fopen(FULL_Destination_INP_Filename_PART_FULL,'a');
        for LineNumber = LeftCap_1_LineNumber:RightCap_1_LineNumber                           % DONT CHANGE
            fprintf(fileID, [SPLIT_RAW_INP_FILE{LineNumber} '\n']);
        end
        disp('Write part - 3 finished: "Boundary Conditions" to "Output Request" details')
        fclose(fileID);
        % PART 04 - REQUEST SDV and HISTORY OUTPUT
        SDV_file_Path              = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter7\ABAQUS_POST_CAL_BENCHMARK_STUDIES';
        SDV_file_name              = 'Requesting_SDV1.txt';
        SDV_file_name_full         = [SDV_file_Path filesep SDV_file_name];
        SDV_FILE_ID                = fileread(SDV_file_name_full);
        SPLIT_SDV_REQUEST_INP_FILE = regexp(SDV_FILE_ID,'\n','split');
        fileID                     = fopen(FULL_Destination_INP_Filename_PART_FULL,'a');
        for LineNumber = 1:numel(SPLIT_SDV_REQUEST_INP_FILE)
            fprintf(fileID, [SPLIT_SDV_REQUEST_INP_FILE{LineNumber} '\n']);
        end
        disp('Write part - 4 finished: "Field output" to "End of Step-1"')
        fclose(fileID);
        %$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        fprintf('The input file "%s" has been written\n', [This_Sim_Folder_Name '.inp'])
        disp('    and all related files have been copied to HPC sim folder\n')
    end
end
disp('\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \')
disp('FILES AND FOLDERS NEEDED FOR HPC ARE READY. Now do the following:')
disp('STEP 01: COPY FOLDERS TO HPC WORK FOLDER')
disp('STEP 02: EDIT SLURM FILE WITH CORRECT .INP FILENAME')
disp('STEP 03: CHANGE DIRECTORY IN PUTTY')
disp('STEP 04: SUBMIT JOB')
disp('STEP 05: NOTE JOB ID & COPY IT TO EXCEL FILE')
disp('STEP 06: ONCE ANALYSIS COMPLETES, COPY FILES BACK TO COMPUTER')
disp('STEP 07: WAIT FOR THEM TO COME IN MY LAPTOP ONEDRIVE')
disp('STEP 08: BU -- COPY THEM TO EXTERNAL HARD DISK')
disp('STEP 09: MOVE FOCUS TO ABAQUS AND ANAYZE ODB FILES')
disp('/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / /')