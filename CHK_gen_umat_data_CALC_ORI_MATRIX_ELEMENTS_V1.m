function [g11, g21, g31, g12, g22, g32, g13, g23, g33] = CHK_gen_umat_data_CALC_ORI_MATRIX_ELEMENTS_V1(phi1, phi, phi2)

g11 = +cosd(phi1).*cosd(phi2) - sind(phi1).*sind(phi2).*cosd(phi);
g21 = -cosd(phi1).*sind(phi2) - sind(phi1).*cosd(phi2).*cosd(phi);
g31 = +sind(phi1).*sind(phi);
g12 = +sind(phi1).*cosd(phi2) + cosd(phi1).*sind(phi2).*cosd(phi);
g22 = -sind(phi1).*sind(phi2) + cosd(phi1).*cosd(phi2).*cosd(phi);
g32 = -cosd(phi1).*sind(phi);
g13 = sind(phi2).*sind(phi);
g23 = cosd(phi2).*sind(phi);
g33 = cosd(phi);

end