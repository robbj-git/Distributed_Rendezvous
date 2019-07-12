% Produced by CVXGEN, 2019-04-24 04:09:08 -0400.
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
if isfield(params, 'x_1')
  x_1 = params.x_1;
elseif isfield(params, 'x')
  x_1 = params.x{1};
else
  error 'could not find x_1'
end
if isfield(params, 'x_2')
  x_2 = params.x_2;
elseif isfield(params, 'x')
  x_2 = params.x{2};
else
  error 'could not find x_2'
end
if isfield(params, 'x_3')
  x_3 = params.x_3;
elseif isfield(params, 'x')
  x_3 = params.x{3};
else
  error 'could not find x_3'
end
if isfield(params, 'x_4')
  x_4 = params.x_4;
elseif isfield(params, 'x')
  x_4 = params.x{4};
else
  error 'could not find x_4'
end
if isfield(params, 'x_5')
  x_5 = params.x_5;
elseif isfield(params, 'x')
  x_5 = params.x{5};
else
  error 'could not find x_5'
end
if isfield(params, 'x_6')
  x_6 = params.x_6;
elseif isfield(params, 'x')
  x_6 = params.x{6};
else
  error 'could not find x_6'
end
if isfield(params, 'x_7')
  x_7 = params.x_7;
elseif isfield(params, 'x')
  x_7 = params.x{7};
else
  error 'could not find x_7'
end
if isfield(params, 'x_8')
  x_8 = params.x_8;
elseif isfield(params, 'x')
  x_8 = params.x{8};
else
  error 'could not find x_8'
end
if isfield(params, 'x_9')
  x_9 = params.x_9;
elseif isfield(params, 'x')
  x_9 = params.x{9};
else
  error 'could not find x_9'
end
if isfield(params, 'x_10')
  x_10 = params.x_10;
elseif isfield(params, 'x')
  x_10 = params.x{10};
else
  error 'could not find x_10'
end
if isfield(params, 'x_11')
  x_11 = params.x_11;
elseif isfield(params, 'x')
  x_11 = params.x{11};
else
  error 'could not find x_11'
end
if isfield(params, 'x_12')
  x_12 = params.x_12;
elseif isfield(params, 'x')
  x_12 = params.x{12};
else
  error 'could not find x_12'
end
if isfield(params, 'x_13')
  x_13 = params.x_13;
elseif isfield(params, 'x')
  x_13 = params.x{13};
else
  error 'could not find x_13'
end
if isfield(params, 'x_14')
  x_14 = params.x_14;
elseif isfield(params, 'x')
  x_14 = params.x{14};
else
  error 'could not find x_14'
end
if isfield(params, 'x_15')
  x_15 = params.x_15;
elseif isfield(params, 'x')
  x_15 = params.x{15};
else
  error 'could not find x_15'
end
if isfield(params, 'x_16')
  x_16 = params.x_16;
elseif isfield(params, 'x')
  x_16 = params.x{16};
else
  error 'could not find x_16'
end
if isfield(params, 'x_17')
  x_17 = params.x_17;
elseif isfield(params, 'x')
  x_17 = params.x{17};
else
  error 'could not find x_17'
end
if isfield(params, 'x_18')
  x_18 = params.x_18;
elseif isfield(params, 'x')
  x_18 = params.x{18};
else
  error 'could not find x_18'
end
if isfield(params, 'x_19')
  x_19 = params.x_19;
elseif isfield(params, 'x')
  x_19 = params.x{19};
else
  error 'could not find x_19'
end
if isfield(params, 'x_20')
  x_20 = params.x_20;
elseif isfield(params, 'x')
  x_20 = params.x{20};
else
  error 'could not find x_20'
end
if isfield(params, 'x_21')
  x_21 = params.x_21;
elseif isfield(params, 'x')
  x_21 = params.x{21};
else
  error 'could not find x_21'
end
if isfield(params, 'x_22')
  x_22 = params.x_22;
elseif isfield(params, 'x')
  x_22 = params.x{22};
else
  error 'could not find x_22'
end
if isfield(params, 'x_23')
  x_23 = params.x_23;
elseif isfield(params, 'x')
  x_23 = params.x{23};
else
  error 'could not find x_23'
end
if isfield(params, 'x_24')
  x_24 = params.x_24;
