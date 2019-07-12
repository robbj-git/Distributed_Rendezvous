/* Produced by CVXGEN, 2019-05-01 05:36:41 -0400.  */
/* CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com. */
/* The code in this file is Copyright (C) 2006-2017 Jacob Mattingley. */
/* CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial */
/* applications without prior written permission from Jacob Mattingley. */

/* Filename: solver.c. */
/* Description: Main solver file. */
#include "solver.h"
double eval_gap(void) {
  int i;
  double gap;
  gap = 0;
  for (i = 0; i < 600; i++)
    gap += work.z[i]*work.s[i];
  return gap;
}
void set_defaults(void) {
  settings.resid_tol = 1e-6;
  settings.eps = 1e-4;
  settings.max_iters = 25;
  settings.refine_steps = 1;
  settings.s_init = 1;
  settings.z_init = 1;
  settings.debug = 0;
  settings.verbose = 1;
  settings.verbose_refinement = 0;
  settings.better_start = 1;
  settings.kkt_reg = 1e-7;
}
void setup_pointers(void) {
  work.y = work.x + 300;
  work.s = work.x + 500;
  work.z = work.x + 1100;
  vars.u_0 = work.x + 0;
  vars.u_1 = work.x + 1;
  vars.u_2 = work.x + 2;
  vars.u_3 = work.x + 3;
  vars.u_4 = work.x + 4;
  vars.u_5 = work.x + 5;
  vars.u_6 = work.x + 6;
  vars.u_7 = work.x + 7;
  vars.u_8 = work.x + 8;
  vars.u_9 = work.x + 9;
  vars.u_10 = work.x + 10;
  vars.u_11 = work.x + 11;
  vars.u_12 = work.x + 12;
  vars.u_13 = work.x + 13;
  vars.u_14 = work.x + 14;
  vars.u_15 = work.x + 15;
  vars.u_16 = work.x + 16;
  vars.u_17 = work.x + 17;
  vars.u_18 = work.x + 18;
  vars.u_19 = work.x + 19;
  vars.u_20 = work.x + 20;
  vars.u_21 = work.x + 21;
  vars.u_22 = work.x + 22;
  vars.u_23 = work.x + 23;
  vars.u_24 = work.x + 24;
  vars.u_25 = work.x + 25;
  vars.u_26 = work.x + 26;
  vars.u_27 = work.x + 27;
  vars.u_28 = work.x + 28;
  vars.u_29 = work.x + 29;
  vars.u_30 = work.x + 30;
  vars.u_31 = work.x + 31;
  vars.u_32 = work.x + 32;
  vars.u_33 = work.x + 33;
  vars.u_34 = work.x + 34;
  vars.u_35 = work.x + 35;
  vars.u_36 = work.x + 36;
  vars.u_37 = work.x + 37;
  vars.u_38 = work.x + 38;
  vars.u_39 = work.x + 39;
  vars.u_40 = work.x + 40;
  vars.u_41 = work.x + 41;
  vars.u_42 = work.x + 42;
  vars.u_43 = work.x + 43;
  vars.u_44 = work.x + 44;
  vars.u_45 = work.x + 45;
  vars.u_46 = work.x + 46;
  vars.u_47 = work.x + 47;
  vars.u_48 = work.x + 48;
  vars.u_49 = work.x + 49;
  vars.u_50 = work.x + 50;
  vars.u_51 = work.x + 51;
  vars.u_52 = work.x + 52;
  vars.u_53 = work.x + 53;
  vars.u_54 = work.x + 54;
  vars.u_55 = work.x + 55;
  vars.u_56 = work.x + 56;
  vars.u_57 = work.x + 57;
  vars.u_58 = work.x + 58;
  vars.u_59 = work.x + 59;
  vars.u_60 = work.x + 60;
  vars.u_61 = work.x + 61;
  vars.u_62 = work.x + 62;
  vars.u_63 = work.x + 63;
  vars.u_64 = work.x + 64;
  vars.u_65 = work.x + 65;
  vars.u_66 = work.x + 66;
  vars.u_67 = work.x + 67;
  vars.u_68 = work.x + 68;
  vars.u_69 = work.x + 69;
  vars.u_70 = work.x + 70;
  vars.u_71 = work.x + 71;
  vars.u_72 = work.x + 72;
  vars.u_73 = work.x + 73;
  vars.u_74 = work.x + 74;
  vars.u_75 = work.x + 75;
  vars.u_76 = work.x + 76;
  vars.u_77 = work.x + 77;
  vars.u_78 = work.x + 78;
  vars.u_79 = work.x + 79;
  vars.u_80 = work.x + 80;
  vars.u_81 = work.x + 81;
  vars.u_82 = work.x + 82;
  vars.u_83 = work.x + 83;
  vars.u_84 = work.x + 84;
  vars.u_85 = work.x + 85;
  vars.u_86 = work.x + 86;
  vars.u_87 = work.x + 87;
  vars.u_88 = work.x + 88;
  vars.u_89 = work.x + 89;
  vars.u_90 = work.x + 90;
  vars.u_91 = work.x + 91;
  vars.u_92 = work.x + 92;
  vars.u_93 = work.x + 93;
  vars.u_94 = work.x + 94;
  vars.u_95 = work.x + 95;
  vars.u_96 = work.x + 96;
  vars.u_97 = work.x + 97;
  vars.u_98 = work.x + 98;
  vars.u_99 = work.x + 99;
  vars.x_1 = work.x + 100;
  vars.x_2 = work.x + 102;
  vars.x_3 = work.x + 104;
  vars.x_4 = work.x + 106;
  vars.x_5 = work.x + 108;
  vars.x_6 = work.x + 110;
  vars.x_7 = work.x + 112;
  vars.x_8 = work.x + 114;
  vars.x_9 = work.x + 116;
  vars.x_10 = work.x + 118;
  vars.x_11 = work.x + 120;
  vars.x_12 = work.x + 122;
  vars.x_13 = work.x + 124;
  vars.x_14 = work.x + 126;
  vars.x_15 = work.x + 128;
  vars.x_16 = work.x + 130;
  vars.x_17 = work.x + 132;
  vars.x_18 = work.x + 134;
  vars.x_19 = work.x + 136;
  vars.x_20 = work.x + 138;
  vars.x_21 = work.x + 140;
  vars.x_22 = work.x + 142;
  vars.x_23 = work.x + 144;
  vars.x_24 = work.x + 146;
  vars.x_25 = work.x + 148;
  vars.x_26 = work.x + 150;
  vars.x_27 = work.x + 152;
  vars.x_28 = work.x + 154;
  vars.x_29 = work.x + 156;
  vars.x_30 = work.x + 158;
  vars.x_31 = work.x + 160;
  vars.x_32 = work.x + 162;
  vars.x_33 = work.x + 164;
  vars.x_34 = work.x + 166;
  vars.x_35 = work.x + 168;
  vars.x_36 = work.x + 170;
  vars.x_37 = work.x + 172;
  vars.x_38 = work.x + 174;
  vars.x_39 = work.x + 176;
  vars.x_40 = work.x + 178;
  vars.x_41 = work.x + 180;
  vars.x_42 = work.x + 182;
  vars.x_43 = work.x + 184;
  vars.x_44 = work.x + 186;
  vars.x_45 = work.x + 188;
  vars.x_46 = work.x + 190;
  vars.x_47 = work.x + 192;
  vars.x_48 = work.x + 194;
  vars.x_49 = work.x + 196;
  vars.x_50 = work.x + 198;
  vars.x_51 = work.x + 200;
  vars.x_52 = work.x + 202;
  vars.x_53 = work.x + 204;
  vars.x_54 = work.x + 206;
  vars.x_55 = work.x + 208;
  vars.x_56 = work.x + 210;
  vars.x_57 = work.x + 212;
  vars.x_58 = work.x + 214;
  vars.x_59 = work.x + 216;
  vars.x_60 = work.x + 218;
  vars.x_61 = work.x + 220;
  vars.x_62 = work.x + 222;
  vars.x_63 = work.x + 224;
  vars.x_64 = work.x + 226;
  vars.x_65 = work.x + 228;
  vars.x_66 = work.x + 230;
  vars.x_67 = work.x + 232;
  vars.x_68 = work.x + 234;
  vars.x_69 = work.x + 236;
  vars.x_70 = work.x + 238;
  vars.x_71 = work.x + 240;
  vars.x_72 = work.x + 242;
  vars.x_73 = work.x + 244;
  vars.x_74 = work.x + 246;
  vars.x_75 = work.x + 248;
  vars.x_76 = work.x + 250;
  vars.x_77 = work.x + 252;
  vars.x_78 = work.x + 254;
  vars.x_79 = work.x + 256;
  vars.x_80 = work.x + 258;
  vars.x_81 = work.x + 260;
  vars.x_82 = work.x + 262;
  vars.x_83 = work.x + 264;
  vars.x_84 = work.x + 266;
  vars.x_85 = work.x + 268;
  vars.x_86 = work.x + 270;
  vars.x_87 = work.x + 272;
  vars.x_88 = work.x + 274;
  vars.x_89 = work.x + 276;
  vars.x_90 = work.x + 278;
  vars.x_91 = work.x + 280;
  vars.x_92 = work.x + 282;
  vars.x_93 = work.x + 284;
  vars.x_94 = work.x + 286;
  vars.x_95 = work.x + 288;
  vars.x_96 = work.x + 290;
  vars.x_97 = work.x + 292;
  vars.x_98 = work.x + 294;
  vars.x_99 = work.x + 296;
  vars.x_100 = work.x + 298;
}
void setup_indexed_params(void) {
  /* In CVXGEN, you can say */
  /*   parameters */
  /*     A[i] (5,3), i=1..4 */
  /*   end */
  /* This function sets up A[2] to be a pointer to A_2, which is a length-15 */
  /* vector of doubles. */
  /* If you access parameters that you haven't defined in CVXGEN, the result */
  /* is undefined. */
  params.b[0] = params.b_0;
  params.x[0] = params.x_0;
  params.b[1] = params.b_1;
  params.b[2] = params.b_2;
  params.b[3] = params.b_3;
  params.b[4] = params.b_4;
  params.b[5] = params.b_5;
  params.b[6] = params.b_6;
  params.b[7] = params.b_7;
  params.b[8] = params.b_8;
  params.b[9] = params.b_9;
  params.b[10] = params.b_10;
  params.b[11] = params.b_11;
  params.b[12] = params.b_12;
  params.b[13] = params.b_13;
  params.b[14] = params.b_14;
  params.b[15] = params.b_15;
  params.b[16] = params.b_16;
  params.b[17] = params.b_17;
  params.b[18] = params.b_18;
  params.b[19] = params.b_19;
  params.b[20] = params.b_20;
  params.b[21] = params.b_21;
  params.b[22] = params.b_22;
  params.b[23] = params.b_23;
  params.b[24] = params.b_24;
  params.b[25] = params.b_25;
  params.b[26] = params.b_26;
  params.b[27] = params.b_27;
  params.b[28] = params.b_28;
  params.b[29] = params.b_29;
  params.b[30] = params.b_30;
  params.b[31] = params.b_31;
  params.b[32] = params.b_32;
  params.b[33] = params.b_33;
  params.b[34] = params.b_34;
  params.b[35] = params.b_35;
  params.b[36] = params.b_36;
  params.b[37] = params.b_37;
  params.b[38] = params.b_38;
  params.b[39] = params.b_39;
  params.b[40] = params.b_40;
  params.b[41] = params.b_41;
  params.b[42] = params.b_42;
  params.b[43] = params.b_43;
  params.b[44] = params.b_44;
  params.b[45] = params.b_45;
  params.b[46] = params.b_46;
  params.b[47] = params.b_47;
  params.b[48] = params.b_48;
  params.b[49] = params.b_49;
  params.b[50] = params.b_50;
  params.b[51] = params.b_51;
  params.b[52] = params.b_52;
  params.b[53] = params.b_53;
  params.b[54] = params.b_54;
  params.b[55] = params.b_55;
  params.b[56] = params.b_56;
  params.b[57] = params.b_57;
  params.b[58] = params.b_58;
  params.b[59] = params.b_59;
  params.b[60] = params.b_60;
  params.b[61] = params.b_61;
  params.b[62] = params.b_62;
  params.b[63] = params.b_63;
  params.b[64] = params.b_64;
  params.b[65] = params.b_65;
  params.b[66] = params.b_66;
  params.b[67] = params.b_67;
  params.b[68] = params.b_68;
  params.b[69] = params.b_69;
  params.b[70] = params.b_70;
  params.b[71] = params.b_71;
  params.b[72] = params.b_72;
  params.b[73] = params.b_73;
  params.b[74] = params.b_74;
  params.b[75] = params.b_75;
  params.b[76] = params.b_76;
  params.b[77] = params.b_77;
  params.b[78] = params.b_78;
  params.b[79] = params.b_79;
  params.b[80] = params.b_80;
  params.b[81] = params.b_81;
  params.b[82] = params.b_82;
  params.b[83] = params.b_83;
  params.b[84] = params.b_84;
  params.b[85] = params.b_85;
  params.b[86] = params.b_86;
  params.b[87] = params.b_87;
  params.b[88] = params.b_88;
  params.b[89] = params.b_89;
  params.b[90] = params.b_90;
  params.b[91] = params.b_91;
  params.b[92] = params.b_92;
  params.b[93] = params.b_93;
  params.b[94] = params.b_94;
  params.b[95] = params.b_95;
  params.b[96] = params.b_96;
  params.b[97] = params.b_97;
  params.b[98] = params.b_98;
  params.b[99] = params.b_99;
  params.b[100] = params.b_100;
  params.dist[1] = params.dist_1;
  params.dist[2] = params.dist_2;
  params.dist[3] = params.dist_3;
  params.dist[4] = params.dist_4;
  params.dist[5] = params.dist_5;
  params.dist[6] = params.dist_6;
  params.dist[7] = params.dist_7;
  params.dist[8] = params.dist_8;
  params.dist[9] = params.dist_9;
  params.dist[10] = params.dist_10;
  params.dist[11] = params.dist_11;
  params.dist[12] = params.dist_12;
  params.dist[13] = params.dist_13;
  params.dist[14] = params.dist_14;
  params.dist[15] = params.dist_15;
  params.dist[16] = params.dist_16;
  params.dist[17] = params.dist_17;
  params.dist[18] = params.dist_18;
  params.dist[19] = params.dist_19;
  params.dist[20] = params.dist_20;
  params.dist[21] = params.dist_21;
  params.dist[22] = params.dist_22;
  params.dist[23] = params.dist_23;
  params.dist[24] = params.dist_24;
  params.dist[25] = params.dist_25;
  params.dist[26] = params.dist_26;
  params.dist[27] = params.dist_27;
  params.dist[28] = params.dist_28;
  params.dist[29] = params.dist_29;
  params.dist[30] = params.dist_30;
  params.dist[31] = params.dist_31;
  params.dist[32] = params.dist_32;
  params.dist[33] = params.dist_33;
  params.dist[34] = params.dist_34;
  params.dist[35] = params.dist_35;
  params.dist[36] = params.dist_36;
  params.dist[37] = params.dist_37;
  params.dist[38] = params.dist_38;
  params.dist[39] = params.dist_39;
  params.dist[40] = params.dist_40;
  params.dist[41] = params.dist_41;
  params.dist[42] = params.dist_42;
  params.dist[43] = params.dist_43;
  params.dist[44] = params.dist_44;
  params.dist[45] = params.dist_45;
  params.dist[46] = params.dist_46;
  params.dist[47] = params.dist_47;
  params.dist[48] = params.dist_48;
  params.dist[49] = params.dist_49;
  params.dist[50] = params.dist_50;
  params.dist[51] = params.dist_51;
  params.dist[52] = params.dist_52;
  params.dist[53] = params.dist_53;
  params.dist[54] = params.dist_54;
  params.dist[55] = params.dist_55;
  params.dist[56] = params.dist_56;
  params.dist[57] = params.dist_57;
  params.dist[58] = params.dist_58;
  params.dist[59] = params.dist_59;
  params.dist[60] = params.dist_60;
  params.dist[61] = params.dist_61;
  params.dist[62] = params.dist_62;
  params.dist[63] = params.dist_63;
  params.dist[64] = params.dist_64;
  params.dist[65] = params.dist_65;
  params.dist[66] = params.dist_66;
  params.dist[67] = params.dist_67;
  params.dist[68] = params.dist_68;
  params.dist[69] = params.dist_69;
  params.dist[70] = params.dist_70;
  params.dist[71] = params.dist_71;
  params.dist[72] = params.dist_72;
  params.dist[73] = params.dist_73;
  params.dist[74] = params.dist_74;
  params.dist[75] = params.dist_75;
  params.dist[76] = params.dist_76;
  params.dist[77] = params.dist_77;
  params.dist[78] = params.dist_78;
  params.dist[79] = params.dist_79;
  params.dist[80] = params.dist_80;
  params.dist[81] = params.dist_81;
  params.dist[82] = params.dist_82;
  params.dist[83] = params.dist_83;
  params.dist[84] = params.dist_84;
  params.dist[85] = params.dist_85;
  params.dist[86] = params.dist_86;
  params.dist[87] = params.dist_87;
  params.dist[88] = params.dist_88;
  params.dist[89] = params.dist_89;
  params.dist[90] = params.dist_90;
  params.dist[91] = params.dist_91;
  params.dist[92] = params.dist_92;
  params.dist[93] = params.dist_93;
  params.dist[94] = params.dist_94;
  params.dist[95] = params.dist_95;
  params.dist[96] = params.dist_96;
  params.dist[97] = params.dist_97;
  params.dist[98] = params.dist_98;
  params.dist[99] = params.dist_99;
  params.dist[100] = params.dist_100;
}
void setup_indexed_optvars(void) {
  /* In CVXGEN, you can say */
  /*   variables */
  /*     x[i] (5), i=2..4 */
  /*   end */
  /* This function sets up x[3] to be a pointer to x_3, which is a length-5 */
  /* vector of doubles. */
  /* If you access variables that you haven't defined in CVXGEN, the result */
  /* is undefined. */
  vars.u[0] = vars.u_0;
  vars.x[1] = vars.x_1;
  vars.u[1] = vars.u_1;
  vars.x[2] = vars.x_2;
  vars.u[2] = vars.u_2;
  vars.x[3] = vars.x_3;
  vars.u[3] = vars.u_3;
  vars.x[4] = vars.x_4;
  vars.u[4] = vars.u_4;
  vars.x[5] = vars.x_5;
  vars.u[5] = vars.u_5;
  vars.x[6] = vars.x_6;
  vars.u[6] = vars.u_6;
  vars.x[7] = vars.x_7;
  vars.u[7] = vars.u_7;
  vars.x[8] = vars.x_8;
  vars.u[8] = vars.u_8;
  vars.x[9] = vars.x_9;
  vars.u[9] = vars.u_9;
  vars.x[10] = vars.x_10;
  vars.u[10] = vars.u_10;
  vars.x[11] = vars.x_11;
  vars.u[11] = vars.u_11;
  vars.x[12] = vars.x_12;
  vars.u[12] = vars.u_12;
  vars.x[13] = vars.x_13;
  vars.u[13] = vars.u_13;
  vars.x[14] = vars.x_14;
  vars.u[14] = vars.u_14;
  vars.x[15] = vars.x_15;
  vars.u[15] = vars.u_15;
  vars.x[16] = vars.x_16;
  vars.u[16] = vars.u_16;
  vars.x[17] = vars.x_17;
  vars.u[17] = vars.u_17;
  vars.x[18] = vars.x_18;
  vars.u[18] = vars.u_18;
  vars.x[19] = vars.x_19;
  vars.u[19] = vars.u_19;
  vars.x[20] = vars.x_20;
  vars.u[20] = vars.u_20;
  vars.x[21] = vars.x_21;
  vars.u[21] = vars.u_21;
  vars.x[22] = vars.x_22;
  vars.u[22] = vars.u_22;
  vars.x[23] = vars.x_23;
  vars.u[23] = vars.u_23;
  vars.x[24] = vars.x_24;
  vars.u[24] = vars.u_24;
  vars.x[25] = vars.x_25;
  vars.u[25] = vars.u_25;
  vars.x[26] = vars.x_26;
  vars.u[26] = vars.u_26;
  vars.x[27] = vars.x_27;
  vars.u[27] = vars.u_27;
  vars.x[28] = vars.x_28;
  vars.u[28] = vars.u_28;
  vars.x[29] = vars.x_29;
  vars.u[29] = vars.u_29;
  vars.x[30] = vars.x_30;
  vars.u[30] = vars.u_30;
  vars.x[31] = vars.x_31;
  vars.u[31] = vars.u_31;
  vars.x[32] = vars.x_32;
  vars.u[32] = vars.u_32;
  vars.x[33] = vars.x_33;
  vars.u[33] = vars.u_33;
  vars.x[34] = vars.x_34;
  vars.u[34] = vars.u_34;
  vars.x[35] = vars.x_35;
  vars.u[35] = vars.u_35;
  vars.x[36] = vars.x_36;
  vars.u[36] = vars.u_36;
  vars.x[37] = vars.x_37;
  vars.u[37] = vars.u_37;
  vars.x[38] = vars.x_38;
  vars.u[38] = vars.u_38;
  vars.x[39] = vars.x_39;
  vars.u[39] = vars.u_39;
  vars.x[40] = vars.x_40;
  vars.u[40] = vars.u_40;
  vars.x[41] = vars.x_41;
  vars.u[41] = vars.u_41;
  vars.x[42] = vars.x_42;
  vars.u[42] = vars.u_42;
  vars.x[43] = vars.x_43;
  vars.u[43] = vars.u_43;
  vars.x[44] = vars.x_44;
  vars.u[44] = vars.u_44;
  vars.x[45] = vars.x_45;
  vars.u[45] = vars.u_45;
  vars.x[46] = vars.x_46;
  vars.u[46] = vars.u_46;
  vars.x[47] = vars.x_47;
  vars.u[47] = vars.u_47;
  vars.x[48] = vars.x_48;
  vars.u[48] = vars.u_48;
  vars.x[49] = vars.x_49;
  vars.u[49] = vars.u_49;
  vars.x[50] = vars.x_50;
  vars.u[50] = vars.u_50;
  vars.x[51] = vars.x_51;
  vars.u[51] = vars.u_51;
  vars.x[52] = vars.x_52;
  vars.u[52] = vars.u_52;
  vars.x[53] = vars.x_53;
  vars.u[53] = vars.u_53;
  vars.x[54] = vars.x_54;
  vars.u[54] = vars.u_54;
  vars.x[55] = vars.x_55;
  vars.u[55] = vars.u_55;
  vars.x[56] = vars.x_56;
  vars.u[56] = vars.u_56;
  vars.x[57] = vars.x_57;
  vars.u[57] = vars.u_57;
  vars.x[58] = vars.x_58;
  vars.u[58] = vars.u_58;
  vars.x[59] = vars.x_59;
  vars.u[59] = vars.u_59;
  vars.x[60] = vars.x_60;
  vars.u[60] = vars.u_60;
  vars.x[61] = vars.x_61;
  vars.u[61] = vars.u_61;
  vars.x[62] = vars.x_62;
  vars.u[62] = vars.u_62;
  vars.x[63] = vars.x_63;
  vars.u[63] = vars.u_63;
  vars.x[64] = vars.x_64;
  vars.u[64] = vars.u_64;
  vars.x[65] = vars.x_65;
  vars.u[65] = vars.u_65;
  vars.x[66] = vars.x_66;
  vars.u[66] = vars.u_66;
  vars.x[67] = vars.x_67;
  vars.u[67] = vars.u_67;
  vars.x[68] = vars.x_68;
  vars.u[68] = vars.u_68;
  vars.x[69] = vars.x_69;
  vars.u[69] = vars.u_69;
  vars.x[70] = vars.x_70;
  vars.u[70] = vars.u_70;
  vars.x[71] = vars.x_71;
  vars.u[71] = vars.u_71;
  vars.x[72] = vars.x_72;
  vars.u[72] = vars.u_72;
  vars.x[73] = vars.x_73;
  vars.u[73] = vars.u_73;
  vars.x[74] = vars.x_74;
  vars.u[74] = vars.u_74;
  vars.x[75] = vars.x_75;
  vars.u[75] = vars.u_75;
  vars.x[76] = vars.x_76;
  vars.u[76] = vars.u_76;
  vars.x[77] = vars.x_77;
  vars.u[77] = vars.u_77;
  vars.x[78] = vars.x_78;
  vars.u[78] = vars.u_78;
  vars.x[79] = vars.x_79;
  vars.u[79] = vars.u_79;
  vars.x[80] = vars.x_80;
  vars.u[80] = vars.u_80;
  vars.x[81] = vars.x_81;
  vars.u[81] = vars.u_81;
  vars.x[82] = vars.x_82;
  vars.u[82] = vars.u_82;
  vars.x[83] = vars.x_83;
  vars.u[83] = vars.u_83;
  vars.x[84] = vars.x_84;
  vars.u[84] = vars.u_84;
  vars.x[85] = vars.x_85;
  vars.u[85] = vars.u_85;
  vars.x[86] = vars.x_86;
  vars.u[86] = vars.u_86;
  vars.x[87] = vars.x_87;
  vars.u[87] = vars.u_87;
  vars.x[88] = vars.x_88;
  vars.u[88] = vars.u_88;
  vars.x[89] = vars.x_89;
  vars.u[89] = vars.u_89;
  vars.x[90] = vars.x_90;
  vars.u[90] = vars.u_90;
  vars.x[91] = vars.x_91;
  vars.u[91] = vars.u_91;
  vars.x[92] = vars.x_92;
  vars.u[92] = vars.u_92;
  vars.x[93] = vars.x_93;
  vars.u[93] = vars.u_93;
  vars.x[94] = vars.x_94;
  vars.u[94] = vars.u_94;
  vars.x[95] = vars.x_95;
  vars.u[95] = vars.u_95;
  vars.x[96] = vars.x_96;
  vars.u[96] = vars.u_96;
  vars.x[97] = vars.x_97;
  vars.u[97] = vars.u_97;
  vars.x[98] = vars.x_98;
  vars.u[98] = vars.u_98;
  vars.x[99] = vars.x_99;
  vars.u[99] = vars.u_99;
  vars.x[100] = vars.x_100;
}
void setup_indexing(void) {
  setup_pointers();
  setup_indexed_params();
  setup_indexed_optvars();
}
void set_start(void) {
  int i;
  for (i = 0; i < 300; i++)
    work.x[i] = 0;
  for (i = 0; i < 200; i++)
    work.y[i] = 0;
  for (i = 0; i < 600; i++)
    work.s[i] = (work.h[i] > 0) ? work.h[i] : settings.s_init;
  for (i = 0; i < 600; i++)
    work.z[i] = settings.z_init;
}
double eval_objv(void) {
  int i;
  double objv;
  /* Borrow space in work.rhs. */
  multbyP(work.rhs, work.x);
  objv = 0;
  for (i = 0; i < 300; i++)
    objv += work.x[i]*work.rhs[i];
  objv *= 0.5;
  for (i = 0; i < 300; i++)
    objv += work.q[i]*work.x[i];
  objv += work.quad_783933743104[0]+work.quad_339902681088[0]+work.quad_135673548800[0]+work.quad_945197019136[0]+work.quad_21094948864[0]+work.quad_390374883328[0]+work.quad_311039037440[0]+work.quad_722651664384[0]+work.quad_73848643584[0]+work.quad_715760762880[0]+work.quad_619396980736[0]+work.quad_449708576768[0]+work.quad_644345716736[0]+work.quad_540410519552[0]+work.quad_271462109184[0]+work.quad_337763737600[0]+work.quad_454123520[0]+work.quad_15178178560[0]+work.quad_912311828480[0]+work.quad_525854347264[0]+work.quad_811378728960[0]+work.quad_956960821248[0]+work.quad_858261053440[0]+work.quad_79292780544[0]+work.quad_894503522304[0]+work.quad_529861754880[0]+work.quad_188954988544[0]+work.quad_479319134208[0]+work.quad_438557184000[0]+work.quad_276701544448[0]+work.quad_957826908160[0]+work.quad_787955007488[0]+work.quad_229586399232[0]+work.quad_298037764096[0]+work.quad_336626724864[0]+work.quad_862155403264[0]+work.quad_172180238336[0]+work.quad_41109282816[0]+work.quad_408821272576[0]+work.quad_531479920640[0]+work.quad_66459115520[0]+work.quad_426683604992[0]+work.quad_362338459648[0]+work.quad_315426017280[0]+work.quad_682029228032[0]+work.quad_387352723456[0]+work.quad_182158622720[0]+work.quad_56488431616[0]+work.quad_756622581760[0]+work.quad_728018997248[0]+work.quad_616301277184[0]+work.quad_632025530368[0]+work.quad_668853317632[0]+work.quad_286410539008[0]+work.quad_108500058112[0]+work.quad_120311644160[0]+work.quad_783421177856[0]+work.quad_205489786880[0]+work.quad_119575924736[0]+work.quad_660066217984[0]+work.quad_338899619840[0]+work.quad_116745433088[0]+work.quad_398729715712[0]+work.quad_30011367424[0]+work.quad_820310663168[0]+work.quad_237639622656[0]+work.quad_436907212800[0]+work.quad_561861996544[0]+work.quad_864719745024[0]+work.quad_80000786432[0]+work.quad_137359151104[0]+work.quad_496874647552[0]+work.quad_457243086848[0]+work.quad_646019588096[0]+work.quad_699077853184[0]+work.quad_133305888768[0]+work.quad_389579476992[0]+work.quad_679202607104[0]+work.quad_814084317184[0]+work.quad_685652762624[0]+work.quad_482903588864[0]+work.quad_918029041664[0]+work.quad_895295102976[0]+work.quad_268949368832[0]+work.quad_640282755072[0]+work.quad_600831926272[0]+work.quad_677249937408[0]+work.quad_942395060224[0]+work.quad_500862464000[0]+work.quad_100016951296[0]+work.quad_156372979712[0]+work.quad_715727052800[0]+work.quad_167550902272[0]+work.quad_700380606464[0]+work.quad_968886419456[0]+work.quad_425464229888[0]+work.quad_18233458688[0]+work.quad_590495412224[0]+work.quad_23338029056[0]+work.quad_611537010688[0]+work.quad_440025944064[0];
  return objv;
}
void fillrhs_aff(void) {
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 300;
  r3 = work.rhs + 900;
  r4 = work.rhs + 1500;
  /* r1 = -A^Ty - G^Tz - Px - q. */
  multbymAT(r1, work.y);
  multbymGT(work.buffer, work.z);
  for (i = 0; i < 300; i++)
    r1[i] += work.buffer[i];
  multbyP(work.buffer, work.x);
  for (i = 0; i < 300; i++)
    r1[i] -= work.buffer[i] + work.q[i];
  /* r2 = -z. */
  for (i = 0; i < 600; i++)
    r2[i] = -work.z[i];
  /* r3 = -Gx - s + h. */
  multbymG(r3, work.x);
  for (i = 0; i < 600; i++)
    r3[i] += -work.s[i] + work.h[i];
  /* r4 = -Ax + b. */
  multbymA(r4, work.x);
  for (i = 0; i < 200; i++)
    r4[i] += work.b[i];
}
void fillrhs_cc(void) {
  int i;
  double *r2;
  double *ds_aff, *dz_aff;
  double mu;
  double alpha;
  double sigma;
  double smu;
  double minval;
  r2 = work.rhs + 300;
  ds_aff = work.lhs_aff + 300;
  dz_aff = work.lhs_aff + 900;
  mu = 0;
  for (i = 0; i < 600; i++)
    mu += work.s[i]*work.z[i];
  /* Don't finish calculating mu quite yet. */
  /* Find min(min(ds./s), min(dz./z)). */
  minval = 0;
  for (i = 0; i < 600; i++)
    if (ds_aff[i] < minval*work.s[i])
      minval = ds_aff[i]/work.s[i];
  for (i = 0; i < 600; i++)
    if (dz_aff[i] < minval*work.z[i])
      minval = dz_aff[i]/work.z[i];
  /* Find alpha. */
  if (-1 < minval)
      alpha = 1;
  else
      alpha = -1/minval;
  sigma = 0;
  for (i = 0; i < 600; i++)
    sigma += (work.s[i] + alpha*ds_aff[i])*
      (work.z[i] + alpha*dz_aff[i]);
  sigma /= mu;
  sigma = sigma*sigma*sigma;
  /* Finish calculating mu now. */
  mu *= 0.0016666666666666668;
  smu = sigma*mu;
  /* Fill-in the rhs. */
  for (i = 0; i < 300; i++)
    work.rhs[i] = 0;
  for (i = 900; i < 1700; i++)
    work.rhs[i] = 0;
  for (i = 0; i < 600; i++)
    r2[i] = work.s_inv[i]*(smu - ds_aff[i]*dz_aff[i]);
}
void refine(double *target, double *var) {
  int i, j;
  double *residual = work.buffer;
  double norm2;
  double *new_var = work.buffer2;
  for (j = 0; j < settings.refine_steps; j++) {
    norm2 = 0;
    matrix_multiply(residual, var);
    for (i = 0; i < 1700; i++) {
      residual[i] = residual[i] - target[i];
      norm2 += residual[i]*residual[i];
    }
#ifndef ZERO_LIBRARY_MODE
    if (settings.verbose_refinement) {
      if (j == 0)
        printf("Initial residual before refinement has norm squared %.6g.\n", norm2);
      else
        printf("After refinement we get squared norm %.6g.\n", norm2);
    }
#endif
    /* Solve to find new_var = KKT \ (target - A*var). */
    ldl_solve(residual, new_var);
    /* Update var += new_var, or var += KKT \ (target - A*var). */
    for (i = 0; i < 1700; i++) {
      var[i] -= new_var[i];
    }
  }
#ifndef ZERO_LIBRARY_MODE
  if (settings.verbose_refinement) {
    /* Check the residual once more, but only if we're reporting it, since */
    /* it's expensive. */
    norm2 = 0;
    matrix_multiply(residual, var);
    for (i = 0; i < 1700; i++) {
      residual[i] = residual[i] - target[i];
      norm2 += residual[i]*residual[i];
    }
    if (j == 0)
      printf("Initial residual before refinement has norm squared %.6g.\n", norm2);
    else
      printf("After refinement we get squared norm %.6g.\n", norm2);
  }
#endif
}
double calc_ineq_resid_squared(void) {
  /* Calculates the norm ||-Gx - s + h||. */
  double norm2_squared;
  int i;
  /* Find -Gx. */
  multbymG(work.buffer, work.x);
  /* Add -s + h. */
  for (i = 0; i < 600; i++)
    work.buffer[i] += -work.s[i] + work.h[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 600; i++)
    norm2_squared += work.buffer[i]*work.buffer[i];
  return norm2_squared;
}
double calc_eq_resid_squared(void) {
  /* Calculates the norm ||-Ax + b||. */
  double norm2_squared;
  int i;
  /* Find -Ax. */
  multbymA(work.buffer, work.x);
  /* Add +b. */
  for (i = 0; i < 200; i++)
    work.buffer[i] += work.b[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 200; i++)
    norm2_squared += work.buffer[i]*work.buffer[i];
  return norm2_squared;
}
void better_start(void) {
  /* Calculates a better starting point, using a similar approach to CVXOPT. */
  /* Not yet speed optimized. */
  int i;
  double *x, *s, *z, *y;
  double alpha;
  work.block_33[0] = -1;
  /* Make sure sinvz is 1 to make hijacked KKT system ok. */
  for (i = 0; i < 600; i++)
    work.s_inv_z[i] = 1;
  fill_KKT();
  ldl_factor();
  fillrhs_start();
  /* Borrow work.lhs_aff for the solution. */
  ldl_solve(work.rhs, work.lhs_aff);
  /* Don't do any refinement for now. Precision doesn't matter too much. */
  x = work.lhs_aff;
  s = work.lhs_aff + 300;
  z = work.lhs_aff + 900;
  y = work.lhs_aff + 1500;
  /* Just set x and y as is. */
  for (i = 0; i < 300; i++)
    work.x[i] = x[i];
  for (i = 0; i < 200; i++)
    work.y[i] = y[i];
  /* Now complete the initialization. Start with s. */
  /* Must have alpha > max(z). */
  alpha = -1e99;
  for (i = 0; i < 600; i++)
    if (alpha < z[i])
      alpha = z[i];
  if (alpha < 0) {
    for (i = 0; i < 600; i++)
      work.s[i] = -z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 600; i++)
      work.s[i] = -z[i] + alpha;
  }
  /* Now initialize z. */
  /* Now must have alpha > max(-z). */
  alpha = -1e99;
  for (i = 0; i < 600; i++)
    if (alpha < -z[i])
      alpha = -z[i];
  if (alpha < 0) {
    for (i = 0; i < 600; i++)
      work.z[i] = z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 600; i++)
      work.z[i] = z[i] + alpha;
  }
}
void fillrhs_start(void) {
  /* Fill rhs with (-q, 0, h, b). */
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 300;
  r3 = work.rhs + 900;
  r4 = work.rhs + 1500;
  for (i = 0; i < 300; i++)
    r1[i] = -work.q[i];
  for (i = 0; i < 600; i++)
    r2[i] = 0;
  for (i = 0; i < 600; i++)
    r3[i] = work.h[i];
  for (i = 0; i < 200; i++)
    r4[i] = work.b[i];
}
long solve(void) {
  int i;
  int iter;
  double *dx, *ds, *dy, *dz;
  double minval;
  double alpha;
  work.converged = 0;
  setup_pointers();
  pre_ops();
#ifndef ZERO_LIBRARY_MODE
  if (settings.verbose)
    printf("iter     objv        gap       |Ax-b|    |Gx+s-h|    step\n");
#endif
  fillq();
  fillh();
  fillb();
  if (settings.better_start)
    better_start();
  else
    set_start();
  for (iter = 0; iter < settings.max_iters; iter++) {
    for (i = 0; i < 600; i++) {
      work.s_inv[i] = 1.0 / work.s[i];
      work.s_inv_z[i] = work.s_inv[i]*work.z[i];
    }
    work.block_33[0] = 0;
    fill_KKT();
    ldl_factor();
    /* Affine scaling directions. */
    fillrhs_aff();
    ldl_solve(work.rhs, work.lhs_aff);
    refine(work.rhs, work.lhs_aff);
    /* Centering plus corrector directions. */
    fillrhs_cc();
    ldl_solve(work.rhs, work.lhs_cc);
    refine(work.rhs, work.lhs_cc);
    /* Add the two together and store in aff. */
    for (i = 0; i < 1700; i++)
      work.lhs_aff[i] += work.lhs_cc[i];
    /* Rename aff to reflect its new meaning. */
    dx = work.lhs_aff;
    ds = work.lhs_aff + 300;
    dz = work.lhs_aff + 900;
    dy = work.lhs_aff + 1500;
    /* Find min(min(ds./s), min(dz./z)). */
    minval = 0;
    for (i = 0; i < 600; i++)
      if (ds[i] < minval*work.s[i])
        minval = ds[i]/work.s[i];
    for (i = 0; i < 600; i++)
      if (dz[i] < minval*work.z[i])
        minval = dz[i]/work.z[i];
    /* Find alpha. */
    if (-0.99 < minval)
      alpha = 1;
    else
      alpha = -0.99/minval;
    /* Update the primal and dual variables. */
    for (i = 0; i < 300; i++)
      work.x[i] += alpha*dx[i];
    for (i = 0; i < 600; i++)
      work.s[i] += alpha*ds[i];
    for (i = 0; i < 600; i++)
      work.z[i] += alpha*dz[i];
    for (i = 0; i < 200; i++)
      work.y[i] += alpha*dy[i];
    work.gap = eval_gap();
    work.eq_resid_squared = calc_eq_resid_squared();
    work.ineq_resid_squared = calc_ineq_resid_squared();
#ifndef ZERO_LIBRARY_MODE
    if (settings.verbose) {
      work.optval = eval_objv();
      printf("%3d   %10.3e  %9.2e  %9.2e  %9.2e  % 6.4f\n",
          iter+1, work.optval, work.gap, sqrt(work.eq_resid_squared),
          sqrt(work.ineq_resid_squared), alpha);
    }
#endif
    /* Test termination conditions. Requires optimality, and satisfied */
    /* constraints. */
    if (   (work.gap < settings.eps)
        && (work.eq_resid_squared <= settings.resid_tol*settings.resid_tol)
        && (work.ineq_resid_squared <= settings.resid_tol*settings.resid_tol)
       ) {
      work.converged = 1;
      work.optval = eval_objv();
      return iter+1;
    }
  }
  return iter;
}
