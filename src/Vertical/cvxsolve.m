% Produced by CVXGEN, 2019-04-23 04:29:21 -0400.
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

  minimize(quad_form(b_0*(x_0 - xb), Q) + quad_form(u_0, R) + quad_form(b_1*(x_1 - xb), Q) + quad_form(u_1, R) + quad_form(b_2*(x_2 - xb), Q) + quad_form(u_2, R) + quad_form(b_3*(x_3 - xb), Q) + quad_form(u_3, R) + quad_form(b_4*(x_4 - xb), Q) + quad_form(u_4, R) + quad_form(b_5*(x_5 - xb), Q) + quad_form(u_5, R) + quad_form(b_6*(x_6 - xb), Q) + quad_form(u_6, R) + quad_form(b_7*(x_7 - xb), Q) + quad_form(u_7, R) + quad_form(b_8*(x_8 - xb), Q) + quad_form(u_8, R) + quad_form(b_9*(x_9 - xb), Q) + quad_form(u_9, R) + quad_form(b_10*(x_10 - xb), Q) + quad_form(u_10, R) + quad_form(b_11*(x_11 - xb), Q) + quad_form(u_11, R) + quad_form(b_12*(x_12 - xb), Q) + quad_form(u_12, R) + quad_form(b_13*(x_13 - xb), Q) + quad_form(u_13, R) + quad_form(b_14*(x_14 - xb), Q) + quad_form(u_14, R) + quad_form(b_15*(x_15 - xb), Q) + quad_form(u_15, R) + quad_form(b_16*(x_16 - xb), Q) + quad_form(u_16, R) + quad_form(b_17*(x_17 - xb), Q) + quad_form(u_17, R) + quad_form(b_18*(x_18 - xb), Q) + quad_form(u_18, R) + quad_form(b_19*(x_19 - xb), Q) + quad_form(u_19, R) + quad_form(b_20*(x_20 - xb), Q) + quad_form(u_20, R) + quad_form(b_21*(x_21 - xb), Q) + quad_form(u_21, R) + quad_form(b_22*(x_22 - xb), Q) + quad_form(u_22, R) + quad_form(b_23*(x_23 - xb), Q) + quad_form(u_23, R) + quad_form(b_24*(x_24 - xb), Q) + quad_form(u_24, R) + quad_form(b_25*(x_25 - xb), P));
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
    b_1*x_1(2) >=  - kl*x_1(1) + wmin_land;
    b_2*x_2(2) >=  - kl*x_2(1) + wmin_land;
    b_3*x_3(2) >=  - kl*x_3(1) + wmin_land;
    b_4*x_4(2) >=  - kl*x_4(1) + wmin_land;
    b_5*x_5(2) >=  - kl*x_5(1) + wmin_land;
    b_6*x_6(2) >=  - kl*x_6(1) + wmin_land;
    b_7*x_7(2) >=  - kl*x_7(1) + wmin_land;
    b_8*x_8(2) >=  - kl*x_8(1) + wmin_land;
    b_9*x_9(2) >=  - kl*x_9(1) + wmin_land;
    b_10*x_10(2) >=  - kl*x_10(1) + wmin_land;
    b_11*x_11(2) >=  - kl*x_11(1) + wmin_land;
    b_12*x_12(2) >=  - kl*x_12(1) + wmin_land;
    b_13*x_13(2) >=  - kl*x_13(1) + wmin_land;
    b_14*x_14(2) >=  - kl*x_14(1) + wmin_land;
    b_15*x_15(2) >=  - kl*x_15(1) + wmin_land;
    b_16*x_16(2) >=  - kl*x_16(1) + wmin_land;
    b_17*x_17(2) >=  - kl*x_17(1) + wmin_land;
    b_18*x_18(2) >=  - kl*x_18(1) + wmin_land;
    b_19*x_19(2) >=  - kl*x_19(1) + wmin_land;
    b_20*x_20(2) >=  - kl*x_20(1) + wmin_land;
    b_21*x_21(2) >=  - kl*x_21(1) + wmin_land;
    b_22*x_22(2) >=  - kl*x_22(1) + wmin_land;
    b_23*x_23(2) >=  - kl*x_23(1) + wmin_land;
    b_24*x_24(2) >=  - kl*x_24(1) + wmin_land;
    b_25*x_25(2) >=  - kl*x_25(1) + wmin_land;
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
status.cvx_status = cvx_status;
% Provide a drop-in replacement for csolve.
status.optval = cvx_optval;
status.converged = strcmp(cvx_status, 'Solved');
