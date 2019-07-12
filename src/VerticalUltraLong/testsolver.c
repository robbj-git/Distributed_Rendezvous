/* Produced by CVXGEN, 2019-05-01 05:37:16 -0400.  */
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
  params.b_46[0] = -1.6510825248767813;
  params.b_47[0] = -0.06565787059365391;
  params.b_48[0] = -0.5512951504486665;
  params.b_49[0] = 0.8307464872626844;
  params.b_50[0] = 0.9869848924080182;
  params.b_51[0] = 0.7643716874230573;
  params.b_52[0] = 0.7567216550196565;
  params.b_53[0] = -0.5055995034042868;
  params.b_54[0] = 0.6725392189410702;
  params.b_55[0] = -0.6406053441727284;
  params.b_56[0] = 0.29117547947550015;
  params.b_57[0] = -0.6967713677405021;
  params.b_58[0] = -0.21941980294587182;
  params.b_59[0] = -1.753884276680243;
  params.b_60[0] = -1.0292983112626475;
  params.b_61[0] = 1.8864104246942706;
  params.b_62[0] = -1.077663182579704;
  params.b_63[0] = 0.7659100437893209;
  params.b_64[0] = 0.6019074328549583;
  params.b_65[0] = 0.8957565577499285;
  params.b_66[0] = -0.09964555746227477;
  params.b_67[0] = 0.38665509840745127;
  params.b_68[0] = -1.7321223042686946;
  params.b_69[0] = -1.7097514487110663;
  params.b_70[0] = -1.2040958948116867;
  params.b_71[0] = -1.3925560119658358;
  params.b_72[0] = -1.5995826216742213;
  params.b_73[0] = -1.4828245415645833;
  params.b_74[0] = 0.21311092723061398;
  params.b_75[0] = -1.248740700304487;
  params.b_76[0] = 1.808404972124833;
  params.b_77[0] = 0.7264471152297065;
  params.b_78[0] = 0.16407869343908477;
  params.b_79[0] = 0.8287224032315907;
  params.b_80[0] = -0.9444533161899464;
  params.b_81[0] = 1.7069027370149112;
  params.b_82[0] = 1.3567722311998827;
  params.b_83[0] = 0.9052779937121489;
  params.b_84[0] = -0.07904017565835986;
  params.b_85[0] = 1.3684127435065871;
  params.b_86[0] = 0.979009293697437;
  params.b_87[0] = 0.6413036255984501;
  params.b_88[0] = 1.6559010680237511;
  params.b_89[0] = 0.5346622551502991;
  params.b_90[0] = -0.5362376605895625;
  params.b_91[0] = 0.2113782926017822;
  params.b_92[0] = -1.2144776931994525;
  params.b_93[0] = -1.2317108144255875;
  params.b_94[0] = 0.9026784957312834;
  params.b_95[0] = 1.1397468137245244;
  params.b_96[0] = 1.8883934547350631;
  params.b_97[0] = 1.4038856681660068;
  params.b_98[0] = 0.17437730638329096;
  params.b_99[0] = -1.6408365219077408;
  params.b_100[0] = -0.04450702153554875;
  /* Make this a diagonal PSD matrix, even though it's not diagonal. */
  params.P[0] = 1.9279363475621256;
  params.P[2] = 0;
  params.P[1] = 0;
  params.P[3] = 1.7876181995034763;
  params.A[0] = -0.05962309578364744;
  params.A[1] = -0.1788825540764547;
  params.A[2] = -1.1280569263625857;
  params.A[3] = -1.2911464767927057;
  params.B[0] = -1.7055053231225696;
  params.B[1] = 1.56957275034837;
  params.wmin[0] = -1.2803532337981178;
  params.wmax[0] = 0.2866646349426427;
  params.kl[0] = 0.8282538394324146;
  params.wmin_land[0] = -0.09821784879574724;
  params.hs[0] = -1.1625066019105454;
  params.dist_1[0] = 0.9228324965161532;
  params.dl[0] = 0.6044910817663975;
  params.ds[0] = -0.0840868104920891;
  params.dist_2[0] = -0.900877978017443;
  params.dist_3[0] = 0.608892500264739;
  params.dist_4[0] = 1.8257980452695217;
  params.dist_5[0] = -0.25791777529922877;
  params.dist_6[0] = -1.7194699796493191;
  params.dist_7[0] = -1.7690740487081298;
  params.dist_8[0] = -1.6685159248097703;
  params.dist_9[0] = 1.8388287490128845;
  params.dist_10[0] = 0.16304334474597537;
  params.dist_11[0] = 1.3498497306788897;
  params.dist_12[0] = -1.3198658230514613;
  params.dist_13[0] = -0.9586197090843394;
  params.dist_14[0] = 0.7679100474913709;
  params.dist_15[0] = 1.5822813125679343;
  params.dist_16[0] = -0.6372460621593619;
  params.dist_17[0] = -1.741307208038867;
  params.dist_18[0] = 1.456478677642575;
  params.dist_19[0] = -0.8365102166820959;
  params.dist_20[0] = 0.9643296255982503;
  params.dist_21[0] = -1.367865381194024;
  params.dist_22[0] = 0.7798537405635035;
  params.dist_23[0] = 1.3656784761245926;
  params.dist_24[0] = 0.9086083149868371;
  params.dist_25[0] = -0.5635699005460344;
  params.dist_26[0] = 0.9067590059607915;
  params.dist_27[0] = -1.4421315032701587;
  params.dist_28[0] = -0.7447235390671119;
  params.dist_29[0] = -0.32166897326822186;
  params.dist_30[0] = 1.5088481557772684;
  params.dist_31[0] = -1.385039165715428;
  params.dist_32[0] = 1.5204991609972622;
  params.dist_33[0] = 1.1958572768832156;
  params.dist_34[0] = 1.8864971883119228;
  params.dist_35[0] = -0.5291880667861584;
  params.dist_36[0] = -1.1802409243688836;
  params.dist_37[0] = -1.037718718661604;
  params.dist_38[0] = 1.3114512056856835;
  params.dist_39[0] = 1.8609125943756615;
  params.dist_40[0] = 0.7952399935216938;
  params.dist_41[0] = -0.07001183290468038;
  params.dist_42[0] = -0.8518009412754686;
  params.dist_43[0] = 1.3347515373726386;
  params.dist_44[0] = 1.4887180335977037;
  params.dist_45[0] = -1.6314736327976336;
  params.dist_46[0] = -1.1362021159208933;
  params.dist_47[0] = 1.327044361831466;
  params.dist_48[0] = 1.3932155883179842;
  params.dist_49[0] = -0.7413880049440107;
  params.dist_50[0] = -0.8828216126125747;
  params.dist_51[0] = -0.27673991192616;
  params.dist_52[0] = 0.15778600105866714;
  params.dist_53[0] = -1.6177327399735457;
  params.dist_54[0] = 1.3476485548544606;
  params.dist_55[0] = 0.13893948140528378;
  params.dist_56[0] = 1.0998712601636944;
  params.dist_57[0] = -1.0766549376946926;
  params.dist_58[0] = 1.8611734044254629;
  params.dist_59[0] = 1.0041092292735172;
  params.dist_60[0] = -0.6276245424321543;
  params.dist_61[0] = 1.794110587839819;
  params.dist_62[0] = 0.8020471158650913;
  params.dist_63[0] = 1.362244341944948;
  params.dist_64[0] = -1.8180107765765245;
  params.dist_65[0] = -1.7774338357932473;
  params.dist_66[0] = 0.9709490941985153;
  params.dist_67[0] = -0.7812542682064318;
  params.dist_68[0] = 0.0671374633729811;
  params.dist_69[0] = -1.374950305314906;
  params.dist_70[0] = 1.9118096386279388;
  params.dist_71[0] = 0.011004190697677885;
  params.dist_72[0] = 1.3160043138989015;
  params.dist_73[0] = -1.7038488148800144;
  params.dist_74[0] = -0.08433819112864738;
  params.dist_75[0] = -1.7508820783768964;
  params.dist_76[0] = 1.536965724350949;
  params.dist_77[0] = -0.21675928514816478;
  params.dist_78[0] = -1.725800326952653;
  params.dist_79[0] = -1.6940148707361717;
  params.dist_80[0] = 0.15517063201268;
  params.dist_81[0] = -1.697734381979077;
  params.dist_82[0] = -1.264910727950229;
  params.dist_83[0] = -0.2545716633339441;
  params.dist_84[0] = -0.008868675926170244;
  params.dist_85[0] = 0.3332476609670296;
  params.dist_86[0] = 0.48205072561962936;
  params.dist_87[0] = -0.5087540014293261;
  params.dist_88[0] = 0.4749463319223195;
  params.dist_89[0] = -1.371021366459455;
  params.dist_90[0] = -0.8979660982652256;
  params.dist_91[0] = 1.194873082385242;
  params.dist_92[0] = -1.3876427970939353;
  params.dist_93[0] = -1.106708108457053;
  params.dist_94[0] = -1.0280872812241797;
  params.dist_95[0] = -0.08197078070773234;
  params.dist_96[0] = -1.9970179118324083;
  params.dist_97[0] = -1.878754557910134;
  params.dist_98[0] = -0.15380739340877803;
  params.dist_99[0] = -1.349917260533923;
  params.dist_100[0] = 0.7180072150931407;
}
