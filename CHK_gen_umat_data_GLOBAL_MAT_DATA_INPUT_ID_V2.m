function [UMDATA, IDGMDS, n, adot, c11, c12, c44, h0, taus, tau0, q, q1, MATDATA] = CHK_gen_umat_data_GLOBAL_MAT_DATA_INPUT_ID_V2()

% GLOBAL MATERIAL PARAMETER DATA FILE

% NAME OF THE FILE: GMP_DATA_01.dat
% FOLDER LOCATION : '~\Grain_Structure_data_Repository\GMP_DATA\'
prompt = {1, 'Global Mat Par Data (GMP Data) folder', 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\GMP_DATA\';
          2, 'GMP Data filename:', 'GMP_DATA_01.dat';
          3, 'ID of Global Mat Data Set (from 1st col. in a/b file)', '1'};
dlgtitle = 'Input the filename and GMDS ID';
dims     = [1 60];
definput = prompt(:,3)';
GMDDetails = inputdlg(prompt(:,2)', dlgtitle, dims, definput);

GMP_DATA_folder   = GMDDetails{1};
GMP_DATA_filename = GMDDetails{2};
IDGMDS            = str2double(GMDDetails{3});


% DATA STORAGE FORMAT:::   IDGMDS,n,adot,c11,c12,c44,h0,taus,tau0,q,q1
% Where, IDGMDS: GLOBAL MATERIAL DATA SET ID
% RULE 1: NO EMPTY LINES ANYWHERE IN THE FILE
% RULE 2: NO SPACES ANYWHERE IN A LINE
% Example file contents:
    % 001,10,0.001,168400.0,121400.0,75400.0,541.5,109.5,60.8,01.0,01.0
    % 002,10,0.001,168400.0,121400.0,75400.0,400.5,075.5,90.8,01.0,01.0
    % and so on
UMDATA = dlmread([GMP_DATA_folder GMP_DATA_filename]);
UMDATA = UMDATA(UMDATA(:,1)==IDGMDS,:);
if isempty(UMDATA)
    disp('Enter the correct IDGMDS')
end


IDGMDS = UMDATA(1);
n      = UMDATA(2);
adot   = UMDATA(3);
c11    = UMDATA(4);
c12    = UMDATA(5);
c44    = UMDATA(6);
h0     = UMDATA(7);
taus   = UMDATA(8);
tau0   = UMDATA(9);
q      = UMDATA(10);
q1     = UMDATA(11);
MATDATA = [c11, c12, c44,     0.,     0.,     0.,     0.,     0. % 01
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 02
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 03
           1.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 04
           1.,     1.,     1.,     1.,     1.,     0.,     0.,     0.     % 05
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 06
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 07
          -1.,     0.,     1.,     0.,     0.,     1.,     0.,     0.     % 08  % VECTOR 1
           0.,     1.,     0.,     1.,     0.,     0.,     0.,     0.     % 09  % VECTOR 2
           n ,    adot,    0.,     0.,     0.,     0.,     0.,     0.     % 10
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 11
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 12
           h0,   taus,   tau0,     0.,     0.,     0.,     0.,     0.     % 13
           q ,     q1,     0.,     0.,     0.,     0.,     0.,     0.     % 14
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 15
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 16
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 17
           0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 18
           0.5,     1.,     0.,     0.,     0.,     0.,     0.,     0.    % 19
           1.,    10.,  1e-05,     0.,     0.,     0.,     0.,     0.];   % 20
end