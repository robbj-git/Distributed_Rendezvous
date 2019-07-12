% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(b_0*(x_0 - xb), Q) + quad_form(u_0, R) + quad_form(b_1*(x_1 - xb), Q) + quad_form(u_1, R) + quad_form(b_2*(x_2 - xb), Q) + quad_form(u_2, R) + quad_form(b_3*(x_3 - xb), Q) + quad_form(u_3, R) + quad_form(b_4*(x_4 - xb), Q) + quad_form(u_4, R) + quad_form(b_5*(x_5 - xb), Q) + quad_form(u_5, R) + quad_form(b_6*(x_6 - xb), Q) + quad_form(u_6, R) + quad_form(b_7*(x_7 - xb), Q) + quad_form(u_7, R) + quad_form(b_8*(x_8 - xb), Q) + quad_form(u_8, R) + quad_form(b_9*(x_9 - xb), Q) + quad_form(u_9, R) + quad_form(b_10*(x_10 - xb), Q) + quad_form(u_10, R) + quad_form(b_11*(x_11 - xb), Q) + quad_form(u_11, R) + quad_form(b_12*(x_12 - xb), Q) + quad_form(u_12, R) + quad_form(b_13*(x_13 - xb), Q) + quad_form(u_13, R) + quad_form(b_14*(x_14 - xb), Q) + quad_form(u_14, R) + quad_form(b_15*(x_15 - xb), Q) + quad_form(u_15, R) + quad_form(b_16*(x_16 - xb), Q) + quad_form(u_16, R) + quad_form(b_17*(x_17 - xb), Q) + quad_form(u_17, R) + quad_form(b_18*(x_18 - xb), Q) + quad_form(u_18, R) + quad_form(b_19*(x_19 - xb), Q) + quad_form(u_19, R) + quad_form(b_20*(x_20 - xb), Q) + quad_form(u_20, R) + quad_form(b_21*(x_21 - xb), Q) + quad_form(u_21, R) + quad_form(b_22*(x_22 - xb), Q) + quad_form(u_22, R) + quad_form(b_23*(x_23 - xb), Q) + quad_form(u_23, R) + quad_form(b_24*(x_24 - xb), Q) + quad_form(u_24, R) + quad_form(b_25*(x_25 - xb), P))
%   subject to
%     x_1 == A*x_0 + B*u_0
%     x_2 == A*x_1 + B*u_1
%     x_3 == A*x_2 + B*u_2
%     x_4 == A*x_3 + B*u_3
%     x_5 == A*x_4 + B*u_4
%     x_6 == A*x_5 + B*u_5
%     x_7 == A*x_6 + B*u_6
%     x_8 == A*x_7 + B*u_7
%     x_9 == A*x_8 + B*u_8
%     x_10 == A*x_9 + B*u_9
%     x_11 == A*x_10 + B*u_10
%     x_12 == A*x_11 + B*u_11
%     x_13 == A*x_12 + B*u_12
%     x_14 == A*x_13 + B*u_13
%     x_15 == A*x_14 + B*u_14
%     x_16 == A*x_15 + B*u_15
%     x_17 == A*x_16 + B*u_16
%     x_18 == A*x_17 + B*u_17
%     x_19 == A*x_18 + B*u_18
%     x_20 == A*x_19 + B*u_19
%     x_21 == A*x_20 + B*u_20
%     x_22 == A*x_21 + B*u_21
%     x_23 == A*x_22 + B*u_22
%     x_24 == A*x_23 + B*u_23
%     x_25 == A*x_24 + B*u_24
%     wmin <= x_1(2)
%     wmin <= x_2(2)
%     wmin <= x_3(2)
%     wmin <= x_4(2)
%     wmin <= x_5(2)
%     wmin <= x_6(2)
%     wmin <= x_7(2)
%     wmin <= x_8(2)
%     wmin <= x_9(2)
%     wmin <= x_10(2)
%     wmin <= x_11(2)
%     wmin <= x_12(2)
%     wmin <= x_13(2)
%     wmin <= x_14(2)
%     wmin <= x_15(2)
%     wmin <= x_16(2)
%     wmin <= x_17(2)
%     wmin <= x_18(2)
%     wmin <= x_19(2)
%     wmin <= x_20(2)
%     wmin <= x_21(2)
%     wmin <= x_22(2)
%     wmin <= x_23(2)
%     wmin <= x_24(2)
%     wmin <= x_25(2)
%     wmin <= u_0
%     wmin <= u_1
%     wmin <= u_2
%     wmin <= u_3
%     wmin <= u_4
%     wmin <= u_5
%     wmin <= u_6
%     wmin <= u_7
%     wmin <= u_8
%     wmin <= u_9
%     wmin <= u_10
%     wmin <= u_11
%     wmin <= u_12
%     wmin <= u_13
%     wmin <= u_14
%     wmin <= u_15
%     wmin <= u_16
%     wmin <= u_17
%     wmin <= u_18
%     wmin <= u_19
%     wmin <= u_20
%     wmin <= u_21
%     wmin <= u_22
%     wmin <= u_23
%     wmin <= u_24
%     u_0 <= wmax
%     u_1 <= wmax
%     u_2 <= wmax
%     u_3 <= wmax
%     u_4 <= wmax
%     u_5 <= wmax
%     u_6 <= wmax
%     u_7 <= wmax
%     u_8 <= wmax
%     u_9 <= wmax
%     u_10 <= wmax
%     u_11 <= wmax
%     u_12 <= wmax
%     u_13 <= wmax
%     u_14 <= wmax
%     u_15 <= wmax
%     u_16 <= wmax
%     u_17 <= wmax
%     u_18 <= wmax
%     u_19 <= wmax
%     u_20 <= wmax
%     u_21 <= wmax
%     u_22 <= wmax
%     u_23 <= wmax
%     u_24 <= wmax
%     b_1*x_1(2) >=  - kl*x_1(1) + wmin_land
%     b_2*x_2(2) >=  - kl*x_2(1) + wmin_land
%     b_3*x_3(2) >=  - kl*x_3(1) + wmin_land
%     b_4*x_4(2) >=  - kl*x_4(1) + wmin_land
%     b_5*x_5(2) >=  - kl*x_5(1) + wmin_land
%     b_6*x_6(2) >=  - kl*x_6(1) + wmin_land
%     b_7*x_7(2) >=  - kl*x_7(1) + wmin_land
%     b_8*x_8(2) >=  - kl*x_8(1) + wmin_land
%     b_9*x_9(2) >=  - kl*x_9(1) + wmin_land
%     b_10*x_10(2) >=  - kl*x_10(1) + wmin_land
%     b_11*x_11(2) >=  - kl*x_11(1) + wmin_land
%     b_12*x_12(2) >=  - kl*x_12(1) + wmin_land
%     b_13*x_13(2) >=  - kl*x_13(1) + wmin_land
%     b_14*x_14(2) >=  - kl*x_14(1) + wmin_land
%     b_15*x_15(2) >=  - kl*x_15(1) + wmin_land
%     b_16*x_16(2) >=  - kl*x_16(1) + wmin_land
%     b_17*x_17(2) >=  - kl*x_17(1) + wmin_land
%     b_18*x_18(2) >=  - kl*x_18(1) + wmin_land
%     b_19*x_19(2) >=  - kl*x_19(1) + wmin_land
%     b_20*x_20(2) >=  - kl*x_20(1) + wmin_land
%     b_21*x_21(2) >=  - kl*x_21(1) + wmin_land
%     b_22*x_22(2) >=  - kl*x_22(1) + wmin_land
%     b_23*x_23(2) >=  - kl*x_23(1) + wmin_land
%     b_24*x_24(2) >=  - kl*x_24(1) + wmin_land
%     b_25*x_25(2) >=  - kl*x_25(1) + wmin_land
%     x_1(1) >= 0
%     x_2(1) >= 0
%     x_3(1) >= 0
%     x_4(1) >= 0
%     x_5(1) >= 0
%     x_6(1) >= 0
%     x_7(1) >= 0
%     x_8(1) >= 0
%     x_9(1) >= 0
%     x_10(1) >= 0
%     x_11(1) >= 0
%     x_12(1) >= 0
%     x_13(1) >= 0
%     x_14(1) >= 0
%     x_15(1) >= 0
%     x_16(1) >= 0
%     x_17(1) >= 0
%     x_18(1) >= 0
%     x_19(1) >= 0
%     x_20(1) >= 0
%     x_21(1) >= 0
%     x_22(1) >= 0
%     x_23(1) >= 0
%     x_24(1) >= 0
%     x_25(1) >= 0
%     b_1*dist_1*hs + (dl - ds)*x_1(1) <= dl*hs
%     b_2*dist_2*hs + (dl - ds)*x_2(1) <= dl*hs
%     b_3*dist_3*hs + (dl - ds)*x_3(1) <= dl*hs
%     b_4*dist_4*hs + (dl - ds)*x_4(1) <= dl*hs
%     b_5*dist_5*hs + (dl - ds)*x_5(1) <= dl*hs
%     b_6*dist_6*hs + (dl - ds)*x_6(1) <= dl*hs
%     b_7*dist_7*hs + (dl - ds)*x_7(1) <= dl*hs
%     b_8*dist_8*hs + (dl - ds)*x_8(1) <= dl*hs
%     b_9*dist_9*hs + (dl - ds)*x_9(1) <= dl*hs
%     b_10*dist_10*hs + (dl - ds)*x_10(1) <= dl*hs
%     b_11*dist_11*hs + (dl - ds)*x_11(1) <= dl*hs
%     b_12*dist_12*hs + (dl - ds)*x_12(1) <= dl*hs
%     b_13*dist_13*hs + (dl - ds)*x_13(1) <= dl*hs
%     b_14*dist_14*hs + (dl - ds)*x_14(1) <= dl*hs
%     b_15*dist_15*hs + (dl - ds)*x_15(1) <= dl*hs
%     b_16*dist_16*hs + (dl - ds)*x_16(1) <= dl*hs
%     b_17*dist_17*hs + (dl - ds)*x_17(1) <= dl*hs
%     b_18*dist_18*hs + (dl - ds)*x_18(1) <= dl*hs
%     b_19*dist_19*hs + (dl - ds)*x_19(1) <= dl*hs
%     b_20*dist_20*hs + (dl - ds)*x_20(1) <= dl*hs
%     b_21*dist_21*hs + (dl - ds)*x_21(1) <= dl*hs
%     b_22*dist_22*hs + (dl - ds)*x_22(1) <= dl*hs
%     b_23*dist_23*hs + (dl - ds)*x_23(1) <= dl*hs
%     b_24*dist_24*hs + (dl - ds)*x_24(1) <= dl*hs
%     b_25*dist_25*hs + (dl - ds)*x_25(1) <= dl*hs
%
% with variables
%      u_0   1 x 1
%      u_1   1 x 1
%      u_2   1 x 1
%      u_3   1 x 1
%      u_4   1 x 1
%      u_5   1 x 1
%      u_6   1 x 1
%      u_7   1 x 1
%      u_8   1 x 1
%      u_9   1 x 1
%     u_10   1 x 1
%     u_11   1 x 1
%     u_12   1 x 1
%     u_13   1 x 1
%     u_14   1 x 1
%     u_15   1 x 1
%     u_16   1 x 1
%     u_17   1 x 1
%     u_18   1 x 1
%     u_19   1 x 1
%     u_20   1 x 1
%     u_21   1 x 1
%     u_22   1 x 1
%     u_23   1 x 1
%     u_24   1 x 1
%      x_1   2 x 1
%      x_2   2 x 1
%      x_3   2 x 1
%      x_4   2 x 1
%      x_5   2 x 1
%      x_6   2 x 1
%      x_7   2 x 1
%      x_8   2 x 1
%      x_9   2 x 1
%     x_10   2 x 1
%     x_11   2 x 1
%     x_12   2 x 1
%     x_13   2 x 1
%     x_14   2 x 1
%     x_15   2 x 1
%     x_16   2 x 1
%     x_17   2 x 1
%     x_18   2 x 1
%     x_19   2 x 1
%     x_20   2 x 1
%     x_21   2 x 1
%     x_22   2 x 1
%     x_23   2 x 1
%     x_24   2 x 1
%     x_25   2 x 1
%
% and parameters
%        A   2 x 2
%        B   2 x 1
%        P   2 x 2    PSD
%        Q   2 x 2    PSD
%        R   1 x 1    PSD
%      b_0   1 x 1
%      b_1   1 x 1
%      b_2   1 x 1
%      b_3   1 x 1
%      b_4   1 x 1
%      b_5   1 x 1
%      b_6   1 x 1
%      b_7   1 x 1
%      b_8   1 x 1
%      b_9   1 x 1
%     b_10   1 x 1
%     b_11   1 x 1
%     b_12   1 x 1
%     b_13   1 x 1
%     b_14   1 x 1
%     b_15   1 x 1
%     b_16   1 x 1
%     b_17   1 x 1
%     b_18   1 x 1
%     b_19   1 x 1
%     b_20   1 x 1
%     b_21   1 x 1
%     b_22   1 x 1
%     b_23   1 x 1
%     b_24   1 x 1
%     b_25   1 x 1
%   dist_1   1 x 1
%   dist_2   1 x 1
%   dist_3   1 x 1
%   dist_4   1 x 1
%   dist_5   1 x 1
%   dist_6   1 x 1
%   dist_7   1 x 1
%   dist_8   1 x 1
%   dist_9   1 x 1
%  dist_10   1 x 1
%  dist_11   1 x 1
%  dist_12   1 x 1
%  dist_13   1 x 1
%  dist_14   1 x 1
%  dist_15   1 x 1
%  dist_16   1 x 1
%  dist_17   1 x 1
%  dist_18   1 x 1
%  dist_19   1 x 1
%  dist_20   1 x 1
%  dist_21   1 x 1
%  dist_22   1 x 1
%  dist_23   1 x 1
%  dist_24   1 x 1
%  dist_25   1 x 1
%       dl   1 x 1
%       ds   1 x 1
%       hs   1 x 1
%       kl   1 x 1    positive
%     wmax   1 x 1    positive
%     wmin   1 x 1    negative
% wmin_land   1 x 1    negative
%      x_0   2 x 1
%       xb   2 x 1
%
% Note:
%   - Check status.converged, which will be 1 if optimization succeeded.
%   - You don't have to specify settings if you don't want to.
%   - To hide output, use settings.verbose = 0.
%   - To change iterations, use settings.max_iters = 20.
%   - You may wish to compare with cvxsolve to check the solver is correct.
%
% Specify params.A, ..., params.xb, then run
%   [vars, status] = csolve(params, settings)
% Produced by CVXGEN, 2019-04-23 04:29:21 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