elseif isfield(params, 'x')
  x_24 = params.x{24};
else
  error 'could not find x_24'
end
if isfield(params, 'x_25')
  x_25 = params.x_25;
elseif isfield(params, 'x')
  x_25 = params.x{25};
else
  error 'could not find x_25'
end
if isfield(params, 'x_26')
  x_26 = params.x_26;
elseif isfield(params, 'x')
  x_26 = params.x{26};
else
  error 'could not find x_26'
end
if isfield(params, 'x_27')
  x_27 = params.x_27;
elseif isfield(params, 'x')
  x_27 = params.x{27};
else
  error 'could not find x_27'
end
if isfield(params, 'x_28')
  x_28 = params.x_28;
elseif isfield(params, 'x')
  x_28 = params.x{28};
else
  error 'could not find x_28'
end
if isfield(params, 'x_29')
  x_29 = params.x_29;
elseif isfield(params, 'x')
  x_29 = params.x{29};
else
  error 'could not find x_29'
end
if isfield(params, 'x_30')
  x_30 = params.x_30;
elseif isfield(params, 'x')
  x_30 = params.x{30};
else
  error 'could not find x_30'
end
if isfield(params, 'x_31')
  x_31 = params.x_31;
elseif isfield(params, 'x')
  x_31 = params.x{31};
else
  error 'could not find x_31'
end
if isfield(params, 'x_32')
  x_32 = params.x_32;
elseif isfield(params, 'x')
  x_32 = params.x{32};
else
  error 'could not find x_32'
end
if isfield(params, 'x_33')
  x_33 = params.x_33;
elseif isfield(params, 'x')
  x_33 = params.x{33};
else
  error 'could not find x_33'
end
if isfield(params, 'x_34')
  x_34 = params.x_34;
elseif isfield(params, 'x')
  x_34 = params.x{34};
else
  error 'could not find x_34'
end
if isfield(params, 'x_35')
  x_35 = params.x_35;
elseif isfield(params, 'x')
  x_35 = params.x{35};
else
  error 'could not find x_35'
end
if isfield(params, 'x_36')
  x_36 = params.x_36;
elseif isfield(params, 'x')
  x_36 = params.x{36};
else
  error 'could not find x_36'
end
if isfield(params, 'x_37')
  x_37 = params.x_37;
elseif isfield(params, 'x')
  x_37 = params.x{37};
else
  error 'could not find x_37'
end
if isfield(params, 'x_38')
  x_38 = params.x_38;
elseif isfield(params, 'x')
  x_38 = params.x{38};
else
  error 'could not find x_38'
end
if isfield(params, 'x_39')
  x_39 = params.x_39;
elseif isfield(params, 'x')
  x_39 = params.x{39};
else
  error 'could not find x_39'
end
if isfield(params, 'x_40')
  x_40 = params.x_40;
elseif isfield(params, 'x')
  x_40 = params.x{40};
else
  error 'could not find x_40'
end
if isfield(params, 'x_41')
  x_41 = params.x_41;
elseif isfield(params, 'x')
  x_41 = params.x{41};
else
  error 'could not find x_41'
end
if isfield(params, 'x_42')
  x_42 = params.x_42;
elseif isfield(params, 'x')
  x_42 = params.x{42};
else
  error 'could not find x_42'
end
if isfield(params, 'x_43')
  x_43 = params.x_43;
elseif isfield(params, 'x')
  x_43 = params.x{43};
else
  error 'could not find x_43'
end
if isfield(params, 'x_44')
  x_44 = params.x_44;
elseif isfield(params, 'x')
  x_44 = params.x{44};
else
  error 'could not find x_44'
end
if isfield(params, 'x_45')
  x_45 = params.x_45;
elseif isfield(params, 'x')
  x_45 = params.x{45};
else
  error 'could not find x_45'
