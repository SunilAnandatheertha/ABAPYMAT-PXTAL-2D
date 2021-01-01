function [Vector1, Vector2] = CHK_gen_umat_data_BUILD_HKL_UVW_VECTORS_V1(g11, g21, g31, g12, g22, g32, g13, g23, g33, hklparallel, uvwparallel)

hkl = [g13 g23 g33];
uvw = [g11 g21 g31]; 
% Vector1 = [g13 g23 g33 repmat([0 0 1 0 0], size(g13,1), 1)];
% Vector2 = [g11 g21 g31 repmat([1 0 0 0 0], size(g13,1), 1)];
Vector1 = [hkl repmat([hklparallel 0 0], size(g13,1), 1)];
Vector2 = [uvw repmat([uvwparallel 0 0], size(g13,1), 1)];
%     % Following 3 are the D.C's of [1 0 0], [0 1 0], [0 0 1] in sample coordinate system
%     sample100 = [g11 g12 g13]
%     sample010 = [g21 g22 g23]
%     sample001 = [g31 g32 g33]
%     % The following 3 are the D.C's (i.e., hkl or uvw) for RD, TD and ND in crystal coordinate system
%     crystal_uvw_RD = [g11 g21 g31]
%     crystal_____TD = [g12 g22 g32]
%     crystal_hkl_ND = [g13 g23 g33]
% - - - - - - - - - - - - - - - - - - - - - -
end