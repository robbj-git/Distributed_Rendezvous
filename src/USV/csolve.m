% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(x_0 - xb_0, Q) + quad_form(ub_0, R) + quad_form(x_1 - xb_1, Q) + quad_form(ub_1, R) + quad_form(x_2 - xb_2, Q) + quad_form(ub_2, R) + quad_form(x_3 - xb_3, Q) + quad_form(ub_3, R) + quad_form(x_4 - xb_4, Q) + quad_form(ub_4, R) + quad_form(x_5 - xb_5, Q) + quad_form(ub_5, R) + quad_form(x_6 - xb_6, Q) + quad_form(ub_6, R) + quad_form(x_7 - xb_7, Q) + quad_form(ub_7, R) + quad_form(x_8 - xb_8, Q) + quad_form(ub_8, R) + quad_form(x_9 - xb_9, Q) + quad_form(ub_9, R) + quad_form(x_10 - xb_10, Q) + quad_form(ub_10, R) + quad_form(x_11 - xb_11, Q) + quad_form(ub_11, R) + quad_form(x_12 - xb_12, Q) + quad_form(ub_12, R) + quad_form(x_13 - xb_13, Q) + quad_form(ub_13, R) + quad_form(x_14 - xb_14, Q) + quad_form(ub_14, R) + quad_form(x_15 - xb_15, Q) + quad_form(ub_15, R) + quad_form(x_16 - xb_16, Q) + quad_form(ub_16, R) + quad_form(x_17 - xb_17, Q) + quad_form(ub_17, R) + quad_form(x_18 - xb_18, Q) + quad_form(ub_18, R) + quad_form(x_19 - xb_19, Q) + quad_form(ub_19, R) + quad_form(x_20 - xb_20, Q) + quad_form(ub_20, R) + quad_form(x_21 - xb_21, Q) + quad_form(ub_21, R) + quad_form(x_22 - xb_22, Q) + quad_form(ub_22, R) + quad_form(x_23 - xb_23, Q) + quad_form(ub_23, R) + quad_form(x_24 - xb_24, Q) + quad_form(ub_24, R) + quad_form(x_25 - xb_25, Q) + quad_form(ub_25, R) + quad_form(x_26 - xb_26, Q) + quad_form(ub_26, R) + quad_form(x_27 - xb_27, Q) + quad_form(ub_27, R) + quad_form(x_28 - xb_28, Q) + quad_form(ub_28, R) + quad_form(x_29 - xb_29, Q) + quad_form(ub_29, R) + quad_form(x_30 - xb_30, Q) + quad_form(ub_30, R) + quad_form(x_31 - xb_31, Q) + quad_form(ub_31, R) + quad_form(x_32 - xb_32, Q) + quad_form(ub_32, R) + quad_form(x_33 - xb_33, Q) + quad_form(ub_33, R) + quad_form(x_34 - xb_34, Q) + quad_form(ub_34, R) + quad_form(x_35 - xb_35, Q) + quad_form(ub_35, R) + quad_form(x_36 - xb_36, Q) + quad_form(ub_36, R) + quad_form(x_37 - xb_37, Q) + quad_form(ub_37, R) + quad_form(x_38 - xb_38, Q) + quad_form(ub_38, R) + quad_form(x_39 - xb_39, Q) + quad_form(ub_39, R) + quad_form(x_40 - xb_40, Q) + quad_form(ub_40, R) + quad_form(x_41 - xb_41, Q) + quad_form(ub_41, R) + quad_form(x_42 - xb_42, Q) + quad_form(ub_42, R) + quad_form(x_43 - xb_43, Q) + quad_form(ub_43, R) + quad_form(x_44 - xb_44, Q) + quad_form(ub_44, R) + quad_form(x_45 - xb_45, P))
%   subject to
%     xb_1 == A*xb_0 + B*ub_0
%     xb_2 == A*xb_1 + B*ub_1
%     xb_3 == A*xb_2 + B*ub_2
%     xb_4 == A*xb_3 + B*ub_3
%     xb_5 == A*xb_4 + B*ub_4
%     xb_6 == A*xb_5 + B*ub_5
%     xb_7 == A*xb_6 + B*ub_6
%     xb_8 == A*xb_7 + B*ub_7
%     xb_9 == A*xb_8 + B*ub_8
%     xb_10 == A*xb_9 + B*ub_9
%     xb_11 == A*xb_10 + B*ub_10
%     xb_12 == A*xb_11 + B*ub_11
%     xb_13 == A*xb_12 + B*ub_12
%     xb_14 == A*xb_13 + B*ub_13
%     xb_15 == A*xb_14 + B*ub_14
%     xb_16 == A*xb_15 + B*ub_15
%     xb_17 == A*xb_16 + B*ub_16
%     xb_18 == A*xb_17 + B*ub_17
%     xb_19 == A*xb_18 + B*ub_18
%     xb_20 == A*xb_19 + B*ub_19
%     xb_21 == A*xb_20 + B*ub_20
%     xb_22 == A*xb_21 + B*ub_21
%     xb_23 == A*xb_22 + B*ub_22
%     xb_24 == A*xb_23 + B*ub_23
%     xb_25 == A*xb_24 + B*ub_24
%     xb_26 == A*xb_25 + B*ub_25
%     xb_27 == A*xb_26 + B*ub_26
%     xb_28 == A*xb_27 + B*ub_27
%     xb_29 == A*xb_28 + B*ub_28
%     xb_30 == A*xb_29 + B*ub_29
%     xb_31 == A*xb_30 + B*ub_30
%     xb_32 == A*xb_31 + B*ub_31
%     xb_33 == A*xb_32 + B*ub_32
%     xb_34 == A*xb_33 + B*ub_33
%     xb_35 == A*xb_34 + B*ub_34
%     xb_36 == A*xb_35 + B*ub_35
%     xb_37 == A*xb_36 + B*ub_36
%     xb_38 == A*xb_37 + B*ub_37
%     xb_39 == A*xb_38 + B*ub_38
%     xb_40 == A*xb_39 + B*ub_39
%     xb_41 == A*xb_40 + B*ub_40
%     xb_42 == A*xb_41 + B*ub_41
%     xb_43 == A*xb_42 + B*ub_42
%     xb_44 == A*xb_43 + B*ub_43
%     xb_45 == A*xb_44 + B*ub_44
%     amin <= ub_0
%     amin <= ub_1
%     amin <= ub_2
%     amin <= ub_3
%     amin <= ub_4
%     amin <= ub_5
%     amin <= ub_6
%     amin <= ub_7
%     amin <= ub_8
%     amin <= ub_9
%     amin <= ub_10
%     amin <= ub_11
%     amin <= ub_12
%     amin <= ub_13
%     amin <= ub_14
%     amin <= ub_15
%     amin <= ub_16
%     amin <= ub_17
%     amin <= ub_18
%     amin <= ub_19
%     amin <= ub_20
%     amin <= ub_21
%     amin <= ub_22
%     amin <= ub_23
%     amin <= ub_24
%     amin <= ub_25
%     amin <= ub_26
%     amin <= ub_27
%     amin <= ub_28
%     amin <= ub_29
%     amin <= ub_30
%     amin <= ub_31
%     amin <= ub_32
%     amin <= ub_33
%     amin <= ub_34
%     amin <= ub_35
%     amin <= ub_36
%     amin <= ub_37
%     amin <= ub_38
%     amin <= ub_39
%     amin <= ub_40
%     amin <= ub_41
%     amin <= ub_42
%     amin <= ub_43
%     amin <= ub_44
%     ub_0 <= amax
%     ub_1 <= amax
%     ub_2 <= amax
%     ub_3 <= amax
%     ub_4 <= amax
%     ub_5 <= amax
%     ub_6 <= amax
%     ub_7 <= amax
%     ub_8 <= amax
%     ub_9 <= amax
%     ub_10 <= amax
%     ub_11 <= amax
%     ub_12 <= amax
%     ub_13 <= amax
%     ub_14 <= amax
%     ub_15 <= amax
%     ub_16 <= amax
%     ub_17 <= amax
%     ub_18 <= amax
%     ub_19 <= amax
%     ub_20 <= amax
%     ub_21 <= amax
%     ub_22 <= amax
%     ub_23 <= amax
%     ub_24 <= amax
%     ub_25 <= amax
%     ub_26 <= amax
%     ub_27 <= amax
%     ub_28 <= amax
%     ub_29 <= amax
%     ub_30 <= amax
%     ub_31 <= amax
%     ub_32 <= amax
%     ub_33 <= amax
%     ub_34 <= amax
%     ub_35 <= amax
%     ub_36 <= amax
%     ub_37 <= amax
%     ub_38 <= amax
%     ub_39 <= amax
%     ub_40 <= amax
%     ub_41 <= amax
%     ub_42 <= amax
%     ub_43 <= amax
%     ub_44 <= amax
%     -vmax <= xb_1(3)
%     -vmax <= xb_2(3)
%     -vmax <= xb_3(3)
%     -vmax <= xb_4(3)
%     -vmax <= xb_5(3)
%     -vmax <= xb_6(3)
%     -vmax <= xb_7(3)
%     -vmax <= xb_8(3)
%     -vmax <= xb_9(3)
%     -vmax <= xb_10(3)
%     -vmax <= xb_11(3)
%     -vmax <= xb_12(3)
%     -vmax <= xb_13(3)
%     -vmax <= xb_14(3)
%     -vmax <= xb_15(3)
%     -vmax <= xb_16(3)
%     -vmax <= xb_17(3)
%     -vmax <= xb_18(3)
%     -vmax <= xb_19(3)
%     -vmax <= xb_20(3)
%     -vmax <= xb_21(3)
%     -vmax <= xb_22(3)
%     -vmax <= xb_23(3)
%     -vmax <= xb_24(3)
%     -vmax <= xb_25(3)
%     -vmax <= xb_26(3)
%     -vmax <= xb_27(3)
%     -vmax <= xb_28(3)
%     -vmax <= xb_29(3)
%     -vmax <= xb_30(3)
%     -vmax <= xb_31(3)
%     -vmax <= xb_32(3)
%     -vmax <= xb_33(3)
%     -vmax <= xb_34(3)
%     -vmax <= xb_35(3)
%     -vmax <= xb_36(3)
%     -vmax <= xb_37(3)
%     -vmax <= xb_38(3)
%     -vmax <= xb_39(3)
%     -vmax <= xb_40(3)
%     -vmax <= xb_41(3)
%     -vmax <= xb_42(3)
%     -vmax <= xb_43(3)
%     -vmax <= xb_44(3)
%     -vmax <= xb_45(3)
%     xb_1(3) <= vmax
%     xb_2(3) <= vmax
%     xb_3(3) <= vmax
%     xb_4(3) <= vmax
%     xb_5(3) <= vmax
%     xb_6(3) <= vmax
%     xb_7(3) <= vmax
%     xb_8(3) <= vmax
%     xb_9(3) <= vmax
%     xb_10(3) <= vmax
%     xb_11(3) <= vmax
%     xb_12(3) <= vmax
%     xb_13(3) <= vmax
%     xb_14(3) <= vmax
%     xb_15(3) <= vmax
%     xb_16(3) <= vmax
%     xb_17(3) <= vmax
%     xb_18(3) <= vmax
%     xb_19(3) <= vmax
%     xb_20(3) <= vmax
%     xb_21(3) <= vmax
%     xb_22(3) <= vmax
%     xb_23(3) <= vmax
%     xb_24(3) <= vmax
%     xb_25(3) <= vmax
%     xb_26(3) <= vmax
%     xb_27(3) <= vmax
%     xb_28(3) <= vmax
%     xb_29(3) <= vmax
%     xb_30(3) <= vmax
%     xb_31(3) <= vmax
%     xb_32(3) <= vmax
%     xb_33(3) <= vmax
%     xb_34(3) <= vmax
%     xb_35(3) <= vmax
%     xb_36(3) <= vmax
%     xb_37(3) <= vmax
%     xb_38(3) <= vmax
%     xb_39(3) <= vmax
%     xb_40(3) <= vmax
%     xb_41(3) <= vmax
%     xb_42(3) <= vmax
%     xb_43(3) <= vmax
%     xb_44(3) <= vmax
%     xb_45(3) <= vmax
%     -vmax <= xb_1(4)
%     -vmax <= xb_2(4)
%     -vmax <= xb_3(4)
%     -vmax <= xb_4(4)
%     -vmax <= xb_5(4)
%     -vmax <= xb_6(4)
%     -vmax <= xb_7(4)
%     -vmax <= xb_8(4)
%     -vmax <= xb_9(4)
%     -vmax <= xb_10(4)
%     -vmax <= xb_11(4)
%     -vmax <= xb_12(4)
%     -vmax <= xb_13(4)
%     -vmax <= xb_14(4)
%     -vmax <= xb_15(4)
%     -vmax <= xb_16(4)
%     -vmax <= xb_17(4)
%     -vmax <= xb_18(4)
%     -vmax <= xb_19(4)
%     -vmax <= xb_20(4)
%     -vmax <= xb_21(4)
%     -vmax <= xb_22(4)
%     -vmax <= xb_23(4)
%     -vmax <= xb_24(4)
%     -vmax <= xb_25(4)
%     -vmax <= xb_26(4)
%     -vmax <= xb_27(4)
%     -vmax <= xb_28(4)
%     -vmax <= xb_29(4)
%     -vmax <= xb_30(4)
%     -vmax <= xb_31(4)
%     -vmax <= xb_32(4)
%     -vmax <= xb_33(4)
%     -vmax <= xb_34(4)
%     -vmax <= xb_35(4)
%     -vmax <= xb_36(4)
%     -vmax <= xb_37(4)
%     -vmax <= xb_38(4)
%     -vmax <= xb_39(4)
%     -vmax <= xb_40(4)
%     -vmax <= xb_41(4)
%     -vmax <= xb_42(4)
%     -vmax <= xb_43(4)
%     -vmax <= xb_44(4)
%     -vmax <= xb_45(4)
%     xb_1(4) <= vmax
%     xb_2(4) <= vmax
%     xb_3(4) <= vmax
%     xb_4(4) <= vmax
%     xb_5(4) <= vmax
%     xb_6(4) <= vmax
%     xb_7(4) <= vmax
%     xb_8(4) <= vmax
%     xb_9(4) <= vmax
%     xb_10(4) <= vmax
%     xb_11(4) <= vmax
%     xb_12(4) <= vmax
%     xb_13(4) <= vmax
%     xb_14(4) <= vmax
%     xb_15(4) <= vmax
%     xb_16(4) <= vmax
%     xb_17(4) <= vmax
%     xb_18(4) <= vmax
%     xb_19(4) <= vmax
%     xb_20(4) <= vmax
%     xb_21(4) <= vmax
%     xb_22(4) <= vmax
%     xb_23(4) <= vmax
%     xb_24(4) <= vmax
%     xb_25(4) <= vmax
%     xb_26(4) <= vmax
%     xb_27(4) <= vmax
%     xb_28(4) <= vmax
%     xb_29(4) <= vmax
%     xb_30(4) <= vmax
%     xb_31(4) <= vmax
%     xb_32(4) <= vmax
%     xb_33(4) <= vmax
%     xb_34(4) <= vmax
%     xb_35(4) <= vmax
%     xb_36(4) <= vmax
%     xb_37(4) <= vmax
%     xb_38(4) <= vmax
%     xb_39(4) <= vmax
%     xb_40(4) <= vmax
%     xb_41(4) <= vmax
%     xb_42(4) <= vmax
%     xb_43(4) <= vmax
%     xb_44(4) <= vmax
%     xb_45(4) <= vmax
%
% with variables
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
%    ub_25   2 x 1
%    ub_26   2 x 1
%    ub_27   2 x 1
%    ub_28   2 x 1
%    ub_29   2 x 1
%    ub_30   2 x 1
%    ub_31   2 x 1
%    ub_32   2 x 1
%    ub_33   2 x 1
%    ub_34   2 x 1
%    ub_35   2 x 1
%    ub_36   2 x 1
%    ub_37   2 x 1
%    ub_38   2 x 1
%    ub_39   2 x 1
%    ub_40   2 x 1
%    ub_41   2 x 1
%    ub_42   2 x 1
%    ub_43   2 x 1
%    ub_44   2 x 1
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
% Produced by CVXGEN, 2019-04-24 04:09:08 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
