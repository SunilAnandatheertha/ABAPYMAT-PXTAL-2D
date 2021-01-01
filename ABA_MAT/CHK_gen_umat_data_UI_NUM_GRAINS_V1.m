function [TotalNumGrains, NumGrainsx, NumGrainsy] = CHK_gen_umat_data_UI_NUM_GRAINS_V1()

TotalNumGrains = 1; NumGrainsx = 2; NumGrainsy = 2; %Intentionally set unequal. DONT CHANGE
while NumGrainsx*NumGrainsy~=TotalNumGrains
    prompt = {1, 'Total number of grains'   , '192';...
              2, 'Number of grains along x' , '96';...
              3, 'Number of grains along y' , '2' };
    dlgtitle = 'Details of basic grain structure morphology';
    dims     = [1 50];
    definput = prompt(:,3)';
    GStrucMorphBase = inputdlg(prompt(:,2)', dlgtitle, dims, definput);
    TotalNumGrains = str2double(GStrucMorphBase{1});
    NumGrainsx     = str2double(GStrucMorphBase{2});
    NumGrainsy     = str2double(GStrucMorphBase{3});
    if NumGrainsx*NumGrainsy~=TotalNumGrains
        disp('PRODUCT ALONG X AND Y SHOULD EQUAL TOTAL NUMBER OF GRAINS')
    end
end
end