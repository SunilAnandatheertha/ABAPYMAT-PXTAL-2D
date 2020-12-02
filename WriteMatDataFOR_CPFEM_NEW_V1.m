%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


Grain_Structure_ID_10digit_number = num2str(randi(1e10));


EASetRanumNumber = num2str(randi(1e10));
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DataFolder = 'C:\Users\anandats\OneDrive - Coventry University\coventry-thesis\MATLAB codes\Grain_Structure_data_Repository\';
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
EA_TC  = [00 90 00;  % Cube
          00 45 00;  % Goss
          35 45 00;  % Brass 
          90 35 45;  % Copper
          59 37 63]; % S
%------------------------------------------------
Ntc  = 5; % Number of TC
TCid = [1 2 3 4 5]; % TC id number
%------------------------------------------------
%            W    G     B    C    S
Vf_loc_B = [0.07 0.11 0.38 0.15 0.30];
Vf_loc_A = [0.04 0.12 0.42 0.13 0.26];
Vf_loc_C = [0.06 0.18 0.31 0.13 0.18];
%------------------------------------------------
TotalNumGrains = 48;
NumGrainsx     = 24;
NumGrainsy     = 2;
%------------------------------------------------
Vf_loc = Vf_loc_B;
%------------------------------------------------
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
Eulerangles
TC_numGrains_final
Vf_loc'
ActualVf
Vf_ratios_needed_to_actual
grain_orientation_dis = reshape(wither, NumGrainsx, NumGrainsy)';

phi1 = Eulerangles(:,1); phi  = Eulerangles(:,2); phi2 = Eulerangles(:,3);

dlmwrite([DataFolder Grain_Structure_ID_10digit_number '_EulerAngles_SetNum_' EASetRanumNumber '.txt'], [phi1 phi phi2])
%%%%%%%%%%%%%%%%%%%%
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
g132333  = [g13 g23 g33]
g1112131 = [g11 g21 g31]

Vector1 = [g13 g23 g33 repmat([0 0 1 0 0], size(g13,1), 1)];
Vector2 = [g11 g21 g31 repmat([1 0 0 0 0], size(g13,1), 1)];

%-----------------------------------------------------------------------
MATDATA = [168400.,121400., 75400.,     0.,     0.,     0.,     0.,     0. % 01
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 02
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 03
            1.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 04
            1.,     1.,     1.,     1.,     1.,     0.,     0.,     0.     % 05
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 06
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 07
           -1.,     0.,     1.,     0.,     0.,     1.,     0.,     0.     % 08  % VECTOR 1
            0.,     1.,     0.,     1.,     0.,     0.,     0.,     0.     % 09  % VECTOR 2
           10.,  0.001,     0.,     0.,     0.,     0.,     0.,     0.     % 10
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 11
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 12
            541.5,  109.5,   60.8,     0.,     0.,     0.,     0.,     0.  % 13
            1.,     1.,     0.,     0.,     0.,     0.,     0.,     0.     % 14
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 15
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 16
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 17
            0.,     0.,     0.,     0.,     0.,     0.,     0.,     0.     % 18
            0.5,     1.,     0.,     0.,     0.,     0.,     0.,     0.    % 19
            1.,    10.,  1e-05,     0.,     0.,     0.,     0.,     0.];   % 20
%-----------------------------------------------------------------------
count = 1;
filename = [Grain_Structure_ID_10digit_number '_MaterialData_SetNum_' EASetRanumNumber '.txt'];
for gx = 1:NumGrainsx
    for gy = 1:NumGrainsy
        dlmwrite([DataFolder filename], ['*Material, name = Mat_Grain_Nx_' num2str(gx) '_Ny_' num2str(gy)], '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite([DataFolder filename], '*Depvar', '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite([DataFolder filename], ['   125,'], '-append', 'delimiter', '', 'precision', '%10.4f')
        dlmwrite([DataFolder filename], '*User Material, constants=160, unsymm', '-append', 'delimiter', '', 'precision', '%10.4f')
        datatowrite = [MATDATA(1:7,:); Vector1(count,:); Vector2(count,:); MATDATA(10:20,:)];
        dlmwrite([DataFolder filename], datatowrite, '-append', 'delimiter', ',', 'precision', '%10.4f')
        fprintf('Writing material data for grain # %d \n', count)
        count = count + 1;
    end
end
fprintf('Filename is %s \n', filename)