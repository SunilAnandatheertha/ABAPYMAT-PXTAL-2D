set(0,'DefaultFigureWindowStyle','docked')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clear IDGS IDTM IDTI
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
close all
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% SPECIFY WHAT IS TO BE CHANGED TO GENERATE THE MODOEL
    % if IDUM is to be changed, then we have to specify the IDTI to
    % which the new IDUM will correspond to.
    % if IDTI is to be changed, then we have to specify the IDUM to 
    % which the new IDTI will correspond to.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% A SINGLE GRAIN STRUCTURE CAN HAVE MANY SAMPLINGS I.E. INSTANCES
% OF THE SAME CRYSTALLOGRAPHIC TEXTURE HAVING A UNIQUE ID
% - - - - - - - - - - - - - - - - - - - - - -
% LEVEL 1: IDGS: ID of the GRAIN STRUCTURE
% LEVEL 2: IDTM: ID of the TEXTURE MODEL
% LEVEL 3: IDUM: ID of the UMAT.1: Pierce and Asaro model [c11, c12, c44, h0, taus, tau0, q, q1]
% LEVEL 4: IDRD: ID of the UMAT RATE DEPENDENCY [n adot]
% LEVEL 5: IDUP: ID of the UMAT PARAMETER DATA SET
% LEVEL 6: IDOD: ID of type of TEXTURE INSTANCIATION w.r.t. orientation distribution:
               % io (Ideal Orientations) or do (Distributed Orientations)
% LEVEL 7: IDTI: ID of a UNIQUE TEXTURE INSTANCE sampled from IDTM
prompt = {1, 'IDGS-grain structure ID'                          , '1';...
          2, 'IDTM-Texture model ID'                            , '1';...
          3, 'IDUM-UMAT mat model ID: (1,2)'                    , '1';...
          4, 'IDRD-rate dependency ID: from(GMP_DATA_##.dat)'   , '1';...
          5, 'IDUP-UMAT par data set ID:  from(GMP_DATA_##.dat)', '1';...
          6, 'IDOD-orientation distr. ID: (io,do)'              , 'io';...
          7, 'IDTI-texture instance ID (#of texture instances'  , '3'};

