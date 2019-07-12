/* Produced by CVXGEN, 2019-05-01 05:37:16 -0400.  */
/* CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com. */
/* The code in this file is Copyright (C) 2006-2017 Jacob Mattingley. */
/* CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial */
/* applications without prior written permission from Jacob Mattingley. */

/* Filename: solver.h. */
/* Description: Header file with relevant definitions. */
#ifndef SOLVER_H
#define SOLVER_H
/* Uncomment the next line to remove all library dependencies. */
/*#define ZERO_LIBRARY_MODE */
#ifdef MATLAB_MEX_FILE
/* Matlab functions. MATLAB_MEX_FILE will be defined by the mex compiler. */
/* If you are not using the mex compiler, this functionality will not intrude, */
/* as it will be completely disabled at compile-time. */
#include "mex.h"
#else
#ifndef ZERO_LIBRARY_MODE
#include <stdio.h>
#endif
#endif
/* Space must be allocated somewhere (testsolver.c, csolve.c or your own */
/* program) for the global variables vars, params, work and settings. */
/* At the bottom of this file, they are externed. */
#ifndef ZERO_LIBRARY_MODE
#include <math.h>
#define pm(A, m, n) printmatrix(#A, A, m, n, 1)
#endif
typedef struct Params_t {
  double b_0[1];
  double x_0[2];
  double xb[2];
  double Q[4];
  double R[1];
  double b_1[1];
  double b_2[1];
  double b_3[1];
  double b_4[1];
  double b_5[1];
  double b_6[1];
  double b_7[1];
  double b_8[1];
  double b_9[1];
  double b_10[1];
  double b_11[1];
  double b_12[1];
  double b_13[1];
  double b_14[1];
  double b_15[1];
  double b_16[1];
  double b_17[1];
  double b_18[1];
  double b_19[1];
  double b_20[1];
  double b_21[1];
  double b_22[1];
  double b_23[1];
  double b_24[1];
  double b_25[1];
  double b_26[1];
  double b_27[1];
  double b_28[1];
  double b_29[1];
  double b_30[1];
  double b_31[1];
  double b_32[1];
  double b_33[1];
  double b_34[1];
  double b_35[1];
  double b_36[1];
  double b_37[1];
  double b_38[1];
  double b_39[1];
  double b_40[1];
  double b_41[1];
  double b_42[1];
  double b_43[1];
  double b_44[1];
  double b_45[1];
  double b_46[1];
  double b_47[1];
  double b_48[1];
  double b_49[1];
  double b_50[1];
  double b_51[1];
  double b_52[1];
  double b_53[1];
  double b_54[1];
  double b_55[1];
  double b_56[1];
  double b_57[1];
  double b_58[1];
  double b_59[1];
  double b_60[1];
  double b_61[1];
  double b_62[1];
  double b_63[1];
  double b_64[1];
  double b_65[1];
  double b_66[1];
  double b_67[1];
  double b_68[1];
  double b_69[1];
  double b_70[1];
  double b_71[1];
  double b_72[1];
  double b_73[1];
  double b_74[1];
  double b_75[1];
  double b_76[1];
  double b_77[1];
  double b_78[1];
  double b_79[1];
  double b_80[1];
  double b_81[1];
  double b_82[1];
  double b_83[1];
  double b_84[1];
  double b_85[1];
  double b_86[1];
  double b_87[1];
  double b_88[1];
  double b_89[1];
  double b_90[1];
  double b_91[1];
  double b_92[1];
  double b_93[1];
  double b_94[1];
  double b_95[1];
  double b_96[1];
  double b_97[1];
  double b_98[1];
  double b_99[1];
  double b_100[1];
  double P[4];
  double A[4];
  double B[2];
  double wmin[1];
  double wmax[1];
  double kl[1];
  double wmin_land[1];
  double hs[1];
  double dist_1[1];
  double dl[1];
  double ds[1];
  double dist_2[1];
  double dist_3[1];
  double dist_4[1];
  double dist_5[1];
  double dist_6[1];
  double dist_7[1];
  double dist_8[1];
  double dist_9[1];
  double dist_10[1];
  double dist_11[1];
  double dist_12[1];
  double dist_13[1];
  double dist_14[1];
  double dist_15[1];
  double dist_16[1];
  double dist_17[1];
  double dist_18[1];
  double dist_19[1];
  double dist_20[1];
  double dist_21[1];
  double dist_22[1];
  double dist_23[1];
  double dist_24[1];
  double dist_25[1];
  double dist_26[1];
  double dist_27[1];
  double dist_28[1];
  double dist_29[1];
  double dist_30[1];
  double dist_31[1];
  double dist_32[1];
  double dist_33[1];
  double dist_34[1];
  double dist_35[1];
  double dist_36[1];
  double dist_37[1];
  double dist_38[1];
  double dist_39[1];
  double dist_40[1];
  double dist_41[1];
  double dist_42[1];
  double dist_43[1];
  double dist_44[1];
  double dist_45[1];
  double dist_46[1];
  double dist_47[1];
  double dist_48[1];
  double dist_49[1];
  double dist_50[1];
  double dist_51[1];
  double dist_52[1];
  double dist_53[1];
  double dist_54[1];
  double dist_55[1];
  double dist_56[1];
  double dist_57[1];
  double dist_58[1];
  double dist_59[1];
  double dist_60[1];
  double dist_61[1];
  double dist_62[1];
  double dist_63[1];
  double dist_64[1];
  double dist_65[1];
  double dist_66[1];
  double dist_67[1];
  double dist_68[1];
  double dist_69[1];
  double dist_70[1];
  double dist_71[1];
  double dist_72[1];
  double dist_73[1];
  double dist_74[1];
  double dist_75[1];
  double dist_76[1];
  double dist_77[1];
  double dist_78[1];
  double dist_79[1];
  double dist_80[1];
  double dist_81[1];
  double dist_82[1];
  double dist_83[1];
  double dist_84[1];
  double dist_85[1];
  double dist_86[1];
  double dist_87[1];
  double dist_88[1];
  double dist_89[1];
  double dist_90[1];
  double dist_91[1];
  double dist_92[1];
  double dist_93[1];
  double dist_94[1];
  double dist_95[1];
  double dist_96[1];
  double dist_97[1];
  double dist_98[1];
  double dist_99[1];
  double dist_100[1];
  double *b[101];
  double *x[1];
  double *dist[101];
} Params;
typedef struct Vars_t {
  double *u_0; /* 1 rows. */
  double *x_1; /* 2 rows. */
  double *u_1; /* 1 rows. */
  double *x_2; /* 2 rows. */
  double *u_2; /* 1 rows. */
  double *x_3; /* 2 rows. */
  double *u_3; /* 1 rows. */
  double *x_4; /* 2 rows. */
  double *u_4; /* 1 rows. */
  double *x_5; /* 2 rows. */
  double *u_5; /* 1 rows. */
  double *x_6; /* 2 rows. */
  double *u_6; /* 1 rows. */
  double *x_7; /* 2 rows. */
  double *u_7; /* 1 rows. */
  double *x_8; /* 2 rows. */
  double *u_8; /* 1 rows. */
  double *x_9; /* 2 rows. */
  double *u_9; /* 1 rows. */
  double *x_10; /* 2 rows. */
  double *u_10; /* 1 rows. */
  double *x_11; /* 2 rows. */
  double *u_11; /* 1 rows. */
  double *x_12; /* 2 rows. */
  double *u_12; /* 1 rows. */
  double *x_13; /* 2 rows. */
  double *u_13; /* 1 rows. */
  double *x_14; /* 2 rows. */
  double *u_14; /* 1 rows. */
  double *x_15; /* 2 rows. */
  double *u_15; /* 1 rows. */
  double *x_16; /* 2 rows. */
  double *u_16; /* 1 rows. */
  double *x_17; /* 2 rows. */
  double *u_17; /* 1 rows. */
  double *x_18; /* 2 rows. */
  double *u_18; /* 1 rows. */
  double *x_19; /* 2 rows. */
  double *u_19; /* 1 rows. */
  double *x_20; /* 2 rows. */
  double *u_20; /* 1 rows. */
  double *x_21; /* 2 rows. */
  double *u_21; /* 1 rows. */
  double *x_22; /* 2 rows. */
  double *u_22; /* 1 rows. */
  double *x_23; /* 2 rows. */
  double *u_23; /* 1 rows. */
  double *x_24; /* 2 rows. */
  double *u_24; /* 1 rows. */
  double *x_25; /* 2 rows. */
  double *u_25; /* 1 rows. */
  double *x_26; /* 2 rows. */
  double *u_26; /* 1 rows. */
  double *x_27; /* 2 rows. */
  double *u_27; /* 1 rows. */
  double *x_28; /* 2 rows. */
  double *u_28; /* 1 rows. */
  double *x_29; /* 2 rows. */
  double *u_29; /* 1 rows. */
  double *x_30; /* 2 rows. */
  double *u_30; /* 1 rows. */
  double *x_31; /* 2 rows. */
  double *u_31; /* 1 rows. */
  double *x_32; /* 2 rows. */
  double *u_32; /* 1 rows. */
  double *x_33; /* 2 rows. */
  double *u_33; /* 1 rows. */
  double *x_34; /* 2 rows. */
  double *u_34; /* 1 rows. */
  double *x_35; /* 2 rows. */
  double *u_35; /* 1 rows. */
  double *x_36; /* 2 rows. */
  double *u_36; /* 1 rows. */
  double *x_37; /* 2 rows. */
  double *u_37; /* 1 rows. */
  double *x_38; /* 2 rows. */
  double *u_38; /* 1 rows. */
  double *x_39; /* 2 rows. */
  double *u_39; /* 1 rows. */
  double *x_40; /* 2 rows. */
  double *u_40; /* 1 rows. */
  double *x_41; /* 2 rows. */
  double *u_41; /* 1 rows. */
  double *x_42; /* 2 rows. */
  double *u_42; /* 1 rows. */
  double *x_43; /* 2 rows. */
  double *u_43; /* 1 rows. */
  double *x_44; /* 2 rows. */
  double *u_44; /* 1 rows. */
  double *x_45; /* 2 rows. */
  double *u_45; /* 1 rows. */
  double *x_46; /* 2 rows. */
  double *u_46; /* 1 rows. */
  double *x_47; /* 2 rows. */
  double *u_47; /* 1 rows. */
  double *x_48; /* 2 rows. */
  double *u_48; /* 1 rows. */
  double *x_49; /* 2 rows. */
  double *u_49; /* 1 rows. */
  double *x_50; /* 2 rows. */
  double *u_50; /* 1 rows. */
  double *x_51; /* 2 rows. */
  double *u_51; /* 1 rows. */
  double *x_52; /* 2 rows. */
  double *u_52; /* 1 rows. */
  double *x_53; /* 2 rows. */
  double *u_53; /* 1 rows. */
  double *x_54; /* 2 rows. */
  double *u_54; /* 1 rows. */
  double *x_55; /* 2 rows. */
  double *u_55; /* 1 rows. */
  double *x_56; /* 2 rows. */
  double *u_56; /* 1 rows. */
  double *x_57; /* 2 rows. */
  double *u_57; /* 1 rows. */
  double *x_58; /* 2 rows. */
  double *u_58; /* 1 rows. */
  double *x_59; /* 2 rows. */
  double *u_59; /* 1 rows. */
  double *x_60; /* 2 rows. */
  double *u_60; /* 1 rows. */
  double *x_61; /* 2 rows. */
  double *u_61; /* 1 rows. */
  double *x_62; /* 2 rows. */
  double *u_62; /* 1 rows. */
  double *x_63; /* 2 rows. */
  double *u_63; /* 1 rows. */
  double *x_64; /* 2 rows. */
  double *u_64; /* 1 rows. */
  double *x_65; /* 2 rows. */
  double *u_65; /* 1 rows. */
  double *x_66; /* 2 rows. */
  double *u_66; /* 1 rows. */
  double *x_67; /* 2 rows. */
  double *u_67; /* 1 rows. */
  double *x_68; /* 2 rows. */
  double *u_68; /* 1 rows. */
  double *x_69; /* 2 rows. */
  double *u_69; /* 1 rows. */
  double *x_70; /* 2 rows. */
  double *u_70; /* 1 rows. */
  double *x_71; /* 2 rows. */
  double *u_71; /* 1 rows. */
  double *x_72; /* 2 rows. */
  double *u_72; /* 1 rows. */
  double *x_73; /* 2 rows. */
  double *u_73; /* 1 rows. */
  double *x_74; /* 2 rows. */
  double *u_74; /* 1 rows. */
  double *x_75; /* 2 rows. */
  double *u_75; /* 1 rows. */
  double *x_76; /* 2 rows. */
  double *u_76; /* 1 rows. */
  double *x_77; /* 2 rows. */
  double *u_77; /* 1 rows. */
  double *x_78; /* 2 rows. */
  double *u_78; /* 1 rows. */
  double *x_79; /* 2 rows. */
  double *u_79; /* 1 rows. */
  double *x_80; /* 2 rows. */
  double *u_80; /* 1 rows. */
  double *x_81; /* 2 rows. */
  double *u_81; /* 1 rows. */
  double *x_82; /* 2 rows. */
  double *u_82; /* 1 rows. */
  double *x_83; /* 2 rows. */
  double *u_83; /* 1 rows. */
  double *x_84; /* 2 rows. */
  double *u_84; /* 1 rows. */
  double *x_85; /* 2 rows. */
  double *u_85; /* 1 rows. */
  double *x_86; /* 2 rows. */
  double *u_86; /* 1 rows. */
  double *x_87; /* 2 rows. */
  double *u_87; /* 1 rows. */
  double *x_88; /* 2 rows. */
  double *u_88; /* 1 rows. */
  double *x_89; /* 2 rows. */
  double *u_89; /* 1 rows. */
  double *x_90; /* 2 rows. */
  double *u_90; /* 1 rows. */
  double *x_91; /* 2 rows. */
  double *u_91; /* 1 rows. */
  double *x_92; /* 2 rows. */
  double *u_92; /* 1 rows. */
  double *x_93; /* 2 rows. */
  double *u_93; /* 1 rows. */
  double *x_94; /* 2 rows. */
  double *u_94; /* 1 rows. */
  double *x_95; /* 2 rows. */
  double *u_95; /* 1 rows. */
  double *x_96; /* 2 rows. */
  double *u_96; /* 1 rows. */
  double *x_97; /* 2 rows. */
  double *u_97; /* 1 rows. */
  double *x_98; /* 2 rows. */
  double *u_98; /* 1 rows. */
  double *x_99; /* 2 rows. */
  double *u_99; /* 1 rows. */
  double *x_100; /* 2 rows. */
  double *u[100];
  double *x[101];
} Vars;
typedef struct Workspace_t {
  double h[600];
  double s_inv[600];
  double s_inv_z[600];
  double b[200];
  double q[300];
  double rhs[1700];
  double x[1700];
  double *s;
  double *z;
  double *y;
  double lhs_aff[1700];
  double lhs_cc[1700];
  double buffer[1700];
  double buffer2[1700];
  double KKT[3696];
  double L[2396];
  double d[1700];
  double v[1700];
  double d_inv[1700];
  double gap;
  double optval;
  double ineq_resid_squared;
  double eq_resid_squared;
  double block_33[1];
  /* Pre-op symbols. */
  double quad_105969278976[4];
  double quad_323753811968[4];
  double quad_589565669376[4];
  double quad_878883119104[4];
  double quad_857783992320[4];
  double quad_880434188288[4];
  double quad_443935657984[4];
  double quad_413064835072[4];
  double quad_245198159872[4];
  double quad_216144961536[4];
  double quad_680649846784[4];
  double quad_437552103424[4];
  double quad_474189975552[4];
  double quad_4479598592[4];
  double quad_787137105920[4];
  double quad_526954905600[4];
  double quad_421957689344[4];
  double quad_631429644288[4];
  double quad_326775631872[4];
  double quad_91388796928[4];
  double quad_720918614016[4];
  double quad_228065918976[4];
  double quad_889875378176[4];
  double quad_128757551104[4];
  double quad_722070175744[4];
  double quad_65594990592[4];
  double quad_559440896000[4];
  double quad_880027639808[4];
  double quad_453240496128[4];
  double quad_687758204928[4];
  double quad_125990965248[4];
  double quad_264811089920[4];
  double quad_308708171776[4];
  double quad_573982068736[4];
  double quad_149627252736[4];
  double quad_154236575744[4];
  double quad_801583075328[4];
  double quad_657845030912[4];
  double quad_793989152768[4];
  double quad_250156064768[4];
  double quad_354079199232[4];
  double quad_358644883456[4];
  double quad_909171941376[4];
  double quad_78250586112[4];
  double quad_480525533184[4];
  double quad_814615805952[4];
  double quad_632646815744[4];
  double quad_3864776704[4];
  double quad_856314527744[4];
  double quad_691637288960[4];
  double quad_703043239936[4];
  double quad_599048884224[4];
  double quad_970081660928[4];
  double quad_721607839744[4];
  double quad_116409208832[4];
  double quad_571050127360[4];
  double quad_344046690304[4];
  double quad_465215348736[4];
  double quad_576453443584[4];
  double quad_436902363136[4];
  double quad_260608118784[4];
  double quad_129330909184[4];
  double quad_793543446528[4];
  double quad_694856929280[4];
  double quad_982214918144[4];
  double quad_134539689984[4];
  double quad_921160790016[4];
  double quad_584299851776[4];
  double quad_886092640256[4];
  double quad_789727875072[4];
  double quad_866367492096[4];
  double quad_23343632384[4];
  double quad_44889354240[4];
  double quad_528997879808[4];
  double quad_383790637056[4];
  double quad_479090700288[4];
  double quad_18145030144[4];
  double quad_258776887296[4];
  double quad_859471396864[4];
  double quad_465660690432[4];
  double quad_395526656000[4];
  double quad_861294891008[4];
  double quad_292671873024[4];
  double quad_691324080128[4];
  double quad_52378902528[4];
  double quad_631377678336[4];
  double quad_448710660096[4];
  double quad_423265660928[4];
  double quad_653317255168[4];
  double quad_639355199488[4];
  double quad_944566530048[4];
  double quad_124408823808[4];
  double quad_630024617984[4];
  double quad_128677871616[4];
  double quad_948510851072[4];
  double quad_761940652032[4];
  double quad_617389780992[4];
  double quad_235159752704[4];
  double quad_445293805568[4];
  double quad_506154033152[4];
  double quad_783933743104[1];
  double quad_339902681088[1];
  double quad_135673548800[1];
  double quad_945197019136[1];
  double quad_21094948864[1];
  double quad_390374883328[1];
  double quad_311039037440[1];
  double quad_722651664384[1];
  double quad_73848643584[1];
  double quad_715760762880[1];
  double quad_619396980736[1];
  double quad_449708576768[1];
  double quad_644345716736[1];
  double quad_540410519552[1];
  double quad_271462109184[1];
  double quad_337763737600[1];
  double quad_454123520[1];
  double quad_15178178560[1];
  double quad_912311828480[1];
  double quad_525854347264[1];
  double quad_811378728960[1];
  double quad_956960821248[1];
  double quad_858261053440[1];
  double quad_79292780544[1];
  double quad_894503522304[1];
  double quad_529861754880[1];
  double quad_188954988544[1];
  double quad_479319134208[1];
  double quad_438557184000[1];
  double quad_276701544448[1];
  double quad_957826908160[1];
  double quad_787955007488[1];
  double quad_229586399232[1];
  double quad_298037764096[1];
  double quad_336626724864[1];
  double quad_862155403264[1];
  double quad_172180238336[1];
  double quad_41109282816[1];
  double quad_408821272576[1];
  double quad_531479920640[1];
  double quad_66459115520[1];
  double quad_426683604992[1];
  double quad_362338459648[1];
  double quad_315426017280[1];
  double quad_682029228032[1];
  double quad_387352723456[1];
  double quad_182158622720[1];
  double quad_56488431616[1];
  double quad_756622581760[1];
  double quad_728018997248[1];
  double quad_616301277184[1];
  double quad_632025530368[1];
  double quad_668853317632[1];
  double quad_286410539008[1];
  double quad_108500058112[1];
  double quad_120311644160[1];
  double quad_783421177856[1];
  double quad_205489786880[1];
  double quad_119575924736[1];
  double quad_660066217984[1];
  double quad_338899619840[1];
  double quad_116745433088[1];
  double quad_398729715712[1];
  double quad_30011367424[1];
  double quad_820310663168[1];
  double quad_237639622656[1];
  double quad_436907212800[1];
  double quad_561861996544[1];
  double quad_864719745024[1];
  double quad_80000786432[1];
  double quad_137359151104[1];
  double quad_496874647552[1];
  double quad_457243086848[1];
  double quad_646019588096[1];
  double quad_699077853184[1];
  double quad_133305888768[1];
  double quad_389579476992[1];
  double quad_679202607104[1];
  double quad_814084317184[1];
  double quad_685652762624[1];
  double quad_482903588864[1];
  double quad_918029041664[1];
  double quad_895295102976[1];
  double quad_268949368832[1];
  double quad_640282755072[1];
  double quad_600831926272[1];
  double quad_677249937408[1];
  double quad_942395060224[1];
  double quad_500862464000[1];
  double quad_100016951296[1];
  double quad_156372979712[1];
  double quad_715727052800[1];
  double quad_167550902272[1];
  double quad_700380606464[1];
  double quad_968886419456[1];
  double quad_425464229888[1];
  double quad_18233458688[1];
  double quad_590495412224[1];
  double quad_23338029056[1];
  double quad_611537010688[1];
  double quad_440025944064[1];
  int converged;
} Workspace;
typedef struct Settings_t {
  double resid_tol;
  double eps;
  int max_iters;
  int refine_steps;
  int better_start;
  /* Better start obviates the need for s_init and z_init. */
  double s_init;
  double z_init;
  int verbose;
  /* Show extra details of the iterative refinement steps. */
  int verbose_refinement;
  int debug;
  /* For regularization. Minimum value of abs(D_ii) in the kkt D factor. */
  double kkt_reg;
} Settings;
extern Vars vars;
extern Params params;
extern Workspace work;
extern Settings settings;
/* Function definitions in ldl.c: */
void ldl_solve(double *target, double *var);
void ldl_factor(void);
double check_factorization(void);
void matrix_multiply(double *result, double *source);
double check_residual(double *target, double *multiplicand);
void fill_KKT(void);

