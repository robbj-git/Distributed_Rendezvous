% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(x_0 - xb_0, Q) + quad_form(u_0, R) + quad_form(x_1 - xb_1, Q) + quad_form(u_1, R) + quad_form(x_2 - xb_2, Q) + quad_form(u_2, R) + quad_form(x_3 - xb_3, Q) + quad_form(u_3, R) + quad_form(x_4 - xb_4, Q) + quad_form(u_4, R) + quad_form(x_5 - xb_5, Q) + quad_form(u_5, R) + quad_form(x_6 - xb_6, Q) + quad_form(u_6, R) + quad_form(x_7 - xb_7, Q) + quad_form(u_7, R) + quad_form(x_8 - xb_8, Q) + quad_form(u_8, R) + quad_form(x_9 - xb_9, Q) + quad_form(u_9, R) + quad_form(x_10 - xb_10, Q) + quad_form(u_10, R) + quad_form(x_11 - xb_11, Q) + quad_form(u_11, R) + quad_form(x_12 - xb_12, Q) + quad_form(u_12, R) + quad_form(x_13 - xb_13, Q) + quad_form(u_13, R) + quad_form(x_14 - xb_14, Q) + quad_form(u_14, R) + quad_form(x_15 - xb_15, Q) + quad_form(u_15, R) + quad_form(x_16 - xb_16, Q) + quad_form(u_16, R) + quad_form(x_17 - xb_17, Q) + quad_form(u_17, R) + quad_form(x_18 - xb_18, Q) + quad_form(u_18, R) + quad_form(x_19 - xb_19, Q) + quad_form(u_19, R) + quad_form(x_20 - xb_20, Q) + quad_form(u_20, R) + quad_form(x_21 - xb_21, Q) + quad_form(u_21, R) + quad_form(x_22 - xb_22, Q) + quad_form(u_22, R) + quad_form(x_23 - xb_23, Q) + quad_form(u_23, R) + quad_form(x_24 - xb_24, Q) + quad_form(u_24, R) + quad_form(x_25 - xb_25, Q) + quad_form(u_25, R) + quad_form(x_26 - xb_26, Q) + quad_form(u_26, R) + quad_form(x_27 - xb_27, Q) + quad_form(u_27, R) + quad_form(x_28 - xb_28, Q) + quad_form(u_28, R) + quad_form(x_29 - xb_29, Q) + quad_form(u_29, R) + quad_form(x_30 - xb_30, Q) + quad_form(u_30, R) + quad_form(x_31 - xb_31, Q) + quad_form(u_31, R) + quad_form(x_32 - xb_32, Q) + quad_form(u_32, R) + quad_form(x_33 - xb_33, Q) + quad_form(u_33, R) + quad_form(x_34 - xb_34, Q) + quad_form(u_34, R) + quad_form(x_35 - xb_35, Q) + quad_form(u_35, R) + quad_form(x_36 - xb_36, Q) + quad_form(u_36, R) + quad_form(x_37 - xb_37, Q) + quad_form(u_37, R) + quad_form(x_38 - xb_38, Q) + quad_form(u_38, R) + quad_form(x_39 - xb_39, Q) + quad_form(u_39, R) + quad_form(x_40 - xb_40, Q) + quad_form(u_40, R) + quad_form(x_41 - xb_41, Q) + quad_form(u_41, R) + quad_form(x_42 - xb_42, Q) + quad_form(u_42, R) + quad_form(x_43 - xb_43, Q) + quad_form(u_43, R) + quad_form(x_44 - xb_44, Q) + quad_form(u_44, R) + quad_form(x_45 - xb_45, P))
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
%     x_26 == A*x_25 + B*u_25
%     x_27 == A*x_26 + B*u_26
%     x_28 == A*x_27 + B*u_27
%     x_29 == A*x_28 + B*u_28
%     x_30 == A*x_29 + B*u_29
%     x_31 == A*x_30 + B*u_30
%     x_32 == A*x_31 + B*u_31
%     x_33 == A*x_32 + B*u_32
%     x_34 == A*x_33 + B*u_33
%     x_35 == A*x_34 + B*u_34
%     x_36 == A*x_35 + B*u_35
%     x_37 == A*x_36 + B*u_36
%     x_38 == A*x_37 + B*u_37
%     x_39 == A*x_38 + B*u_38
%     x_40 == A*x_39 + B*u_39
%     x_41 == A*x_40 + B*u_40
%     x_42 == A*x_41 + B*u_41
%     x_43 == A*x_42 + B*u_42
%     x_44 == A*x_43 + B*u_43
%     x_45 == A*x_44 + B*u_44
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
%     amin <= u_25
%     amin <= u_26
%     amin <= u_27
%     amin <= u_28
%     amin <= u_29
%     amin <= u_30
%     amin <= u_31
%     amin <= u_32
%     amin <= u_33
%     amin <= u_34
%     amin <= u_35
%     amin <= u_36
%     amin <= u_37
%     amin <= u_38
%     amin <= u_39
%     amin <= u_40
%     amin <= u_41
%     amin <= u_42
%     amin <= u_43
%     amin <= u_44
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
%     u_25 <= amax
%     u_26 <= amax
%     u_27 <= amax
%     u_28 <= amax
%     u_29 <= amax
%     u_30 <= amax
%     u_31 <= amax
%     u_32 <= amax
%     u_33 <= amax
%     u_34 <= amax
%     u_35 <= amax
%     u_36 <= amax
%     u_37 <= amax
%     u_38 <= amax
%     u_39 <= amax
%     u_40 <= amax
%     u_41 <= amax
%     u_42 <= amax
%     u_43 <= amax
%     u_44 <= amax
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
%     -vmax <= x_26(3)
%     -vmax <= x_27(3)
%     -vmax <= x_28(3)
%     -vmax <= x_29(3)
%     -vmax <= x_30(3)
%     -vmax <= x_31(3)
%     -vmax <= x_32(3)
%     -vmax <= x_33(3)
%     -vmax <= x_34(3)
%     -vmax <= x_35(3)
%     -vmax <= x_36(3)
%     -vmax <= x_37(3)
%     -vmax <= x_38(3)
%     -vmax <= x_39(3)
%     -vmax <= x_40(3)
%     -vmax <= x_41(3)
%     -vmax <= x_42(3)
%     -vmax <= x_43(3)
%     -vmax <= x_44(3)
%     -vmax <= x_45(3)
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
%     x_26(3) <= vmax
%     x_27(3) <= vmax
%     x_28(3) <= vmax
%     x_29(3) <= vmax
%     x_30(3) <= vmax
%     x_31(3) <= vmax
%     x_32(3) <= vmax
%     x_33(3) <= vmax
%     x_34(3) <= vmax
%     x_35(3) <= vmax
%     x_36(3) <= vmax
%     x_37(3) <= vmax
%     x_38(3) <= vmax
%     x_39(3) <= vmax
%     x_40(3) <= vmax
%     x_41(3) <= vmax
%     x_42(3) <= vmax
%     x_43(3) <= vmax
%     x_44(3) <= vmax
%     x_45(3) <= vmax
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
%     -vmax <= x_26(4)
%     -vmax <= x_27(4)
%     -vmax <= x_28(4)
%     -vmax <= x_29(4)
%     -vmax <= x_30(4)
%     -vmax <= x_31(4)
%     -vmax <= x_32(4)
%     -vmax <= x_33(4)
%     -vmax <= x_34(4)
%     -vmax <= x_35(4)
%     -vmax <= x_36(4)
%     -vmax <= x_37(4)
%     -vmax <= x_38(4)
%     -vmax <= x_39(4)
%     -vmax <= x_40(4)
%     -vmax <= x_41(4)
%     -vmax <= x_42(4)
%     -vmax <= x_43(4)
%     -vmax <= x_44(4)
%     -vmax <= x_45(4)
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
%     x_26(4) <= vmax
%     x_27(4) <= vmax
%     x_28(4) <= vmax
%     x_29(4) <= vmax
%     x_30(4) <= vmax
%     x_31(4) <= vmax
%     x_32(4) <= vmax
%     x_33(4) <= vmax
%     x_34(4) <= vmax
%     x_35(4) <= vmax
%     x_36(4) <= vmax
%     x_37(4) <= vmax
%     x_38(4) <= vmax
%     x_39(4) <= vmax
%     x_40(4) <= vmax
%     x_41(4) <= vmax
%     x_42(4) <= vmax
%     x_43(4) <= vmax
%     x_44(4) <= vmax
%     x_45(4) <= vmax
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
%     u_25   2 x 1
%     u_26   2 x 1
%     u_27   2 x 1
%     u_28   2 x 1
%     u_29   2 x 1
%     u_30   2 x 1
%     u_31   2 x 1
%     u_32   2 x 1
%     u_33   2 x 1
%     u_34   2 x 1
%     u_35   2 x 1
%     u_36   2 x 1
%     u_37   2 x 1
%     u_38   2 x 1
%     u_39   2 x 1
%     u_40   2 x 1
%     u_41   2 x 1
%     u_42   2 x 1
%     u_43   2 x 1
%     u_44   2 x 1
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
%     x_26   4 x 1
%     x_27   4 x 1
%     x_28   4 x 1
%     x_29   4 x 1
%     x_30   4 x 1
%     x_31   4 x 1
%     x_32   4 x 1
%     x_33   4 x 1
%     x_34   4 x 1
%     x_35   4 x 1
%     x_36   4 x 1
%     x_37   4 x 1
%     x_38   4 x 1
%     x_39   4 x 1
%     x_40   4 x 1
%     x_41   4 x 1
%     x_42   4 x 1
%     x_43   4 x 1
%     x_44   4 x 1
%     x_45   4 x 1
%
% and parameters
%        A   4 x 4
%        B   4 x 2
%        P   4 x 4    PSD
%        Q   4 x 4    PSD
%        R   2 x 2    PSD
%     amax   1 x 1    positive
%     amin   1 x 1    negative
%     vmax   1 x 1    positive
%      x_0   4 x 1
%     xb_0   4 x 1
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
%    xb_26   4 x 1
%    xb_27   4 x 1
%    xb_28   4 x 1
%    xb_29   4 x 1
%    xb_30   4 x 1
%    xb_31   4 x 1
%    xb_32   4 x 1
%    xb_33   4 x 1
%    xb_34   4 x 1
%    xb_35   4 x 1
%    xb_36   4 x 1
%    xb_37   4 x 1
%    xb_38   4 x 1
%    xb_39   4 x 1
%    xb_40   4 x 1
%    xb_41   4 x 1
%    xb_42   4 x 1
%    xb_43   4 x 1
%    xb_44   4 x 1
%    xb_45   4 x 1
%
% Note:
%   - Check status.converged, which will be 1 if optimization succeeded.
%   - You don't have to specify settings if you don't want to.
%   - To hide output, use settings.verbose = 0.
%   - To change iterations, use settings.max_iters = 20.
%   - You may wish to compare with cvxsolve to check the solver is correct.
%
% Specify params.A, ..., params.xb_45, then run
%   [vars, status] = csolve(params, settings)
% Produced by CVXGEN, 2019-04-24 04:05:21 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
