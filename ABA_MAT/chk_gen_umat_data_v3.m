%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc
close all
warning('off')
set(0, 'DefaultFigureWindowStyle', 'docked')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Root_Folder = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\UMAT_DATA\';
%------------------------------------------------------------------
ResetTEXTURE = CHK_gen_umat_data_UI_TEX_RESET_PROMT_V1();
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 1. Acquire preliminary user inputs
[IDVALUES, IDGS, IDTM, IDUM, IDRD, IDUP, IDOD, IDTI, IDETItoGTEX, IDETI, IDSim] = CHK_gen_umat_data_ACQUIRE_PRELIMINARY_INPUTS_V1();
%------------------------------------------------------------------
% 1. User input to specify which material dataset should be used
% 2. 
[UMDATA, IDGMDS, n, adot, c11, c12, c44, h0, taus, tau0, q, q1, MATDATA] = CHK_gen_umat_data_GLOBAL_MAT_DATA_INPUT_ID_V2();
%------------------------------------------------------------------
% 1. 
[Ntc, TCid, TCidnames, EA_TC] = CHK_gen_umat_data_REF_STD_ORIENTATIONS_V1();
% - - - - - - - - - - - - - - - - - - - - - -e
%            W    G     B    C    S
Vf_loc_B = [0.07 0.11 0.38 0.15 0.30];
Vf_loc_A = [0.04 0.12 0.42 0.13 0.26];
Vf_loc_C = [0.06 0.18 0.31 0.13 0.18];
%------------------------------------------------------------------
[TotalNumGrains, NumGrainsx, NumGrainsy] = CHK_gen_umat_data_UI_NUM_GRAINS_V1();
% - - - - - - - - - - - - - - - - - - - - - -
[TEXLOCATIONDetails, TEXLOCATION] = CHK_gen_umat_data_UI_ACQUIRE_TEX_LOC_DETAILS_V1();
% - - - - - - - - - - - - - - - - - - - - - -
switch upper(TEXLOCATIONDetails{1})
    case 'A';        Vf_loc = Vf_loc_A;
    case 'B';        Vf_loc = Vf_loc_B;
    case 'C';        Vf_loc = Vf_loc_C;
    otherwise;       Vf_loc = Vf_loc_B;
        disp('Location entered does not match records');
        disp('I am considering location B')
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
hklparallel = [0 0 1];
uvwparallel = [1 0 0];
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if IDETItoGTEX == 0
    if IDETI == 0
        for texinstance = 1:1:IDTI
            % - - - - - - - - - - - - - - - - - - - - - -
            if IDSim<=9;                   CalIDstr = ['00' num2str(IDSim)];
            elseif IDSim>9 && IDSim<=99;   CalIDstr = ['0' num2str(IDSim)];
            elseif IDSim>99 && IDSim<=999; CalIDstr = num2str(IDSim);
            end
            % - - - - - - - - - - - - - - - - - - - - - -
            FNbase = ['Loc' TEXLOCATIONDetails{1} '__CalIter' CalIDstr '__Ng' num2str(TotalNumGrains), 'x' num2str(NumGrainsx), 'y' num2str(NumGrainsy),...
                      '__GS' IDVALUES{1} '__TM' IDVALUES{2} '__UM' IDVALUES{3},'__RD' IDVALUES{4} '__UP' IDVALUES{5} '__OD.' IDVALUES{6},...
                      '__TxIn' num2str(texinstance) '__IDGMDS' num2str(IDGMDS)];
            % - - - - - - - - - - - - - - - - - - - - - -
            [Vf_loc]           = CHK_gen_umat_data_ADJUST_VOL_FRAC_V1(Vf_loc);
            % - - - - - - - - - - - - - - - - - - - - - -
            [TC_NumGrains_loc, TC_numGrains_final, ActualVf, Vf_ratios_needed_to_actual, grain_orientation_dis, phi1, phi, phi2] = CHK_gen_umat_data_CALC_EULERANGLEDISTR_V1(TotalNumGrains, Vf_loc, EA_TC, TCid, NumGrainsx, NumGrainsy);
            % - - - - - - - - - - - - - - - - - - - - - -
            [g11, g21, g31, g12, g22, g32, g13, g23, g33] = CHK_gen_umat_data_CALC_ORI_MATRIX_ELEMENTS_V1(phi1, phi, phi2);
            % - - - - - - - - - - - - - - - - - - - - - -
            [Vector1, Vector2] = CHK_gen_umat_data_BUILD_HKL_UVW_VECTORS_V1(g11, g21, g31, g12, g22, g32, g13, g23, g33, hklparallel, uvwparallel);
            % - - - - - - - - - - - - - - - - - - - - - -
            CHK_gen_umat_data_WRITE_TEXINFO_EA_UMAT_DATA_TEXTFILE_V1(Root_Folder, FNbase, NumGrainsx, NumGrainsy, MATDATA, Vector1, Vector2, Vf_loc, ActualVf, Vf_ratios_needed_to_actual, TC_numGrains_final, phi1, phi, phi2)
            % - - - - - - - - - - - - - - - - - - - - - -
            CHK_gen_umat_data_VIZ_TEX_DISTR_V2(grain_orientation_dis, TotalNumGrains, NumGrainsx, NumGrainsy, FNbase, Root_Folder, texinstance)
            %[Vf_loc' ActualVf TC_numGrains_final]
        end
    else
    end
elseif IDETItoGTEX == 1
    if IDETI == 0
    elseif  IDETI == 1
        % - - - - - - - - - - - - - - - - - - - - - -
        if ResetTEXTURE == 1
            [Vf_loc]           = CHK_gen_umat_data_ADJUST_VOL_FRAC_V1(Vf_loc);
            [TC_NumGrains_loc, TC_numGrains_final, ActualVf, Vf_ratios_needed_to_actual,...
                grain_orientation_dis, phi1, phi, phi2] = CHK_gen_umat_data_CALC_EULERANGLEDISTR_V1(TotalNumGrains, Vf_loc, EA_TC, TCid, NumGrainsx, NumGrainsy);
            % - - - - - - - - - - - - - - - - - - - - - -
            [g11, g21, g31, g12, g22, g32, g13, g23, g33] = CHK_gen_umat_data_CALC_ORI_MATRIX_ELEMENTS_V1(phi1, phi, phi2);
            % - - - - - - - - - - - - - - - - - - - - - -
            [Vector1, Vector2] = CHK_gen_umat_data_BUILD_HKL_UVW_VECTORS_V1(g11, g21, g31, g12, g22, g32, g13, g23, g33, hklparallel, uvwparallel);
        else
            grain_orientation_dis = reshape(grain_orientation_dis, NumGrainsy, NumGrainsx);
            % - - - - - - - - - - - - - - - - - - - - - -
            for texinstance = 1:1:IDTI
                % - - - - - - - - - - - - - - - - - - - - - -
                if IDSim<=9;                   CalIDstr = ['00' num2str(IDSim)];
                elseif IDSim>9  && IDSim<=99;  CalIDstr = ['0'  num2str(IDSim)];
                elseif IDSim>99 && IDSim<=999; CalIDstr = num2str(IDSim);
                end
                % - - - - - - - - - - - - - - - - - - - - - -
                FNbase = ['Loc' TEXLOCATIONDetails{1} '__CalIter' CalIDstr '__Ng' num2str(TotalNumGrains), 'x' num2str(NumGrainsx), 'y' num2str(NumGrainsy),...
                          '__GS' IDVALUES{1} '__TM' IDVALUES{2} '__UM'  IDVALUES{3},...
                          '__RD' IDVALUES{4} '__UP' IDVALUES{5} '__OD.' IDVALUES{6},...
                          '__TxIn' num2str(texinstance) '__IDGMDS' num2str(IDGMDS)];
                % - - - - - - - - - - - - - - - - - - - - - -
                CHK_gen_umat_data_WRITE_TEXINFO_EA_UMAT_DATA_TEXTFILE_V1(Root_Folder, FNbase, NumGrainsx, NumGrainsy, MATDATA, Vector1, Vector2, Vf_loc, ActualVf, Vf_ratios_needed_to_actual, TC_numGrains_final, phi1, phi, phi2, TEXLOCATION, TCidnames)
                % - - - - - - - - - - - - - - - - - - - - - -
                CHK_gen_umat_data_VIZ_TEX_DISTR_V2(grain_orientation_dis, TotalNumGrains, NumGrainsx, NumGrainsy, FNbase, Root_Folder, texinstance)
                %[Vf_loc' ActualVf TC_numGrains_final]
            end   
        end
    end    
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
warning('on')
figure(1)