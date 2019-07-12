% Produced by CVXGEN, 2019-04-24 11:04:00 -0400.
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
b_0 = params.b_0;
if isfield(params, 'b_1')
  b_1 = params.b_1;
elseif isfield(params, 'b')
  b_1 = params.b{1};
else
  error 'could not find b_1'
end
if isfield(params, 'b_2')
  b_2 = params.b_2;
elseif isfield(params, 'b')
  b_2 = params.b{2};
else
  error 'could not find b_2'
end
if isfield(params, 'b_3')
  b_3 = params.b_3;
elseif isfield(params, 'b')
  b_3 = params.b{3};
else
  error 'could not find b_3'
end
if isfield(params, 'b_4')
  b_4 = params.b_4;
elseif isfield(params, 'b')
  b_4 = params.b{4};
else
  error 'could not find b_4'
end
if isfield(params, 'b_5')
  b_5 = params.b_5;
elseif isfield(params, 'b')
  b_5 = params.b{5};
else
  error 'could not find b_5'
end
if isfield(params, 'b_6')
  b_6 = params.b_6;
elseif isfield(params, 'b')
  b_6 = params.b{6};
else
  error 'could not find b_6'
end
if isfield(params, 'b_7')
  b_7 = params.b_7;
elseif isfield(params, 'b')
  b_7 = params.b{7};
else
  error 'could not find b_7'
end
if isfield(params, 'b_8')
  b_8 = params.b_8;
elseif isfield(params, 'b')
  b_8 = params.b{8};
else
  error 'could not find b_8'
end
if isfield(params, 'b_9')
  b_9 = params.b_9;
elseif isfield(params, 'b')
  b_9 = params.b{9};
else
  error 'could not find b_9'
end
if isfield(params, 'b_10')
  b_10 = params.b_10;
elseif isfield(params, 'b')
  b_10 = params.b{10};
else
  error 'could not find b_10'
end
if isfield(params, 'b_11')
  b_11 = params.b_11;
elseif isfield(params, 'b')
  b_11 = params.b{11};
else
  error 'could not find b_11'
end
if isfield(params, 'b_12')
  b_12 = params.b_12;
elseif isfield(params, 'b')
  b_12 = params.b{12};
else
  error 'could not find b_12'
end
if isfield(params, 'b_13')
  b_13 = params.b_13;
elseif isfield(params, 'b')
  b_13 = params.b{13};
else
  error 'could not find b_13'
end
if isfield(params, 'b_14')
  b_14 = params.b_14;
elseif isfield(params, 'b')
  b_14 = params.b{14};
else
  error 'could not find b_14'
end
if isfield(params, 'b_15')
  b_15 = params.b_15;
elseif isfield(params, 'b')
  b_15 = params.b{15};
else
  error 'could not find b_15'
end
if isfield(params, 'b_16')
  b_16 = params.b_16;
elseif isfield(params, 'b')
  b_16 = params.b{16};
else
  error 'could not find b_16'
end
if isfield(params, 'b_17')
  b_17 = params.b_17;
elseif isfield(params, 'b')
  b_17 = params.b{17};
else
  error 'could not find b_17'
end
if isfield(params, 'b_18')
  b_18 = params.b_18;
elseif isfield(params, 'b')
  b_18 = params.b{18};
else
  error 'could not find b_18'
end
if isfield(params, 'b_19')
  b_19 = params.b_19;
elseif isfield(params, 'b')
  b_19 = params.b{19};
else
  error 'could not find b_19'
end
if isfield(params, 'b_20')
  b_20 = params.b_20;
elseif isfield(params, 'b')
  b_20 = params.b{20};
else
  error 'could not find b_20'
end
if isfield(params, 'b_21')
  b_21 = params.b_21;
elseif isfield(params, 'b')
  b_21 = params.b{21};
else
  error 'could not find b_21'
end
if isfield(params, 'b_22')
  b_22 = params.b_22;
elseif isfield(params, 'b')
  b_22 = params.b{22};
else
  error 'could not find b_22'
end
if isfield(params, 'b_23')
  b_23 = params.b_23;
elseif isfield(params, 'b')
  b_23 = params.b{23};
else
  error 'could not find b_23'
end
if isfield(params, 'b_24')
  b_24 = params.b_24;
elseif isfield(params, 'b')
  b_24 = params.b{24};
else
  error 'could not find b_24'
end
if isfield(params, 'b_25')
  b_25 = params.b_25;
elseif isfield(params, 'b')
  b_25 = params.b{25};
else
  error 'could not find b_25'
