% Produced by CVXGEN, 2019-04-24 04:05:21 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: cvxsolve.m.
% Description: Solution file, via cvx, for use with sample.m.
function [vars, status] = cvxsolve(params, settings)
A = params.A;
B = params.B;
P = params.P;
Q = params.Q;
R = params.R;
amax = params.amax;
amin = params.amin;
vmax = params.vmax;
x_0 = params.x_0;
xb_0 = params.xb_0;
if isfield(params, 'xb_1')
  xb_1 = params.xb_1;
elseif isfield(params, 'xb')
  xb_1 = params.xb{1};
else
  error 'could not find xb_1'
end
if isfield(params, 'xb_2')
  xb_2 = params.xb_2;
elseif isfield(params, 'xb')
  xb_2 = params.xb{2};
else
  error 'could not find xb_2'
end
if isfield(params, 'xb_3')
  xb_3 = params.xb_3;
elseif isfield(params, 'xb')
  xb_3 = params.xb{3};
else
  error 'could not find xb_3'
end
if isfield(params, 'xb_4')
  xb_4 = params.xb_4;
elseif isfield(params, 'xb')
  xb_4 = params.xb{4};
else
  error 'could not find xb_4'
end
if isfield(params, 'xb_5')
  xb_5 = params.xb_5;
elseif isfield(params, 'xb')
  xb_5 = params.xb{5};
else
  error 'could not find xb_5'
end
if isfield(params, 'xb_6')
  xb_6 = params.xb_6;
elseif isfield(params, 'xb')
  xb_6 = params.xb{6};
else
  error 'could not find xb_6'
end
if isfield(params, 'xb_7')
  xb_7 = params.xb_7;
elseif isfield(params, 'xb')
  xb_7 = params.xb{7};
else
  error 'could not find xb_7'
end
if isfield(params, 'xb_8')
  xb_8 = params.xb_8;
elseif isfield(params, 'xb')
  xb_8 = params.xb{8};
else
  error 'could not find xb_8'
end
if isfield(params, 'xb_9')
  xb_9 = params.xb_9;
elseif isfield(params, 'xb')
  xb_9 = params.xb{9};
else
  error 'could not find xb_9'
end
if isfield(params, 'xb_10')
  xb_10 = params.xb_10;
elseif isfield(params, 'xb')
  xb_10 = params.xb{10};
else
  error 'could not find xb_10'
end
if isfield(params, 'xb_11')
  xb_11 = params.xb_11;
elseif isfield(params, 'xb')
  xb_11 = params.xb{11};
else
  error 'could not find xb_11'
end
if isfield(params, 'xb_12')
  xb_12 = params.xb_12;
elseif isfield(params, 'xb')
  xb_12 = params.xb{12};
else
  error 'could not find xb_12'
end
if isfield(params, 'xb_13')
  xb_13 = params.xb_13;
elseif isfield(params, 'xb')
  xb_13 = params.xb{13};
else
  error 'could not find xb_13'
end
if isfield(params, 'xb_14')
  xb_14 = params.xb_14;
elseif isfield(params, 'xb')
  xb_14 = params.xb{14};
else
  error 'could not find xb_14'
end
if isfield(params, 'xb_15')
  xb_15 = params.xb_15;
elseif isfield(params, 'xb')
  xb_15 = params.xb{15};
else
  error 'could not find xb_15'
end
if isfield(params, 'xb_16')
  xb_16 = params.xb_16;
elseif isfield(params, 'xb')
  xb_16 = params.xb{16};
else
  error 'could not find xb_16'
end
if isfield(params, 'xb_17')
  xb_17 = params.xb_17;
elseif isfield(params, 'xb')
  xb_17 = params.xb{17};
else
  error 'could not find xb_17'
end
if isfield(params, 'xb_18')
  xb_18 = params.xb_18;
elseif isfield(params, 'xb')
  xb_18 = params.xb{18};
else
  error 'could not find xb_18'
end
if isfield(params, 'xb_19')
  xb_19 = params.xb_19;
elseif isfield(params, 'xb')
  xb_19 = params.xb{19};
else
  error 'could not find xb_19'
