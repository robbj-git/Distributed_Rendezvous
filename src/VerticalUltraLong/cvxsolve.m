% Produced by CVXGEN, 2019-05-01 05:35:47 -0400.
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
if isfield(params, 'b_46')
  b_46 = params.b_46;
elseif isfield(params, 'b')
  b_46 = params.b{46};
else
  error 'could not find b_46'
end
if isfield(params, 'b_47')
  b_47 = params.b_47;
elseif isfield(params, 'b')
  b_47 = params.b{47};
else
  error 'could not find b_47'
end
if isfield(params, 'b_48')
  b_48 = params.b_48;
elseif isfield(params, 'b')
  b_48 = params.b{48};
else
  error 'could not find b_48'
end
if isfield(params, 'b_49')
  b_49 = params.b_49;
elseif isfield(params, 'b')
  b_49 = params.b{49};
else
  error 'could not find b_49'
end
if isfield(params, 'b_50')
  b_50 = params.b_50;
elseif isfield(params, 'b')
  b_50 = params.b{50};
else
  error 'could not find b_50'
end
if isfield(params, 'b_51')
  b_51 = params.b_51;
elseif isfield(params, 'b')
  b_51 = params.b{51};
else
  error 'could not find b_51'
end
if isfield(params, 'b_52')
  b_52 = params.b_52;
elseif isfield(params, 'b')
  b_52 = params.b{52};
else
  error 'could not find b_52'
end
if isfield(params, 'b_53')
  b_53 = params.b_53;
elseif isfield(params, 'b')
  b_53 = params.b{53};
else
  error 'could not find b_53'
end
if isfield(params, 'b_54')
  b_54 = params.b_54;
elseif isfield(params, 'b')
  b_54 = params.b{54};
else
  error 'could not find b_54'
end
if isfield(params, 'b_55')
  b_55 = params.b_55;
elseif isfield(params, 'b')
  b_55 = params.b{55};
else
  error 'could not find b_55'
end
if isfield(params, 'b_56')
  b_56 = params.b_56;
elseif isfield(params, 'b')
  b_56 = params.b{56};
else
  error 'could not find b_56'
end
if isfield(params, 'b_57')
  b_57 = params.b_57;
elseif isfield(params, 'b')
  b_57 = params.b{57};
else
  error 'could not find b_57'
end
if isfield(params, 'b_58')
  b_58 = params.b_58;
elseif isfield(params, 'b')
  b_58 = params.b{58};
else
  error 'could not find b_58'
end
if isfield(params, 'b_59')
  b_59 = params.b_59;
elseif isfield(params, 'b')
  b_59 = params.b{59};
else
  error 'could not find b_59'
end
if isfield(params, 'b_60')
  b_60 = params.b_60;
elseif isfield(params, 'b')
  b_60 = params.b{60};
else
  error 'could not find b_60'
end
if isfield(params, 'b_61')
  b_61 = params.b_61;
elseif isfield(params, 'b')
  b_61 = params.b{61};
else
  error 'could not find b_61'
end
if isfield(params, 'b_62')
  b_62 = params.b_62;
elseif isfield(params, 'b')
  b_62 = params.b{62};
else
  error 'could not find b_62'
end
if isfield(params, 'b_63')
  b_63 = params.b_63;
elseif isfield(params, 'b')
  b_63 = params.b{63};
else
  error 'could not find b_63'
end
if isfield(params, 'b_64')
  b_64 = params.b_64;
elseif isfield(params, 'b')
  b_64 = params.b{64};
else
  error 'could not find b_64'
end
if isfield(params, 'b_65')
  b_65 = params.b_65;
elseif isfield(params, 'b')
  b_65 = params.b{65};
else
  error 'could not find b_65'
end
if isfield(params, 'b_66')
  b_66 = params.b_66;
elseif isfield(params, 'b')
  b_66 = params.b{66};
else
  error 'could not find b_66'
end
if isfield(params, 'b_67')
  b_67 = params.b_67;
elseif isfield(params, 'b')
  b_67 = params.b{67};
else
  error 'could not find b_67'
end
if isfield(params, 'b_68')
  b_68 = params.b_68;
elseif isfield(params, 'b')
  b_68 = params.b{68};
else
  error 'could not find b_68'
end
if isfield(params, 'b_69')
  b_69 = params.b_69;
elseif isfield(params, 'b')
  b_69 = params.b{69};
else
  error 'could not find b_69'
end
if isfield(params, 'b_70')
  b_70 = params.b_70;
elseif isfield(params, 'b')
  b_70 = params.b{70};
else
  error 'could not find b_70'
end
if isfield(params, 'b_71')
  b_71 = params.b_71;
elseif isfield(params, 'b')
  b_71 = params.b{71};
else
  error 'could not find b_71'
end
if isfield(params, 'b_72')
  b_72 = params.b_72;
elseif isfield(params, 'b')
  b_72 = params.b{72};
else
  error 'could not find b_72'
end
if isfield(params, 'b_73')
  b_73 = params.b_73;
elseif isfield(params, 'b')
  b_73 = params.b{73};
else
  error 'could not find b_73'
end
if isfield(params, 'b_74')
  b_74 = params.b_74;
elseif isfield(params, 'b')
  b_74 = params.b{74};
else
  error 'could not find b_74'
end
if isfield(params, 'b_75')
  b_75 = params.b_75;
elseif isfield(params, 'b')
  b_75 = params.b{75};
else
  error 'could not find b_75'
end
if isfield(params, 'b_76')
  b_76 = params.b_76;
elseif isfield(params, 'b')
  b_76 = params.b{76};
else
  error 'could not find b_76'
end
if isfield(params, 'b_77')
  b_77 = params.b_77;
elseif isfield(params, 'b')
  b_77 = params.b{77};
else
  error 'could not find b_77'
end
if isfield(params, 'b_78')
  b_78 = params.b_78;
elseif isfield(params, 'b')
  b_78 = params.b{78};
else
  error 'could not find b_78'
end
if isfield(params, 'b_79')
  b_79 = params.b_79;
elseif isfield(params, 'b')
  b_79 = params.b{79};
else
  error 'could not find b_79'
end
if isfield(params, 'b_80')
  b_80 = params.b_80;
elseif isfield(params, 'b')
  b_80 = params.b{80};
else
  error 'could not find b_80'
end
if isfield(params, 'b_81')
  b_81 = params.b_81;
elseif isfield(params, 'b')
  b_81 = params.b{81};
else
  error 'could not find b_81'
end
if isfield(params, 'b_82')
  b_82 = params.b_82;
elseif isfield(params, 'b')
  b_82 = params.b{82};
else
  error 'could not find b_82'
end
if isfield(params, 'b_83')
  b_83 = params.b_83;
elseif isfield(params, 'b')
  b_83 = params.b{83};
else
  error 'could not find b_83'
end
if isfield(params, 'b_84')
  b_84 = params.b_84;
elseif isfield(params, 'b')
  b_84 = params.b{84};
else
  error 'could not find b_84'
end
if isfield(params, 'b_85')
  b_85 = params.b_85;
elseif isfield(params, 'b')
  b_85 = params.b{85};
else
  error 'could not find b_85'
