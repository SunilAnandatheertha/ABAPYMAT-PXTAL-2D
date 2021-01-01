function [IDVALUES, IDGS, IDTM, IDUM, IDRD, IDUP, IDOD, IDTI, IDETItoGTEX, IDETI, IDSim] = CHK_gen_umat_data_ACQUIRE_PRELIMINARY_INPUTS_V1()

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

prompt = {01, 'IDGS  - grain structure ID'                          , '1';...
          02, 'IDTM  - Texture model ID'                            , '1';...
          03, 'IDUM  - UMAT mat model ID: (1(use this for now), 2)' , '1';...
          04, 'IDRD  - rate dependency ID: from(GMP_DATA_##.dat)'   , '1';...
          05, 'IDUP  - UMAT par data set ID:  from(GMP_DATA_##.dat)', '1';...
          06, 'IDOD  - orientation distr. ID: (io,do)'              , 'io';...
          07, 'IDTI  - # of texture instances' , '4';...
          08, 'IDETItoGTEX - equi-tex-instanciate all (Ngx,Ngy) permutations to one global texture ? (enter: 0-no, 1-yes)', '1';...
          09, 'IDETI - equi-tex-instanciate all texture instances for a given (ngx,ngy)? (enter: 0-no, 1-yes)', '1';...
          10, 'IDSim - Enter the simulation number ID'              , '19'};

dlgtitle = 'Input the ID values and # of texture instances to be sampled';
dims     = [1 120];
definput = prompt(:,3)';
IDVALUES = inputdlg(prompt(:,2)', dlgtitle, dims, definput);
% - - - - - - - - - - - - - - - - - - - - - -
IDGS        = str2double(IDVALUES{01});
IDTM        = str2double(IDVALUES{02});
IDUM        = str2double(IDVALUES{03});
IDRD        = str2double(IDVALUES{04});
IDUP        = str2double(IDVALUES{05});
IDOD        = str2double(IDVALUES{06});
IDTI        = str2double(IDVALUES{07});
IDETItoGTEX = str2double(IDVALUES{08});
IDETI       = str2double(IDVALUES{09});
IDSim       = str2double(IDVALUES{10});

end