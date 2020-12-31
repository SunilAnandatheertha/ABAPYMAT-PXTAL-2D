function [Ntc, TCid, TCidnames, EA_TC] = CHK_gen_umat_data_REF_STD_ORIENTATIONS_V1()

EA_TC  = {'00', '90', '00';  % Cube
          '00', '45', '00';  % Goss
          '35', '45', '00';  % Brass
          '90', '35', '45';  % Copper
          '59', '37', '63'}; % S
%------------------------------------------------
Ntc  = 5; % Number of TC
TCid = [1 2 3 4 5]; % TC id number
TCidnames = ['W_id1_', EA_TC{1,1}, '_', EA_TC{1,2}, '_', EA_TC{1,3};
             'G_id2_', EA_TC{2,1}, '_', EA_TC{2,2}, '_', EA_TC{2,3};
             'B_id3_', EA_TC{3,1}, '_', EA_TC{3,2}, '_', EA_TC{3,3};
             'C_id4_', EA_TC{4,1}, '_', EA_TC{4,2}, '_', EA_TC{4,3};
             'S_id5_', EA_TC{5,1}, '_', EA_TC{5,2}, '_', EA_TC{5,3};
             ];
EA_TC = str2double(EA_TC);
end