end
if isfield(params, 'b_26')
  b_26 = params.b_26;
elseif isfield(params, 'b')
  b_26 = params.b{26};
else
  error 'could not find b_26'
end
if isfield(params, 'b_27')
  b_27 = params.b_27;
elseif isfield(params, 'b')
  b_27 = params.b{27};
else
  error 'could not find b_27'
end
if isfield(params, 'b_28')
  b_28 = params.b_28;
elseif isfield(params, 'b')
  b_28 = params.b{28};
else
  error 'could not find b_28'
end
if isfield(params, 'b_29')
  b_29 = params.b_29;
elseif isfield(params, 'b')
  b_29 = params.b{29};
else
  error 'could not find b_29'
end
if isfield(params, 'b_30')
  b_30 = params.b_30;
elseif isfield(params, 'b')
  b_30 = params.b{30};
else
  error 'could not find b_30'
end
if isfield(params, 'b_31')
  b_31 = params.b_31;
elseif isfield(params, 'b')
  b_31 = params.b{31};
else
  error 'could not find b_31'
end
if isfield(params, 'b_32')
  b_32 = params.b_32;
elseif isfield(params, 'b')
  b_32 = params.b{32};
else
  error 'could not find b_32'
end
if isfield(params, 'b_33')
  b_33 = params.b_33;
elseif isfield(params, 'b')
  b_33 = params.b{33};
else
  error 'could not find b_33'
end
if isfield(params, 'b_34')
  b_34 = params.b_34;
elseif isfield(params, 'b')
  b_34 = params.b{34};
else
  error 'could not find b_34'
end
if isfield(params, 'b_35')
  b_35 = params.b_35;
elseif isfield(params, 'b')
  b_35 = params.b{35};
else
  error 'could not find b_35'
end
if isfield(params, 'b_36')
  b_36 = params.b_36;
elseif isfield(params, 'b')
  b_36 = params.b{36};
else
  error 'could not find b_36'
end
if isfield(params, 'b_37')
  b_37 = params.b_37;
elseif isfield(params, 'b')
  b_37 = params.b{37};
else
  error 'could not find b_37'
end
if isfield(params, 'b_38')
  b_38 = params.b_38;
elseif isfield(params, 'b')
  b_38 = params.b{38};
else
  error 'could not find b_38'
end
if isfield(params, 'b_39')
  b_39 = params.b_39;
elseif isfield(params, 'b')
  b_39 = params.b{39};
else
  error 'could not find b_39'
end
if isfield(params, 'b_40')
  b_40 = params.b_40;
elseif isfield(params, 'b')
  b_40 = params.b{40};
else
  error 'could not find b_40'
end
if isfield(params, 'b_41')
  b_41 = params.b_41;
elseif isfield(params, 'b')
  b_41 = params.b{41};
else
  error 'could not find b_41'
end
if isfield(params, 'b_42')
  b_42 = params.b_42;
elseif isfield(params, 'b')
  b_42 = params.b{42};
else
  error 'could not find b_42'
end
if isfield(params, 'b_43')
  b_43 = params.b_43;
elseif isfield(params, 'b')
  b_43 = params.b{43};
else
  error 'could not find b_43'
end
if isfield(params, 'b_44')
  b_44 = params.b_44;
elseif isfield(params, 'b')
  b_44 = params.b{44};
else
  error 'could not find b_44'
end
if isfield(params, 'b_45')
  b_45 = params.b_45;
elseif isfield(params, 'b')
  b_45 = params.b{45};
else
  error 'could not find b_45'
end
if isfield(params, 'dist_1')
  dist_1 = params.dist_1;
elseif isfield(params, 'dist')
  dist_1 = params.dist{1};
else
  error 'could not find dist_1'
end
if isfield(params, 'dist_2')
  dist_2 = params.dist_2;
elseif isfield(params, 'dist')
  dist_2 = params.dist{2};
else
  error 'could not find dist_2'
end
if isfield(params, 'dist_3')
  dist_3 = params.dist_3;
elseif isfield(params, 'dist')
  dist_3 = params.dist{3};
else
  error 'could not find dist_3'
end
if isfield(params, 'dist_4')
  dist_4 = params.dist_4;
elseif isfield(params, 'dist')
  dist_4 = params.dist{4};
else
  error 'could not find dist_4'
end
if isfield(params, 'dist_5')
  dist_5 = params.dist_5;
elseif isfield(params, 'dist')
  dist_5 = params.dist{5};
else
  error 'could not find dist_5'
