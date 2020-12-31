function [TEXLOCATIONDetails, TEXLOCATION] = CHK_gen_umat_data_UI_ACQUIRE_TEX_LOC_DETAILS_V1()

prompt = {1, 'Enter texture location:', 'B';};
dlgtitle = 'TEXTURE LOCATION';
dims     = [1 40];
definput = prompt(:,3)';
TEXLOCATIONDetails = inputdlg(prompt(:,2)', dlgtitle, dims, definput);

TEXLOCATION = ['Texture location is ID: ' TEXLOCATIONDetails{1}];
end