end
if isfield(params, 'b_86')
  b_86 = params.b_86;
elseif isfield(params, 'b')
  b_86 = params.b{86};
else
  error 'could not find b_86'
end
if isfield(params, 'b_87')
  b_87 = params.b_87;
elseif isfield(params, 'b')
  b_87 = params.b{87};
else
  error 'could not find b_87'
end
if isfield(params, 'b_88')
  b_88 = params.b_88;
elseif isfield(params, 'b')
  b_88 = params.b{88};
else
  error 'could not find b_88'
end
if isfield(params, 'b_89')
  b_89 = params.b_89;
elseif isfield(params, 'b')
  b_89 = params.b{89};
else
  error 'could not find b_89'
end
if isfield(params, 'b_90')
  b_90 = params.b_90;
elseif isfield(params, 'b')
  b_90 = params.b{90};
else
  error 'could not find b_90'
end
if isfield(params, 'b_91')
  b_91 = params.b_91;
elseif isfield(params, 'b')
  b_91 = params.b{91};
else
  error 'could not find b_91'
end
if isfield(params, 'b_92')
  b_92 = params.b_92;
elseif isfield(params, 'b')
  b_92 = params.b{92};
else
  error 'could not find b_92'
end
if isfield(params, 'b_93')
  b_93 = params.b_93;
elseif isfield(params, 'b')
  b_93 = params.b{93};
else
  error 'could not find b_93'
end
if isfield(params, 'b_94')
  b_94 = params.b_94;
elseif isfield(params, 'b')
  b_94 = params.b{94};
else
  error 'could not find b_94'
end
if isfield(params, 'b_95')
  b_95 = params.b_95;
elseif isfield(params, 'b')
  b_95 = params.b{95};
else
  error 'could not find b_95'
end
if isfield(params, 'b_96')
  b_96 = params.b_96;
elseif isfield(params, 'b')
  b_96 = params.b{96};
else
  error 'could not find b_96'
end
if isfield(params, 'b_97')
  b_97 = params.b_97;
elseif isfield(params, 'b')
  b_97 = params.b{97};
else
  error 'could not find b_97'
end
if isfield(params, 'b_98')
  b_98 = params.b_98;
elseif isfield(params, 'b')
  b_98 = params.b{98};
else
  error 'could not find b_98'
end
if isfield(params, 'b_99')
  b_99 = params.b_99;
elseif isfield(params, 'b')
  b_99 = params.b{99};
else
  error 'could not find b_99'
end
if isfield(params, 'b_100')
  b_100 = params.b_100;
elseif isfield(params, 'b')
  b_100 = params.b{100};
else
  error 'could not find b_100'
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
if isfield(params, 'dist_46')
  dist_46 = params.dist_46;
elseif isfield(params, 'dist')
  dist_46 = params.dist{46};
else
  error 'could not find dist_46'
end
if isfield(params, 'dist_47')
  dist_47 = params.dist_47;
elseif isfield(params, 'dist')
  dist_47 = params.dist{47};
else
  error 'could not find dist_47'
end
if isfield(params, 'dist_48')
  dist_48 = params.dist_48;
elseif isfield(params, 'dist')
  dist_48 = params.dist{48};
else
  error 'could not find dist_48'
end
if isfield(params, 'dist_49')
  dist_49 = params.dist_49;
elseif isfield(params, 'dist')
  dist_49 = params.dist{49};
else
  error 'could not find dist_49'
end
if isfield(params, 'dist_50')
  dist_50 = params.dist_50;
elseif isfield(params, 'dist')
  dist_50 = params.dist{50};
else
  error 'could not find dist_50'
end
if isfield(params, 'dist_51')
  dist_51 = params.dist_51;
elseif isfield(params, 'dist')
  dist_51 = params.dist{51};
else
  error 'could not find dist_51'
end
if isfield(params, 'dist_52')
  dist_52 = params.dist_52;
elseif isfield(params, 'dist')
  dist_52 = params.dist{52};
else
  error 'could not find dist_52'
end
if isfield(params, 'dist_53')
  dist_53 = params.dist_53;
elseif isfield(params, 'dist')
  dist_53 = params.dist{53};
else
  error 'could not find dist_53'
end
if isfield(params, 'dist_54')
  dist_54 = params.dist_54;
elseif isfield(params, 'dist')
  dist_54 = params.dist{54};
else
  error 'could not find dist_54'
end
if isfield(params, 'dist_55')
  dist_55 = params.dist_55;
elseif isfield(params, 'dist')
  dist_55 = params.dist{55};
else
  error 'could not find dist_55'
end
if isfield(params, 'dist_56')
  dist_56 = params.dist_56;
elseif isfield(params, 'dist')
  dist_56 = params.dist{56};
else
  error 'could not find dist_56'
end
if isfield(params, 'dist_57')
  dist_57 = params.dist_57;
elseif isfield(params, 'dist')
  dist_57 = params.dist{57};
else
  error 'could not find dist_57'
end
if isfield(params, 'dist_58')
  dist_58 = params.dist_58;
elseif isfield(params, 'dist')
  dist_58 = params.dist{58};
else
  error 'could not find dist_58'
end
if isfield(params, 'dist_59')
  dist_59 = params.dist_59;
elseif isfield(params, 'dist')
  dist_59 = params.dist{59};
else
  error 'could not find dist_59'
end
if isfield(params, 'dist_60')
  dist_60 = params.dist_60;
elseif isfield(params, 'dist')
  dist_60 = params.dist{60};
else
  error 'could not find dist_60'
end
if isfield(params, 'dist_61')
  dist_61 = params.dist_61;
elseif isfield(params, 'dist')
  dist_61 = params.dist{61};
else
  error 'could not find dist_61'
end
if isfield(params, 'dist_62')
  dist_62 = params.dist_62;
elseif isfield(params, 'dist')
  dist_62 = params.dist{62};
else
  error 'could not find dist_62'
end
if isfield(params, 'dist_63')
  dist_63 = params.dist_63;
elseif isfield(params, 'dist')
  dist_63 = params.dist{63};
else
  error 'could not find dist_63'
end
if isfield(params, 'dist_64')
  dist_64 = params.dist_64;
elseif isfield(params, 'dist')
  dist_64 = params.dist{64};
else
  error 'could not find dist_64'
end
if isfield(params, 'dist_65')
  dist_65 = params.dist_65;
elseif isfield(params, 'dist')
  dist_65 = params.dist{65};
else
  error 'could not find dist_65'
end
if isfield(params, 'dist_66')
  dist_66 = params.dist_66;
elseif isfield(params, 'dist')
  dist_66 = params.dist{66};
else
  error 'could not find dist_66'
end
if isfield(params, 'dist_67')
  dist_67 = params.dist_67;
elseif isfield(params, 'dist')
  dist_67 = params.dist{67};
else
  error 'could not find dist_67'
end
if isfield(params, 'dist_68')
  dist_68 = params.dist_68;
elseif isfield(params, 'dist')
  dist_68 = params.dist{68};
else
  error 'could not find dist_68'
end
if isfield(params, 'dist_69')
  dist_69 = params.dist_69;
elseif isfield(params, 'dist')
  dist_69 = params.dist{69};