dlgtitle = 'Input the ID values and # of texture instances to be sampled';
dims     = [1 50];
definput = prompt(:,3)';
IDVALUES = inputdlg(prompt(:,2)', dlgtitle, dims, definput);
% - - - - - - - - - - - - - - - - - - - - - -
IDGS = str2double(IDVALUES{1});
IDTM = str2double(IDVALUES{2});
IDUM = str2double(IDVALUES{3});
IDRD = str2double(IDVALUES{4});
IDUP = str2double(IDVALUES{5});
IDOD = str2double(IDVALUES{6});
IDTI = str2double(IDVALUES{7});
% - - - - - - - - - - - - - - - - - - - - - -
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Root_Folder = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\Chapter6\Grain_Structure_data_Repository\UMAT_DATA\';
% THE FOLLOWING SET OF FILES WILL BE WRITTEN IN "Data_Folder_1":
    % (1) "GMP_DATA_01.dat" in '~.\Chapter6\Grain_Structure_data_Repository\GMP_DATA'
    % (2) "__GS#__TM#__UM#__RD#__UP#__TY#__TI#_EuAng"
    % (3) "__GS#__TM#__UM#__RD#__UP#__TY#__TI#_UMATdata"
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
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
%------------------------------------------------
%            W    G     B    C    S
Vf_loc_B = [0.07 0.11 0.38 0.15 0.30];
Vf_loc_A = [0.04 0.12 0.42 0.13 0.26];
Vf_loc_C = [0.06 0.18 0.31 0.13 0.18];
%------------------------------------------------
TotalNumGrains = 1;NumGrainsx = 2; NumGrainsy =2; %Intentionally set unequal. DONT CHANGE
while NumGrainsx*NumGrainsy~=TotalNumGrains
    prompt = {1, 'Total number of grains'   , '48';...
              2, 'Number of grains along x' , '24';...
              3, 'Number of grains along y' , '2' };
    dlgtitle = 'Details of basic grain structure morphology';
    dims     = [1 50];
    definput = prompt(:,3)';
    GStrucMorphBase = inputdlg(prompt(:,2)', dlgtitle, dims, definput);
    TotalNumGrains = str2double(GStrucMorphBase{1});
    NumGrainsx     = str2double(GStrucMorphBase{2});
    NumGrainsy     = str2double(GStrucMorphBase{3});
    disp('PRODUCT ALONG X AND Y SHOULD EQUAL TOTAL NUMBER OF GRAINS')
end

%------------------------------------------------
prompt = {1, 'Enter texture location:', 'B';};
dlgtitle = 'TEXTURE LOCATION';
dims     = [1 40];
definput = prompt(:,3)';
TEXLOCATIONDetails = inputdlg(prompt(:,2)', dlgtitle, dims, definput);

TEXLOCATION = ['Texture location is ID: ' TEXLOCATIONDetails{1}];

switch upper(TEXLOCATION)
    case 'A'
        Vf_loc = Vf_loc_A;
    case 'B'
        Vf_loc = Vf_loc_B;
    case 'C'
        Vf_loc = Vf_loc_C;
    otherwise
        Vf_loc = Vf_loc_B;
        disp('Location entered does not match records')
        disp('I am considering location B')
end
%------------------------------------------------------------------------------------------------
%------------------------------------------------------------------------------------------------
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
%------------------------------------------------------------------------------------------------
%------------------------------------------------------------------------------------------------
for texinstance = 1:1:IDTI
    FNbase = ['__GS' IDVALUES{1} '__TM' IDVALUES{2} '__UM' IDVALUES{3},...
              '__RD' IDVALUES{4} '__UP' IDVALUES{5} '__OD.' IDVALUES{6},...
              '__TexInstance' num2str(texinstance)];
    % Adjust the volume fractions
    if sum(Vf_loc)~=1
        GreaterBy = sum(Vf_loc) - 1;
        EachGreaterBy = Vf_loc*GreaterBy;
        Vf_loc = Vf_loc - EachGreaterBy;
        sum(Vf_loc)
        if sum(Vf_loc)~=1
            ChooseThis = randperm(numel(Vf_loc), 1);
            Vf_loc(ChooseThis) = Vf_loc(ChooseThis) - (sum(Vf_loc) - 1);
        end
    end
    sum(Vf_loc)
    %------------------------------------------------
    TC_NumGrains_loc = floor(TotalNumGrains*Vf_loc);
    %------------------------------------------------
    wither = NaN(TotalNumGrains, 1);

    for TC_ID = 1:numel(TC_NumGrains_loc)
        ngtc = TC_NumGrains_loc(TC_ID);

        nanloc = find(isnan(wither));
        sel = randperm(numel(nanloc), ngtc)';

        wither(nanloc(sel))=TC_ID;
    end

    nanloc = find(isnan(wither));

    if numel(find(isnan(wither)))>0
        for count = 1:numel(nanloc)
            wither(nanloc(count)) = randi(5);
        end
    end

    TC_numGrains_final = zeros(5,1);
    for count = 1:numel(TCid)
        TC_numGrains_final(count) = numel(find(wither==TCid(count)));
    end

    ActualVf = TC_numGrains_final/TotalNumGrains;
    Vf_ratios_needed_to_actual = Vf_loc'./ActualVf;

    Eulerangles = zeros(TotalNumGrains,3);
    for count = 1:TotalNumGrains
       Eulerangles(count,:) = EA_TC(wither(count),:);
    end
    %%%%%%%%%%%%%%%%%%%%
    %Eulerangles
    %TC_numGrains_final
    %Vf_loc'
    %ActualVf
    %Vf_ratios_needed_to_actual
    %%%%%%%%%%%%%%%%%%%%
    grain_orientation_dis = reshape(wither, NumGrainsx, NumGrainsy)';

    phi1 = Eulerangles(:,1); phi  = Eulerangles(:,2); phi2 = Eulerangles(:,3);

    
    g11 = +cosd(phi1).*cosd(phi2) - sind(phi1).*sind(phi2).*cosd(phi);
    g21 = -cosd(phi1).*sind(phi2) - sind(phi1).*cosd(phi2).*cosd(phi);
    g31 = +sind(phi1).*sind(phi);
    g12 = +sind(phi1).*cosd(phi2) + cosd(phi1).*sind(phi2).*cosd(phi);
    g22 = -sind(phi1).*sind(phi2) + cosd(phi1).*cosd(phi2).*cosd(phi);
    g32 = -cosd(phi1).*sind(phi);
    g13 = sind(phi2).*sind(phi);
    g23 = cosd(phi2).*sind(phi);
    g33 = cosd(phi);
    %%%%%%%%%%%%%%%%%%%
    g132333  = [g13 g23 g33];
    g1112131 = [g11 g21 g31];

    Vector1 = [g13 g23 g33 repmat([0 0 1 0 0], size(g13,1), 1)];
    Vector2 = [g11 g21 g31 repmat([1 0 0 0 0], size(g13,1), 1)];
    %-----------------------------------------------------------------------
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
            fprintf('Writing material data for grain # %d \n', count)
            count = count + 1;
        end
    end
    fprintf('Filename is %s \n', filename)
    filepathname_EA = [Root_Folder 'EULER_ANGLES\' FNbase '__EuAng.txt'];
    dlmwrite(filepathname_EA, [phi1 phi phi2])
    filepathname_Vf = [Root_Folder 'TEX_DISTRIBUTION_INFO\' FNbase '__TexDistrData.txt'];
    dlmwrite(filepathname_Vf, [Vf_loc' ActualVf Vf_ratios_needed_to_actual TC_numGrains_final])
    filepathname_TClocTCidnames = [Root_Folder 'TEX_DISTRIBUTION_INFO\' FNbase '__TClocTCidnames.txt'];
    dlmwrite(filepathname_TClocTCidnames, TEXLOCATION, 'delimiter', '')
    dlmwrite(filepathname_TClocTCidnames, TCidnames, '-append', 'delimiter', '')
    %-----------------------------------------------------------------------
    % grain_orientation_dis
    xx = linspace(0, size(grain_orientation_dis,2)+1, size(grain_orientation_dis,2) + 1);
    xx = xx - xx(2)/2 + 1;

    yy = linspace(0, size(grain_orientation_dis,1)+1, size(grain_orientation_dis,1) + 1);
    yy = yy - yy(2)/2 + 1;
    [xx, yy] = meshgrid(xx, yy);

    patches = cell(size(grain_orientation_dis));
    for r = 1:size(grain_orientation_dis, 1)
        for c = 1:size(grain_orientation_dis, 2)
            patches{r,c} = [xx(r, c)     yy(r,c);
                            xx(r+1, c)   yy(r+1,c);
                            xx(r+1, c+1) yy(r+1,c+1);
                            xx(r, c+1)   yy(r,c+1)];
        end
    end
    
    figurehandle = figure;
    hold on
    patchcolors = {'g', 'b', 'r', 'm', 'c'};
    for count = 1:numel(patches)
        patch(patches{count}(:,1)', patches{count}(:,2)', patchcolors{grain_orientation_dis(count)})
    end


    axis equal
    TitleTextLine1 = [num2str(TotalNumGrains) '_' num2str(NumGrainsx) '_' num2str(NumGrainsy) '_' FNbase];
    
    ht = title(TitleTextLine1);
    axis tight
    cbh = colorbar('Ticks',[1, 2, 3, 4, 5, 6], 'TickLabels', {'W','G','B','C','S', '.'}, 'location', 'southoutside');
    haha = colormap([0 1 0;
                     0 0 1;
                     1 0 0;
                     1 0 1;
                     0 1 1]);
    cpos = cbh.Position;

    set(cbh, 'Position', [1.5*cpos(1) 0.6*cpos(2) 0.8*cpos(3) 3*cpos(4)])
    caxis([1 5])
    set(gca, 'fontsize', 14)
    set(ht,  'fontsize', 10)
    set(cbh, 'fontsize', 12)
    set(cbh, 'FontWeight', 'normal')
    set(cbh, 'FontWeight', 'normal')
    set(ht, 'FontWeight', 'normal')
    set(gca,'XColor', 'none','YColor','none')
    figurecount = startfigurenumber+1;
    imagename = [FNbase '__' num2str(TotalNumGrains) '_' num2str(NumGrainsx) '_' num2str(NumGrainsy) '.tiff'];
    imagefilepath = [Root_Folder 'TEX_DISTRIBUTION_INFO\'];
    imagefilepathname = [imagefilepath imagename];
    print('-dtiff', imagefilepathname)
    pause(0.1)
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end