end
if isfield(params, 'xb_20')
  xb_20 = params.xb_20;
elseif isfield(params, 'xb')
  xb_20 = params.xb{20};
else
  error 'could not find xb_20'
end
if isfield(params, 'xb_21')
  xb_21 = params.xb_21;
elseif isfield(params, 'xb')
  xb_21 = params.xb{21};
else
  error 'could not find xb_21'
end
if isfield(params, 'xb_22')
  xb_22 = params.xb_22;
elseif isfield(params, 'xb')
  xb_22 = params.xb{22};
else
  error 'could not find xb_22'
end
if isfield(params, 'xb_23')
  xb_23 = params.xb_23;
elseif isfield(params, 'xb')
  xb_23 = params.xb{23};
else
  error 'could not find xb_23'
end
if isfield(params, 'xb_24')
  xb_24 = params.xb_24;
elseif isfield(params, 'xb')
  xb_24 = params.xb{24};
else
  error 'could not find xb_24'
end
if isfield(params, 'xb_25')
  xb_25 = params.xb_25;
elseif isfield(params, 'xb')
  xb_25 = params.xb{25};
else
  error 'could not find xb_25'
end
if isfield(params, 'xb_26')
  xb_26 = params.xb_26;
elseif isfield(params, 'xb')
  xb_26 = params.xb{26};
else
  error 'could not find xb_26'
end
if isfield(params, 'xb_27')
  xb_27 = params.xb_27;
elseif isfield(params, 'xb')
  xb_27 = params.xb{27};
else
  error 'could not find xb_27'
end
if isfield(params, 'xb_28')
  xb_28 = params.xb_28;
elseif isfield(params, 'xb')
  xb_28 = params.xb{28};
else
  error 'could not find xb_28'
end
if isfield(params, 'xb_29')
  xb_29 = params.xb_29;
elseif isfield(params, 'xb')
  xb_29 = params.xb{29};
else
  error 'could not find xb_29'
end
if isfield(params, 'xb_30')
  xb_30 = params.xb_30;
elseif isfield(params, 'xb')
  xb_30 = params.xb{30};
else
  error 'could not find xb_30'
end
if isfield(params, 'xb_31')
  xb_31 = params.xb_31;
elseif isfield(params, 'xb')
  xb_31 = params.xb{31};
else
  error 'could not find xb_31'
end
if isfield(params, 'xb_32')
  xb_32 = params.xb_32;
elseif isfield(params, 'xb')
  xb_32 = params.xb{32};
else
  error 'could not find xb_32'
end
if isfield(params, 'xb_33')
  xb_33 = params.xb_33;
elseif isfield(params, 'xb')
  xb_33 = params.xb{33};
else
  error 'could not find xb_33'
end
if isfield(params, 'xb_34')
  xb_34 = params.xb_34;
elseif isfield(params, 'xb')
  xb_34 = params.xb{34};
else
  error 'could not find xb_34'
end
if isfield(params, 'xb_35')
  xb_35 = params.xb_35;
elseif isfield(params, 'xb')
  xb_35 = params.xb{35};
else
  error 'could not find xb_35'
end
if isfield(params, 'xb_36')
  xb_36 = params.xb_36;
elseif isfield(params, 'xb')
  xb_36 = params.xb{36};
else
  error 'could not find xb_36'
end
if isfield(params, 'xb_37')
  xb_37 = params.xb_37;
elseif isfield(params, 'xb')
  xb_37 = params.xb{37};
else
  error 'could not find xb_37'
end
if isfield(params, 'xb_38')
  xb_38 = params.xb_38;
elseif isfield(params, 'xb')
  xb_38 = params.xb{38};
else
  error 'could not find xb_38'
end
if isfield(params, 'xb_39')
  xb_39 = params.xb_39;
elseif isfield(params, 'xb')
  xb_39 = params.xb{39};
else
  error 'could not find xb_39'
end
if isfield(params, 'xb_40')
  xb_40 = params.xb_40;
elseif isfield(params, 'xb')
  xb_40 = params.xb{40};
else
  error 'could not find xb_40'