end
if isfield(params, 'dist_6')
  dist_6 = params.dist_6;
elseif isfield(params, 'dist')
  dist_6 = params.dist{6};
else
  error 'could not find dist_6'
end
if isfield(params, 'dist_7')
  dist_7 = params.dist_7;
elseif isfield(params, 'dist')
  dist_7 = params.dist{7};
else
  error 'could not find dist_7'
end
if isfield(params, 'dist_8')
  dist_8 = params.dist_8;
elseif isfield(params, 'dist')
  dist_8 = params.dist{8};
else
  error 'could not find dist_8'
end
if isfield(params, 'dist_9')
  dist_9 = params.dist_9;
elseif isfield(params, 'dist')
  dist_9 = params.dist{9};
else
  error 'could not find dist_9'
end
if isfield(params, 'dist_10')
  dist_10 = params.dist_10;
elseif isfield(params, 'dist')
  dist_10 = params.dist{10};
else
  error 'could not find dist_10'
end
if isfield(params, 'dist_11')
  dist_11 = params.dist_11;
elseif isfield(params, 'dist')
  dist_11 = params.dist{11};
else
  error 'could not find dist_11'
end
if isfield(params, 'dist_12')
  dist_12 = params.dist_12;
elseif isfield(params, 'dist')
  dist_12 = params.dist{12};
else
  error 'could not find dist_12'
end
if isfield(params, 'dist_13')
  dist_13 = params.dist_13;
elseif isfield(params, 'dist')
  dist_13 = params.dist{13};
else
  error 'could not find dist_13'
end
if isfield(params, 'dist_14')
  dist_14 = params.dist_14;
elseif isfield(params, 'dist')
  dist_14 = params.dist{14};
else
  error 'could not find dist_14'
end
if isfield(params, 'dist_15')
  dist_15 = params.dist_15;
elseif isfield(params, 'dist')
  dist_15 = params.dist{15};
else
  error 'could not find dist_15'
end
if isfield(params, 'dist_16')
  dist_16 = params.dist_16;
elseif isfield(params, 'dist')
  dist_16 = params.dist{16};
else
  error 'could not find dist_16'
end
if isfield(params, 'dist_17')
  dist_17 = params.dist_17;
elseif isfield(params, 'dist')
  dist_17 = params.dist{17};
else
  error 'could not find dist_17'
end
if isfield(params, 'dist_18')
  dist_18 = params.dist_18;
elseif isfield(params, 'dist')
  dist_18 = params.dist{18};
else
  error 'could not find dist_18'
end
if isfield(params, 'dist_19')
  dist_19 = params.dist_19;
elseif isfield(params, 'dist')
  dist_19 = params.dist{19};
else
  error 'could not find dist_19'
end
if isfield(params, 'dist_20')
  dist_20 = params.dist_20;
elseif isfield(params, 'dist')
  dist_20 = params.dist{20};
else
  error 'could not find dist_20'
end
if isfield(params, 'dist_21')
  dist_21 = params.dist_21;
elseif isfield(params, 'dist')
  dist_21 = params.dist{21};
else
  error 'could not find dist_21'
end
if isfield(params, 'dist_22')
  dist_22 = params.dist_22;
elseif isfield(params, 'dist')
  dist_22 = params.dist{22};
else
  error 'could not find dist_22'
end
if isfield(params, 'dist_23')
  dist_23 = params.dist_23;
elseif isfield(params, 'dist')
  dist_23 = params.dist{23};
else
  error 'could not find dist_23'
end
if isfield(params, 'dist_24')
  dist_24 = params.dist_24;
elseif isfield(params, 'dist')
  dist_24 = params.dist{24};
else
  error 'could not find dist_24'
end
if isfield(params, 'dist_25')
  dist_25 = params.dist_25;
elseif isfield(params, 'dist')
  dist_25 = params.dist{25};
else
  error 'could not find dist_25'
end
if isfield(params, 'dist_26')
  dist_26 = params.dist_26;
elseif isfield(params, 'dist')
  dist_26 = params.dist{26};
else
  error 'could not find dist_26'
end
if isfield(params, 'dist_27')
  dist_27 = params.dist_27;
elseif isfield(params, 'dist')
  dist_27 = params.dist{27};
else
  error 'could not find dist_27'
end
if isfield(params, 'dist_28')
  dist_28 = params.dist_28;
elseif isfield(params, 'dist')
  dist_28 = params.dist{28};
else
  error 'could not find dist_28'
end
if isfield(params, 'dist_29')
  dist_29 = params.dist_29;