end
xb_0 = params.xb_0;
cvx_begin
  % Caution: automatically generated by cvxgen. May be incorrect.
  variable ub_0(2, 1);
  variable xb_1(4, 1);
  variable ub_1(2, 1);
  variable xb_2(4, 1);
  variable ub_2(2, 1);
  variable xb_3(4, 1);
  variable ub_3(2, 1);
  variable xb_4(4, 1);
  variable ub_4(2, 1);
  variable xb_5(4, 1);
  variable ub_5(2, 1);
  variable xb_6(4, 1);
  variable ub_6(2, 1);
  variable xb_7(4, 1);
  variable ub_7(2, 1);
  variable xb_8(4, 1);
  variable ub_8(2, 1);
  variable xb_9(4, 1);
  variable ub_9(2, 1);
  variable xb_10(4, 1);
  variable ub_10(2, 1);
  variable xb_11(4, 1);
  variable ub_11(2, 1);
  variable xb_12(4, 1);
  variable ub_12(2, 1);
  variable xb_13(4, 1);
  variable ub_13(2, 1);
  variable xb_14(4, 1);
  variable ub_14(2, 1);
  variable xb_15(4, 1);
  variable ub_15(2, 1);
  variable xb_16(4, 1);
  variable ub_16(2, 1);
  variable xb_17(4, 1);
  variable ub_17(2, 1);
  variable xb_18(4, 1);
  variable ub_18(2, 1);
  variable xb_19(4, 1);
  variable ub_19(2, 1);
  variable xb_20(4, 1);
  variable ub_20(2, 1);
  variable xb_21(4, 1);
  variable ub_21(2, 1);
  variable xb_22(4, 1);
  variable ub_22(2, 1);
  variable xb_23(4, 1);
  variable ub_23(2, 1);
  variable xb_24(4, 1);
  variable ub_24(2, 1);
  variable xb_25(4, 1);
  variable ub_25(2, 1);
  variable xb_26(4, 1);
  variable ub_26(2, 1);
  variable xb_27(4, 1);
  variable ub_27(2, 1);
  variable xb_28(4, 1);
  variable ub_28(2, 1);
  variable xb_29(4, 1);
  variable ub_29(2, 1);
  variable xb_30(4, 1);
  variable ub_30(2, 1);
  variable xb_31(4, 1);
  variable ub_31(2, 1);
  variable xb_32(4, 1);
  variable ub_32(2, 1);
  variable xb_33(4, 1);
  variable ub_33(2, 1);
  variable xb_34(4, 1);
  variable ub_34(2, 1);
  variable xb_35(4, 1);
  variable ub_35(2, 1);
  variable xb_36(4, 1);
  variable ub_36(2, 1);
  variable xb_37(4, 1);
  variable ub_37(2, 1);
  variable xb_38(4, 1);
  variable ub_38(2, 1);
  variable xb_39(4, 1);
  variable ub_39(2, 1);
  variable xb_40(4, 1);
  variable ub_40(2, 1);
  variable xb_41(4, 1);
  variable ub_41(2, 1);
  variable xb_42(4, 1);
  variable ub_42(2, 1);
  variable xb_43(4, 1);
  variable ub_43(2, 1);
  variable xb_44(4, 1);
  variable ub_44(2, 1);
  variable xb_45(4, 1);

  minimize(quad_form(x_0 - xb_0, Q) + quad_form(ub_0, R) + quad_form(x_1 - xb_1, Q) + quad_form(ub_1, R) + quad_form(x_2 - xb_2, Q) + quad_form(ub_2, R) + quad_form(x_3 - xb_3, Q) + quad_form(ub_3, R) + quad_form(x_4 - xb_4, Q) + quad_form(ub_4, R) + quad_form(x_5 - xb_5, Q) + quad_form(ub_5, R) + quad_form(x_6 - xb_6, Q) + quad_form(ub_6, R) + quad_form(x_7 - xb_7, Q) + quad_form(ub_7, R) + quad_form(x_8 - xb_8, Q) + quad_form(ub_8, R) + quad_form(x_9 - xb_9, Q) + quad_form(ub_9, R) + quad_form(x_10 - xb_10, Q) + quad_form(ub_10, R) + quad_form(x_11 - xb_11, Q) + quad_form(ub_11, R) + quad_form(x_12 - xb_12, Q) + quad_form(ub_12, R) + quad_form(x_13 - xb_13, Q) + quad_form(ub_13, R) + quad_form(x_14 - xb_14, Q) + quad_form(ub_14, R) + quad_form(x_15 - xb_15, Q) + quad_form(ub_15, R) + quad_form(x_16 - xb_16, Q) + quad_form(ub_16, R) + quad_form(x_17 - xb_17, Q) + quad_form(ub_17, R) + quad_form(x_18 - xb_18, Q) + quad_form(ub_18, R) + quad_form(x_19 - xb_19, Q) + quad_form(ub_19, R) + quad_form(x_20 - xb_20, Q) + quad_form(ub_20, R) + quad_form(x_21 - xb_21, Q) + quad_form(ub_21, R) + quad_form(x_22 - xb_22, Q) + quad_form(ub_22, R) + quad_form(x_23 - xb_23, Q) + quad_form(ub_23, R) + quad_form(x_24 - xb_24, Q) + quad_form(ub_24, R) + quad_form(x_25 - xb_25, Q) + quad_form(ub_25, R) + quad_form(x_26 - xb_26, Q) + quad_form(ub_26, R) + quad_form(x_27 - xb_27, Q) + quad_form(ub_27, R) + quad_form(x_28 - xb_28, Q) + quad_form(ub_28, R) + quad_form(x_29 - xb_29, Q) + quad_form(ub_29, R) + quad_form(x_30 - xb_30, Q) + quad_form(ub_30, R) + quad_form(x_31 - xb_31, Q) + quad_form(ub_31, R) + quad_form(x_32 - xb_32, Q) + quad_form(ub_32, R) + quad_form(x_33 - xb_33, Q) + quad_form(ub_33, R) + quad_form(x_34 - xb_34, Q) + quad_form(ub_34, R) + quad_form(x_35 - xb_35, Q) + quad_form(ub_35, R) + quad_form(x_36 - xb_36, Q) + quad_form(ub_36, R) + quad_form(x_37 - xb_37, Q) + quad_form(ub_37, R) + quad_form(x_38 - xb_38, Q) + quad_form(ub_38, R) + quad_form(x_39 - xb_39, Q) + quad_form(ub_39, R) + quad_form(x_40 - xb_40, Q) + quad_form(ub_40, R) + quad_form(x_41 - xb_41, Q) + quad_form(ub_41, R) + quad_form(x_42 - xb_42, Q) + quad_form(ub_42, R) + quad_form(x_43 - xb_43, Q) + quad_form(ub_43, R) + quad_form(x_44 - xb_44, Q) + quad_form(ub_44, R) + quad_form(x_45 - xb_45, P));
  subject to
    xb_1 == A*xb_0 + B*ub_0;
    xb_2 == A*xb_1 + B*ub_1;
    xb_3 == A*xb_2 + B*ub_2;
    xb_4 == A*xb_3 + B*ub_3;
    xb_5 == A*xb_4 + B*ub_4;
    xb_6 == A*xb_5 + B*ub_5;
    xb_7 == A*xb_6 + B*ub_6;
    xb_8 == A*xb_7 + B*ub_7;
    xb_9 == A*xb_8 + B*ub_8;
    xb_10 == A*xb_9 + B*ub_9;
    xb_11 == A*xb_10 + B*ub_10;
    xb_12 == A*xb_11 + B*ub_11;
    xb_13 == A*xb_12 + B*ub_12;
    xb_14 == A*xb_13 + B*ub_13;
    xb_15 == A*xb_14 + B*ub_14;
    xb_16 == A*xb_15 + B*ub_15;
    xb_17 == A*xb_16 + B*ub_16;
    xb_18 == A*xb_17 + B*ub_17;
    xb_19 == A*xb_18 + B*ub_18;
    xb_20 == A*xb_19 + B*ub_19;
    xb_21 == A*xb_20 + B*ub_20;
    xb_22 == A*xb_21 + B*ub_21;
    xb_23 == A*xb_22 + B*ub_22;
    xb_24 == A*xb_23 + B*ub_23;
    xb_25 == A*xb_24 + B*ub_24;
    xb_26 == A*xb_25 + B*ub_25;
    xb_27 == A*xb_26 + B*ub_26;
    xb_28 == A*xb_27 + B*ub_27;
    xb_29 == A*xb_28 + B*ub_28;
    xb_30 == A*xb_29 + B*ub_29;
    xb_31 == A*xb_30 + B*ub_30;
    xb_32 == A*xb_31 + B*ub_31;
    xb_33 == A*xb_32 + B*ub_32;
    xb_34 == A*xb_33 + B*ub_33;
    xb_35 == A*xb_34 + B*ub_34;
    xb_36 == A*xb_35 + B*ub_35;
    xb_37 == A*xb_36 + B*ub_36;
    xb_38 == A*xb_37 + B*ub_37;
    xb_39 == A*xb_38 + B*ub_38;
    xb_40 == A*xb_39 + B*ub_39;
    xb_41 == A*xb_40 + B*ub_40;
    xb_42 == A*xb_41 + B*ub_41;
    xb_43 == A*xb_42 + B*ub_42;
    xb_44 == A*xb_43 + B*ub_43;
    xb_45 == A*xb_44 + B*ub_44;
    amin <= ub_0;
    amin <= ub_1;
    amin <= ub_2;
    amin <= ub_3;
    amin <= ub_4;
    amin <= ub_5;
    amin <= ub_6;
    amin <= ub_7;
    amin <= ub_8;
    amin <= ub_9;
    amin <= ub_10;
    amin <= ub_11;
    amin <= ub_12;
    amin <= ub_13;
    amin <= ub_14;
    amin <= ub_15;
    amin <= ub_16;
    amin <= ub_17;
    amin <= ub_18;
    amin <= ub_19;
    amin <= ub_20;
    amin <= ub_21;
    amin <= ub_22;
    amin <= ub_23;
    amin <= ub_24;
    amin <= ub_25;
    amin <= ub_26;
    amin <= ub_27;
    amin <= ub_28;
    amin <= ub_29;
    amin <= ub_30;
    amin <= ub_31;
    amin <= ub_32;
    amin <= ub_33;
    amin <= ub_34;
    amin <= ub_35;
    amin <= ub_36;
    amin <= ub_37;
    amin <= ub_38;
    amin <= ub_39;
    amin <= ub_40;
    amin <= ub_41;
    amin <= ub_42;
    amin <= ub_43;
    amin <= ub_44;
    ub_0 <= amax;
    ub_1 <= amax;
    ub_2 <= amax;
    ub_3 <= amax;
    ub_4 <= amax;
    ub_5 <= amax;
    ub_6 <= amax;
    ub_7 <= amax;
    ub_8 <= amax;
    ub_9 <= amax;
    ub_10 <= amax;
    ub_11 <= amax;
    ub_12 <= amax;
    ub_13 <= amax;
    ub_14 <= amax;
    ub_15 <= amax;
    ub_16 <= amax;
    ub_17 <= amax;
    ub_18 <= amax;
    ub_19 <= amax;
    ub_20 <= amax;
    ub_21 <= amax;
    ub_22 <= amax;
    ub_23 <= amax;
    ub_24 <= amax;
    ub_25 <= amax;
    ub_26 <= amax;
    ub_27 <= amax;
    ub_28 <= amax;
    ub_29 <= amax;
    ub_30 <= amax;
    ub_31 <= amax;
    ub_32 <= amax;
    ub_33 <= amax;
    ub_34 <= amax;
    ub_35 <= amax;
    ub_36 <= amax;
    ub_37 <= amax;
    ub_38 <= amax;
    ub_39 <= amax;
    ub_40 <= amax;
    ub_41 <= amax;
    ub_42 <= amax;
    ub_43 <= amax;
    ub_44 <= amax;
    -vmax <= xb_1(3);
    -vmax <= xb_2(3);
    -vmax <= xb_3(3);
    -vmax <= xb_4(3);
    -vmax <= xb_5(3);
    -vmax <= xb_6(3);
    -vmax <= xb_7(3);
    -vmax <= xb_8(3);
    -vmax <= xb_9(3);
    -vmax <= xb_10(3);
    -vmax <= xb_11(3);
    -vmax <= xb_12(3);
    -vmax <= xb_13(3);
    -vmax <= xb_14(3);
    -vmax <= xb_15(3);
    -vmax <= xb_16(3);
    -vmax <= xb_17(3);
    -vmax <= xb_18(3);
    -vmax <= xb_19(3);
    -vmax <= xb_20(3);
    -vmax <= xb_21(3);
    -vmax <= xb_22(3);
    -vmax <= xb_23(3);
    -vmax <= xb_24(3);
    -vmax <= xb_25(3);
    -vmax <= xb_26(3);
    -vmax <= xb_27(3);
    -vmax <= xb_28(3);
    -vmax <= xb_29(3);
    -vmax <= xb_30(3);
    -vmax <= xb_31(3);
    -vmax <= xb_32(3);
    -vmax <= xb_33(3);
    -vmax <= xb_34(3);
    -vmax <= xb_35(3);
    -vmax <= xb_36(3);
    -vmax <= xb_37(3);
    -vmax <= xb_38(3);
    -vmax <= xb_39(3);
    -vmax <= xb_40(3);
    -vmax <= xb_41(3);
    -vmax <= xb_42(3);
    -vmax <= xb_43(3);
    -vmax <= xb_44(3);
    -vmax <= xb_45(3);
    xb_1(3) <= vmax;
    xb_2(3) <= vmax;
    xb_3(3) <= vmax;
    xb_4(3) <= vmax;
    xb_5(3) <= vmax;
    xb_6(3) <= vmax;
    xb_7(3) <= vmax;
    xb_8(3) <= vmax;
    xb_9(3) <= vmax;
    xb_10(3) <= vmax;
    xb_11(3) <= vmax;
    xb_12(3) <= vmax;
    xb_13(3) <= vmax;
    xb_14(3) <= vmax;
    xb_15(3) <= vmax;
    xb_16(3) <= vmax;
    xb_17(3) <= vmax;
    xb_18(3) <= vmax;
    xb_19(3) <= vmax;
    xb_20(3) <= vmax;
    xb_21(3) <= vmax;
    xb_22(3) <= vmax;
    xb_23(3) <= vmax;
    xb_24(3) <= vmax;
    xb_25(3) <= vmax;
    xb_26(3) <= vmax;
    xb_27(3) <= vmax;
    xb_28(3) <= vmax;
    xb_29(3) <= vmax;
    xb_30(3) <= vmax;
    xb_31(3) <= vmax;
    xb_32(3) <= vmax;
    xb_33(3) <= vmax;
    xb_34(3) <= vmax;
    xb_35(3) <= vmax;
    xb_36(3) <= vmax;
    xb_37(3) <= vmax;
    xb_38(3) <= vmax;
    xb_39(3) <= vmax;
    xb_40(3) <= vmax;
    xb_41(3) <= vmax;
    xb_42(3) <= vmax;
    xb_43(3) <= vmax;
    xb_44(3) <= vmax;
    xb_45(3) <= vmax;
    -vmax <= xb_1(4);
    -vmax <= xb_2(4);
    -vmax <= xb_3(4);
    -vmax <= xb_4(4);
    -vmax <= xb_5(4);
    -vmax <= xb_6(4);
    -vmax <= xb_7(4);
    -vmax <= xb_8(4);
    -vmax <= xb_9(4);
    -vmax <= xb_10(4);
    -vmax <= xb_11(4);
    -vmax <= xb_12(4);
    -vmax <= xb_13(4);
    -vmax <= xb_14(4);
    -vmax <= xb_15(4);
    -vmax <= xb_16(4);
    -vmax <= xb_17(4);
    -vmax <= xb_18(4);
    -vmax <= xb_19(4);
    -vmax <= xb_20(4);
    -vmax <= xb_21(4);
    -vmax <= xb_22(4);
    -vmax <= xb_23(4);
    -vmax <= xb_24(4);
    -vmax <= xb_25(4);
    -vmax <= xb_26(4);
    -vmax <= xb_27(4);
    -vmax <= xb_28(4);
    -vmax <= xb_29(4);
    -vmax <= xb_30(4);
    -vmax <= xb_31(4);
    -vmax <= xb_32(4);
    -vmax <= xb_33(4);
    -vmax <= xb_34(4);
    -vmax <= xb_35(4);
    -vmax <= xb_36(4);
    -vmax <= xb_37(4);
    -vmax <= xb_38(4);
    -vmax <= xb_39(4);
    -vmax <= xb_40(4);
    -vmax <= xb_41(4);
    -vmax <= xb_42(4);
    -vmax <= xb_43(4);
    -vmax <= xb_44(4);
    -vmax <= xb_45(4);
    xb_1(4) <= vmax;
    xb_2(4) <= vmax;
    xb_3(4) <= vmax;
    xb_4(4) <= vmax;
    xb_5(4) <= vmax;
    xb_6(4) <= vmax;
    xb_7(4) <= vmax;
    xb_8(4) <= vmax;
    xb_9(4) <= vmax;
    xb_10(4) <= vmax;
    xb_11(4) <= vmax;
    xb_12(4) <= vmax;
    xb_13(4) <= vmax;
    xb_14(4) <= vmax;
    xb_15(4) <= vmax;
    xb_16(4) <= vmax;
    xb_17(4) <= vmax;
    xb_18(4) <= vmax;
    xb_19(4) <= vmax;
    xb_20(4) <= vmax;
    xb_21(4) <= vmax;
    xb_22(4) <= vmax;
    xb_23(4) <= vmax;
    xb_24(4) <= vmax;
    xb_25(4) <= vmax;
    xb_26(4) <= vmax;
    xb_27(4) <= vmax;
    xb_28(4) <= vmax;
    xb_29(4) <= vmax;
    xb_30(4) <= vmax;
    xb_31(4) <= vmax;
    xb_32(4) <= vmax;
    xb_33(4) <= vmax;
    xb_34(4) <= vmax;
    xb_35(4) <= vmax;
    xb_36(4) <= vmax;
    xb_37(4) <= vmax;
    xb_38(4) <= vmax;
    xb_39(4) <= vmax;
    xb_40(4) <= vmax;
    xb_41(4) <= vmax;
    xb_42(4) <= vmax;
    xb_43(4) <= vmax;
    xb_44(4) <= vmax;
    xb_45(4) <= vmax;
