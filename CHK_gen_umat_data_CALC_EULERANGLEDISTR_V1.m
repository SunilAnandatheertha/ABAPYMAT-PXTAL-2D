function [TC_NumGrains_loc, TC_numGrains_final, ActualVf, Vf_ratios_needed_to_actual, grain_orientation_dis, phi1, phi, phi2] = CHK_gen_umat_data_CALC_EULERANGLEDISTR_V1(TotalNumGrains, Vf_loc, EA_TC, TCid, NumGrainsx, NumGrainsy)

TC_NumGrains_loc = floor(TotalNumGrains*Vf_loc);
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
Vf_ratios_needed_to_actual = ActualVf./Vf_loc';

Eulerangles = zeros(TotalNumGrains,3);
for count = 1:TotalNumGrains
   Eulerangles(count,:) = EA_TC(wither(count),:);
end
%%%%%%%%%%%%%%%%%%%%
%Eulerangles
%TC_numGrains_final
%Vf_loc'
%Vf_ratios_needed_to_actual
%%%%%%%%%%%%%%%%%%%%
grain_orientation_dis = reshape(wither, NumGrainsx, NumGrainsy)';

phi1 = Eulerangles(:,1); phi  = Eulerangles(:,2); phi2 = Eulerangles(:,3);


end