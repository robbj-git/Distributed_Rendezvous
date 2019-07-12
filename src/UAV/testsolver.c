/* Produced by CVXGEN, 2019-04-24 04:05:41 -0400.  */
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
  params.xb_1[0] = 0.7050196079205251;
  params.xb_1[1] = 0.3634512696654033;
  params.xb_1[2] = -1.9040724704913385;
  params.xb_1[3] = 0.23541635196352795;
  params.xb_2[0] = -0.9629902123701384;
  params.xb_2[1] = -0.3395952119597214;
  params.xb_2[2] = -0.865899672914725;
  params.xb_2[3] = 0.7725516732519853;
  params.xb_3[0] = -0.23818512931704205;
  params.xb_3[1] = -1.372529046100147;
  params.xb_3[2] = 0.17859607212737894;
  params.xb_3[3] = 1.1212590580454682;
  params.xb_4[0] = -0.774545870495281;
  params.xb_4[1] = -1.1121684642712744;
  params.xb_4[2] = -0.44811496977740495;
  params.xb_4[3] = 1.7455345994417217;
  params.xb_5[0] = 1.9039816898917352;
  params.xb_5[1] = 0.6895347036512547;
  params.xb_5[2] = 1.6113364341535923;
  params.xb_5[3] = 1.383003485172717;
  params.xb_6[0] = -0.48802383468444344;
  params.xb_6[1] = -1.631131964513103;
  params.xb_6[2] = 0.6136436100941447;
  params.xb_6[3] = 0.2313630495538037;
  params.xb_7[0] = -0.5537409477496875;
  params.xb_7[1] = -1.0997819806406723;
  params.xb_7[2] = -0.3739203344950055;
  params.xb_7[3] = -0.12423900520332376;
  params.xb_8[0] = -0.923057686995755;
  params.xb_8[1] = -0.8328289030982696;
  params.xb_8[2] = -0.16925440270808823;
  params.xb_8[3] = 1.442135651787706;
  params.xb_9[0] = 0.34501161787128565;
  params.xb_9[1] = -0.8660485502711608;
  params.xb_9[2] = -0.8880899735055947;
  params.xb_9[3] = -0.1815116979122129;
  params.xb_10[0] = -1.17835862158005;
  params.xb_10[1] = -1.1944851558277074;
  params.xb_10[2] = 0.05614023926976763;
  params.xb_10[3] = -1.6510825248767813;
  params.xb_11[0] = -0.06565787059365391;
  params.xb_11[1] = -0.5512951504486665;
  params.xb_11[2] = 0.8307464872626844;
  params.xb_11[3] = 0.9869848924080182;
  params.xb_12[0] = 0.7643716874230573;
  params.xb_12[1] = 0.7567216550196565;
  params.xb_12[2] = -0.5055995034042868;
  params.xb_12[3] = 0.6725392189410702;
  params.xb_13[0] = -0.6406053441727284;
  params.xb_13[1] = 0.29117547947550015;
  params.xb_13[2] = -0.6967713677405021;
  params.xb_13[3] = -0.21941980294587182;
  params.xb_14[0] = -1.753884276680243;
  params.xb_14[1] = -1.0292983112626475;
  params.xb_14[2] = 1.8864104246942706;
  params.xb_14[3] = -1.077663182579704;
  params.xb_15[0] = 0.7659100437893209;
  params.xb_15[1] = 0.6019074328549583;
  params.xb_15[2] = 0.8957565577499285;
  params.xb_15[3] = -0.09964555746227477;
  params.xb_16[0] = 0.38665509840745127;
  params.xb_16[1] = -1.7321223042686946;
  params.xb_16[2] = -1.7097514487110663;
  params.xb_16[3] = -1.2040958948116867;
  params.xb_17[0] = -1.3925560119658358;
  params.xb_17[1] = -1.5995826216742213;
  params.xb_17[2] = -1.4828245415645833;
  params.xb_17[3] = 0.21311092723061398;
  params.xb_18[0] = -1.248740700304487;
  params.xb_18[1] = 1.808404972124833;
  params.xb_18[2] = 0.7264471152297065;
  params.xb_18[3] = 0.16407869343908477;
  params.xb_19[0] = 0.8287224032315907;
  params.xb_19[1] = -0.9444533161899464;
  params.xb_19[2] = 1.7069027370149112;
  params.xb_19[3] = 1.3567722311998827;
  params.xb_20[0] = 0.9052779937121489;
  params.xb_20[1] = -0.07904017565835986;
  params.xb_20[2] = 1.3684127435065871;
  params.xb_20[3] = 0.979009293697437;
  params.xb_21[0] = 0.6413036255984501;
  params.xb_21[1] = 1.6559010680237511;
  params.xb_21[2] = 0.5346622551502991;
  params.xb_21[3] = -0.5362376605895625;
  params.xb_22[0] = 0.2113782926017822;
  params.xb_22[1] = -1.2144776931994525;
  params.xb_22[2] = -1.2317108144255875;
  params.xb_22[3] = 0.9026784957312834;
  params.xb_23[0] = 1.1397468137245244;
  params.xb_23[1] = 1.8883934547350631;
  params.xb_23[2] = 1.4038856681660068;
  params.xb_23[3] = 0.17437730638329096;
  params.xb_24[0] = -1.6408365219077408;
  params.xb_24[1] = -0.04450702153554875;
  params.xb_24[2] = 1.7117453902485025;
  params.xb_24[3] = 1.1504727980139053;
  params.xb_25[0] = -0.05962309578364744;
  params.xb_25[1] = -0.1788825540764547;
  params.xb_25[2] = -1.1280569263625857;
  params.xb_25[3] = -1.2911464767927057;
  params.xb_26[0] = -1.7055053231225696;
  params.xb_26[1] = 1.56957275034837;
  params.xb_26[2] = 0.5607064675962357;
  params.xb_26[3] = -1.4266707301147146;
  params.xb_27[0] = -0.3434923211351708;
  params.xb_27[1] = -1.8035643024085055;
  params.xb_27[2] = -1.1625066019105454;
  params.xb_27[3] = 0.9228324965161532;
  params.xb_28[0] = 0.6044910817663975;
  params.xb_28[1] = -0.0840868104920891;
  params.xb_28[2] = -0.900877978017443;
  params.xb_28[3] = 0.608892500264739;
  params.xb_29[0] = 1.8257980452695217;
  params.xb_29[1] = -0.25791777529922877;
  params.xb_29[2] = -1.7194699796493191;
  params.xb_29[3] = -1.7690740487081298;
  params.xb_30[0] = -1.6685159248097703;
  params.xb_30[1] = 1.8388287490128845;
  params.xb_30[2] = 0.16304334474597537;
  params.xb_30[3] = 1.3498497306788897;
  params.xb_31[0] = -1.3198658230514613;
  params.xb_31[1] = -0.9586197090843394;
  params.xb_31[2] = 0.7679100474913709;
  params.xb_31[3] = 1.5822813125679343;
  params.xb_32[0] = -0.6372460621593619;
  params.xb_32[1] = -1.741307208038867;
  params.xb_32[2] = 1.456478677642575;
  params.xb_32[3] = -0.8365102166820959;
  params.xb_33[0] = 0.9643296255982503;
  params.xb_33[1] = -1.367865381194024;
  params.xb_33[2] = 0.7798537405635035;
  params.xb_33[3] = 1.3656784761245926;
  params.xb_34[0] = 0.9086083149868371;
  params.xb_34[1] = -0.5635699005460344;
  params.xb_34[2] = 0.9067590059607915;
  params.xb_34[3] = -1.4421315032701587;
  params.xb_35[0] = -0.7447235390671119;
  params.xb_35[1] = -0.32166897326822186;
  params.xb_35[2] = 1.5088481557772684;
  params.xb_35[3] = -1.385039165715428;
  params.xb_36[0] = 1.5204991609972622;
  params.xb_36[1] = 1.1958572768832156;
  params.xb_36[2] = 1.8864971883119228;
  params.xb_36[3] = -0.5291880667861584;
  params.xb_37[0] = -1.1802409243688836;
  params.xb_37[1] = -1.037718718661604;
  params.xb_37[2] = 1.3114512056856835;
  params.xb_37[3] = 1.8609125943756615;
  params.xb_38[0] = 0.7952399935216938;
  params.xb_38[1] = -0.07001183290468038;
  params.xb_38[2] = -0.8518009412754686;
  params.xb_38[3] = 1.3347515373726386;
  params.xb_39[0] = 1.4887180335977037;
  params.xb_39[1] = -1.6314736327976336;
  params.xb_39[2] = -1.1362021159208933;
  params.xb_39[3] = 1.327044361831466;
  params.xb_40[0] = 1.3932155883179842;
  params.xb_40[1] = -0.7413880049440107;
  params.xb_40[2] = -0.8828216126125747;
  params.xb_40[3] = -0.27673991192616;
  params.xb_41[0] = 0.15778600105866714;
  params.xb_41[1] = -1.6177327399735457;
  params.xb_41[2] = 1.3476485548544606;
  params.xb_41[3] = 0.13893948140528378;
  params.xb_42[0] = 1.0998712601636944;
  params.xb_42[1] = -1.0766549376946926;
  params.xb_42[2] = 1.8611734044254629;
  params.xb_42[3] = 1.0041092292735172;
  params.xb_43[0] = -0.6276245424321543;
  params.xb_43[1] = 1.794110587839819;
  params.xb_43[2] = 0.8020471158650913;
  params.xb_43[3] = 1.362244341944948;
  params.xb_44[0] = -1.8180107765765245;
  params.xb_44[1] = -1.7774338357932473;
  params.xb_44[2] = 0.9709490941985153;
  params.xb_44[3] = -0.7812542682064318;
  params.xb_45[0] = 0.0671374633729811;
  params.xb_45[1] = -1.374950305314906;
  params.xb_45[2] = 1.9118096386279388;
  params.xb_45[3] = 0.011004190697677885;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.P[0] = 1.8290010784747253;
  params.P[4] = 0;
  params.P[8] = 0;
  params.P[12] = 0;
  params.P[1] = 0;
  params.P[5] = 1.0740377962799963;
  params.P[9] = 0;
  params.P[13] = 0;
  params.P[2] = 0;
  params.P[6] = 0;
  params.P[10] = 1.478915452217838;
  params.P[14] = 0;
  params.P[3] = 0;
  params.P[7] = 0;
  params.P[11] = 0;
  params.P[15] = 1.0622794804057758;
  params.A[0] = 1.536965724350949;
  params.A[1] = -0.21675928514816478;
  params.A[2] = -1.725800326952653;
  params.A[3] = -1.6940148707361717;
  params.A[4] = 0.15517063201268;
  params.A[5] = -1.697734381979077;
  params.A[6] = -1.264910727950229;
  params.A[7] = -0.2545716633339441;
  params.A[8] = -0.008868675926170244;
  params.A[9] = 0.3332476609670296;
  params.A[10] = 0.48205072561962936;
  params.A[11] = -0.5087540014293261;
  params.A[12] = 0.4749463319223195;
  params.A[13] = -1.371021366459455;
  params.A[14] = -0.8979660982652256;
  params.A[15] = 1.194873082385242;
  params.B[0] = -1.3876427970939353;
  params.B[1] = -1.106708108457053;
  params.B[2] = -1.0280872812241797;
  params.B[3] = -0.08197078070773234;
  params.B[4] = -1.9970179118324083;
  params.B[5] = -1.878754557910134;
  params.B[6] = -0.15380739340877803;
  params.B[7] = -1.349917260533923;
  params.amin[0] = -1.3590036075465703;
  params.amax[0] = 1.5904091743532769;
  params.vmax[0] = 1.1563267174754204;
}
