% csolve  Solves a custom quadratic program very rapidly.
%
% [vars, status] = csolve(params, settings)
%
% solves the convex optimization problem
%
%   minimize(quad_form(b_0*(x_0 - xb), Q) + quad_form(u_0, R) + quad_form(b_1*(x_1 - xb), Q) + quad_form(u_1, R) + quad_form(b_2*(x_2 - xb), Q) + quad_form(u_2, R) + quad_form(b_3*(x_3 - xb), Q) + quad_form(u_3, R) + quad_form(b_4*(x_4 - xb), Q) + quad_form(u_4, R) + quad_form(b_5*(x_5 - xb), Q) + quad_form(u_5, R) + quad_form(b_6*(x_6 - xb), Q) + quad_form(u_6, R) + quad_form(b_7*(x_7 - xb), Q) + quad_form(u_7, R) + quad_form(b_8*(x_8 - xb), Q) + quad_form(u_8, R) + quad_form(b_9*(x_9 - xb), Q) + quad_form(u_9, R) + quad_form(b_10*(x_10 - xb), Q) + quad_form(u_10, R) + quad_form(b_11*(x_11 - xb), Q) + quad_form(u_11, R) + quad_form(b_12*(x_12 - xb), Q) + quad_form(u_12, R) + quad_form(b_13*(x_13 - xb), Q) + quad_form(u_13, R) + quad_form(b_14*(x_14 - xb), Q) + quad_form(u_14, R) + quad_form(b_15*(x_15 - xb), Q) + quad_form(u_15, R) + quad_form(b_16*(x_16 - xb), Q) + quad_form(u_16, R) + quad_form(b_17*(x_17 - xb), Q) + quad_form(u_17, R) + quad_form(b_18*(x_18 - xb), Q) + quad_form(u_18, R) + quad_form(b_19*(x_19 - xb), Q) + quad_form(u_19, R) + quad_form(b_20*(x_20 - xb), Q) + quad_form(u_20, R) + quad_form(b_21*(x_21 - xb), Q) + quad_form(u_21, R) + quad_form(b_22*(x_22 - xb), Q) + quad_form(u_22, R) + quad_form(b_23*(x_23 - xb), Q) + quad_form(u_23, R) + quad_form(b_24*(x_24 - xb), Q) + quad_form(u_24, R) + quad_form(b_25*(x_25 - xb), Q) + quad_form(u_25, R) + quad_form(b_26*(x_26 - xb), Q) + quad_form(u_26, R) + quad_form(b_27*(x_27 - xb), Q) + quad_form(u_27, R) + quad_form(b_28*(x_28 - xb), Q) + quad_form(u_28, R) + quad_form(b_29*(x_29 - xb), Q) + quad_form(u_29, R) + quad_form(b_30*(x_30 - xb), Q) + quad_form(u_30, R) + quad_form(b_31*(x_31 - xb), Q) + quad_form(u_31, R) + quad_form(b_32*(x_32 - xb), Q) + quad_form(u_32, R) + quad_form(b_33*(x_33 - xb), Q) + quad_form(u_33, R) + quad_form(b_34*(x_34 - xb), Q) + quad_form(u_34, R) + quad_form(b_35*(x_35 - xb), Q) + quad_form(u_35, R) + quad_form(b_36*(x_36 - xb), Q) + quad_form(u_36, R) + quad_form(b_37*(x_37 - xb), Q) + quad_form(u_37, R) + quad_form(b_38*(x_38 - xb), Q) + quad_form(u_38, R) + quad_form(b_39*(x_39 - xb), Q) + quad_form(u_39, R) + quad_form(b_40*(x_40 - xb), Q) + quad_form(u_40, R) + quad_form(b_41*(x_41 - xb), Q) + quad_form(u_41, R) + quad_form(b_42*(x_42 - xb), Q) + quad_form(u_42, R) + quad_form(b_43*(x_43 - xb), Q) + quad_form(u_43, R) + quad_form(b_44*(x_44 - xb), Q) + quad_form(u_44, R) + quad_form(b_45*(x_45 - xb), Q) + quad_form(u_45, R) + quad_form(b_46*(x_46 - xb), Q) + quad_form(u_46, R) + quad_form(b_47*(x_47 - xb), Q) + quad_form(u_47, R) + quad_form(b_48*(x_48 - xb), Q) + quad_form(u_48, R) + quad_form(b_49*(x_49 - xb), Q) + quad_form(u_49, R) + quad_form(b_50*(x_50 - xb), Q) + quad_form(u_50, R) + quad_form(b_51*(x_51 - xb), Q) + quad_form(u_51, R) + quad_form(b_52*(x_52 - xb), Q) + quad_form(u_52, R) + quad_form(b_53*(x_53 - xb), Q) + quad_form(u_53, R) + quad_form(b_54*(x_54 - xb), Q) + quad_form(u_54, R) + quad_form(b_55*(x_55 - xb), Q) + quad_form(u_55, R) + quad_form(b_56*(x_56 - xb), Q) + quad_form(u_56, R) + quad_form(b_57*(x_57 - xb), Q) + quad_form(u_57, R) + quad_form(b_58*(x_58 - xb), Q) + quad_form(u_58, R) + quad_form(b_59*(x_59 - xb), Q) + quad_form(u_59, R) + quad_form(b_60*(x_60 - xb), Q) + quad_form(u_60, R) + quad_form(b_61*(x_61 - xb), Q) + quad_form(u_61, R) + quad_form(b_62*(x_62 - xb), Q) + quad_form(u_62, R) + quad_form(b_63*(x_63 - xb), Q) + quad_form(u_63, R) + quad_form(b_64*(x_64 - xb), Q) + quad_form(u_64, R) + quad_form(b_65*(x_65 - xb), Q) + quad_form(u_65, R) + quad_form(b_66*(x_66 - xb), Q) + quad_form(u_66, R) + quad_form(b_67*(x_67 - xb), Q) + quad_form(u_67, R) + quad_form(b_68*(x_68 - xb), Q) + quad_form(u_68, R) + quad_form(b_69*(x_69 - xb), Q) + quad_form(u_69, R) + quad_form(b_70*(x_70 - xb), Q) + quad_form(u_70, R) + quad_form(b_71*(x_71 - xb), Q) + quad_form(u_71, R) + quad_form(b_72*(x_72 - xb), Q) + quad_form(u_72, R) + quad_form(b_73*(x_73 - xb), Q) + quad_form(u_73, R) + quad_form(b_74*(x_74 - xb), Q) + quad_form(u_74, R) + quad_form(b_75*(x_75 - xb), Q) + quad_form(u_75, R) + quad_form(b_76*(x_76 - xb), Q) + quad_form(u_76, R) + quad_form(b_77*(x_77 - xb), Q) + quad_form(u_77, R) + quad_form(b_78*(x_78 - xb), Q) + quad_form(u_78, R) + quad_form(b_79*(x_79 - xb), Q) + quad_form(u_79, R) + quad_form(b_80*(x_80 - xb), Q) + quad_form(u_80, R) + quad_form(b_81*(x_81 - xb), Q) + quad_form(u_81, R) + quad_form(b_82*(x_82 - xb), Q) + quad_form(u_82, R) + quad_form(b_83*(x_83 - xb), Q) + quad_form(u_83, R) + quad_form(b_84*(x_84 - xb), Q) + quad_form(u_84, R) + quad_form(b_85*(x_85 - xb), Q) + quad_form(u_85, R) + quad_form(b_86*(x_86 - xb), Q) + quad_form(u_86, R) + quad_form(b_87*(x_87 - xb), Q) + quad_form(u_87, R) + quad_form(b_88*(x_88 - xb), Q) + quad_form(u_88, R) + quad_form(b_89*(x_89 - xb), Q) + quad_form(u_89, R) + quad_form(b_90*(x_90 - xb), Q) + quad_form(u_90, R) + quad_form(b_91*(x_91 - xb), Q) + quad_form(u_91, R) + quad_form(b_92*(x_92 - xb), Q) + quad_form(u_92, R) + quad_form(b_93*(x_93 - xb), Q) + quad_form(u_93, R) + quad_form(b_94*(x_94 - xb), Q) + quad_form(u_94, R) + quad_form(b_95*(x_95 - xb), Q) + quad_form(u_95, R) + quad_form(b_96*(x_96 - xb), Q) + quad_form(u_96, R) + quad_form(b_97*(x_97 - xb), Q) + quad_form(u_97, R) + quad_form(b_98*(x_98 - xb), Q) + quad_form(u_98, R) + quad_form(b_99*(x_99 - xb), Q) + quad_form(u_99, R) + quad_form(b_100*(x_100 - xb), P))
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
%     x_46 == A*x_45 + B*u_45
%     x_47 == A*x_46 + B*u_46
%     x_48 == A*x_47 + B*u_47
%     x_49 == A*x_48 + B*u_48
%     x_50 == A*x_49 + B*u_49
%     x_51 == A*x_50 + B*u_50
%     x_52 == A*x_51 + B*u_51
%     x_53 == A*x_52 + B*u_52
%     x_54 == A*x_53 + B*u_53
%     x_55 == A*x_54 + B*u_54
%     x_56 == A*x_55 + B*u_55
%     x_57 == A*x_56 + B*u_56
%     x_58 == A*x_57 + B*u_57
%     x_59 == A*x_58 + B*u_58
%     x_60 == A*x_59 + B*u_59
%     x_61 == A*x_60 + B*u_60
%     x_62 == A*x_61 + B*u_61
%     x_63 == A*x_62 + B*u_62
%     x_64 == A*x_63 + B*u_63
%     x_65 == A*x_64 + B*u_64
%     x_66 == A*x_65 + B*u_65
%     x_67 == A*x_66 + B*u_66
%     x_68 == A*x_67 + B*u_67
%     x_69 == A*x_68 + B*u_68
%     x_70 == A*x_69 + B*u_69
%     x_71 == A*x_70 + B*u_70
%     x_72 == A*x_71 + B*u_71
%     x_73 == A*x_72 + B*u_72
%     x_74 == A*x_73 + B*u_73
%     x_75 == A*x_74 + B*u_74
%     x_76 == A*x_75 + B*u_75
%     x_77 == A*x_76 + B*u_76
%     x_78 == A*x_77 + B*u_77
%     x_79 == A*x_78 + B*u_78
%     x_80 == A*x_79 + B*u_79
%     x_81 == A*x_80 + B*u_80
%     x_82 == A*x_81 + B*u_81
%     x_83 == A*x_82 + B*u_82
%     x_84 == A*x_83 + B*u_83
%     x_85 == A*x_84 + B*u_84
%     x_86 == A*x_85 + B*u_85
%     x_87 == A*x_86 + B*u_86
%     x_88 == A*x_87 + B*u_87
%     x_89 == A*x_88 + B*u_88
%     x_90 == A*x_89 + B*u_89
%     x_91 == A*x_90 + B*u_90
%     x_92 == A*x_91 + B*u_91
%     x_93 == A*x_92 + B*u_92
%     x_94 == A*x_93 + B*u_93
%     x_95 == A*x_94 + B*u_94
%     x_96 == A*x_95 + B*u_95
%     x_97 == A*x_96 + B*u_96
%     x_98 == A*x_97 + B*u_97
%     x_99 == A*x_98 + B*u_98
%     x_100 == A*x_99 + B*u_99
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
%     wmin <= x_26(2)
%     wmin <= x_27(2)
%     wmin <= x_28(2)
%     wmin <= x_29(2)
%     wmin <= x_30(2)
%     wmin <= x_31(2)
%     wmin <= x_32(2)
%     wmin <= x_33(2)
%     wmin <= x_34(2)
%     wmin <= x_35(2)
%     wmin <= x_36(2)
%     wmin <= x_37(2)
%     wmin <= x_38(2)
%     wmin <= x_39(2)
%     wmin <= x_40(2)
%     wmin <= x_41(2)
%     wmin <= x_42(2)
%     wmin <= x_43(2)
%     wmin <= x_44(2)
%     wmin <= x_45(2)
%     wmin <= x_46(2)
%     wmin <= x_47(2)
%     wmin <= x_48(2)
%     wmin <= x_49(2)
%     wmin <= x_50(2)
%     wmin <= x_51(2)
%     wmin <= x_52(2)
%     wmin <= x_53(2)
%     wmin <= x_54(2)
%     wmin <= x_55(2)
%     wmin <= x_56(2)
%     wmin <= x_57(2)
%     wmin <= x_58(2)
%     wmin <= x_59(2)
%     wmin <= x_60(2)
%     wmin <= x_61(2)
%     wmin <= x_62(2)
%     wmin <= x_63(2)
%     wmin <= x_64(2)
%     wmin <= x_65(2)
%     wmin <= x_66(2)
%     wmin <= x_67(2)
%     wmin <= x_68(2)
%     wmin <= x_69(2)
%     wmin <= x_70(2)
%     wmin <= x_71(2)
%     wmin <= x_72(2)
%     wmin <= x_73(2)
%     wmin <= x_74(2)
%     wmin <= x_75(2)
%     wmin <= x_76(2)
%     wmin <= x_77(2)
%     wmin <= x_78(2)
%     wmin <= x_79(2)
%     wmin <= x_80(2)
%     wmin <= x_81(2)
%     wmin <= x_82(2)
%     wmin <= x_83(2)
%     wmin <= x_84(2)
%     wmin <= x_85(2)
%     wmin <= x_86(2)
%     wmin <= x_87(2)
%     wmin <= x_88(2)
%     wmin <= x_89(2)
%     wmin <= x_90(2)
%     wmin <= x_91(2)
%     wmin <= x_92(2)
%     wmin <= x_93(2)
%     wmin <= x_94(2)
%     wmin <= x_95(2)
%     wmin <= x_96(2)
%     wmin <= x_97(2)
%     wmin <= x_98(2)
%     wmin <= x_99(2)
%     wmin <= x_100(2)
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
%     wmin <= u_25
%     wmin <= u_26
%     wmin <= u_27
%     wmin <= u_28
%     wmin <= u_29
%     wmin <= u_30
%     wmin <= u_31
%     wmin <= u_32
%     wmin <= u_33
%     wmin <= u_34
%     wmin <= u_35
%     wmin <= u_36
%     wmin <= u_37
%     wmin <= u_38
%     wmin <= u_39
%     wmin <= u_40
%     wmin <= u_41
%     wmin <= u_42
%     wmin <= u_43
%     wmin <= u_44
%     wmin <= u_45
%     wmin <= u_46
%     wmin <= u_47
%     wmin <= u_48
%     wmin <= u_49
%     wmin <= u_50
%     wmin <= u_51
%     wmin <= u_52
%     wmin <= u_53
%     wmin <= u_54
%     wmin <= u_55
%     wmin <= u_56
%     wmin <= u_57
%     wmin <= u_58
%     wmin <= u_59
%     wmin <= u_60
%     wmin <= u_61
%     wmin <= u_62
%     wmin <= u_63
%     wmin <= u_64
%     wmin <= u_65
%     wmin <= u_66
%     wmin <= u_67
%     wmin <= u_68
%     wmin <= u_69
%     wmin <= u_70
%     wmin <= u_71
%     wmin <= u_72
%     wmin <= u_73
%     wmin <= u_74
%     wmin <= u_75
%     wmin <= u_76
%     wmin <= u_77
%     wmin <= u_78
%     wmin <= u_79
%     wmin <= u_80
%     wmin <= u_81
%     wmin <= u_82
%     wmin <= u_83
%     wmin <= u_84
%     wmin <= u_85
%     wmin <= u_86
%     wmin <= u_87
%     wmin <= u_88
%     wmin <= u_89
%     wmin <= u_90
%     wmin <= u_91
%     wmin <= u_92
%     wmin <= u_93
%     wmin <= u_94
%     wmin <= u_95
%     wmin <= u_96
%     wmin <= u_97
%     wmin <= u_98
%     wmin <= u_99
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
%     u_25 <= wmax
%     u_26 <= wmax
%     u_27 <= wmax
%     u_28 <= wmax
%     u_29 <= wmax
%     u_30 <= wmax
%     u_31 <= wmax
%     u_32 <= wmax
%     u_33 <= wmax
%     u_34 <= wmax
%     u_35 <= wmax
%     u_36 <= wmax
%     u_37 <= wmax
%     u_38 <= wmax
%     u_39 <= wmax
%     u_40 <= wmax
%     u_41 <= wmax
%     u_42 <= wmax
%     u_43 <= wmax
%     u_44 <= wmax
%     u_45 <= wmax
%     u_46 <= wmax
%     u_47 <= wmax
%     u_48 <= wmax
%     u_49 <= wmax
%     u_50 <= wmax
%     u_51 <= wmax
%     u_52 <= wmax
%     u_53 <= wmax
%     u_54 <= wmax
%     u_55 <= wmax
%     u_56 <= wmax
%     u_57 <= wmax
%     u_58 <= wmax
%     u_59 <= wmax
%     u_60 <= wmax
%     u_61 <= wmax
%     u_62 <= wmax
%     u_63 <= wmax
%     u_64 <= wmax
%     u_65 <= wmax
%     u_66 <= wmax
%     u_67 <= wmax
%     u_68 <= wmax
%     u_69 <= wmax
%     u_70 <= wmax
%     u_71 <= wmax
%     u_72 <= wmax
%     u_73 <= wmax
%     u_74 <= wmax
%     u_75 <= wmax
%     u_76 <= wmax
%     u_77 <= wmax
%     u_78 <= wmax
%     u_79 <= wmax
%     u_80 <= wmax
%     u_81 <= wmax
%     u_82 <= wmax
%     u_83 <= wmax
%     u_84 <= wmax
%     u_85 <= wmax
%     u_86 <= wmax
%     u_87 <= wmax
%     u_88 <= wmax
%     u_89 <= wmax
%     u_90 <= wmax
%     u_91 <= wmax
%     u_92 <= wmax
%     u_93 <= wmax
%     u_94 <= wmax
%     u_95 <= wmax
%     u_96 <= wmax
%     u_97 <= wmax
%     u_98 <= wmax
%     u_99 <= wmax
%     x_1(2) >=  - kl*x_1(1) + wmin_land
%     x_2(2) >=  - kl*x_2(1) + wmin_land
%     x_3(2) >=  - kl*x_3(1) + wmin_land
%     x_4(2) >=  - kl*x_4(1) + wmin_land
%     x_5(2) >=  - kl*x_5(1) + wmin_land
%     x_6(2) >=  - kl*x_6(1) + wmin_land
%     x_7(2) >=  - kl*x_7(1) + wmin_land
%     x_8(2) >=  - kl*x_8(1) + wmin_land
%     x_9(2) >=  - kl*x_9(1) + wmin_land
%     x_10(2) >=  - kl*x_10(1) + wmin_land
%     x_11(2) >=  - kl*x_11(1) + wmin_land
%     x_12(2) >=  - kl*x_12(1) + wmin_land
%     x_13(2) >=  - kl*x_13(1) + wmin_land
%     x_14(2) >=  - kl*x_14(1) + wmin_land
%     x_15(2) >=  - kl*x_15(1) + wmin_land
%     x_16(2) >=  - kl*x_16(1) + wmin_land
%     x_17(2) >=  - kl*x_17(1) + wmin_land
%     x_18(2) >=  - kl*x_18(1) + wmin_land
%     x_19(2) >=  - kl*x_19(1) + wmin_land
%     x_20(2) >=  - kl*x_20(1) + wmin_land
%     x_21(2) >=  - kl*x_21(1) + wmin_land
%     x_22(2) >=  - kl*x_22(1) + wmin_land
%     x_23(2) >=  - kl*x_23(1) + wmin_land
%     x_24(2) >=  - kl*x_24(1) + wmin_land
%     x_25(2) >=  - kl*x_25(1) + wmin_land
%     x_26(2) >=  - kl*x_26(1) + wmin_land
%     x_27(2) >=  - kl*x_27(1) + wmin_land
%     x_28(2) >=  - kl*x_28(1) + wmin_land
%     x_29(2) >=  - kl*x_29(1) + wmin_land
%     x_30(2) >=  - kl*x_30(1) + wmin_land
%     x_31(2) >=  - kl*x_31(1) + wmin_land
%     x_32(2) >=  - kl*x_32(1) + wmin_land
%     x_33(2) >=  - kl*x_33(1) + wmin_land
%     x_34(2) >=  - kl*x_34(1) + wmin_land
%     x_35(2) >=  - kl*x_35(1) + wmin_land
%     x_36(2) >=  - kl*x_36(1) + wmin_land
%     x_37(2) >=  - kl*x_37(1) + wmin_land
%     x_38(2) >=  - kl*x_38(1) + wmin_land
%     x_39(2) >=  - kl*x_39(1) + wmin_land
%     x_40(2) >=  - kl*x_40(1) + wmin_land
%     x_41(2) >=  - kl*x_41(1) + wmin_land
%     x_42(2) >=  - kl*x_42(1) + wmin_land
%     x_43(2) >=  - kl*x_43(1) + wmin_land
%     x_44(2) >=  - kl*x_44(1) + wmin_land
%     x_45(2) >=  - kl*x_45(1) + wmin_land
%     x_46(2) >=  - kl*x_46(1) + wmin_land
%     x_47(2) >=  - kl*x_47(1) + wmin_land
%     x_48(2) >=  - kl*x_48(1) + wmin_land
%     x_49(2) >=  - kl*x_49(1) + wmin_land
%     x_50(2) >=  - kl*x_50(1) + wmin_land
%     x_51(2) >=  - kl*x_51(1) + wmin_land
%     x_52(2) >=  - kl*x_52(1) + wmin_land
%     x_53(2) >=  - kl*x_53(1) + wmin_land
%     x_54(2) >=  - kl*x_54(1) + wmin_land
%     x_55(2) >=  - kl*x_55(1) + wmin_land
%     x_56(2) >=  - kl*x_56(1) + wmin_land
%     x_57(2) >=  - kl*x_57(1) + wmin_land
%     x_58(2) >=  - kl*x_58(1) + wmin_land
%     x_59(2) >=  - kl*x_59(1) + wmin_land
%     x_60(2) >=  - kl*x_60(1) + wmin_land
%     x_61(2) >=  - kl*x_61(1) + wmin_land
%     x_62(2) >=  - kl*x_62(1) + wmin_land
%     x_63(2) >=  - kl*x_63(1) + wmin_land
%     x_64(2) >=  - kl*x_64(1) + wmin_land
%     x_65(2) >=  - kl*x_65(1) + wmin_land
%     x_66(2) >=  - kl*x_66(1) + wmin_land
%     x_67(2) >=  - kl*x_67(1) + wmin_land
%     x_68(2) >=  - kl*x_68(1) + wmin_land
%     x_69(2) >=  - kl*x_69(1) + wmin_land
%     x_70(2) >=  - kl*x_70(1) + wmin_land
%     x_71(2) >=  - kl*x_71(1) + wmin_land
%     x_72(2) >=  - kl*x_72(1) + wmin_land
%     x_73(2) >=  - kl*x_73(1) + wmin_land
%     x_74(2) >=  - kl*x_74(1) + wmin_land
%     x_75(2) >=  - kl*x_75(1) + wmin_land
%     x_76(2) >=  - kl*x_76(1) + wmin_land
%     x_77(2) >=  - kl*x_77(1) + wmin_land
%     x_78(2) >=  - kl*x_78(1) + wmin_land
%     x_79(2) >=  - kl*x_79(1) + wmin_land
%     x_80(2) >=  - kl*x_80(1) + wmin_land
%     x_81(2) >=  - kl*x_81(1) + wmin_land
%     x_82(2) >=  - kl*x_82(1) + wmin_land
%     x_83(2) >=  - kl*x_83(1) + wmin_land
%     x_84(2) >=  - kl*x_84(1) + wmin_land
%     x_85(2) >=  - kl*x_85(1) + wmin_land
%     x_86(2) >=  - kl*x_86(1) + wmin_land
%     x_87(2) >=  - kl*x_87(1) + wmin_land
%     x_88(2) >=  - kl*x_88(1) + wmin_land
%     x_89(2) >=  - kl*x_89(1) + wmin_land
%     x_90(2) >=  - kl*x_90(1) + wmin_land
%     x_91(2) >=  - kl*x_91(1) + wmin_land
%     x_92(2) >=  - kl*x_92(1) + wmin_land
%     x_93(2) >=  - kl*x_93(1) + wmin_land
%     x_94(2) >=  - kl*x_94(1) + wmin_land
%     x_95(2) >=  - kl*x_95(1) + wmin_land
%     x_96(2) >=  - kl*x_96(1) + wmin_land
%     x_97(2) >=  - kl*x_97(1) + wmin_land
%     x_98(2) >=  - kl*x_98(1) + wmin_land
%     x_99(2) >=  - kl*x_99(1) + wmin_land
%     x_100(2) >=  - kl*x_100(1) + wmin_land
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
%     x_26(1) >= 0
%     x_27(1) >= 0
%     x_28(1) >= 0
%     x_29(1) >= 0
%     x_30(1) >= 0
%     x_31(1) >= 0
%     x_32(1) >= 0
%     x_33(1) >= 0
%     x_34(1) >= 0
%     x_35(1) >= 0
%     x_36(1) >= 0
%     x_37(1) >= 0
%     x_38(1) >= 0
%     x_39(1) >= 0
%     x_40(1) >= 0
%     x_41(1) >= 0
%     x_42(1) >= 0
%     x_43(1) >= 0
%     x_44(1) >= 0
%     x_45(1) >= 0
%     x_46(1) >= 0
%     x_47(1) >= 0
%     x_48(1) >= 0
%     x_49(1) >= 0
%     x_50(1) >= 0
%     x_51(1) >= 0
%     x_52(1) >= 0
%     x_53(1) >= 0
%     x_54(1) >= 0
%     x_55(1) >= 0
%     x_56(1) >= 0
%     x_57(1) >= 0
%     x_58(1) >= 0
%     x_59(1) >= 0
%     x_60(1) >= 0
%     x_61(1) >= 0
%     x_62(1) >= 0
%     x_63(1) >= 0
%     x_64(1) >= 0
%     x_65(1) >= 0
%     x_66(1) >= 0
%     x_67(1) >= 0
%     x_68(1) >= 0
%     x_69(1) >= 0
%     x_70(1) >= 0
%     x_71(1) >= 0
%     x_72(1) >= 0
%     x_73(1) >= 0
%     x_74(1) >= 0
%     x_75(1) >= 0
%     x_76(1) >= 0
%     x_77(1) >= 0
%     x_78(1) >= 0
%     x_79(1) >= 0
%     x_80(1) >= 0
%     x_81(1) >= 0
%     x_82(1) >= 0
%     x_83(1) >= 0
%     x_84(1) >= 0
%     x_85(1) >= 0
%     x_86(1) >= 0
%     x_87(1) >= 0
%     x_88(1) >= 0
%     x_89(1) >= 0
%     x_90(1) >= 0
%     x_91(1) >= 0
%     x_92(1) >= 0
%     x_93(1) >= 0
%     x_94(1) >= 0
%     x_95(1) >= 0
%     x_96(1) >= 0
%     x_97(1) >= 0
%     x_98(1) >= 0
%     x_99(1) >= 0
%     x_100(1) >= 0
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
%     b_26*dist_26*hs + (dl - ds)*x_26(1) <= dl*hs
%     b_27*dist_27*hs + (dl - ds)*x_27(1) <= dl*hs
%     b_28*dist_28*hs + (dl - ds)*x_28(1) <= dl*hs
%     b_29*dist_29*hs + (dl - ds)*x_29(1) <= dl*hs
%     b_30*dist_30*hs + (dl - ds)*x_30(1) <= dl*hs
%     b_31*dist_31*hs + (dl - ds)*x_31(1) <= dl*hs
%     b_32*dist_32*hs + (dl - ds)*x_32(1) <= dl*hs
%     b_33*dist_33*hs + (dl - ds)*x_33(1) <= dl*hs
%     b_34*dist_34*hs + (dl - ds)*x_34(1) <= dl*hs
%     b_35*dist_35*hs + (dl - ds)*x_35(1) <= dl*hs
%     b_36*dist_36*hs + (dl - ds)*x_36(1) <= dl*hs
%     b_37*dist_37*hs + (dl - ds)*x_37(1) <= dl*hs
%     b_38*dist_38*hs + (dl - ds)*x_38(1) <= dl*hs
%     b_39*dist_39*hs + (dl - ds)*x_39(1) <= dl*hs
%     b_40*dist_40*hs + (dl - ds)*x_40(1) <= dl*hs
%     b_41*dist_41*hs + (dl - ds)*x_41(1) <= dl*hs
%     b_42*dist_42*hs + (dl - ds)*x_42(1) <= dl*hs
%     b_43*dist_43*hs + (dl - ds)*x_43(1) <= dl*hs
%     b_44*dist_44*hs + (dl - ds)*x_44(1) <= dl*hs
%     b_45*dist_45*hs + (dl - ds)*x_45(1) <= dl*hs
%     b_46*dist_46*hs + (dl - ds)*x_46(1) <= dl*hs
%     b_47*dist_47*hs + (dl - ds)*x_47(1) <= dl*hs
%     b_48*dist_48*hs + (dl - ds)*x_48(1) <= dl*hs
%     b_49*dist_49*hs + (dl - ds)*x_49(1) <= dl*hs
%     b_50*dist_50*hs + (dl - ds)*x_50(1) <= dl*hs
%     b_51*dist_51*hs + (dl - ds)*x_51(1) <= dl*hs
%     b_52*dist_52*hs + (dl - ds)*x_52(1) <= dl*hs
%     b_53*dist_53*hs + (dl - ds)*x_53(1) <= dl*hs
%     b_54*dist_54*hs + (dl - ds)*x_54(1) <= dl*hs
%     b_55*dist_55*hs + (dl - ds)*x_55(1) <= dl*hs
%     b_56*dist_56*hs + (dl - ds)*x_56(1) <= dl*hs
%     b_57*dist_57*hs + (dl - ds)*x_57(1) <= dl*hs
%     b_58*dist_58*hs + (dl - ds)*x_58(1) <= dl*hs
%     b_59*dist_59*hs + (dl - ds)*x_59(1) <= dl*hs
%     b_60*dist_60*hs + (dl - ds)*x_60(1) <= dl*hs
%     b_61*dist_61*hs + (dl - ds)*x_61(1) <= dl*hs
%     b_62*dist_62*hs + (dl - ds)*x_62(1) <= dl*hs
%     b_63*dist_63*hs + (dl - ds)*x_63(1) <= dl*hs
%     b_64*dist_64*hs + (dl - ds)*x_64(1) <= dl*hs
%     b_65*dist_65*hs + (dl - ds)*x_65(1) <= dl*hs
%     b_66*dist_66*hs + (dl - ds)*x_66(1) <= dl*hs
%     b_67*dist_67*hs + (dl - ds)*x_67(1) <= dl*hs
%     b_68*dist_68*hs + (dl - ds)*x_68(1) <= dl*hs
%     b_69*dist_69*hs + (dl - ds)*x_69(1) <= dl*hs
%     b_70*dist_70*hs + (dl - ds)*x_70(1) <= dl*hs
%     b_71*dist_71*hs + (dl - ds)*x_71(1) <= dl*hs
%     b_72*dist_72*hs + (dl - ds)*x_72(1) <= dl*hs
%     b_73*dist_73*hs + (dl - ds)*x_73(1) <= dl*hs
%     b_74*dist_74*hs + (dl - ds)*x_74(1) <= dl*hs
%     b_75*dist_75*hs + (dl - ds)*x_75(1) <= dl*hs
%     b_76*dist_76*hs + (dl - ds)*x_76(1) <= dl*hs
%     b_77*dist_77*hs + (dl - ds)*x_77(1) <= dl*hs
%     b_78*dist_78*hs + (dl - ds)*x_78(1) <= dl*hs
%     b_79*dist_79*hs + (dl - ds)*x_79(1) <= dl*hs
%     b_80*dist_80*hs + (dl - ds)*x_80(1) <= dl*hs
%     b_81*dist_81*hs + (dl - ds)*x_81(1) <= dl*hs
%     b_82*dist_82*hs + (dl - ds)*x_82(1) <= dl*hs
%     b_83*dist_83*hs + (dl - ds)*x_83(1) <= dl*hs
%     b_84*dist_84*hs + (dl - ds)*x_84(1) <= dl*hs
%     b_85*dist_85*hs + (dl - ds)*x_85(1) <= dl*hs
%     b_86*dist_86*hs + (dl - ds)*x_86(1) <= dl*hs
%     b_87*dist_87*hs + (dl - ds)*x_87(1) <= dl*hs
%     b_88*dist_88*hs + (dl - ds)*x_88(1) <= dl*hs
%     b_89*dist_89*hs + (dl - ds)*x_89(1) <= dl*hs
%     b_90*dist_90*hs + (dl - ds)*x_90(1) <= dl*hs
%     b_91*dist_91*hs + (dl - ds)*x_91(1) <= dl*hs
%     b_92*dist_92*hs + (dl - ds)*x_92(1) <= dl*hs
%     b_93*dist_93*hs + (dl - ds)*x_93(1) <= dl*hs
%     b_94*dist_94*hs + (dl - ds)*x_94(1) <= dl*hs
%     b_95*dist_95*hs + (dl - ds)*x_95(1) <= dl*hs
%     b_96*dist_96*hs + (dl - ds)*x_96(1) <= dl*hs
%     b_97*dist_97*hs + (dl - ds)*x_97(1) <= dl*hs
%     b_98*dist_98*hs + (dl - ds)*x_98(1) <= dl*hs
%     b_99*dist_99*hs + (dl - ds)*x_99(1) <= dl*hs
%     b_100*dist_100*hs + (dl - ds)*x_100(1) <= dl*hs
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
%     u_25   1 x 1
%     u_26   1 x 1
%     u_27   1 x 1
%     u_28   1 x 1
%     u_29   1 x 1
%     u_30   1 x 1
%     u_31   1 x 1
%     u_32   1 x 1
%     u_33   1 x 1
%     u_34   1 x 1
%     u_35   1 x 1
%     u_36   1 x 1
%     u_37   1 x 1
%     u_38   1 x 1
%     u_39   1 x 1
%     u_40   1 x 1
%     u_41   1 x 1
%     u_42   1 x 1
%     u_43   1 x 1
%     u_44   1 x 1
%     u_45   1 x 1
%     u_46   1 x 1
%     u_47   1 x 1
%     u_48   1 x 1
%     u_49   1 x 1
%     u_50   1 x 1
%     u_51   1 x 1
%     u_52   1 x 1
%     u_53   1 x 1
%     u_54   1 x 1
%     u_55   1 x 1
%     u_56   1 x 1
%     u_57   1 x 1
%     u_58   1 x 1
%     u_59   1 x 1
%     u_60   1 x 1
%     u_61   1 x 1
%     u_62   1 x 1
%     u_63   1 x 1
%     u_64   1 x 1
%     u_65   1 x 1
%     u_66   1 x 1
%     u_67   1 x 1
%     u_68   1 x 1
%     u_69   1 x 1
%     u_70   1 x 1
%     u_71   1 x 1
%     u_72   1 x 1
%     u_73   1 x 1
%     u_74   1 x 1
%     u_75   1 x 1
%     u_76   1 x 1
%     u_77   1 x 1
%     u_78   1 x 1
%     u_79   1 x 1
%     u_80   1 x 1
%     u_81   1 x 1
%     u_82   1 x 1
%     u_83   1 x 1
%     u_84   1 x 1
%     u_85   1 x 1
%     u_86   1 x 1
%     u_87   1 x 1
%     u_88   1 x 1
%     u_89   1 x 1
%     u_90   1 x 1
%     u_91   1 x 1
%     u_92   1 x 1
%     u_93   1 x 1
%     u_94   1 x 1
%     u_95   1 x 1
%     u_96   1 x 1
%     u_97   1 x 1
%     u_98   1 x 1
%     u_99   1 x 1
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
%     x_26   2 x 1
%     x_27   2 x 1
%     x_28   2 x 1
%     x_29   2 x 1
%     x_30   2 x 1
%     x_31   2 x 1
%     x_32   2 x 1
%     x_33   2 x 1
%     x_34   2 x 1
%     x_35   2 x 1
%     x_36   2 x 1
%     x_37   2 x 1
%     x_38   2 x 1
%     x_39   2 x 1
%     x_40   2 x 1
%     x_41   2 x 1
%     x_42   2 x 1
%     x_43   2 x 1
%     x_44   2 x 1
%     x_45   2 x 1
%     x_46   2 x 1
%     x_47   2 x 1
%     x_48   2 x 1
%     x_49   2 x 1
%     x_50   2 x 1
%     x_51   2 x 1
%     x_52   2 x 1
%     x_53   2 x 1
%     x_54   2 x 1
%     x_55   2 x 1
%     x_56   2 x 1
%     x_57   2 x 1
%     x_58   2 x 1
%     x_59   2 x 1
%     x_60   2 x 1
%     x_61   2 x 1
%     x_62   2 x 1
%     x_63   2 x 1
%     x_64   2 x 1
%     x_65   2 x 1
%     x_66   2 x 1
%     x_67   2 x 1
%     x_68   2 x 1
%     x_69   2 x 1
%     x_70   2 x 1
%     x_71   2 x 1
%     x_72   2 x 1
%     x_73   2 x 1
%     x_74   2 x 1
%     x_75   2 x 1
%     x_76   2 x 1
%     x_77   2 x 1
%     x_78   2 x 1
%     x_79   2 x 1
%     x_80   2 x 1
%     x_81   2 x 1
%     x_82   2 x 1
%     x_83   2 x 1
%     x_84   2 x 1
%     x_85   2 x 1
%     x_86   2 x 1
%     x_87   2 x 1
%     x_88   2 x 1
%     x_89   2 x 1
%     x_90   2 x 1
%     x_91   2 x 1
%     x_92   2 x 1
%     x_93   2 x 1
%     x_94   2 x 1
%     x_95   2 x 1
%     x_96   2 x 1
%     x_97   2 x 1
%     x_98   2 x 1
%     x_99   2 x 1
%    x_100   2 x 1
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
%     b_26   1 x 1
%     b_27   1 x 1
%     b_28   1 x 1
%     b_29   1 x 1
%     b_30   1 x 1
%     b_31   1 x 1
%     b_32   1 x 1
%     b_33   1 x 1
%     b_34   1 x 1
%     b_35   1 x 1
%     b_36   1 x 1
%     b_37   1 x 1
%     b_38   1 x 1
%     b_39   1 x 1
%     b_40   1 x 1
%     b_41   1 x 1
%     b_42   1 x 1
%     b_43   1 x 1
%     b_44   1 x 1
%     b_45   1 x 1
%     b_46   1 x 1
%     b_47   1 x 1
%     b_48   1 x 1
%     b_49   1 x 1
%     b_50   1 x 1
%     b_51   1 x 1
%     b_52   1 x 1
%     b_53   1 x 1
%     b_54   1 x 1
%     b_55   1 x 1
%     b_56   1 x 1
%     b_57   1 x 1
%     b_58   1 x 1
%     b_59   1 x 1
%     b_60   1 x 1
%     b_61   1 x 1
%     b_62   1 x 1
%     b_63   1 x 1
%     b_64   1 x 1
%     b_65   1 x 1
%     b_66   1 x 1
%     b_67   1 x 1
%     b_68   1 x 1
%     b_69   1 x 1
%     b_70   1 x 1
%     b_71   1 x 1
%     b_72   1 x 1
%     b_73   1 x 1
%     b_74   1 x 1
%     b_75   1 x 1
%     b_76   1 x 1
%     b_77   1 x 1
%     b_78   1 x 1
%     b_79   1 x 1
%     b_80   1 x 1
%     b_81   1 x 1
%     b_82   1 x 1
%     b_83   1 x 1
%     b_84   1 x 1
%     b_85   1 x 1
%     b_86   1 x 1
%     b_87   1 x 1
%     b_88   1 x 1
%     b_89   1 x 1
%     b_90   1 x 1
%     b_91   1 x 1
%     b_92   1 x 1
%     b_93   1 x 1
%     b_94   1 x 1
%     b_95   1 x 1
%     b_96   1 x 1
%     b_97   1 x 1
%     b_98   1 x 1
%     b_99   1 x 1
%    b_100   1 x 1
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
%  dist_26   1 x 1
%  dist_27   1 x 1
%  dist_28   1 x 1
%  dist_29   1 x 1
%  dist_30   1 x 1
%  dist_31   1 x 1
%  dist_32   1 x 1
%  dist_33   1 x 1
%  dist_34   1 x 1
%  dist_35   1 x 1
%  dist_36   1 x 1
%  dist_37   1 x 1
%  dist_38   1 x 1
%  dist_39   1 x 1
%  dist_40   1 x 1
%  dist_41   1 x 1
%  dist_42   1 x 1
%  dist_43   1 x 1
%  dist_44   1 x 1
%  dist_45   1 x 1
%  dist_46   1 x 1
%  dist_47   1 x 1
%  dist_48   1 x 1
%  dist_49   1 x 1
%  dist_50   1 x 1
%  dist_51   1 x 1
%  dist_52   1 x 1
%  dist_53   1 x 1
%  dist_54   1 x 1
%  dist_55   1 x 1
%  dist_56   1 x 1
%  dist_57   1 x 1
%  dist_58   1 x 1
%  dist_59   1 x 1
%  dist_60   1 x 1
%  dist_61   1 x 1
%  dist_62   1 x 1
%  dist_63   1 x 1
%  dist_64   1 x 1
%  dist_65   1 x 1
%  dist_66   1 x 1
%  dist_67   1 x 1
%  dist_68   1 x 1
%  dist_69   1 x 1
%  dist_70   1 x 1
%  dist_71   1 x 1
%  dist_72   1 x 1
%  dist_73   1 x 1
%  dist_74   1 x 1
%  dist_75   1 x 1
%  dist_76   1 x 1
%  dist_77   1 x 1
%  dist_78   1 x 1
%  dist_79   1 x 1
%  dist_80   1 x 1
%  dist_81   1 x 1
%  dist_82   1 x 1
%  dist_83   1 x 1
%  dist_84   1 x 1
%  dist_85   1 x 1
%  dist_86   1 x 1
%  dist_87   1 x 1
%  dist_88   1 x 1
%  dist_89   1 x 1
%  dist_90   1 x 1
%  dist_91   1 x 1
%  dist_92   1 x 1
%  dist_93   1 x 1
%  dist_94   1 x 1
%  dist_95   1 x 1
%  dist_96   1 x 1
%  dist_97   1 x 1
%  dist_98   1 x 1
%  dist_99   1 x 1
% dist_100   1 x 1
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
% Produced by CVXGEN, 2019-05-01 05:35:47 -0400.
% CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com.
% The code in this file is Copyright (C) 2006-2017 Jacob Mattingley.
% CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial
% applications without prior written permission from Jacob Mattingley.

% Filename: csolve.m.
% Description: Help file for the Matlab solver interface.