elseif isfield(params, 'dist')
  dist_29 = params.dist{29};
else
  error 'could not find dist_29'
end
if isfield(params, 'dist_30')
  dist_30 = params.dist_30;
elseif isfield(params, 'dist')
  dist_30 = params.dist{30};
else
  error 'could not find dist_30'
end
if isfield(params, 'dist_31')
  dist_31 = params.dist_31;
elseif isfield(params, 'dist')
  dist_31 = params.dist{31};
else
  error 'could not find dist_31'
end
if isfield(params, 'dist_32')
  dist_32 = params.dist_32;
elseif isfield(params, 'dist')
  dist_32 = params.dist{32};
else
  error 'could not find dist_32'
end
if isfield(params, 'dist_33')
  dist_33 = params.dist_33;
elseif isfield(params, 'dist')
  dist_33 = params.dist{33};
else
  error 'could not find dist_33'
end
if isfield(params, 'dist_34')
  dist_34 = params.dist_34;
elseif isfield(params, 'dist')
  dist_34 = params.dist{34};
else
  error 'could not find dist_34'
end
if isfield(params, 'dist_35')
  dist_35 = params.dist_35;
elseif isfield(params, 'dist')
  dist_35 = params.dist{35};
else
  error 'could not find dist_35'
end
if isfield(params, 'dist_36')
  dist_36 = params.dist_36;
elseif isfield(params, 'dist')
  dist_36 = params.dist{36};
else
  error 'could not find dist_36'
end
if isfield(params, 'dist_37')
  dist_37 = params.dist_37;
elseif isfield(params, 'dist')
  dist_37 = params.dist{37};
else
  error 'could not find dist_37'
end
if isfield(params, 'dist_38')
  dist_38 = params.dist_38;
elseif isfield(params, 'dist')
  dist_38 = params.dist{38};
else
  error 'could not find dist_38'
end
if isfield(params, 'dist_39')
  dist_39 = params.dist_39;
elseif isfield(params, 'dist')
  dist_39 = params.dist{39};
else
  error 'could not find dist_39'
end
if isfield(params, 'dist_40')
  dist_40 = params.dist_40;
elseif isfield(params, 'dist')
  dist_40 = params.dist{40};
else
  error 'could not find dist_40'
end
if isfield(params, 'dist_41')
  dist_41 = params.dist_41;
elseif isfield(params, 'dist')
  dist_41 = params.dist{41};
else
  error 'could not find dist_41'
end
if isfield(params, 'dist_42')
  dist_42 = params.dist_42;
elseif isfield(params, 'dist')
  dist_42 = params.dist{42};
else
  error 'could not find dist_42'
end
if isfield(params, 'dist_43')
  dist_43 = params.dist_43;
elseif isfield(params, 'dist')
  dist_43 = params.dist{43};
else
  error 'could not find dist_43'
end
if isfield(params, 'dist_44')
  dist_44 = params.dist_44;
elseif isfield(params, 'dist')
  dist_44 = params.dist{44};
else
  error 'could not find dist_44'
end
if isfield(params, 'dist_45')
  dist_45 = params.dist_45;
elseif isfield(params, 'dist')
  dist_45 = params.dist{45};
else
  error 'could not find dist_45'
