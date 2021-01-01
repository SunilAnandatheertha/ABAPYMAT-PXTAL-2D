function CHK_gen_umat_data_WRITE_TEXINFO_EA_UMAT_DATA_TEXTFILE_V1(Root_Folder, FNbase, NumGrainsx, NumGrainsy, MATDATA, Vector1, Vector2, Vf_loc, ActualVf, Vf_ratios_needed_to_actual, TC_numGrains_final, phi1, phi, phi2, TEXLOCATION, TCidnames)

disp('- - - - - - - - - - - - - -')
count = 1;
filepathname = [Root_Folder 'UMAT_FORMAT\' FNbase '__UMATdata.txt'];
% filename = [IDGS '_MaterialData_SetNum_' IDTI '.txt'];
for gx = 1:NumGrainsx
    for gy = 1:NumGrainsy
        dlmwrite(filepathname, ['*Material, name = Mat_Grain_Nx_' num2str(gx) '_Ny_' num2str(gy)], '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite(filepathname, '*Depvar', '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite(filepathname, ['   125,'], '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite(filepathname, '*User Material, constants=160, unsymm', '-append', 'delimiter', '', 'precision', '%10.4f')
        datatowrite = [MATDATA(1:7,:); Vector1(count,:); Vector2(count,:); MATDATA(10:20,:)];
        dlmwrite(filepathname, datatowrite, '-append', 'delimiter', ',', 'precision', '%10.4f')
        if mod(count, 5)==0
            fprintf('Writing material data for grain # %d \n', count)
        end
        count = count + 1;
    end
end
% fprintf('Filename is %s \n', filename)
filepathname_EA = [Root_Folder 'EULER_ANGLES\' FNbase '__EuAng.txt'];
dlmwrite(filepathname_EA, [phi1 phi phi2])
filepathname_Vf = [Root_Folder 'TEX_DISTRIBUTION_INFO\' FNbase '__TexDistrData.txt'];
dlmwrite(filepathname_Vf, [Vf_loc' ActualVf Vf_ratios_needed_to_actual TC_numGrains_final])
filepathname_TClocTCidnames = [Root_Folder 'TEX_DISTRIBUTION_INFO\' FNbase '__TClocTCidnames.txt'];
dlmwrite(filepathname_TClocTCidnames, TEXLOCATION, 'delimiter', '')
dlmwrite(filepathname_TClocTCidnames, TCidnames, '-append', 'delimiter', '')
disp('- - - - - - - - - - - - - -')
end