cvx_end
vars.ub_0 = ub_0;
vars.ub_1 = ub_1;
vars.ub{1} = ub_1;
vars.ub_2 = ub_2;
vars.ub{2} = ub_2;
vars.ub_3 = ub_3;
vars.ub{3} = ub_3;
vars.ub_4 = ub_4;
vars.ub{4} = ub_4;
vars.ub_5 = ub_5;
vars.ub{5} = ub_5;
vars.ub_6 = ub_6;
vars.ub{6} = ub_6;
vars.ub_7 = ub_7;
vars.ub{7} = ub_7;
vars.ub_8 = ub_8;
vars.ub{8} = ub_8;
vars.ub_9 = ub_9;
vars.ub{9} = ub_9;
vars.ub_10 = ub_10;
vars.ub{10} = ub_10;
vars.ub_11 = ub_11;
vars.ub{11} = ub_11;
vars.ub_12 = ub_12;
vars.ub{12} = ub_12;
vars.ub_13 = ub_13;
vars.ub{13} = ub_13;
vars.ub_14 = ub_14;
vars.ub{14} = ub_14;
vars.ub_15 = ub_15;
vars.ub{15} = ub_15;
vars.ub_16 = ub_16;
vars.ub{16} = ub_16;
vars.ub_17 = ub_17;
vars.ub{17} = ub_17;
vars.ub_18 = ub_18;
vars.ub{18} = ub_18;
vars.ub_19 = ub_19;
vars.ub{19} = ub_19;
vars.ub_20 = ub_20;
vars.ub{20} = ub_20;
vars.ub_21 = ub_21;
vars.ub{21} = ub_21;
vars.ub_22 = ub_22;
vars.ub{22} = ub_22;
vars.ub_23 = ub_23;
vars.ub{23} = ub_23;
vars.ub_24 = ub_24;
vars.ub{24} = ub_24;
vars.ub_25 = ub_25;
vars.ub{25} = ub_25;
vars.ub_26 = ub_26;
vars.ub{26} = ub_26;
vars.ub_27 = ub_27;
vars.ub{27} = ub_27;
vars.ub_28 = ub_28;
vars.ub{28} = ub_28;
vars.ub_29 = ub_29;
vars.ub{29} = ub_29;
vars.ub_30 = ub_30;
vars.ub{30} = ub_30;
vars.ub_31 = ub_31;
vars.ub{31} = ub_31;
vars.ub_32 = ub_32;
vars.ub{32} = ub_32;
vars.ub_33 = ub_33;
vars.ub{33} = ub_33;
vars.ub_34 = ub_34;
vars.ub{34} = ub_34;
vars.ub_35 = ub_35;
vars.ub{35} = ub_35;
vars.ub_36 = ub_36;
vars.ub{36} = ub_36;
vars.ub_37 = ub_37;
vars.ub{37} = ub_37;
vars.ub_38 = ub_38;
vars.ub{38} = ub_38;
vars.ub_39 = ub_39;
vars.ub{39} = ub_39;
vars.ub_40 = ub_40;
vars.ub{40} = ub_40;
vars.ub_41 = ub_41;
vars.ub{41} = ub_41;
vars.ub_42 = ub_42;
vars.ub{42} = ub_42;
vars.ub_43 = ub_43;
vars.ub{43} = ub_43;
vars.ub_44 = ub_44;
vars.ub{44} = ub_44;
vars.xb_1 = xb_1;
vars.xb{1} = xb_1;
vars.xb_2 = xb_2;
vars.xb{2} = xb_2;
vars.xb_3 = xb_3;
vars.xb{3} = xb_3;
vars.xb_4 = xb_4;
vars.xb{4} = xb_4;
vars.xb_5 = xb_5;
vars.xb{5} = xb_5;
vars.xb_6 = xb_6;
vars.xb{6} = xb_6;
vars.xb_7 = xb_7;
vars.xb{7} = xb_7;
vars.xb_8 = xb_8;
vars.xb{8} = xb_8;
vars.xb_9 = xb_9;
vars.xb{9} = xb_9;
vars.xb_10 = xb_10;
vars.xb{10} = xb_10;
vars.xb_11 = xb_11;
vars.xb{11} = xb_11;
vars.xb_12 = xb_12;
vars.xb{12} = xb_12;
vars.xb_13 = xb_13;
vars.xb{13} = xb_13;
vars.xb_14 = xb_14;
vars.xb{14} = xb_14;
vars.xb_15 = xb_15;
vars.xb{15} = xb_15;
vars.xb_16 = xb_16;
vars.xb{16} = xb_16;
vars.xb_17 = xb_17;
vars.xb{17} = xb_17;
vars.xb_18 = xb_18;
vars.xb{18} = xb_18;
vars.xb_19 = xb_19;
vars.xb{19} = xb_19;
vars.xb_20 = xb_20;
vars.xb{20} = xb_20;
vars.xb_21 = xb_21;
vars.xb{21} = xb_21;
vars.xb_22 = xb_22;
vars.xb{22} = xb_22;
vars.xb_23 = xb_23;
vars.xb{23} = xb_23;
vars.xb_24 = xb_24;
vars.xb{24} = xb_24;
vars.xb_25 = xb_25;
vars.xb{25} = xb_25;
vars.xb_26 = xb_26;
vars.xb{26} = xb_26;
vars.xb_27 = xb_27;
vars.xb{27} = xb_27;
vars.xb_28 = xb_28;
vars.xb{28} = xb_28;
vars.xb_29 = xb_29;
vars.xb{29} = xb_29;
vars.xb_30 = xb_30;
vars.xb{30} = xb_30;
vars.xb_31 = xb_31;
vars.xb{31} = xb_31;
vars.xb_32 = xb_32;
vars.xb{32} = xb_32;
vars.xb_33 = xb_33;
vars.xb{33} = xb_33;
vars.xb_34 = xb_34;
vars.xb{34} = xb_34;
vars.xb_35 = xb_35;
vars.xb{35} = xb_35;
vars.xb_36 = xb_36;
vars.xb{36} = xb_36;
vars.xb_37 = xb_37;
vars.xb{37} = xb_37;
vars.xb_38 = xb_38;
vars.xb{38} = xb_38;
vars.xb_39 = xb_39;
vars.xb{39} = xb_39;
vars.xb_40 = xb_40;
vars.xb{40} = xb_40;
vars.xb_41 = xb_41;
vars.xb{41} = xb_41;
vars.xb_42 = xb_42;
vars.xb{42} = xb_42;
vars.xb_43 = xb_43;
vars.xb{43} = xb_43;
vars.xb_44 = xb_44;
vars.xb{44} = xb_44;
vars.xb_45 = xb_45;
vars.xb{45} = xb_45;
status.cvx_status = cvx_status;
% Provide a drop-in replacement for csolve.
status.optval = cvx_optval;
status.converged = strcmp(cvx_status, 'Solved');
