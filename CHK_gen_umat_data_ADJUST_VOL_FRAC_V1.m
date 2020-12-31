function [Vf_loc] = CHK_gen_umat_data_ADJUST_VOL_FRAC_V1(Vf_loc)

% Adjust the volume fractions
if sum(Vf_loc)~=1
    GreaterBy = sum(Vf_loc) - 1;
    EachGreaterBy = Vf_loc*GreaterBy;
    Vf_loc = Vf_loc - EachGreaterBy;
    %sum(Vf_loc)
    if sum(Vf_loc)~=1
        ChooseThis = randperm(numel(Vf_loc), 1);
        Vf_loc(ChooseThis) = Vf_loc(ChooseThis) - (sum(Vf_loc) - 1);
    end
end
%sum(Vf_loc)
end