/* Function definitions in matrix_support.c: */
void multbymA(double *lhs, double *rhs);
void multbymAT(double *lhs, double *rhs);
void multbymG(double *lhs, double *rhs);
void multbymGT(double *lhs, double *rhs);
void multbyP(double *lhs, double *rhs);
void fillq(void);
void fillh(void);
void fillb(void);
void pre_ops(void);

/* Function definitions in solver.c: */
double eval_gap(void);
void set_defaults(void);
void setup_pointers(void);
void setup_indexed_params(void);
void setup_indexed_optvars(void);
void setup_indexing(void);
void set_start(void);
double eval_objv(void);
void fillrhs_aff(void);
void fillrhs_cc(void);
void refine(double *target, double *var);
double calc_ineq_resid_squared(void);
double calc_eq_resid_squared(void);
void better_start(void);
void fillrhs_start(void);
long solve(void);

/* Function definitions in testsolver.c: */
int main(int argc, char **argv);
void load_default_data(void);

/* Function definitions in util.c: */
void tic(void);
float toc(void);
float tocq(void);
void printmatrix(char *name, double *A, int m, int n, int sparse);
double unif(double lower, double upper);
float ran1(long*idum, int reset);
float randn_internal(long *idum, int reset);
double randn(void);
void reset_rand(void);

#endif