end
if isfield(params, 'xb_41')
  xb_41 = params.xb_41;
elseif isfield(params, 'xb')
  xb_41 = params.xb{41};
else
  error 'could not find xb_41'
end
if isfield(params, 'xb_42')
  xb_42 = params.xb_42;
elseif isfield(params, 'xb')
  xb_42 = params.xb{42};
else
  error 'could not find xb_42'
end
if isfield(params, 'xb_43')
  xb_43 = params.xb_43;
elseif isfield(params, 'xb')
  xb_43 = params.xb{43};
else
  error 'could not find xb_43'
end
if isfield(params, 'xb_44')
  xb_44 = params.xb_44;
elseif isfield(params, 'xb')
  xb_44 = params.xb{44};
else
  error 'could not find xb_44'
end
if isfield(params, 'xb_45')
  xb_45 = params.xb_45;
elseif isfield(params, 'xb')
  xb_45 = params.xb{45};
else
  error 'could not find xb_45'
end
cvx_begin
  % Caution: automatically generated by cvxgen. May be incorrect.
  variable u_0(2, 1);
  variable x_1(4, 1);
  variable u_1(2, 1);
  variable x_2(4, 1);
  variable u_2(2, 1);
  variable x_3(4, 1);
  variable u_3(2, 1);
  variable x_4(4, 1);
  variable u_4(2, 1);
  variable x_5(4, 1);
  variable u_5(2, 1);
  variable x_6(4, 1);
  variable u_6(2, 1);
  variable x_7(4, 1);
  variable u_7(2, 1);
  variable x_8(4, 1);
  variable u_8(2, 1);
  variable x_9(4, 1);
  variable u_9(2, 1);
  variable x_10(4, 1);
  variable u_10(2, 1);
  variable x_11(4, 1);
  variable u_11(2, 1);
  variable x_12(4, 1);
  variable u_12(2, 1);
  variable x_13(4, 1);
  variable u_13(2, 1);
  variable x_14(4, 1);
  variable u_14(2, 1);
  variable x_15(4, 1);
  variable u_15(2, 1);
  variable x_16(4, 1);
  variable u_16(2, 1);
  variable x_17(4, 1);
  variable u_17(2, 1);
  variable x_18(4, 1);
  variable u_18(2, 1);
  variable x_19(4, 1);
  variable u_19(2, 1);
  variable x_20(4, 1);
  variable u_20(2, 1);
  variable x_21(4, 1);
  variable u_21(2, 1);
  variable x_22(4, 1);
  variable u_22(2, 1);
  variable x_23(4, 1);
  variable u_23(2, 1);
  variable x_24(4, 1);
  variable u_24(2, 1);
  variable x_25(4, 1);
  variable u_25(2, 1);
  variable x_26(4, 1);
  variable u_26(2, 1);
  variable x_27(4, 1);
  variable u_27(2, 1);
  variable x_28(4, 1);
  variable u_28(2, 1);
  variable x_29(4, 1);
  variable u_29(2, 1);
  variable x_30(4, 1);
  variable u_30(2, 1);
  variable x_31(4, 1);
  variable u_31(2, 1);
  variable x_32(4, 1);
  variable u_32(2, 1);
  variable x_33(4, 1);
  variable u_33(2, 1);
  variable x_34(4, 1);
  variable u_34(2, 1);
  variable x_35(4, 1);
  variable u_35(2, 1);
  variable x_36(4, 1);
  variable u_36(2, 1);
  variable x_37(4, 1);
  variable u_37(2, 1);
  variable x_38(4, 1);
  variable u_38(2, 1);
  variable x_39(4, 1);
  variable u_39(2, 1);
  variable x_40(4, 1);
  variable u_40(2, 1);
  variable x_41(4, 1);
  variable u_41(2, 1);
  variable x_42(4, 1);
  variable u_42(2, 1);
  variable x_43(4, 1);
  variable u_43(2, 1);
  variable x_44(4, 1);
  variable u_44(2, 1);
  variable x_45(4, 1);

  minimize(quad_form(x_0 - xb_0, Q) + quad_form(u_0, R) + quad_form(x_1 - xb_1, Q) + quad_form(u_1, R) + quad_form(x_2 - xb_2, Q) + quad_form(u_2, R) + quad_form(x_3 - xb_3, Q) + quad_form(u_3, R) + quad_form(x_4 - xb_4, Q) + quad_form(u_4, R) + quad_form(x_5 - xb_5, Q) + quad_form(u_5, R) + quad_form(x_6 - xb_6, Q) + quad_form(u_6, R) + quad_form(x_7 - xb_7, Q) + quad_form(u_7, R) + quad_form(x_8 - xb_8, Q) + quad_form(u_8, R) + quad_form(x_9 - xb_9, Q) + quad_form(u_9, R) + quad_form(x_10 - xb_10, Q) + quad_form(u_10, R) + quad_form(x_11 - xb_11, Q) + quad_form(u_11, R) + quad_form(x_12 - xb_12, Q) + quad_form(u_12, R) + quad_form(x_13 - xb_13, Q) + quad_form(u_13, R) + quad_form(x_14 - xb_14, Q) + quad_form(u_14, R) + quad_form(x_15 - xb_15, Q) + quad_form(u_15, R) + quad_form(x_16 - xb_16, Q) + quad_form(u_16, R) + quad_form(x_17 - xb_17, Q) + quad_form(u_17, R) + quad_form(x_18 - xb_18, Q) + quad_form(u_18, R) + quad_form(x_19 - xb_19, Q) + quad_form(u_19, R) + quad_form(x_20 - xb_20, Q) + quad_form(u_20, R) + quad_form(x_21 - xb_21, Q) + quad_form(u_21, R) + quad_form(x_22 - xb_22, Q) + quad_form(u_22, R) + quad_form(x_23 - xb_23, Q) + quad_form(u_23, R) + quad_form(x_24 - xb_24, Q) + quad_form(u_24, R) + quad_form(x_25 - xb_25, Q) + quad_form(u_25, R) + quad_form(x_26 - xb_26, Q) + quad_form(u_26, R) + quad_form(x_27 - xb_27, Q) + quad_form(u_27, R) + quad_form(x_28 - xb_28, Q) + quad_form(u_28, R) + quad_form(x_29 - xb_29, Q) + quad_form(u_29, R) + quad_form(x_30 - xb_30, Q) + quad_form(u_30, R) + quad_form(x_31 - xb_31, Q) + quad_form(u_31, R) + quad_form(x_32 - xb_32, Q) + quad_form(u_32, R) + quad_form(x_33 - xb_33, Q) + quad_form(u_33, R) + quad_form(x_34 - xb_34, Q) + quad_form(u_34, R) + quad_form(x_35 - xb_35, Q) + quad_form(u_35, R) + quad_form(x_36 - xb_36, Q) + quad_form(u_36, R) + quad_form(x_37 - xb_37, Q) + quad_form(u_37, R) + quad_form(x_38 - xb_38, Q) + quad_form(u_38, R) + quad_form(x_39 - xb_39, Q) + quad_form(u_39, R) + quad_form(x_40 - xb_40, Q) + quad_form(u_40, R) + quad_form(x_41 - xb_41, Q) + quad_form(u_41, R) + quad_form(x_42 - xb_42, Q) + quad_form(u_42, R) + quad_form(x_43 - xb_43, Q) + quad_form(u_43, R) + quad_form(x_44 - xb_44, Q) + quad_form(u_44, R) + quad_form(x_45 - xb_45, P));
  subject to
    x_1 == A*x_0 + B*u_0;
    x_2 == A*x_1 + B*u_1;
    x_3 == A*x_2 + B*u_2;
    x_4 == A*x_3 + B*u_3;
    x_5 == A*x_4 + B*u_4;
    x_6 == A*x_5 + B*u_5;
    x_7 == A*x_6 + B*u_6;
    x_8 == A*x_7 + B*u_7;
    x_9 == A*x_8 + B*u_8;
    x_10 == A*x_9 + B*u_9;
    x_11 == A*x_10 + B*u_10;
    x_12 == A*x_11 + B*u_11;
    x_13 == A*x_12 + B*u_12;
    x_14 == A*x_13 + B*u_13;
    x_15 == A*x_14 + B*u_14;
    x_16 == A*x_15 + B*u_15;
    x_17 == A*x_16 + B*u_16;
    x_18 == A*x_17 + B*u_17;
    x_19 == A*x_18 + B*u_18;
    x_20 == A*x_19 + B*u_19;
    x_21 == A*x_20 + B*u_20;
    x_22 == A*x_21 + B*u_21;
    x_23 == A*x_22 + B*u_22;
    x_24 == A*x_23 + B*u_23;
    x_25 == A*x_24 + B*u_24;
    x_26 == A*x_25 + B*u_25;
    x_27 == A*x_26 + B*u_26;
    x_28 == A*x_27 + B*u_27;
    x_29 == A*x_28 + B*u_28;
    x_30 == A*x_29 + B*u_29;
    x_31 == A*x_30 + B*u_30;
    x_32 == A*x_31 + B*u_31;
    x_33 == A*x_32 + B*u_32;
    x_34 == A*x_33 + B*u_33;
    x_35 == A*x_34 + B*u_34;
    x_36 == A*x_35 + B*u_35;
    x_37 == A*x_36 + B*u_36;
    x_38 == A*x_37 + B*u_37;
    x_39 == A*x_38 + B*u_38;
    x_40 == A*x_39 + B*u_39;
    x_41 == A*x_40 + B*u_40;
    x_42 == A*x_41 + B*u_41;
    x_43 == A*x_42 + B*u_42;
    x_44 == A*x_43 + B*u_43;
    x_45 == A*x_44 + B*u_44;
    amin <= u_0;
    amin <= u_1;
    amin <= u_2;
    amin <= u_3;
    amin <= u_4;
    amin <= u_5;
    amin <= u_6;
    amin <= u_7;
    amin <= u_8;
    amin <= u_9;
    amin <= u_10;
    amin <= u_11;
    amin <= u_12;
    amin <= u_13;
    amin <= u_14;
    amin <= u_15;
    amin <= u_16;
    amin <= u_17;
    amin <= u_18;
    amin <= u_19;
    amin <= u_20;
    amin <= u_21;
    amin <= u_22;
    amin <= u_23;
    amin <= u_24;
    amin <= u_25;
    amin <= u_26;
    amin <= u_27;
    amin <= u_28;
    amin <= u_29;
    amin <= u_30;
    amin <= u_31;
    amin <= u_32;
    amin <= u_33;
    amin <= u_34;
    amin <= u_35;
    amin <= u_36;
    amin <= u_37;
    amin <= u_38;
    amin <= u_39;
    amin <= u_40;
    amin <= u_41;
    amin <= u_42;
    amin <= u_43;
    amin <= u_44;
    u_0 <= amax;
    u_1 <= amax;
    u_2 <= amax;
    u_3 <= amax;
    u_4 <= amax;
    u_5 <= amax;
    u_6 <= amax;
    u_7 <= amax;
    u_8 <= amax;
    u_9 <= amax;
    u_10 <= amax;
    u_11 <= amax;
    u_12 <= amax;
    u_13 <= amax;
    u_14 <= amax;
    u_15 <= amax;
    u_16 <= amax;
    u_17 <= amax;
    u_18 <= amax;
    u_19 <= amax;
    u_20 <= amax;
    u_21 <= amax;
    u_22 <= amax;
    u_23 <= amax;
    u_24 <= amax;
    u_25 <= amax;
    u_26 <= amax;
    u_27 <= amax;
    u_28 <= amax;
    u_29 <= amax;
    u_30 <= amax;
    u_31 <= amax;
    u_32 <= amax;
    u_33 <= amax;
    u_34 <= amax;
    u_35 <= amax;
    u_36 <= amax;
    u_37 <= amax;
    u_38 <= amax;
    u_39 <= amax;
    u_40 <= amax;
    u_41 <= amax;
    u_42 <= amax;
    u_43 <= amax;
    u_44 <= amax;
    -vmax <= x_1(3);
    -vmax <= x_2(3);
    -vmax <= x_3(3);
    -vmax <= x_4(3);
    -vmax <= x_5(3);
    -vmax <= x_6(3);
    -vmax <= x_7(3);
    -vmax <= x_8(3);
    -vmax <= x_9(3);
    -vmax <= x_10(3);
    -vmax <= x_11(3);
    -vmax <= x_12(3);
    -vmax <= x_13(3);
    -vmax <= x_14(3);
    -vmax <= x_15(3);
    -vmax <= x_16(3);
    -vmax <= x_17(3);
    -vmax <= x_18(3);
    -vmax <= x_19(3);
    -vmax <= x_20(3);
    -vmax <= x_21(3);
    -vmax <= x_22(3);
    -vmax <= x_23(3);
    -vmax <= x_24(3);
    -vmax <= x_25(3);
    -vmax <= x_26(3);
    -vmax <= x_27(3);
    -vmax <= x_28(3);
    -vmax <= x_29(3);
    -vmax <= x_30(3);
    -vmax <= x_31(3);
    -vmax <= x_32(3);
    -vmax <= x_33(3);
    -vmax <= x_34(3);
    -vmax <= x_35(3);
    -vmax <= x_36(3);
    -vmax <= x_37(3);
    -vmax <= x_38(3);
    -vmax <= x_39(3);
    -vmax <= x_40(3);
    -vmax <= x_41(3);
    -vmax <= x_42(3);
    -vmax <= x_43(3);
    -vmax <= x_44(3);
    -vmax <= x_45(3);
    x_1(3) <= vmax;
    x_2(3) <= vmax;
    x_3(3) <= vmax;
    x_4(3) <= vmax;
    x_5(3) <= vmax;
    x_6(3) <= vmax;
    x_7(3) <= vmax;
    x_8(3) <= vmax;
    x_9(3) <= vmax;
    x_10(3) <= vmax;
    x_11(3) <= vmax;
    x_12(3) <= vmax;
    x_13(3) <= vmax;
    x_14(3) <= vmax;
    x_15(3) <= vmax;
    x_16(3) <= vmax;
    x_17(3) <= vmax;
    x_18(3) <= vmax;
    x_19(3) <= vmax;
    x_20(3) <= vmax;
    x_21(3) <= vmax;
    x_22(3) <= vmax;
    x_23(3) <= vmax;
    x_24(3) <= vmax;
    x_25(3) <= vmax;
    x_26(3) <= vmax;
    x_27(3) <= vmax;
    x_28(3) <= vmax;
    x_29(3) <= vmax;
    x_30(3) <= vmax;
    x_31(3) <= vmax;
    x_32(3) <= vmax;
    x_33(3) <= vmax;
    x_34(3) <= vmax;
    x_35(3) <= vmax;
    x_36(3) <= vmax;
    x_37(3) <= vmax;
    x_38(3) <= vmax;
    x_39(3) <= vmax;
    x_40(3) <= vmax;
    x_41(3) <= vmax;
    x_42(3) <= vmax;
    x_43(3) <= vmax;
    x_44(3) <= vmax;
    x_45(3) <= vmax;
    -vmax <= x_1(4);
    -vmax <= x_2(4);
    -vmax <= x_3(4);
    -vmax <= x_4(4);
    -vmax <= x_5(4);
    -vmax <= x_6(4);
    -vmax <= x_7(4);
    -vmax <= x_8(4);
    -vmax <= x_9(4);
    -vmax <= x_10(4);
    -vmax <= x_11(4);
    -vmax <= x_12(4);
    -vmax <= x_13(4);
    -vmax <= x_14(4);
    -vmax <= x_15(4);
    -vmax <= x_16(4);
    -vmax <= x_17(4);
    -vmax <= x_18(4);
    -vmax <= x_19(4);
    -vmax <= x_20(4);
    -vmax <= x_21(4);
    -vmax <= x_22(4);
    -vmax <= x_23(4);
    -vmax <= x_24(4);
    -vmax <= x_25(4);
    -vmax <= x_26(4);
    -vmax <= x_27(4);
    -vmax <= x_28(4);
    -vmax <= x_29(4);
    -vmax <= x_30(4);
    -vmax <= x_31(4);
    -vmax <= x_32(4);
    -vmax <= x_33(4);
    -vmax <= x_34(4);
    -vmax <= x_35(4);
    -vmax <= x_36(4);
    -vmax <= x_37(4);
    -vmax <= x_38(4);
    -vmax <= x_39(4);
    -vmax <= x_40(4);
    -vmax <= x_41(4);
    -vmax <= x_42(4);
    -vmax <= x_43(4);
    -vmax <= x_44(4);
    -vmax <= x_45(4);
    x_1(4) <= vmax;
    x_2(4) <= vmax;
    x_3(4) <= vmax;
    x_4(4) <= vmax;
    x_5(4) <= vmax;
    x_6(4) <= vmax;
    x_7(4) <= vmax;
    x_8(4) <= vmax;
    x_9(4) <= vmax;
    x_10(4) <= vmax;
    x_11(4) <= vmax;
    x_12(4) <= vmax;
    x_13(4) <= vmax;
    x_14(4) <= vmax;
    x_15(4) <= vmax;
    x_16(4) <= vmax;
    x_17(4) <= vmax;
    x_18(4) <= vmax;
    x_19(4) <= vmax;
    x_20(4) <= vmax;
    x_21(4) <= vmax;
    x_22(4) <= vmax;
    x_23(4) <= vmax;
    x_24(4) <= vmax;
    x_25(4) <= vmax;
    x_26(4) <= vmax;
    x_27(4) <= vmax;
    x_28(4) <= vmax;
    x_29(4) <= vmax;
    x_30(4) <= vmax;
    x_31(4) <= vmax;
    x_32(4) <= vmax;
    x_33(4) <= vmax;
    x_34(4) <= vmax;
    x_35(4) <= vmax;
    x_36(4) <= vmax;
    x_37(4) <= vmax;
    x_38(4) <= vmax;
    x_39(4) <= vmax;
    x_40(4) <= vmax;
    x_41(4) <= vmax;
    x_42(4) <= vmax;
    x_43(4) <= vmax;
    x_44(4) <= vmax;
    x_45(4) <= vmax;