else
  error 'could not find dist_69'
end
if isfield(params, 'dist_70')
  dist_70 = params.dist_70;
elseif isfield(params, 'dist')
  dist_70 = params.dist{70};
else
  error 'could not find dist_70'
end
if isfield(params, 'dist_71')
  dist_71 = params.dist_71;
elseif isfield(params, 'dist')
  dist_71 = params.dist{71};
else
  error 'could not find dist_71'
end
if isfield(params, 'dist_72')
  dist_72 = params.dist_72;
elseif isfield(params, 'dist')
  dist_72 = params.dist{72};
else
  error 'could not find dist_72'
end
if isfield(params, 'dist_73')
  dist_73 = params.dist_73;
elseif isfield(params, 'dist')
  dist_73 = params.dist{73};
else
  error 'could not find dist_73'
end
if isfield(params, 'dist_74')
  dist_74 = params.dist_74;
elseif isfield(params, 'dist')
  dist_74 = params.dist{74};
else
  error 'could not find dist_74'
end
if isfield(params, 'dist_75')
  dist_75 = params.dist_75;
elseif isfield(params, 'dist')
  dist_75 = params.dist{75};
else
  error 'could not find dist_75'
end
if isfield(params, 'dist_76')
  dist_76 = params.dist_76;
elseif isfield(params, 'dist')
  dist_76 = params.dist{76};
else
  error 'could not find dist_76'
end
if isfield(params, 'dist_77')
  dist_77 = params.dist_77;
elseif isfield(params, 'dist')
  dist_77 = params.dist{77};
else
  error 'could not find dist_77'
end
if isfield(params, 'dist_78')
  dist_78 = params.dist_78;
elseif isfield(params, 'dist')
  dist_78 = params.dist{78};
else
  error 'could not find dist_78'
end
if isfield(params, 'dist_79')
  dist_79 = params.dist_79;
elseif isfield(params, 'dist')
  dist_79 = params.dist{79};
else
  error 'could not find dist_79'
end
if isfield(params, 'dist_80')
  dist_80 = params.dist_80;
elseif isfield(params, 'dist')
  dist_80 = params.dist{80};
else
  error 'could not find dist_80'
end
if isfield(params, 'dist_81')
  dist_81 = params.dist_81;
elseif isfield(params, 'dist')
  dist_81 = params.dist{81};
else
  error 'could not find dist_81'
end
if isfield(params, 'dist_82')
  dist_82 = params.dist_82;
elseif isfield(params, 'dist')
  dist_82 = params.dist{82};
else
  error 'could not find dist_82'
end
if isfield(params, 'dist_83')
  dist_83 = params.dist_83;
elseif isfield(params, 'dist')
  dist_83 = params.dist{83};
else
  error 'could not find dist_83'
end
if isfield(params, 'dist_84')
  dist_84 = params.dist_84;
elseif isfield(params, 'dist')
  dist_84 = params.dist{84};
else
  error 'could not find dist_84'
end
if isfield(params, 'dist_85')
  dist_85 = params.dist_85;
elseif isfield(params, 'dist')
  dist_85 = params.dist{85};
else
  error 'could not find dist_85'
end
if isfield(params, 'dist_86')
  dist_86 = params.dist_86;
elseif isfield(params, 'dist')
  dist_86 = params.dist{86};
else
  error 'could not find dist_86'
end
if isfield(params, 'dist_87')
  dist_87 = params.dist_87;
elseif isfield(params, 'dist')
  dist_87 = params.dist{87};
else
  error 'could not find dist_87'
end
if isfield(params, 'dist_88')
  dist_88 = params.dist_88;
elseif isfield(params, 'dist')
  dist_88 = params.dist{88};
else
  error 'could not find dist_88'
end
if isfield(params, 'dist_89')
  dist_89 = params.dist_89;
elseif isfield(params, 'dist')
  dist_89 = params.dist{89};
else
  error 'could not find dist_89'
end
if isfield(params, 'dist_90')
  dist_90 = params.dist_90;
elseif isfield(params, 'dist')
  dist_90 = params.dist{90};
else
  error 'could not find dist_90'
end
if isfield(params, 'dist_91')
  dist_91 = params.dist_91;
elseif isfield(params, 'dist')
  dist_91 = params.dist{91};
else
  error 'could not find dist_91'
end
if isfield(params, 'dist_92')
  dist_92 = params.dist_92;
elseif isfield(params, 'dist')
  dist_92 = params.dist{92};
else
  error 'could not find dist_92'
end
if isfield(params, 'dist_93')
  dist_93 = params.dist_93;
elseif isfield(params, 'dist')
  dist_93 = params.dist{93};
else
  error 'could not find dist_93'
end
if isfield(params, 'dist_94')
  dist_94 = params.dist_94;
elseif isfield(params, 'dist')
  dist_94 = params.dist{94};
else
  error 'could not find dist_94'
end
if isfield(params, 'dist_95')
  dist_95 = params.dist_95;
elseif isfield(params, 'dist')
  dist_95 = params.dist{95};
else
  error 'could not find dist_95'
end
if isfield(params, 'dist_96')
  dist_96 = params.dist_96;
elseif isfield(params, 'dist')
  dist_96 = params.dist{96};
else
  error 'could not find dist_96'
end
if isfield(params, 'dist_97')
  dist_97 = params.dist_97;
elseif isfield(params, 'dist')
  dist_97 = params.dist{97};
else
  error 'could not find dist_97'
end
if isfield(params, 'dist_98')
  dist_98 = params.dist_98;
elseif isfield(params, 'dist')
  dist_98 = params.dist{98};
else
  error 'could not find dist_98'
end
if isfield(params, 'dist_99')
  dist_99 = params.dist_99;
elseif isfield(params, 'dist')
  dist_99 = params.dist{99};
else
  error 'could not find dist_99'
end
if isfield(params, 'dist_100')
  dist_100 = params.dist_100;
elseif isfield(params, 'dist')
  dist_100 = params.dist{100};