end
dl = params.dl;
ds = params.ds;
hs = params.hs;
kl = params.kl;
wmax = params.wmax;
wmin = params.wmin;
wmin_land = params.wmin_land;
x_0 = params.x_0;
xb = params.xb;
cvx_begin
  % Caution: automatically generated by cvxgen. May be incorrect.
  variable u_0;
  variable x_1(2, 1);
  variable u_1;
  variable x_2(2, 1);
  variable u_2;
  variable x_3(2, 1);
  variable u_3;
  variable x_4(2, 1);
  variable u_4;
  variable x_5(2, 1);
  variable u_5;
  variable x_6(2, 1);
  variable u_6;
  variable x_7(2, 1);
  variable u_7;
  variable x_8(2, 1);
  variable u_8;
  variable x_9(2, 1);
  variable u_9;
  variable x_10(2, 1);
  variable u_10;
  variable x_11(2, 1);
  variable u_11;
  variable x_12(2, 1);
  variable u_12;
  variable x_13(2, 1);
  variable u_13;
  variable x_14(2, 1);
  variable u_14;
  variable x_15(2, 1);
  variable u_15;
  variable x_16(2, 1);
  variable u_16;
  variable x_17(2, 1);
  variable u_17;
  variable x_18(2, 1);
  variable u_18;
  variable x_19(2, 1);
  variable u_19;
  variable x_20(2, 1);
  variable u_20;
  variable x_21(2, 1);
  variable u_21;
  variable x_22(2, 1);
  variable u_22;
  variable x_23(2, 1);
  variable u_23;
  variable x_24(2, 1);
  variable u_24;
  variable x_25(2, 1);
  variable u_25;
  variable x_26(2, 1);
  variable u_26;
  variable x_27(2, 1);
  variable u_27;
  variable x_28(2, 1);
  variable u_28;
  variable x_29(2, 1);
  variable u_29;
  variable x_30(2, 1);
  variable u_30;
  variable x_31(2, 1);
  variable u_31;
  variable x_32(2, 1);
  variable u_32;
  variable x_33(2, 1);
  variable u_33;
  variable x_34(2, 1);
  variable u_34;
  variable x_35(2, 1);
  variable u_35;
  variable x_36(2, 1);
  variable u_36;
  variable x_37(2, 1);
  variable u_37;
  variable x_38(2, 1);
  variable u_38;
  variable x_39(2, 1);
  variable u_39;
  variable x_40(2, 1);
  variable u_40;
  variable x_41(2, 1);
  variable u_41;
  variable x_42(2, 1);
  variable u_42;
  variable x_43(2, 1);
  variable u_43;
  variable x_44(2, 1);
  variable u_44;
  variable x_45(2, 1);

  minimize(quad_form(b_0*(x_0 - xb), Q) + quad_form(u_0, R) + quad_form(b_1*(x_1 - xb), Q) + quad_form(u_1, R) + quad_form(b_2*(x_2 - xb), Q) + quad_form(u_2, R) + quad_form(b_3*(x_3 - xb), Q) + quad_form(u_3, R) + quad_form(b_4*(x_4 - xb), Q) + quad_form(u_4, R) + quad_form(b_5*(x_5 - xb), Q) + quad_form(u_5, R) + quad_form(b_6*(x_6 - xb), Q) + quad_form(u_6, R) + quad_form(b_7*(x_7 - xb), Q) + quad_form(u_7, R) + quad_form(b_8*(x_8 - xb), Q) + quad_form(u_8, R) + quad_form(b_9*(x_9 - xb), Q) + quad_form(u_9, R) + quad_form(b_10*(x_10 - xb), Q) + quad_form(u_10, R) + quad_form(b_11*(x_11 - xb), Q) + quad_form(u_11, R) + quad_form(b_12*(x_12 - xb), Q) + quad_form(u_12, R) + quad_form(b_13*(x_13 - xb), Q) + quad_form(u_13, R) + quad_form(b_14*(x_14 - xb), Q) + quad_form(u_14, R) + quad_form(b_15*(x_15 - xb), Q) + quad_form(u_15, R) + quad_form(b_16*(x_16 - xb), Q) + quad_form(u_16, R) + quad_form(b_17*(x_17 - xb), Q) + quad_form(u_17, R) + quad_form(b_18*(x_18 - xb), Q) + quad_form(u_18, R) + quad_form(b_19*(x_19 - xb), Q) + quad_form(u_19, R) + quad_form(b_20*(x_20 - xb), Q) + quad_form(u_20, R) + quad_form(b_21*(x_21 - xb), Q) + quad_form(u_21, R) + quad_form(b_22*(x_22 - xb), Q) + quad_form(u_22, R) + quad_form(b_23*(x_23 - xb), Q) + quad_form(u_23, R) + quad_form(b_24*(x_24 - xb), Q) + quad_form(u_24, R) + quad_form(b_25*(x_25 - xb), Q) + quad_form(u_25, R) + quad_form(b_26*(x_26 - xb), Q) + quad_form(u_26, R) + quad_form(b_27*(x_27 - xb), Q) + quad_form(u_27, R) + quad_form(b_28*(x_28 - xb), Q) + quad_form(u_28, R) + quad_form(b_29*(x_29 - xb), Q) + quad_form(u_29, R) + quad_form(b_30*(x_30 - xb), Q) + quad_form(u_30, R) + quad_form(b_31*(x_31 - xb), Q) + quad_form(u_31, R) + quad_form(b_32*(x_32 - xb), Q) + quad_form(u_32, R) + quad_form(b_33*(x_33 - xb), Q) + quad_form(u_33, R) + quad_form(b_34*(x_34 - xb), Q) + quad_form(u_34, R) + quad_form(b_35*(x_35 - xb), Q) + quad_form(u_35, R) + quad_form(b_36*(x_36 - xb), Q) + quad_form(u_36, R) + quad_form(b_37*(x_37 - xb), Q) + quad_form(u_37, R) + quad_form(b_38*(x_38 - xb), Q) + quad_form(u_38, R) + quad_form(b_39*(x_39 - xb), Q) + quad_form(u_39, R) + quad_form(b_40*(x_40 - xb), Q) + quad_form(u_40, R) + quad_form(b_41*(x_41 - xb), Q) + quad_form(u_41, R) + quad_form(b_42*(x_42 - xb), Q) + quad_form(u_42, R) + quad_form(b_43*(x_43 - xb), Q) + quad_form(u_43, R) + quad_form(b_44*(x_44 - xb), Q) + quad_form(u_44, R) + quad_form(b_45*(x_45 - xb), P));
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
    wmin <= x_1(2);
    wmin <= x_2(2);
    wmin <= x_3(2);
    wmin <= x_4(2);
    wmin <= x_5(2);
    wmin <= x_6(2);
    wmin <= x_7(2);
    wmin <= x_8(2);
    wmin <= x_9(2);
    wmin <= x_10(2);
    wmin <= x_11(2);
    wmin <= x_12(2);
    wmin <= x_13(2);
    wmin <= x_14(2);
    wmin <= x_15(2);
    wmin <= x_16(2);
    wmin <= x_17(2);
    wmin <= x_18(2);
    wmin <= x_19(2);
    wmin <= x_20(2);
    wmin <= x_21(2);
    wmin <= x_22(2);
    wmin <= x_23(2);
    wmin <= x_24(2);
    wmin <= x_25(2);
    wmin <= x_26(2);
    wmin <= x_27(2);
    wmin <= x_28(2);
    wmin <= x_29(2);
    wmin <= x_30(2);
    wmin <= x_31(2);
    wmin <= x_32(2);
    wmin <= x_33(2);
    wmin <= x_34(2);
    wmin <= x_35(2);
    wmin <= x_36(2);
    wmin <= x_37(2);
    wmin <= x_38(2);
    wmin <= x_39(2);
    wmin <= x_40(2);
    wmin <= x_41(2);
    wmin <= x_42(2);
    wmin <= x_43(2);
    wmin <= x_44(2);
    wmin <= x_45(2);
    wmin <= u_0;
    wmin <= u_1;
    wmin <= u_2;
    wmin <= u_3;
    wmin <= u_4;
    wmin <= u_5;
    wmin <= u_6;
    wmin <= u_7;
    wmin <= u_8;
    wmin <= u_9;
    wmin <= u_10;
    wmin <= u_11;
    wmin <= u_12;
    wmin <= u_13;
    wmin <= u_14;
    wmin <= u_15;
    wmin <= u_16;
    wmin <= u_17;
    wmin <= u_18;
    wmin <= u_19;
    wmin <= u_20;
    wmin <= u_21;
    wmin <= u_22;
    wmin <= u_23;
    wmin <= u_24;
    wmin <= u_25;
    wmin <= u_26;
    wmin <= u_27;
    wmin <= u_28;
    wmin <= u_29;
    wmin <= u_30;
    wmin <= u_31;
    wmin <= u_32;
    wmin <= u_33;
    wmin <= u_34;
    wmin <= u_35;
    wmin <= u_36;
    wmin <= u_37;
    wmin <= u_38;
    wmin <= u_39;
    wmin <= u_40;
    wmin <= u_41;
    wmin <= u_42;
    wmin <= u_43;
    wmin <= u_44;
    u_0 <= wmax;
    u_1 <= wmax;
    u_2 <= wmax;
    u_3 <= wmax;
    u_4 <= wmax;
    u_5 <= wmax;
    u_6 <= wmax;
    u_7 <= wmax;
    u_8 <= wmax;
    u_9 <= wmax;
    u_10 <= wmax;
    u_11 <= wmax;
    u_12 <= wmax;
    u_13 <= wmax;
    u_14 <= wmax;
    u_15 <= wmax;
    u_16 <= wmax;
    u_17 <= wmax;
    u_18 <= wmax;
    u_19 <= wmax;
    u_20 <= wmax;
    u_21 <= wmax;
    u_22 <= wmax;
    u_23 <= wmax;
    u_24 <= wmax;
    u_25 <= wmax;
    u_26 <= wmax;
    u_27 <= wmax;
    u_28 <= wmax;
    u_29 <= wmax;
    u_30 <= wmax;
    u_31 <= wmax;
    u_32 <= wmax;
    u_33 <= wmax;
    u_34 <= wmax;
    u_35 <= wmax;
    u_36 <= wmax;
    u_37 <= wmax;
    u_38 <= wmax;
    u_39 <= wmax;
    u_40 <= wmax;
    u_41 <= wmax;
    u_42 <= wmax;
    u_43 <= wmax;
    u_44 <= wmax;
    x_1(2) >=  - kl*x_1(1) + wmin_land;
    x_2(2) >=  - kl*x_2(1) + wmin_land;
    x_3(2) >=  - kl*x_3(1) + wmin_land;
    x_4(2) >=  - kl*x_4(1) + wmin_land;
    x_5(2) >=  - kl*x_5(1) + wmin_land;
    x_6(2) >=  - kl*x_6(1) + wmin_land;
    x_7(2) >=  - kl*x_7(1) + wmin_land;
    x_8(2) >=  - kl*x_8(1) + wmin_land;
    x_9(2) >=  - kl*x_9(1) + wmin_land;
    x_10(2) >=  - kl*x_10(1) + wmin_land;
    x_11(2) >=  - kl*x_11(1) + wmin_land;
    x_12(2) >=  - kl*x_12(1) + wmin_land;
    x_13(2) >=  - kl*x_13(1) + wmin_land;
    x_14(2) >=  - kl*x_14(1) + wmin_land;
    x_15(2) >=  - kl*x_15(1) + wmin_land;
    x_16(2) >=  - kl*x_16(1) + wmin_land;
    x_17(2) >=  - kl*x_17(1) + wmin_land;
    x_18(2) >=  - kl*x_18(1) + wmin_land;
    x_19(2) >=  - kl*x_19(1) + wmin_land;
    x_20(2) >=  - kl*x_20(1) + wmin_land;
    x_21(2) >=  - kl*x_21(1) + wmin_land;
    x_22(2) >=  - kl*x_22(1) + wmin_land;
    x_23(2) >=  - kl*x_23(1) + wmin_land;
    x_24(2) >=  - kl*x_24(1) + wmin_land;
    x_25(2) >=  - kl*x_25(1) + wmin_land;
    x_26(2) >=  - kl*x_26(1) + wmin_land;
    x_27(2) >=  - kl*x_27(1) + wmin_land;
    x_28(2) >=  - kl*x_28(1) + wmin_land;
    x_29(2) >=  - kl*x_29(1) + wmin_land;
    x_30(2) >=  - kl*x_30(1) + wmin_land;
    x_31(2) >=  - kl*x_31(1) + wmin_land;
    x_32(2) >=  - kl*x_32(1) + wmin_land;
    x_33(2) >=  - kl*x_33(1) + wmin_land;
    x_34(2) >=  - kl*x_34(1) + wmin_land;
    x_35(2) >=  - kl*x_35(1) + wmin_land;
    x_36(2) >=  - kl*x_36(1) + wmin_land;
    x_37(2) >=  - kl*x_37(1) + wmin_land;
    x_38(2) >=  - kl*x_38(1) + wmin_land;
    x_39(2) >=  - kl*x_39(1) + wmin_land;
    x_40(2) >=  - kl*x_40(1) + wmin_land;
    x_41(2) >=  - kl*x_41(1) + wmin_land;
    x_42(2) >=  - kl*x_42(1) + wmin_land;
    x_43(2) >=  - kl*x_43(1) + wmin_land;
    x_44(2) >=  - kl*x_44(1) + wmin_land;
    x_45(2) >=  - kl*x_45(1) + wmin_land;
    x_1(1) >= 0;
    x_2(1) >= 0;
    x_3(1) >= 0;
    x_4(1) >= 0;
    x_5(1) >= 0;
    x_6(1) >= 0;
    x_7(1) >= 0;
    x_8(1) >= 0;
    x_9(1) >= 0;
    x_10(1) >= 0;
    x_11(1) >= 0;
    x_12(1) >= 0;
    x_13(1) >= 0;
    x_14(1) >= 0;
    x_15(1) >= 0;
    x_16(1) >= 0;
    x_17(1) >= 0;
    x_18(1) >= 0;
    x_19(1) >= 0;
    x_20(1) >= 0;
    x_21(1) >= 0;
    x_22(1) >= 0;
    x_23(1) >= 0;
    x_24(1) >= 0;
    x_25(1) >= 0;
    x_26(1) >= 0;
    x_27(1) >= 0;
    x_28(1) >= 0;
    x_29(1) >= 0;
    x_30(1) >= 0;
    x_31(1) >= 0;
    x_32(1) >= 0;
    x_33(1) >= 0;
    x_34(1) >= 0;
    x_35(1) >= 0;
    x_36(1) >= 0;
    x_37(1) >= 0;
    x_38(1) >= 0;
    x_39(1) >= 0;
    x_40(1) >= 0;
    x_41(1) >= 0;
    x_42(1) >= 0;
    x_43(1) >= 0;
    x_44(1) >= 0;
    x_45(1) >= 0;
    b_1*dist_1*hs + (dl - ds)*x_1(1) <= dl*hs;
    b_2*dist_2*hs + (dl - ds)*x_2(1) <= dl*hs;
    b_3*dist_3*hs + (dl - ds)*x_3(1) <= dl*hs;
    b_4*dist_4*hs + (dl - ds)*x_4(1) <= dl*hs;
    b_5*dist_5*hs + (dl - ds)*x_5(1) <= dl*hs;
    b_6*dist_6*hs + (dl - ds)*x_6(1) <= dl*hs;
    b_7*dist_7*hs + (dl - ds)*x_7(1) <= dl*hs;
    b_8*dist_8*hs + (dl - ds)*x_8(1) <= dl*hs;
    b_9*dist_9*hs + (dl - ds)*x_9(1) <= dl*hs;
    b_10*dist_10*hs + (dl - ds)*x_10(1) <= dl*hs;
    b_11*dist_11*hs + (dl - ds)*x_11(1) <= dl*hs;
    b_12*dist_12*hs + (dl - ds)*x_12(1) <= dl*hs;
    b_13*dist_13*hs + (dl - ds)*x_13(1) <= dl*hs;
    b_14*dist_14*hs + (dl - ds)*x_14(1) <= dl*hs;
    b_15*dist_15*hs + (dl - ds)*x_15(1) <= dl*hs;
    b_16*dist_16*hs + (dl - ds)*x_16(1) <= dl*hs;
    b_17*dist_17*hs + (dl - ds)*x_17(1) <= dl*hs;
    b_18*dist_18*hs + (dl - ds)*x_18(1) <= dl*hs;
    b_19*dist_19*hs + (dl - ds)*x_19(1) <= dl*hs;
    b_20*dist_20*hs + (dl - ds)*x_20(1) <= dl*hs;
    b_21*dist_21*hs + (dl - ds)*x_21(1) <= dl*hs;
    b_22*dist_22*hs + (dl - ds)*x_22(1) <= dl*hs;
    b_23*dist_23*hs + (dl - ds)*x_23(1) <= dl*hs;
    b_24*dist_24*hs + (dl - ds)*x_24(1) <= dl*hs;
    b_25*dist_25*hs + (dl - ds)*x_25(1) <= dl*hs;
    b_26*dist_26*hs + (dl - ds)*x_26(1) <= dl*hs;
    b_27*dist_27*hs + (dl - ds)*x_27(1) <= dl*hs;
    b_28*dist_28*hs + (dl - ds)*x_28(1) <= dl*hs;
    b_29*dist_29*hs + (dl - ds)*x_29(1) <= dl*hs;
    b_30*dist_30*hs + (dl - ds)*x_30(1) <= dl*hs;
    b_31*dist_31*hs + (dl - ds)*x_31(1) <= dl*hs;
    b_32*dist_32*hs + (dl - ds)*x_32(1) <= dl*hs;
    b_33*dist_33*hs + (dl - ds)*x_33(1) <= dl*hs;
    b_34*dist_34*hs + (dl - ds)*x_34(1) <= dl*hs;
    b_35*dist_35*hs + (dl - ds)*x_35(1) <= dl*hs;
    b_36*dist_36*hs + (dl - ds)*x_36(1) <= dl*hs;
    b_37*dist_37*hs + (dl - ds)*x_37(1) <= dl*hs;
    b_38*dist_38*hs + (dl - ds)*x_38(1) <= dl*hs;
    b_39*dist_39*hs + (dl - ds)*x_39(1) <= dl*hs;
    b_40*dist_40*hs + (dl - ds)*x_40(1) <= dl*hs;
    b_41*dist_41*hs + (dl - ds)*x_41(1) <= dl*hs;
    b_42*dist_42*hs + (dl - ds)*x_42(1) <= dl*hs;
    b_43*dist_43*hs + (dl - ds)*x_43(1) <= dl*hs;
    b_44*dist_44*hs + (dl - ds)*x_44(1) <= dl*hs;
    b_45*dist_45*hs + (dl - ds)*x_45(1) <= dl*hs;
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
