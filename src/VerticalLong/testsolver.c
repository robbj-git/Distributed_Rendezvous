/* Produced by CVXGEN, 2019-04-24 11:04:24 -0400.  */
/* CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com. */
/* The code in this file is Copyright (C) 2006-2017 Jacob Mattingley. */
/* CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial */
/* applications without prior written permission from Jacob Mattingley. */

/* Filename: testsolver.c. */
/* Description: Basic test harness for solver.c. */
#include "solver.h"
Vars vars;
Params params;
Workspace work;
Settings settings;
#define NUMTESTS 0
int main(int argc, char **argv) {
  int num_iters;
#if (NUMTESTS > 0)
  int i;
  double time;
  double time_per;
#endif
  set_defaults();
  setup_indexing();
  load_default_data();
  /* Solve problem instance for the record. */
  settings.verbose = 1;
  num_iters = solve();
#ifndef ZERO_LIBRARY_MODE
#if (NUMTESTS > 0)
  /* Now solve multiple problem instances for timing purposes. */
  settings.verbose = 0;
  tic();
  for (i = 0; i < NUMTESTS; i++) {
    solve();
  }
  time = tocq();
  printf("Timed %d solves over %.3f seconds.\n", NUMTESTS, time);
  time_per = time / NUMTESTS;
  if (time_per > 1) {
    printf("Actual time taken per solve: %.3g s.\n", time_per);
  } else if (time_per > 1e-3) {
    printf("Actual time taken per solve: %.3g ms.\n", 1e3*time_per);
  } else {
    printf("Actual time taken per solve: %.3g us.\n", 1e6*time_per);
  }
#endif
#endif
  return 0;
}
void load_default_data(void) {
  params.b_0[0] = 0.20319161029830202;
  params.x_0[0] = 0.8325912904724193;
  params.x_0[1] = -0.8363810443482227;
  params.xb[0] = 0.04331042079065206;
  params.xb[1] = 1.5717878173906188;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.Q[0] = 1.896293088933438;
  params.Q[2] = 0;
  params.Q[1] = 0;
  params.Q[3] = 1.1255853104638363;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.R[0] = 1.2072428781381868;
  params.b_1[0] = -1.7941311867966805;
  params.b_2[0] = -0.23676062539745413;
  params.b_3[0] = -1.8804951564857322;
  params.b_4[0] = -0.17266710242115568;
  params.b_5[0] = 0.596576190459043;
  params.b_6[0] = -0.8860508694080989;
  params.b_7[0] = 0.7050196079205251;
  params.b_8[0] = 0.3634512696654033;
  params.b_9[0] = -1.9040724704913385;
  params.b_10[0] = 0.23541635196352795;
  params.b_11[0] = -0.9629902123701384;
  params.b_12[0] = -0.3395952119597214;
  params.b_13[0] = -0.865899672914725;
  params.b_14[0] = 0.7725516732519853;
  params.b_15[0] = -0.23818512931704205;
  params.b_16[0] = -1.372529046100147;
  params.b_17[0] = 0.17859607212737894;
  params.b_18[0] = 1.1212590580454682;
  params.b_19[0] = -0.774545870495281;
  params.b_20[0] = -1.1121684642712744;
  params.b_21[0] = -0.44811496977740495;
  params.b_22[0] = 1.7455345994417217;
  params.b_23[0] = 1.9039816898917352;
  params.b_24[0] = 0.6895347036512547;
  params.b_25[0] = 1.6113364341535923;
  params.b_26[0] = 1.383003485172717;
  params.b_27[0] = -0.48802383468444344;
  params.b_28[0] = -1.631131964513103;
  params.b_29[0] = 0.6136436100941447;
  params.b_30[0] = 0.2313630495538037;
  params.b_31[0] = -0.5537409477496875;
  params.b_32[0] = -1.0997819806406723;
  params.b_33[0] = -0.3739203344950055;
  params.b_34[0] = -0.12423900520332376;
  params.b_35[0] = -0.923057686995755;
  params.b_36[0] = -0.8328289030982696;
  params.b_37[0] = -0.16925440270808823;
  params.b_38[0] = 1.442135651787706;
  params.b_39[0] = 0.34501161787128565;
  params.b_40[0] = -0.8660485502711608;
  params.b_41[0] = -0.8880899735055947;
  params.b_42[0] = -0.1815116979122129;
  params.b_43[0] = -1.17835862158005;
  params.b_44[0] = -1.1944851558277074;
  params.b_45[0] = 0.05614023926976763;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.P[0] = 1.0872293687808048;
  params.P[2] = 0;
  params.P[1] = 0;
  params.P[3] = 1.4835855323515865;
  params.A[0] = -0.5512951504486665;
  params.A[1] = 0.8307464872626844;
  params.A[2] = 0.9869848924080182;
  params.A[3] = 0.7643716874230573;
  params.B[0] = 0.7567216550196565;
  params.B[1] = -0.5055995034042868;
  params.wmin[0] = -1.336269609470535;
  params.wmax[0] = 0.6796973279136358;
  params.kl[0] = 1.14558773973775;
  params.wmin_land[0] = -0.651614316129749;
  params.hs[0] = -0.21941980294587182;
  params.dist_1[0] = -1.753884276680243;
  params.dl[0] = -1.0292983112626475;
  params.ds[0] = 1.8864104246942706;
  params.dist_2[0] = -1.077663182579704;
  params.dist_3[0] = 0.7659100437893209;
  params.dist_4[0] = 0.6019074328549583;
  params.dist_5[0] = 0.8957565577499285;
  params.dist_6[0] = -0.09964555746227477;
  params.dist_7[0] = 0.38665509840745127;
  params.dist_8[0] = -1.7321223042686946;
  params.dist_9[0] = -1.7097514487110663;
  params.dist_10[0] = -1.2040958948116867;
  params.dist_11[0] = -1.3925560119658358;
  params.dist_12[0] = -1.5995826216742213;
  params.dist_13[0] = -1.4828245415645833;
  params.dist_14[0] = 0.21311092723061398;
  params.dist_15[0] = -1.248740700304487;
  params.dist_16[0] = 1.808404972124833;
  params.dist_17[0] = 0.7264471152297065;
  params.dist_18[0] = 0.16407869343908477;
  params.dist_19[0] = 0.8287224032315907;
  params.dist_20[0] = -0.9444533161899464;
  params.dist_21[0] = 1.7069027370149112;
  params.dist_22[0] = 1.3567722311998827;
  params.dist_23[0] = 0.9052779937121489;
  params.dist_24[0] = -0.07904017565835986;
  params.dist_25[0] = 1.3684127435065871;
  params.dist_26[0] = 0.979009293697437;
  params.dist_27[0] = 0.6413036255984501;
  params.dist_28[0] = 1.6559010680237511;
  params.dist_29[0] = 0.5346622551502991;
  params.dist_30[0] = -0.5362376605895625;
  params.dist_31[0] = 0.2113782926017822;
  params.dist_32[0] = -1.2144776931994525;
  params.dist_33[0] = -1.2317108144255875;
  params.dist_34[0] = 0.9026784957312834;
  params.dist_35[0] = 1.1397468137245244;
  params.dist_36[0] = 1.8883934547350631;
  params.dist_37[0] = 1.4038856681660068;
  params.dist_38[0] = 0.17437730638329096;
  params.dist_39[0] = -1.6408365219077408;
  params.dist_40[0] = -0.04450702153554875;
  params.dist_41[0] = 1.7117453902485025;
  params.dist_42[0] = 1.1504727980139053;
  params.dist_43[0] = -0.05962309578364744;
  params.dist_44[0] = -0.1788825540764547;
  params.dist_45[0] = -1.1280569263625857;
}