else
  error 'could not find dist_100'
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
  variable u_45;
  variable x_46(2, 1);
  variable u_46;
  variable x_47(2, 1);
  variable u_47;
  variable x_48(2, 1);
  variable u_48;
  variable x_49(2, 1);
  variable u_49;
  variable x_50(2, 1);
  variable u_50;
  variable x_51(2, 1);
  variable u_51;
  variable x_52(2, 1);
  variable u_52;
  variable x_53(2, 1);
  variable u_53;
  variable x_54(2, 1);
  variable u_54;
  variable x_55(2, 1);
  variable u_55;
  variable x_56(2, 1);
  variable u_56;
  variable x_57(2, 1);
  variable u_57;
  variable x_58(2, 1);
  variable u_58;
  variable x_59(2, 1);
  variable u_59;
  variable x_60(2, 1);
  variable u_60;
  variable x_61(2, 1);
  variable u_61;
  variable x_62(2, 1);
  variable u_62;
  variable x_63(2, 1);
  variable u_63;
  variable x_64(2, 1);
  variable u_64;
  variable x_65(2, 1);
  variable u_65;
  variable x_66(2, 1);
  variable u_66;
  variable x_67(2, 1);
  variable u_67;
  variable x_68(2, 1);
  variable u_68;
  variable x_69(2, 1);
  variable u_69;
  variable x_70(2, 1);
  variable u_70;
  variable x_71(2, 1);
  variable u_71;
  variable x_72(2, 1);
  variable u_72;
  variable x_73(2, 1);
  variable u_73;
  variable x_74(2, 1);
  variable u_74;
  variable x_75(2, 1);
  variable u_75;
  variable x_76(2, 1);
  variable u_76;
  variable x_77(2, 1);
  variable u_77;
  variable x_78(2, 1);
  variable u_78;
  variable x_79(2, 1);
  variable u_79;
  variable x_80(2, 1);
  variable u_80;
  variable x_81(2, 1);
  variable u_81;
  variable x_82(2, 1);
  variable u_82;
  variable x_83(2, 1);
  variable u_83;
  variable x_84(2, 1);
  variable u_84;
  variable x_85(2, 1);
  variable u_85;
  variable x_86(2, 1);
  variable u_86;
  variable x_87(2, 1);
  variable u_87;
  variable x_88(2, 1);
  variable u_88;
  variable x_89(2, 1);
  variable u_89;
  variable x_90(2, 1);
  variable u_90;
  variable x_91(2, 1);
  variable u_91;
  variable x_92(2, 1);
  variable u_92;
  variable x_93(2, 1);
  variable u_93;
  variable x_94(2, 1);
  variable u_94;
  variable x_95(2, 1);
  variable u_95;
  variable x_96(2, 1);
  variable u_96;
  variable x_97(2, 1);
  variable u_97;
  variable x_98(2, 1);
  variable u_98;
  variable x_99(2, 1);
  variable u_99;
  variable x_100(2, 1);

  minimize(quad_form(b_0*(x_0 - xb), Q) + quad_form(u_0, R) + quad_form(b_1*(x_1 - xb), Q) + quad_form(u_1, R) + quad_form(b_2*(x_2 - xb), Q) + quad_form(u_2, R) + quad_form(b_3*(x_3 - xb), Q) + quad_form(u_3, R) + quad_form(b_4*(x_4 - xb), Q) + quad_form(u_4, R) + quad_form(b_5*(x_5 - xb), Q) + quad_form(u_5, R) + quad_form(b_6*(x_6 - xb), Q) + quad_form(u_6, R) + quad_form(b_7*(x_7 - xb), Q) + quad_form(u_7, R) + quad_form(b_8*(x_8 - xb), Q) + quad_form(u_8, R) + quad_form(b_9*(x_9 - xb), Q) + quad_form(u_9, R) + quad_form(b_10*(x_10 - xb), Q) + quad_form(u_10, R) + quad_form(b_11*(x_11 - xb), Q) + quad_form(u_11, R) + quad_form(b_12*(x_12 - xb), Q) + quad_form(u_12, R) + quad_form(b_13*(x_13 - xb), Q) + quad_form(u_13, R) + quad_form(b_14*(x_14 - xb), Q) + quad_form(u_14, R) + quad_form(b_15*(x_15 - xb), Q) + quad_form(u_15, R) + quad_form(b_16*(x_16 - xb), Q) + quad_form(u_16, R) + quad_form(b_17*(x_17 - xb), Q) + quad_form(u_17, R) + quad_form(b_18*(x_18 - xb), Q) + quad_form(u_18, R) + quad_form(b_19*(x_19 - xb), Q) + quad_form(u_19, R) + quad_form(b_20*(x_20 - xb), Q) + quad_form(u_20, R) + quad_form(b_21*(x_21 - xb), Q) + quad_form(u_21, R) + quad_form(b_22*(x_22 - xb), Q) + quad_form(u_22, R) + quad_form(b_23*(x_23 - xb), Q) + quad_form(u_23, R) + quad_form(b_24*(x_24 - xb), Q) + quad_form(u_24, R) + quad_form(b_25*(x_25 - xb), Q) + quad_form(u_25, R) + quad_form(b_26*(x_26 - xb), Q) + quad_form(u_26, R) + quad_form(b_27*(x_27 - xb), Q) + quad_form(u_27, R) + quad_form(b_28*(x_28 - xb), Q) + quad_form(u_28, R) + quad_form(b_29*(x_29 - xb), Q) + quad_form(u_29, R) + quad_form(b_30*(x_30 - xb), Q) + quad_form(u_30, R) + quad_form(b_31*(x_31 - xb), Q) + quad_form(u_31, R) + quad_form(b_32*(x_32 - xb), Q) + quad_form(u_32, R) + quad_form(b_33*(x_33 - xb), Q) + quad_form(u_33, R) + quad_form(b_34*(x_34 - xb), Q) + quad_form(u_34, R) + quad_form(b_35*(x_35 - xb), Q) + quad_form(u_35, R) + quad_form(b_36*(x_36 - xb), Q) + quad_form(u_36, R) + quad_form(b_37*(x_37 - xb), Q) + quad_form(u_37, R) + quad_form(b_38*(x_38 - xb), Q) + quad_form(u_38, R) + quad_form(b_39*(x_39 - xb), Q) + quad_form(u_39, R) + quad_form(b_40*(x_40 - xb), Q) + quad_form(u_40, R) + quad_form(b_41*(x_41 - xb), Q) + quad_form(u_41, R) + quad_form(b_42*(x_42 - xb), Q) + quad_form(u_42, R) + quad_form(b_43*(x_43 - xb), Q) + quad_form(u_43, R) + quad_form(b_44*(x_44 - xb), Q) + quad_form(u_44, R) + quad_form(b_45*(x_45 - xb), Q) + quad_form(u_45, R) + quad_form(b_46*(x_46 - xb), Q) + quad_form(u_46, R) + quad_form(b_47*(x_47 - xb), Q) + quad_form(u_47, R) + quad_form(b_48*(x_48 - xb), Q) + quad_form(u_48, R) + quad_form(b_49*(x_49 - xb), Q) + quad_form(u_49, R) + quad_form(b_50*(x_50 - xb), Q) + quad_form(u_50, R) + quad_form(b_51*(x_51 - xb), Q) + quad_form(u_51, R) + quad_form(b_52*(x_52 - xb), Q) + quad_form(u_52, R) + quad_form(b_53*(x_53 - xb), Q) + quad_form(u_53, R) + quad_form(b_54*(x_54 - xb), Q) + quad_form(u_54, R) + quad_form(b_55*(x_55 - xb), Q) + quad_form(u_55, R) + quad_form(b_56*(x_56 - xb), Q) + quad_form(u_56, R) + quad_form(b_57*(x_57 - xb), Q) + quad_form(u_57, R) + quad_form(b_58*(x_58 - xb), Q) + quad_form(u_58, R) + quad_form(b_59*(x_59 - xb), Q) + quad_form(u_59, R) + quad_form(b_60*(x_60 - xb), Q) + quad_form(u_60, R) + quad_form(b_61*(x_61 - xb), Q) + quad_form(u_61, R) + quad_form(b_62*(x_62 - xb), Q) + quad_form(u_62, R) + quad_form(b_63*(x_63 - xb), Q) + quad_form(u_63, R) + quad_form(b_64*(x_64 - xb), Q) + quad_form(u_64, R) + quad_form(b_65*(x_65 - xb), Q) + quad_form(u_65, R) + quad_form(b_66*(x_66 - xb), Q) + quad_form(u_66, R) + quad_form(b_67*(x_67 - xb), Q) + quad_form(u_67, R) + quad_form(b_68*(x_68 - xb), Q) + quad_form(u_68, R) + quad_form(b_69*(x_69 - xb), Q) + quad_form(u_69, R) + quad_form(b_70*(x_70 - xb), Q) + quad_form(u_70, R) + quad_form(b_71*(x_71 - xb), Q) + quad_form(u_71, R) + quad_form(b_72*(x_72 - xb), Q) + quad_form(u_72, R) + quad_form(b_73*(x_73 - xb), Q) + quad_form(u_73, R) + quad_form(b_74*(x_74 - xb), Q) + quad_form(u_74, R) + quad_form(b_75*(x_75 - xb), Q) + quad_form(u_75, R) + quad_form(b_76*(x_76 - xb), Q) + quad_form(u_76, R) + quad_form(b_77*(x_77 - xb), Q) + quad_form(u_77, R) + quad_form(b_78*(x_78 - xb), Q) + quad_form(u_78, R) + quad_form(b_79*(x_79 - xb), Q) + quad_form(u_79, R) + quad_form(b_80*(x_80 - xb), Q) + quad_form(u_80, R) + quad_form(b_81*(x_81 - xb), Q) + quad_form(u_81, R) + quad_form(b_82*(x_82 - xb), Q) + quad_form(u_82, R) + quad_form(b_83*(x_83 - xb), Q) + quad_form(u_83, R) + quad_form(b_84*(x_84 - xb), Q) + quad_form(u_84, R) + quad_form(b_85*(x_85 - xb), Q) + quad_form(u_85, R) + quad_form(b_86*(x_86 - xb), Q) + quad_form(u_86, R) + quad_form(b_87*(x_87 - xb), Q) + quad_form(u_87, R) + quad_form(b_88*(x_88 - xb), Q) + quad_form(u_88, R) + quad_form(b_89*(x_89 - xb), Q) + quad_form(u_89, R) + quad_form(b_90*(x_90 - xb), Q) + quad_form(u_90, R) + quad_form(b_91*(x_91 - xb), Q) + quad_form(u_91, R) + quad_form(b_92*(x_92 - xb), Q) + quad_form(u_92, R) + quad_form(b_93*(x_93 - xb), Q) + quad_form(u_93, R) + quad_form(b_94*(x_94 - xb), Q) + quad_form(u_94, R) + quad_form(b_95*(x_95 - xb), Q) + quad_form(u_95, R) + quad_form(b_96*(x_96 - xb), Q) + quad_form(u_96, R) + quad_form(b_97*(x_97 - xb), Q) + quad_form(u_97, R) + quad_form(b_98*(x_98 - xb), Q) + quad_form(u_98, R) + quad_form(b_99*(x_99 - xb), Q) + quad_form(u_99, R) + quad_form(b_100*(x_100 - xb), P));
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
    x_46 == A*x_45 + B*u_45;
    x_47 == A*x_46 + B*u_46;
    x_48 == A*x_47 + B*u_47;
    x_49 == A*x_48 + B*u_48;
    x_50 == A*x_49 + B*u_49;
    x_51 == A*x_50 + B*u_50;
    x_52 == A*x_51 + B*u_51;
    x_53 == A*x_52 + B*u_52;
    x_54 == A*x_53 + B*u_53;
    x_55 == A*x_54 + B*u_54;
    x_56 == A*x_55 + B*u_55;
    x_57 == A*x_56 + B*u_56;
    x_58 == A*x_57 + B*u_57;
    x_59 == A*x_58 + B*u_58;
    x_60 == A*x_59 + B*u_59;
    x_61 == A*x_60 + B*u_60;
    x_62 == A*x_61 + B*u_61;
    x_63 == A*x_62 + B*u_62;
    x_64 == A*x_63 + B*u_63;
    x_65 == A*x_64 + B*u_64;
    x_66 == A*x_65 + B*u_65;
    x_67 == A*x_66 + B*u_66;
    x_68 == A*x_67 + B*u_67;
    x_69 == A*x_68 + B*u_68;
    x_70 == A*x_69 + B*u_69;
    x_71 == A*x_70 + B*u_70;
    x_72 == A*x_71 + B*u_71;
    x_73 == A*x_72 + B*u_72;
    x_74 == A*x_73 + B*u_73;
    x_75 == A*x_74 + B*u_74;
    x_76 == A*x_75 + B*u_75;
    x_77 == A*x_76 + B*u_76;
    x_78 == A*x_77 + B*u_77;
    x_79 == A*x_78 + B*u_78;
    x_80 == A*x_79 + B*u_79;
    x_81 == A*x_80 + B*u_80;
    x_82 == A*x_81 + B*u_81;
    x_83 == A*x_82 + B*u_82;
    x_84 == A*x_83 + B*u_83;
    x_85 == A*x_84 + B*u_84;
    x_86 == A*x_85 + B*u_85;
    x_87 == A*x_86 + B*u_86;
    x_88 == A*x_87 + B*u_87;
    x_89 == A*x_88 + B*u_88;
    x_90 == A*x_89 + B*u_89;
    x_91 == A*x_90 + B*u_90;
    x_92 == A*x_91 + B*u_91;
    x_93 == A*x_92 + B*u_92;
    x_94 == A*x_93 + B*u_93;
    x_95 == A*x_94 + B*u_94;
    x_96 == A*x_95 + B*u_95;
    x_97 == A*x_96 + B*u_96;
    x_98 == A*x_97 + B*u_97;
    x_99 == A*x_98 + B*u_98;
    x_100 == A*x_99 + B*u_99;
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
    wmin <= x_46(2);
    wmin <= x_47(2);
    wmin <= x_48(2);
    wmin <= x_49(2);
    wmin <= x_50(2);
    wmin <= x_51(2);
    wmin <= x_52(2);
    wmin <= x_53(2);
    wmin <= x_54(2);
    wmin <= x_55(2);
    wmin <= x_56(2);
    wmin <= x_57(2);
    wmin <= x_58(2);
    wmin <= x_59(2);
    wmin <= x_60(2);
    wmin <= x_61(2);
    wmin <= x_62(2);
    wmin <= x_63(2);
    wmin <= x_64(2);
    wmin <= x_65(2);
    wmin <= x_66(2);
    wmin <= x_67(2);
    wmin <= x_68(2);
    wmin <= x_69(2);
    wmin <= x_70(2);
    wmin <= x_71(2);
    wmin <= x_72(2);
    wmin <= x_73(2);
    wmin <= x_74(2);
    wmin <= x_75(2);
    wmin <= x_76(2);
    wmin <= x_77(2);
    wmin <= x_78(2);
    wmin <= x_79(2);
    wmin <= x_80(2);
    wmin <= x_81(2);
    wmin <= x_82(2);
    wmin <= x_83(2);
    wmin <= x_84(2);
    wmin <= x_85(2);
    wmin <= x_86(2);
    wmin <= x_87(2);
    wmin <= x_88(2);
    wmin <= x_89(2);
    wmin <= x_90(2);
    wmin <= x_91(2);
    wmin <= x_92(2);
    wmin <= x_93(2);
    wmin <= x_94(2);
    wmin <= x_95(2);
    wmin <= x_96(2);
    wmin <= x_97(2);
    wmin <= x_98(2);
    wmin <= x_99(2);
    wmin <= x_100(2);
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
    wmin <= u_45;
    wmin <= u_46;
    wmin <= u_47;
    wmin <= u_48;
    wmin <= u_49;
    wmin <= u_50;
    wmin <= u_51;
    wmin <= u_52;
    wmin <= u_53;
    wmin <= u_54;
    wmin <= u_55;
    wmin <= u_56;
    wmin <= u_57;
    wmin <= u_58;
    wmin <= u_59;
    wmin <= u_60;
    wmin <= u_61;
    wmin <= u_62;
    wmin <= u_63;
    wmin <= u_64;
    wmin <= u_65;
    wmin <= u_66;
    wmin <= u_67;
    wmin <= u_68;
    wmin <= u_69;
    wmin <= u_70;
    wmin <= u_71;
    wmin <= u_72;
    wmin <= u_73;
    wmin <= u_74;
    wmin <= u_75;
    wmin <= u_76;
    wmin <= u_77;
    wmin <= u_78;
    wmin <= u_79;
    wmin <= u_80;
    wmin <= u_81;
    wmin <= u_82;
    wmin <= u_83;
    wmin <= u_84;
    wmin <= u_85;
    wmin <= u_86;
    wmin <= u_87;
    wmin <= u_88;
    wmin <= u_89;
    wmin <= u_90;
    wmin <= u_91;
    wmin <= u_92;
    wmin <= u_93;
    wmin <= u_94;
    wmin <= u_95;
    wmin <= u_96;
    wmin <= u_97;
    wmin <= u_98;
    wmin <= u_99;
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
    u_45 <= wmax;
    u_46 <= wmax;
    u_47 <= wmax;
    u_48 <= wmax;
    u_49 <= wmax;
    u_50 <= wmax;
    u_51 <= wmax;
    u_52 <= wmax;
    u_53 <= wmax;
    u_54 <= wmax;
    u_55 <= wmax;
    u_56 <= wmax;
    u_57 <= wmax;
    u_58 <= wmax;
    u_59 <= wmax;
    u_60 <= wmax;
    u_61 <= wmax;
    u_62 <= wmax;
    u_63 <= wmax;
    u_64 <= wmax;
    u_65 <= wmax;
    u_66 <= wmax;
    u_67 <= wmax;
    u_68 <= wmax;
    u_69 <= wmax;
    u_70 <= wmax;
    u_71 <= wmax;
    u_72 <= wmax;
    u_73 <= wmax;
    u_74 <= wmax;
    u_75 <= wmax;
    u_76 <= wmax;
    u_77 <= wmax;
    u_78 <= wmax;
    u_79 <= wmax;
    u_80 <= wmax;
    u_81 <= wmax;
    u_82 <= wmax;
    u_83 <= wmax;
    u_84 <= wmax;
    u_85 <= wmax;
    u_86 <= wmax;
    u_87 <= wmax;
    u_88 <= wmax;
    u_89 <= wmax;
    u_90 <= wmax;
    u_91 <= wmax;
    u_92 <= wmax;
    u_93 <= wmax;
    u_94 <= wmax;
    u_95 <= wmax;
    u_96 <= wmax;
    u_97 <= wmax;
    u_98 <= wmax;
    u_99 <= wmax;
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
    x_46(2) >=  - kl*x_46(1) + wmin_land;
    x_47(2) >=  - kl*x_47(1) + wmin_land;
    x_48(2) >=  - kl*x_48(1) + wmin_land;
    x_49(2) >=  - kl*x_49(1) + wmin_land;
    x_50(2) >=  - kl*x_50(1) + wmin_land;
    x_51(2) >=  - kl*x_51(1) + wmin_land;
    x_52(2) >=  - kl*x_52(1) + wmin_land;
    x_53(2) >=  - kl*x_53(1) + wmin_land;
    x_54(2) >=  - kl*x_54(1) + wmin_land;
    x_55(2) >=  - kl*x_55(1) + wmin_land;
    x_56(2) >=  - kl*x_56(1) + wmin_land;
    x_57(2) >=  - kl*x_57(1) + wmin_land;
    x_58(2) >=  - kl*x_58(1) + wmin_land;
    x_59(2) >=  - kl*x_59(1) + wmin_land;
    x_60(2) >=  - kl*x_60(1) + wmin_land;
    x_61(2) >=  - kl*x_61(1) + wmin_land;
    x_62(2) >=  - kl*x_62(1) + wmin_land;
    x_63(2) >=  - kl*x_63(1) + wmin_land;
    x_64(2) >=  - kl*x_64(1) + wmin_land;
    x_65(2) >=  - kl*x_65(1) + wmin_land;
    x_66(2) >=  - kl*x_66(1) + wmin_land;
    x_67(2) >=  - kl*x_67(1) + wmin_land;
    x_68(2) >=  - kl*x_68(1) + wmin_land;
    x_69(2) >=  - kl*x_69(1) + wmin_land;
    x_70(2) >=  - kl*x_70(1) + wmin_land;
    x_71(2) >=  - kl*x_71(1) + wmin_land;
    x_72(2) >=  - kl*x_72(1) + wmin_land;
    x_73(2) >=  - kl*x_73(1) + wmin_land;
    x_74(2) >=  - kl*x_74(1) + wmin_land;
    x_75(2) >=  - kl*x_75(1) + wmin_land;
    x_76(2) >=  - kl*x_76(1) + wmin_land;
    x_77(2) >=  - kl*x_77(1) + wmin_land;
    x_78(2) >=  - kl*x_78(1) + wmin_land;
    x_79(2) >=  - kl*x_79(1) + wmin_land;
    x_80(2) >=  - kl*x_80(1) + wmin_land;
    x_81(2) >=  - kl*x_81(1) + wmin_land;
    x_82(2) >=  - kl*x_82(1) + wmin_land;
    x_83(2) >=  - kl*x_83(1) + wmin_land;
    x_84(2) >=  - kl*x_84(1) + wmin_land;
    x_85(2) >=  - kl*x_85(1) + wmin_land;
    x_86(2) >=  - kl*x_86(1) + wmin_land;
    x_87(2) >=  - kl*x_87(1) + wmin_land;
    x_88(2) >=  - kl*x_88(1) + wmin_land;
    x_89(2) >=  - kl*x_89(1) + wmin_land;
    x_90(2) >=  - kl*x_90(1) + wmin_land;
    x_91(2) >=  - kl*x_91(1) + wmin_land;
    x_92(2) >=  - kl*x_92(1) + wmin_land;
    x_93(2) >=  - kl*x_93(1) + wmin_land;
    x_94(2) >=  - kl*x_94(1) + wmin_land;
    x_95(2) >=  - kl*x_95(1) + wmin_land;
    x_96(2) >=  - kl*x_96(1) + wmin_land;
    x_97(2) >=  - kl*x_97(1) + wmin_land;
    x_98(2) >=  - kl*x_98(1) + wmin_land;
    x_99(2) >=  - kl*x_99(1) + wmin_land;
    x_100(2) >=  - kl*x_100(1) + wmin_land;
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
    x_46(1) >= 0;
    x_47(1) >= 0;
    x_48(1) >= 0;
    x_49(1) >= 0;
    x_50(1) >= 0;
    x_51(1) >= 0;
    x_52(1) >= 0;
    x_53(1) >= 0;
    x_54(1) >= 0;
    x_55(1) >= 0;
    x_56(1) >= 0;
    x_57(1) >= 0;
    x_58(1) >= 0;
    x_59(1) >= 0;
    x_60(1) >= 0;
    x_61(1) >= 0;
    x_62(1) >= 0;
    x_63(1) >= 0;
    x_64(1) >= 0;
    x_65(1) >= 0;
    x_66(1) >= 0;
    x_67(1) >= 0;
    x_68(1) >= 0;
    x_69(1) >= 0;
    x_70(1) >= 0;
    x_71(1) >= 0;
    x_72(1) >= 0;
    x_73(1) >= 0;
    x_74(1) >= 0;
    x_75(1) >= 0;
    x_76(1) >= 0;
    x_77(1) >= 0;
    x_78(1) >= 0;
    x_79(1) >= 0;
    x_80(1) >= 0;
    x_81(1) >= 0;
    x_82(1) >= 0;
    x_83(1) >= 0;
    x_84(1) >= 0;
    x_85(1) >= 0;
    x_86(1) >= 0;
    x_87(1) >= 0;
    x_88(1) >= 0;
    x_89(1) >= 0;
    x_90(1) >= 0;
    x_91(1) >= 0;
    x_92(1) >= 0;
    x_93(1) >= 0;
    x_94(1) >= 0;
    x_95(1) >= 0;
    x_96(1) >= 0;
    x_97(1) >= 0;
    x_98(1) >= 0;
    x_99(1) >= 0;
    x_100(1) >= 0;
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
    b_46*dist_46*hs + (dl - ds)*x_46(1) <= dl*hs;
    b_47*dist_47*hs + (dl - ds)*x_47(1) <= dl*hs;
    b_48*dist_48*hs + (dl - ds)*x_48(1) <= dl*hs;
    b_49*dist_49*hs + (dl - ds)*x_49(1) <= dl*hs;
    b_50*dist_50*hs + (dl - ds)*x_50(1) <= dl*hs;
    b_51*dist_51*hs + (dl - ds)*x_51(1) <= dl*hs;
    b_52*dist_52*hs + (dl - ds)*x_52(1) <= dl*hs;
    b_53*dist_53*hs + (dl - ds)*x_53(1) <= dl*hs;
    b_54*dist_54*hs + (dl - ds)*x_54(1) <= dl*hs;
    b_55*dist_55*hs + (dl - ds)*x_55(1) <= dl*hs;
    b_56*dist_56*hs + (dl - ds)*x_56(1) <= dl*hs;
    b_57*dist_57*hs + (dl - ds)*x_57(1) <= dl*hs;
    b_58*dist_58*hs + (dl - ds)*x_58(1) <= dl*hs;
    b_59*dist_59*hs + (dl - ds)*x_59(1) <= dl*hs;
    b_60*dist_60*hs + (dl - ds)*x_60(1) <= dl*hs;
    b_61*dist_61*hs + (dl - ds)*x_61(1) <= dl*hs;
    b_62*dist_62*hs + (dl - ds)*x_62(1) <= dl*hs;
    b_63*dist_63*hs + (dl - ds)*x_63(1) <= dl*hs;
    b_64*dist_64*hs + (dl - ds)*x_64(1) <= dl*hs;
    b_65*dist_65*hs + (dl - ds)*x_65(1) <= dl*hs;
    b_66*dist_66*hs + (dl - ds)*x_66(1) <= dl*hs;
    b_67*dist_67*hs + (dl - ds)*x_67(1) <= dl*hs;
    b_68*dist_68*hs + (dl - ds)*x_68(1) <= dl*hs;
    b_69*dist_69*hs + (dl - ds)*x_69(1) <= dl*hs;
    b_70*dist_70*hs + (dl - ds)*x_70(1) <= dl*hs;
    b_71*dist_71*hs + (dl - ds)*x_71(1) <= dl*hs;
    b_72*dist_72*hs + (dl - ds)*x_72(1) <= dl*hs;
    b_73*dist_73*hs + (dl - ds)*x_73(1) <= dl*hs;
    b_74*dist_74*hs + (dl - ds)*x_74(1) <= dl*hs;
    b_75*dist_75*hs + (dl - ds)*x_75(1) <= dl*hs;
    b_76*dist_76*hs + (dl - ds)*x_76(1) <= dl*hs;
    b_77*dist_77*hs + (dl - ds)*x_77(1) <= dl*hs;
    b_78*dist_78*hs + (dl - ds)*x_78(1) <= dl*hs;
    b_79*dist_79*hs + (dl - ds)*x_79(1) <= dl*hs;
    b_80*dist_80*hs + (dl - ds)*x_80(1) <= dl*hs;
    b_81*dist_81*hs + (dl - ds)*x_81(1) <= dl*hs;
    b_82*dist_82*hs + (dl - ds)*x_82(1) <= dl*hs;
    b_83*dist_83*hs + (dl - ds)*x_83(1) <= dl*hs;
    b_84*dist_84*hs + (dl - ds)*x_84(1) <= dl*hs;
    b_85*dist_85*hs + (dl - ds)*x_85(1) <= dl*hs;
    b_86*dist_86*hs + (dl - ds)*x_86(1) <= dl*hs;
    b_87*dist_87*hs + (dl - ds)*x_87(1) <= dl*hs;
    b_88*dist_88*hs + (dl - ds)*x_88(1) <= dl*hs;
    b_89*dist_89*hs + (dl - ds)*x_89(1) <= dl*hs;
    b_90*dist_90*hs + (dl - ds)*x_90(1) <= dl*hs;
    b_91*dist_91*hs + (dl - ds)*x_91(1) <= dl*hs;
    b_92*dist_92*hs + (dl - ds)*x_92(1) <= dl*hs;
    b_93*dist_93*hs + (dl - ds)*x_93(1) <= dl*hs;
    b_94*dist_94*hs + (dl - ds)*x_94(1) <= dl*hs;
    b_95*dist_95*hs + (dl - ds)*x_95(1) <= dl*hs;
    b_96*dist_96*hs + (dl - ds)*x_96(1) <= dl*hs;
    b_97*dist_97*hs + (dl - ds)*x_97(1) <= dl*hs;
    b_98*dist_98*hs + (dl - ds)*x_98(1) <= dl*hs;
    b_99*dist_99*hs + (dl - ds)*x_99(1) <= dl*hs;
    b_100*dist_100*hs + (dl - ds)*x_100(1) <= dl*hs;
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
vars.u_45 = u_45;
vars.u{45} = u_45;
vars.u_46 = u_46;
vars.u{46} = u_46;
vars.u_47 = u_47;
vars.u{47} = u_47;
vars.u_48 = u_48;
vars.u{48} = u_48;
vars.u_49 = u_49;
vars.u{49} = u_49;
vars.u_50 = u_50;
vars.u{50} = u_50;
vars.u_51 = u_51;
vars.u{51} = u_51;
vars.u_52 = u_52;
vars.u{52} = u_52;
vars.u_53 = u_53;
vars.u{53} = u_53;
vars.u_54 = u_54;
vars.u{54} = u_54;
vars.u_55 = u_55;
vars.u{55} = u_55;
vars.u_56 = u_56;
vars.u{56} = u_56;
vars.u_57 = u_57;
vars.u{57} = u_57;
vars.u_58 = u_58;
vars.u{58} = u_58;
vars.u_59 = u_59;
vars.u{59} = u_59;
vars.u_60 = u_60;
vars.u{60} = u_60;
vars.u_61 = u_61;
vars.u{61} = u_61;
vars.u_62 = u_62;
vars.u{62} = u_62;
vars.u_63 = u_63;
vars.u{63} = u_63;
vars.u_64 = u_64;
vars.u{64} = u_64;
vars.u_65 = u_65;
vars.u{65} = u_65;
vars.u_66 = u_66;
vars.u{66} = u_66;
vars.u_67 = u_67;
vars.u{67} = u_67;
vars.u_68 = u_68;
vars.u{68} = u_68;
vars.u_69 = u_69;
vars.u{69} = u_69;
vars.u_70 = u_70;
vars.u{70} = u_70;
vars.u_71 = u_71;
vars.u{71} = u_71;
vars.u_72 = u_72;
vars.u{72} = u_72;
vars.u_73 = u_73;
vars.u{73} = u_73;
vars.u_74 = u_74;
vars.u{74} = u_74;
vars.u_75 = u_75;
vars.u{75} = u_75;
vars.u_76 = u_76;
vars.u{76} = u_76;
vars.u_77 = u_77;
vars.u{77} = u_77;
vars.u_78 = u_78;
vars.u{78} = u_78;
vars.u_79 = u_79;
vars.u{79} = u_79;
vars.u_80 = u_80;
vars.u{80} = u_80;
vars.u_81 = u_81;
vars.u{81} = u_81;
vars.u_82 = u_82;
vars.u{82} = u_82;
vars.u_83 = u_83;
vars.u{83} = u_83;
vars.u_84 = u_84;
vars.u{84} = u_84;
vars.u_85 = u_85;
vars.u{85} = u_85;
vars.u_86 = u_86;
vars.u{86} = u_86;
vars.u_87 = u_87;
vars.u{87} = u_87;
vars.u_88 = u_88;
vars.u{88} = u_88;
vars.u_89 = u_89;
vars.u{89} = u_89;
vars.u_90 = u_90;
vars.u{90} = u_90;
vars.u_91 = u_91;
vars.u{91} = u_91;
vars.u_92 = u_92;
vars.u{92} = u_92;
vars.u_93 = u_93;
vars.u{93} = u_93;
vars.u_94 = u_94;
vars.u{94} = u_94;
vars.u_95 = u_95;
vars.u{95} = u_95;
vars.u_96 = u_96;
vars.u{96} = u_96;
vars.u_97 = u_97;
vars.u{97} = u_97;
vars.u_98 = u_98;
vars.u{98} = u_98;
vars.u_99 = u_99;
vars.u{99} = u_99;
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
vars.x_46 = x_46;
vars.x{46} = x_46;
vars.x_47 = x_47;
vars.x{47} = x_47;
vars.x_48 = x_48;
vars.x{48} = x_48;
vars.x_49 = x_49;
vars.x{49} = x_49;
vars.x_50 = x_50;
vars.x{50} = x_50;
vars.x_51 = x_51;
vars.x{51} = x_51;
vars.x_52 = x_52;
vars.x{52} = x_52;
vars.x_53 = x_53;
vars.x{53} = x_53;
vars.x_54 = x_54;
vars.x{54} = x_54;
vars.x_55 = x_55;
vars.x{55} = x_55;
vars.x_56 = x_56;
vars.x{56} = x_56;
vars.x_57 = x_57;
vars.x{57} = x_57;
vars.x_58 = x_58;
vars.x{58} = x_58;
vars.x_59 = x_59;
vars.x{59} = x_59;
vars.x_60 = x_60;
vars.x{60} = x_60;
vars.x_61 = x_61;
vars.x{61} = x_61;
vars.x_62 = x_62;
vars.x{62} = x_62;
vars.x_63 = x_63;
vars.x{63} = x_63;
vars.x_64 = x_64;
vars.x{64} = x_64;
vars.x_65 = x_65;
vars.x{65} = x_65;
vars.x_66 = x_66;
vars.x{66} = x_66;
vars.x_67 = x_67;
vars.x{67} = x_67;
vars.x_68 = x_68;
vars.x{68} = x_68;
vars.x_69 = x_69;
vars.x{69} = x_69;
vars.x_70 = x_70;
vars.x{70} = x_70;
vars.x_71 = x_71;
vars.x{71} = x_71;
vars.x_72 = x_72;
vars.x{72} = x_72;
vars.x_73 = x_73;
vars.x{73} = x_73;
vars.x_74 = x_74;
vars.x{74} = x_74;
vars.x_75 = x_75;
vars.x{75} = x_75;
vars.x_76 = x_76;
vars.x{76} = x_76;
vars.x_77 = x_77;
vars.x{77} = x_77;
vars.x_78 = x_78;
vars.x{78} = x_78;
vars.x_79 = x_79;
vars.x{79} = x_79;
vars.x_80 = x_80;
vars.x{80} = x_80;
vars.x_81 = x_81;
vars.x{81} = x_81;
vars.x_82 = x_82;
vars.x{82} = x_82;
vars.x_83 = x_83;
vars.x{83} = x_83;
vars.x_84 = x_84;
vars.x{84} = x_84;
vars.x_85 = x_85;
vars.x{85} = x_85;
vars.x_86 = x_86;
vars.x{86} = x_86;
vars.x_87 = x_87;
vars.x{87} = x_87;
vars.x_88 = x_88;
vars.x{88} = x_88;
vars.x_89 = x_89;
vars.x{89} = x_89;
vars.x_90 = x_90;
vars.x{90} = x_90;
vars.x_91 = x_91;
vars.x{91} = x_91;
vars.x_92 = x_92;
vars.x{92} = x_92;
vars.x_93 = x_93;
vars.x{93} = x_93;
vars.x_94 = x_94;
vars.x{94} = x_94;
vars.x_95 = x_95;
vars.x{95} = x_95;
vars.x_96 = x_96;
vars.x{96} = x_96;
vars.x_97 = x_97;
vars.x{97} = x_97;
vars.x_98 = x_98;
vars.x{98} = x_98;
vars.x_99 = x_99;
vars.x{99} = x_99;
vars.x_100 = x_100;
vars.x{100} = x_100;
status.cvx_status = cvx_status;
% Provide a drop-in replacement for csolve.
status.optval = cvx_optval;
status.converged = strcmp(cvx_status, 'Solved');
