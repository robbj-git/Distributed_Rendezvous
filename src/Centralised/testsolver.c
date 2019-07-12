/* Produced by CVXGEN, 2019-04-24 04:05:38 -0400.  */
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
  params.x_0[0] = 0.20319161029830202;
  params.x_0[1] = 0.8325912904724193;
  params.x_0[2] = -0.8363810443482227;
  params.x_0[3] = 0.04331042079065206;
  params.xb_0[0] = 1.5717878173906188;
  params.xb_0[1] = 1.5851723557337523;
  params.xb_0[2] = -1.497658758144655;
  params.xb_0[3] = -1.171028487447253;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.Q[0] = 1.0514672033008299;
  params.Q[4] = 0;
  params.Q[8] = 0;
  params.Q[12] = 0;
  params.Q[1] = 0;
  params.Q[5] = 1.4408098436506365;
  params.Q[9] = 0;
  params.Q[13] = 0;
  params.Q[2] = 0;
  params.Q[6] = 0;
  params.Q[10] = 1.0298762108785668;
  params.Q[14] = 0;
  params.Q[3] = 0;
  params.Q[7] = 0;
  params.Q[11] = 0;
  params.Q[15] = 1.456833224394711;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.R[0] = 1.6491440476147607;
  params.R[2] = 0;
  params.R[1] = 0;
  params.R[3] = 1.2784872826479754;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.P[0] = 1.6762549019801312;
  params.P[4] = 0;
  params.P[8] = 0;
  params.P[12] = 0;
  params.P[1] = 0;
  params.P[5] = 1.5908628174163508;
  params.P[9] = 0;
  params.P[13] = 0;
  params.P[2] = 0;
  params.P[6] = 0;
  params.P[10] = 1.0239818823771654;
  params.P[14] = 0;
  params.P[3] = 0;
  params.P[7] = 0;
  params.P[11] = 0;
  params.P[15] = 1.5588540879908819;
  params.A[0] = -0.9629902123701384;
  params.A[1] = -0.3395952119597214;
  params.A[2] = -0.865899672914725;
  params.A[3] = 0.7725516732519853;
  params.A[4] = -0.23818512931704205;
  params.A[5] = -1.372529046100147;
  params.A[6] = 0.17859607212737894;
  params.A[7] = 1.1212590580454682;
  params.A[8] = -0.774545870495281;
  params.A[9] = -1.1121684642712744;
  params.A[10] = -0.44811496977740495;
  params.A[11] = 1.7455345994417217;
  params.A[12] = 1.9039816898917352;
  params.A[13] = 0.6895347036512547;
  params.A[14] = 1.6113364341535923;
  params.A[15] = 1.383003485172717;
  params.B[0] = -0.48802383468444344;
  params.B[1] = -1.631131964513103;
  params.B[2] = 0.6136436100941447;
  params.B[3] = 0.2313630495538037;
  params.B[4] = -0.5537409477496875;
  params.B[5] = -1.0997819806406723;
  params.B[6] = -0.3739203344950055;
  params.B[7] = -0.12423900520332376;
  params.Ab[0] = -0.923057686995755;
  params.Ab[1] = -0.8328289030982696;
  params.Ab[2] = -0.16925440270808823;
  params.Ab[3] = 1.442135651787706;
  params.Ab[4] = 0.34501161787128565;
  params.Ab[5] = -0.8660485502711608;
  params.Ab[6] = -0.8880899735055947;
  params.Ab[7] = -0.1815116979122129;
  params.Ab[8] = -1.17835862158005;
  params.Ab[9] = -1.1944851558277074;
  params.Ab[10] = 0.05614023926976763;
  params.Ab[11] = -1.6510825248767813;
  params.Ab[12] = -0.06565787059365391;
  params.Ab[13] = -0.5512951504486665;
  params.Ab[14] = 0.8307464872626844;
  params.Ab[15] = 0.9869848924080182;
  params.Bb[0] = 0.7643716874230573;
  params.Bb[1] = 0.7567216550196565;
  params.Bb[2] = -0.5055995034042868;
  params.Bb[3] = 0.6725392189410702;
  params.Bb[4] = -0.6406053441727284;
  params.Bb[5] = 0.29117547947550015;
  params.Bb[6] = -0.6967713677405021;
  params.Bb[7] = -0.21941980294587182;
  params.amin[0] = -0.12305786165987853;
  params.amax[0] = 0.48535084436867626;
  params.amin_b[0] = -1.9432052123471353;
  params.amax_b[0] = 0.46116840871014797;
  params.vmax[0] = 1.3829550218946605;
}