cvx_end
vars.u_0 = u_0;
vars.u_1 = u_1;
vars.u{1} = u_1;
vars.u_2 = u_2;
vars.u{2} = u_2;
vars.u_3 = u_3;
vars.u{3} = u_3;
vars.u_4 = u_4;
vars.u{4} = u_4;
vars.u_5 = u_5;
vars.u{5} = u_5;
vars.u_6 = u_6;
vars.u{6} = u_6;
vars.u_7 = u_7;
vars.u{7} = u_7;
vars.u_8 = u_8;
vars.u{8} = u_8;
vars.u_9 = u_9;
vars.u{9} = u_9;
vars.u_10 = u_10;
vars.u{10} = u_10;
vars.u_11 = u_11;
vars.u{11} = u_11;
vars.u_12 = u_12;
vars.u{12} = u_12;
vars.u_13 = u_13;
vars.u{13} = u_13;
vars.u_14 = u_14;
vars.u{14} = u_14;
vars.u_15 = u_15;
vars.u{15} = u_15;
vars.u_16 = u_16;
vars.u{16} = u_16;
vars.u_17 = u_17;
vars.u{17} = u_17;
vars.u_18 = u_18;
vars.u{18} = u_18;
vars.u_19 = u_19;
vars.u{19} = u_19;
vars.u_20 = u_20;
vars.u{20} = u_20;
vars.u_21 = u_21;
vars.u{21} = u_21;
vars.u_22 = u_22;
vars.u{22} = u_22;
vars.u_23 = u_23;
vars.u{23} = u_23;
vars.u_24 = u_24;
vars.u{24} = u_24;
vars.u_25 = u_25;
vars.u{25} = u_25;
vars.u_26 = u_26;
vars.u{26} = u_26;
vars.u_27 = u_27;
vars.u{27} = u_27;
vars.u_28 = u_28;
vars.u{28} = u_28;
vars.u_29 = u_29;
vars.u{29} = u_29;
vars.u_30 = u_30;
vars.u{30} = u_30;
vars.u_31 = u_31;
vars.u{31} = u_31;
vars.u_32 = u_32;
vars.u{32} = u_32;
vars.u_33 = u_33;
vars.u{33} = u_33;
vars.u_34 = u_34;
vars.u{34} = u_34;
vars.u_35 = u_35;
vars.u{35} = u_35;
vars.u_36 = u_36;
vars.u{36} = u_36;
vars.u_37 = u_37;
vars.u{37} = u_37;
vars.u_38 = u_38;
vars.u{38} = u_38;
vars.u_39 = u_39;
vars.u{39} = u_39;
vars.u_40 = u_40;
vars.u{40} = u_40;
vars.u_41 = u_41;
vars.u{41} = u_41;
vars.u_42 = u_42;
vars.u{42} = u_42;
vars.u_43 = u_43;
vars.u{43} = u_43;
vars.u_44 = u_44;
vars.u{44} = u_44;
vars.x_1 = x_1;
vars.x{1} = x_1;
vars.x_2 = x_2;
vars.x{2} = x_2;
vars.x_3 = x_3;
vars.x{3} = x_3;
vars.x_4 = x_4;
vars.x{4} = x_4;
vars.x_5 = x_5;
vars.x{5} = x_5;
vars.x_6 = x_6;
vars.x{6} = x_6;
vars.x_7 = x_7;
vars.x{7} = x_7;
vars.x_8 = x_8;
vars.x{8} = x_8;
vars.x_9 = x_9;
vars.x{9} = x_9;
vars.x_10 = x_10;
vars.x{10} = x_10;
vars.x_11 = x_11;
vars.x{11} = x_11;
vars.x_12 = x_12;
vars.x{12} = x_12;
vars.x_13 = x_13;
vars.x{13} = x_13;
vars.x_14 = x_14;
vars.x{14} = x_14;
vars.x_15 = x_15;
vars.x{15} = x_15;
vars.x_16 = x_16;
vars.x{16} = x_16;
vars.x_17 = x_17;
vars.x{17} = x_17;
vars.x_18 = x_18;
vars.x{18} = x_18;
vars.x_19 = x_19;
vars.x{19} = x_19;
vars.x_20 = x_20;
vars.x{20} = x_20;
vars.x_21 = x_21;
vars.x{21} = x_21;
vars.x_22 = x_22;
vars.x{22} = x_22;
vars.x_23 = x_23;
vars.x{23} = x_23;
vars.x_24 = x_24;
vars.x{24} = x_24;
vars.x_25 = x_25;
vars.x{25} = x_25;
vars.x_26 = x_26;
vars.x{26} = x_26;
vars.x_27 = x_27;
vars.x{27} = x_27;
vars.x_28 = x_28;
vars.x{28} = x_28;
vars.x_29 = x_29;
vars.x{29} = x_29;
vars.x_30 = x_30;
vars.x{30} = x_30;
vars.x_31 = x_31;
vars.x{31} = x_31;
vars.x_32 = x_32;
vars.x{32} = x_32;
vars.x_33 = x_33;
vars.x{33} = x_33;
vars.x_34 = x_34;
vars.x{34} = x_34;
vars.x_35 = x_35;
vars.x{35} = x_35;
vars.x_36 = x_36;
vars.x{36} = x_36;
vars.x_37 = x_37;
vars.x{37} = x_37;
vars.x_38 = x_38;
vars.x{38} = x_38;
vars.x_39 = x_39;
vars.x{39} = x_39;
vars.x_40 = x_40;
vars.x{40} = x_40;
vars.x_41 = x_41;
vars.x{41} = x_41;
vars.x_42 = x_42;
vars.x{42} = x_42;
vars.x_43 = x_43;
vars.x{43} = x_43;
vars.x_44 = x_44;
vars.x{44} = x_44;
vars.x_45 = x_45;
vars.x{45} = x_45;
status.cvx_status = cvx_status;
% Provide a drop-in replacement for csolve.
status.optval = cvx_optval;
status.converged = strcmp(cvx_status, 'Solved');
