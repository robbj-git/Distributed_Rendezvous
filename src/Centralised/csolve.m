% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(x_0 - xb_0, Q) + quad_form(u_0, R) + quad_form(ub_0, R) + quad_form(x_1 - xb_1, Q) + quad_form(u_1, R) + quad_form(ub_1, R) + quad_form(x_2 - xb_2, Q) + quad_form(u_2, R) + quad_form(ub_2, R) + quad_form(x_3 - xb_3, Q) + quad_form(u_3, R) + quad_form(ub_3, R) + quad_form(x_4 - xb_4, Q) + quad_form(u_4, R) + quad_form(ub_4, R) + quad_form(x_5 - xb_5, Q) + quad_form(u_5, R) + quad_form(ub_5, R) + quad_form(x_6 - xb_6, Q) + quad_form(u_6, R) + quad_form(ub_6, R) + quad_form(x_7 - xb_7, Q) + quad_form(u_7, R) + quad_form(ub_7, R) + quad_form(x_8 - xb_8, Q) + quad_form(u_8, R) + quad_form(ub_8, R) + quad_form(x_9 - xb_9, Q) + quad_form(u_9, R) + quad_form(ub_9, R) + quad_form(x_10 - xb_10, Q) + quad_form(u_10, R) + quad_form(ub_10, R) + quad_form(x_11 - xb_11, Q) + quad_form(u_11, R) + quad_form(ub_11, R) + quad_form(x_12 - xb_12, Q) + quad_form(u_12, R) + quad_form(ub_12, R) + quad_form(x_13 - xb_13, Q) + quad_form(u_13, R) + quad_form(ub_13, R) + quad_form(x_14 - xb_14, Q) + quad_form(u_14, R) + quad_form(ub_14, R) + quad_form(x_15 - xb_15, Q) + quad_form(u_15, R) + quad_form(ub_15, R) + quad_form(x_16 - xb_16, Q) + quad_form(u_16, R) + quad_form(ub_16, R) + quad_form(x_17 - xb_17, Q) + quad_form(u_17, R) + quad_form(ub_17, R) + quad_form(x_18 - xb_18, Q) + quad_form(u_18, R) + quad_form(ub_18, R) + quad_form(x_19 - xb_19, Q) + quad_form(u_19, R) + quad_form(ub_19, R) + quad_form(x_20 - xb_20, Q) + quad_form(u_20, R) + quad_form(ub_20, R) + quad_form(x_21 - xb_21, Q) + quad_form(u_21, R) + quad_form(ub_21, R) + quad_form(x_22 - xb_22, Q) + quad_form(u_22, R) + quad_form(ub_22, R) + quad_form(x_23 - xb_23, Q) + quad_form(u_23, R) + quad_form(ub_23, R) + quad_form(x_24 - xb_24, Q) + quad_form(u_24, R) + quad_form(ub_24, R) + quad_form(x_25 - xb_25, P))
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
%     xb_1 == Ab*xb_0 + Bb*ub_0
%     xb_2 == Ab*xb_1 + Bb*ub_1
%     xb_3 == Ab*xb_2 + Bb*ub_2
%     xb_4 == Ab*xb_3 + Bb*ub_3
%     xb_5 == Ab*xb_4 + Bb*ub_4
%     xb_6 == Ab*xb_5 + Bb*ub_5
%     xb_7 == Ab*xb_6 + Bb*ub_6
%     xb_8 == Ab*xb_7 + Bb*ub_7
%     xb_9 == Ab*xb_8 + Bb*ub_8
%     xb_10 == Ab*xb_9 + Bb*ub_9
%     xb_11 == Ab*xb_10 + Bb*ub_10
%     xb_12 == Ab*xb_11 + Bb*ub_11
%     xb_13 == Ab*xb_12 + Bb*ub_12
%     xb_14 == Ab*xb_13 + Bb*ub_13
%     xb_15 == Ab*xb_14 + Bb*ub_14
%     xb_16 == Ab*xb_15 + Bb*ub_15
%     xb_17 == Ab*xb_16 + Bb*ub_16
%     xb_18 == Ab*xb_17 + Bb*ub_17
%     xb_19 == Ab*xb_18 + Bb*ub_18
%     xb_20 == Ab*xb_19 + Bb*ub_19
%     xb_21 == Ab*xb_20 + Bb*ub_20
%     xb_22 == Ab*xb_21 + Bb*ub_21
%     xb_23 == Ab*xb_22 + Bb*ub_22
%     xb_24 == Ab*xb_23 + Bb*ub_23
%     xb_25 == Ab*xb_24 + Bb*ub_24
%     amin <= u_0
%     amin <= u_1
%     amin <= u_2
%     amin <= u_3
%     amin <= u_4
%     amin <= u_5
%     amin <= u_6
%     amin <= u_7
%     amin <= u_8
%     amin <= u_9
%     amin <= u_10
%     amin <= u_11
%     amin <= u_12
%     amin <= u_13
%     amin <= u_14
%     amin <= u_15
%     amin <= u_16
%     amin <= u_17
%     amin <= u_18
%     amin <= u_19
%     amin <= u_20
%     amin <= u_21
%     amin <= u_22
%     amin <= u_23
%     amin <= u_24
%     u_0 <= amax
%     u_1 <= amax
%     u_2 <= amax
%     u_3 <= amax
%     u_4 <= amax
%     u_5 <= amax
%     u_6 <= amax
%     u_7 <= amax
%     u_8 <= amax
%     u_9 <= amax
%     u_10 <= amax
%     u_11 <= amax
%     u_12 <= amax
%     u_13 <= amax
%     u_14 <= amax
%     u_15 <= amax
%     u_16 <= amax
%     u_17 <= amax
%     u_18 <= amax
%     u_19 <= amax
%     u_20 <= amax
%     u_21 <= amax
%     u_22 <= amax
%     u_23 <= amax
%     u_24 <= amax
%     amin_b <= ub_0
%     amin_b <= ub_1
%     amin_b <= ub_2
%     amin_b <= ub_3
%     amin_b <= ub_4
%     amin_b <= ub_5
%     amin_b <= ub_6
%     amin_b <= ub_7
%     amin_b <= ub_8
%     amin_b <= ub_9
%     amin_b <= ub_10
%     amin_b <= ub_11
%     amin_b <= ub_12
%     amin_b <= ub_13
%     amin_b <= ub_14
%     amin_b <= ub_15
%     amin_b <= ub_16
%     amin_b <= ub_17
%     amin_b <= ub_18
%     amin_b <= ub_19
%     amin_b <= ub_20
%     amin_b <= ub_21
%     amin_b <= ub_22
%     amin_b <= ub_23
%     amin_b <= ub_24
%     ub_0 <= amax_b
%     ub_1 <= amax_b
%     ub_2 <= amax_b
%     ub_3 <= amax_b
%     ub_4 <= amax_b
%     ub_5 <= amax_b
%     ub_6 <= amax_b
%     ub_7 <= amax_b
%     ub_8 <= amax_b
%     ub_9 <= amax_b
%     ub_10 <= amax_b
%     ub_11 <= amax_b
%     ub_12 <= amax_b
%     ub_13 <= amax_b
%     ub_14 <= amax_b
%     ub_15 <= amax_b
%     ub_16 <= amax_b
%     ub_17 <= amax_b
%     ub_18 <= amax_b
%     ub_19 <= amax_b
%     ub_20 <= amax_b
%     ub_21 <= amax_b
%     ub_22 <= amax_b
%     ub_23 <= amax_b
%     ub_24 <= amax_b
%     -vmax <= x_1(3)
%     -vmax <= x_2(3)
%     -vmax <= x_3(3)
%     -vmax <= x_4(3)
%     -vmax <= x_5(3)
%     -vmax <= x_6(3)
%     -vmax <= x_7(3)
%     -vmax <= x_8(3)
%     -vmax <= x_9(3)
%     -vmax <= x_10(3)
%     -vmax <= x_11(3)
%     -vmax <= x_12(3)
%     -vmax <= x_13(3)
%     -vmax <= x_14(3)
%     -vmax <= x_15(3)
%     -vmax <= x_16(3)
%     -vmax <= x_17(3)
%     -vmax <= x_18(3)
%     -vmax <= x_19(3)
%     -vmax <= x_20(3)
%     -vmax <= x_21(3)
%     -vmax <= x_22(3)
%     -vmax <= x_23(3)
%     -vmax <= x_24(3)
%     -vmax <= x_25(3)
%     x_1(3) <= vmax
%     x_2(3) <= vmax
%     x_3(3) <= vmax
%     x_4(3) <= vmax
%     x_5(3) <= vmax
%     x_6(3) <= vmax
%     x_7(3) <= vmax
%     x_8(3) <= vmax
%     x_9(3) <= vmax
%     x_10(3) <= vmax
%     x_11(3) <= vmax
%     x_12(3) <= vmax
%     x_13(3) <= vmax
%     x_14(3) <= vmax
%     x_15(3) <= vmax
%     x_16(3) <= vmax
%     x_17(3) <= vmax
%     x_18(3) <= vmax
%     x_19(3) <= vmax
%     x_20(3) <= vmax
%     x_21(3) <= vmax
%     x_22(3) <= vmax
%     x_23(3) <= vmax
%     x_24(3) <= vmax
%     x_25(3) <= vmax
%     -vmax <= x_1(4)
%     -vmax <= x_2(4)
%     -vmax <= x_3(4)
%     -vmax <= x_4(4)
%     -vmax <= x_5(4)
%     -vmax <= x_6(4)
%     -vmax <= x_7(4)
%     -vmax <= x_8(4)
%     -vmax <= x_9(4)
%     -vmax <= x_10(4)
%     -vmax <= x_11(4)
%     -vmax <= x_12(4)
%     -vmax <= x_13(4)
%     -vmax <= x_14(4)
%     -vmax <= x_15(4)
%     -vmax <= x_16(4)
%     -vmax <= x_17(4)
%     -vmax <= x_18(4)
%     -vmax <= x_19(4)
%     -vmax <= x_20(4)
%     -vmax <= x_21(4)
%     -vmax <= x_22(4)
%     -vmax <= x_23(4)
%     -vmax <= x_24(4)
%     -vmax <= x_25(4)
%     x_1(4) <= vmax
%     x_2(4) <= vmax
%     x_3(4) <= vmax
%     x_4(4) <= vmax
%     x_5(4) <= vmax
%     x_6(4) <= vmax
%     x_7(4) <= vmax
%     x_8(4) <= vmax
%     x_9(4) <= vmax
%     x_10(4) <= vmax
%     x_11(4) <= vmax
%     x_12(4) <= vmax
%     x_13(4) <= vmax
%     x_14(4) <= vmax
%     x_15(4) <= vmax
%     x_16(4) <= vmax
%     x_17(4) <= vmax
%     x_18(4) <= vmax
%     x_19(4) <= vmax
%     x_20(4) <= vmax
%     x_21(4) <= vmax
%     x_22(4) <= vmax
%     x_23(4) <= vmax
%     x_24(4) <= vmax
%     x_25(4) <= vmax
%
% with variables
%      u_0   2 x 1
%      u_1   2 x 1
%      u_2   2 x 1
%      u_3   2 x 1
%      u_4   2 x 1
%      u_5   2 x 1
%      u_6   2 x 1
%      u_7   2 x 1
%      u_8   2 x 1
%      u_9   2 x 1
%     u_10   2 x 1
%     u_11   2 x 1
%     u_12   2 x 1
%     u_13   2 x 1
%     u_14   2 x 1
%     u_15   2 x 1
%     u_16   2 x 1
%     u_17   2 x 1
%     u_18   2 x 1
%     u_19   2 x 1
%     u_20   2 x 1
%     u_21   2 x 1
%     u_22   2 x 1
%     u_23   2 x 1
%     u_24   2 x 1
%     ub_0   2 x 1
%     ub_1   2 x 1
%     ub_2   2 x 1
%     ub_3   2 x 1
%     ub_4   2 x 1
%     ub_5   2 x 1
%     ub_6   2 x 1
%     ub_7   2 x 1
%     ub_8   2 x 1
%     ub_9   2 x 1
%    ub_10   2 x 1
%    ub_11   2 x 1
%    ub_12   2 x 1
%    ub_13   2 x 1
%    ub_14   2 x 1
%    ub_15   2 x 1
%    ub_16   2 x 1
%    ub_17   2 x 1
%    ub_18   2 x 1
%    ub_19   2 x 1
%    ub_20   2 x 1
%    ub_21   2 x 1
%    ub_22   2 x 1
%    ub_23   2 x 1
%    ub_24   2 x 1
%      x_1   4 x 1
%      x_2   4 x 1
%      x_3   4 x 1
%      x_4   4 x 1
%      x_5   4 x 1
%      x_6   4 x 1
%      x_7   4 x 1
%      x_8   4 x 1
%      x_9   4 x 1
%     x_10   4 x 1
%     x_11   4 x 1
%     x_12   4 x 1
%     x_13   4 x 1
%     x_14   4 x 1
%     x_15   4 x 1
%     x_16   4 x 1
%     x_17   4 x 1
%     x_18   4 x 1
%     x_19   4 x 1
%     x_20   4 x 1
%     x_21   4 x 1
%     x_22   4 x 1
%     x_23   4 x 1
%     x_24   4 x 1
%     x_25   4 x 1
%     xb_1   4 x 1
%     xb_2   4 x 1
%     xb_3   4 x 1
%     xb_4   4 x 1
%     xb_5   4 x 1
%     xb_6   4 x 1
%     xb_7   4 x 1
%     xb_8   4 x 1
%     xb_9   4 x 1
%    xb_10   4 x 1
%    xb_11   4 x 1
%    xb_12   4 x 1
%    xb_13   4 x 1
%    xb_14   4 x 1
%    xb_15   4 x 1
%    xb_16   4 x 1
%    xb_17   4 x 1
%    xb_18   4 x 1
%    xb_19   4 x 1
%    xb_20   4 x 1
%    xb_21   4 x 1
%    xb_22   4 x 1
%    xb_23   4 x 1
%    xb_24   4 x 1
%    xb_25   4 x 1
%
% and parameters
%        A   4 x 4
%       Ab   4 x 4
%        B   4 x 2
%       Bb   4 x 2
%        P   4 x 4    PSD
%        Q   4 x 4    PSD
%        R   2 x 2    PSD
%     amax   1 x 1    positive
%   amax_b   1 x 1    positive
%     amin   1 x 1    negative
%   amin_b   1 x 1    negative
%     vmax   1 x 1    positive
%      x_0   4 x 1
%     xb_0   4 x 1
%
% Note:
%   - Check status.converged, which will be 1 if optimization succeeded.
%   - You don't have to specify settings if you don't want to.
%   - To hide output, use settings.verbose = 0.
%   - To change iterations, use settings.max_iters = 20.
%   - You may wish to compare with cvxsolve to check the solver is correct.
%
% Specify params.A, ..., params.xb_0, then run
%   [vars, status] = csolve(params, settings)
% Produced by CVXGEN, 2019-04-24 04:04:53 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
