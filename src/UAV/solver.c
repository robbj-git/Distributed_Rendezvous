/* Produced by CVXGEN, 2019-04-24 04:05:40 -0400.  */
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
  for (i = 0; i < 360; i++)
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
  work.y = work.x + 270;
  work.s = work.x + 450;
  work.z = work.x + 810;
  vars.u_0 = work.x + 0;
  vars.u_1 = work.x + 2;
  vars.u_2 = work.x + 4;
  vars.u_3 = work.x + 6;
  vars.u_4 = work.x + 8;
  vars.u_5 = work.x + 10;
  vars.u_6 = work.x + 12;
  vars.u_7 = work.x + 14;
  vars.u_8 = work.x + 16;
  vars.u_9 = work.x + 18;
  vars.u_10 = work.x + 20;
  vars.u_11 = work.x + 22;
  vars.u_12 = work.x + 24;
  vars.u_13 = work.x + 26;
  vars.u_14 = work.x + 28;
  vars.u_15 = work.x + 30;
  vars.u_16 = work.x + 32;
  vars.u_17 = work.x + 34;
  vars.u_18 = work.x + 36;
  vars.u_19 = work.x + 38;
  vars.u_20 = work.x + 40;
  vars.u_21 = work.x + 42;
  vars.u_22 = work.x + 44;
  vars.u_23 = work.x + 46;
  vars.u_24 = work.x + 48;
  vars.u_25 = work.x + 50;
  vars.u_26 = work.x + 52;
  vars.u_27 = work.x + 54;
  vars.u_28 = work.x + 56;
  vars.u_29 = work.x + 58;
  vars.u_30 = work.x + 60;
  vars.u_31 = work.x + 62;
  vars.u_32 = work.x + 64;
  vars.u_33 = work.x + 66;
  vars.u_34 = work.x + 68;
  vars.u_35 = work.x + 70;
  vars.u_36 = work.x + 72;
  vars.u_37 = work.x + 74;
  vars.u_38 = work.x + 76;
  vars.u_39 = work.x + 78;
  vars.u_40 = work.x + 80;
  vars.u_41 = work.x + 82;
  vars.u_42 = work.x + 84;
  vars.u_43 = work.x + 86;
  vars.u_44 = work.x + 88;
  vars.x_1 = work.x + 90;
  vars.x_2 = work.x + 94;
  vars.x_3 = work.x + 98;
  vars.x_4 = work.x + 102;
  vars.x_5 = work.x + 106;
  vars.x_6 = work.x + 110;
  vars.x_7 = work.x + 114;
  vars.x_8 = work.x + 118;
  vars.x_9 = work.x + 122;
  vars.x_10 = work.x + 126;
  vars.x_11 = work.x + 130;
  vars.x_12 = work.x + 134;
  vars.x_13 = work.x + 138;
  vars.x_14 = work.x + 142;
  vars.x_15 = work.x + 146;
  vars.x_16 = work.x + 150;
  vars.x_17 = work.x + 154;
  vars.x_18 = work.x + 158;
  vars.x_19 = work.x + 162;
  vars.x_20 = work.x + 166;
  vars.x_21 = work.x + 170;
  vars.x_22 = work.x + 174;
  vars.x_23 = work.x + 178;
  vars.x_24 = work.x + 182;
  vars.x_25 = work.x + 186;
  vars.x_26 = work.x + 190;
  vars.x_27 = work.x + 194;
  vars.x_28 = work.x + 198;
  vars.x_29 = work.x + 202;
  vars.x_30 = work.x + 206;
  vars.x_31 = work.x + 210;
  vars.x_32 = work.x + 214;
  vars.x_33 = work.x + 218;
  vars.x_34 = work.x + 222;
  vars.x_35 = work.x + 226;
  vars.x_36 = work.x + 230;
  vars.x_37 = work.x + 234;
  vars.x_38 = work.x + 238;
  vars.x_39 = work.x + 242;
  vars.x_40 = work.x + 246;
  vars.x_41 = work.x + 250;
  vars.x_42 = work.x + 254;
  vars.x_43 = work.x + 258;
  vars.x_44 = work.x + 262;
  vars.x_45 = work.x + 266;
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
  params.x[0] = params.x_0;
  params.xb[0] = params.xb_0;
  params.xb[1] = params.xb_1;
  params.xb[2] = params.xb_2;
  params.xb[3] = params.xb_3;
  params.xb[4] = params.xb_4;
  params.xb[5] = params.xb_5;
  params.xb[6] = params.xb_6;
  params.xb[7] = params.xb_7;
  params.xb[8] = params.xb_8;
  params.xb[9] = params.xb_9;
  params.xb[10] = params.xb_10;
  params.xb[11] = params.xb_11;
  params.xb[12] = params.xb_12;
  params.xb[13] = params.xb_13;
  params.xb[14] = params.xb_14;
  params.xb[15] = params.xb_15;
  params.xb[16] = params.xb_16;
  params.xb[17] = params.xb_17;
  params.xb[18] = params.xb_18;
  params.xb[19] = params.xb_19;
  params.xb[20] = params.xb_20;
  params.xb[21] = params.xb_21;
  params.xb[22] = params.xb_22;
  params.xb[23] = params.xb_23;
  params.xb[24] = params.xb_24;
  params.xb[25] = params.xb_25;
  params.xb[26] = params.xb_26;
  params.xb[27] = params.xb_27;
  params.xb[28] = params.xb_28;
  params.xb[29] = params.xb_29;
  params.xb[30] = params.xb_30;
  params.xb[31] = params.xb_31;
  params.xb[32] = params.xb_32;
  params.xb[33] = params.xb_33;
  params.xb[34] = params.xb_34;
  params.xb[35] = params.xb_35;
  params.xb[36] = params.xb_36;
  params.xb[37] = params.xb_37;
  params.xb[38] = params.xb_38;
  params.xb[39] = params.xb_39;
  params.xb[40] = params.xb_40;
  params.xb[41] = params.xb_41;
  params.xb[42] = params.xb_42;
  params.xb[43] = params.xb_43;
  params.xb[44] = params.xb_44;
  params.xb[45] = params.xb_45;
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
}
void setup_indexing(void) {
  setup_pointers();
  setup_indexed_params();
  setup_indexed_optvars();
}
void set_start(void) {
  int i;
  for (i = 0; i < 270; i++)
    work.x[i] = 0;
  for (i = 0; i < 180; i++)
    work.y[i] = 0;
  for (i = 0; i < 360; i++)
    work.s[i] = (work.h[i] > 0) ? work.h[i] : settings.s_init;
  for (i = 0; i < 360; i++)
    work.z[i] = settings.z_init;
}
double eval_objv(void) {
  int i;
  double objv;
  /* Borrow space in work.rhs. */
  multbyP(work.rhs, work.x);
  objv = 0;
  for (i = 0; i < 270; i++)
    objv += work.x[i]*work.rhs[i];
  objv *= 0.5;
  for (i = 0; i < 270; i++)
    objv += work.q[i]*work.x[i];
  objv += work.quad_513884164096[0]+work.quad_788958081024[0]+work.quad_374560497664[0]+work.quad_606718136320[0]+work.quad_263870058496[0]+work.quad_323313410048[0]+work.quad_835447427072[0]+work.quad_866469752832[0]+work.quad_780297809920[0]+work.quad_929313640448[0]+work.quad_736882544640[0]+work.quad_685030031360[0]+work.quad_256231362560[0]+work.quad_239472939008[0]+work.quad_678005088256[0]+work.quad_67476746240[0]+work.quad_41528709120[0]+work.quad_914721599488[0]+work.quad_938668638208[0]+work.quad_200827822080[0]+work.quad_964538445824[0]+work.quad_498086375424[0]+work.quad_166526738432[0]+work.quad_849159483392[0]+work.quad_192161705984[0]+work.quad_727999463424[0]+work.quad_512511655936[0]+work.quad_484104499200[0]+work.quad_857027723264[0]+work.quad_49952149504[0]+work.quad_977066876928[0]+work.quad_554623475712[0]+work.quad_468130324480[0]+work.quad_112549814272[0]+work.quad_864864751616[0]+work.quad_885212905472[0]+work.quad_527754874880[0]+work.quad_542107860992[0]+work.quad_761311268864[0]+work.quad_434894467072[0]+work.quad_288263913472[0]+work.quad_934005862400[0]+work.quad_490908278784[0]+work.quad_401341784064[0]+work.quad_737798402048[0]+work.quad_431452737536[0];
  return objv;
}
void fillrhs_aff(void) {
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 270;
  r3 = work.rhs + 630;
  r4 = work.rhs + 990;
  /* r1 = -A^Ty - G^Tz - Px - q. */
  multbymAT(r1, work.y);
  multbymGT(work.buffer, work.z);
  for (i = 0; i < 270; i++)
    r1[i] += work.buffer[i];
  multbyP(work.buffer, work.x);
  for (i = 0; i < 270; i++)
    r1[i] -= work.buffer[i] + work.q[i];
  /* r2 = -z. */
  for (i = 0; i < 360; i++)
    r2[i] = -work.z[i];
  /* r3 = -Gx - s + h. */
  multbymG(r3, work.x);
  for (i = 0; i < 360; i++)
    r3[i] += -work.s[i] + work.h[i];
  /* r4 = -Ax + b. */
  multbymA(r4, work.x);
  for (i = 0; i < 180; i++)
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
  r2 = work.rhs + 270;
  ds_aff = work.lhs_aff + 270;
  dz_aff = work.lhs_aff + 630;
  mu = 0;
  for (i = 0; i < 360; i++)
    mu += work.s[i]*work.z[i];
  /* Don't finish calculating mu quite yet. */
  /* Find min(min(ds./s), min(dz./z)). */
  minval = 0;
  for (i = 0; i < 360; i++)
    if (ds_aff[i] < minval*work.s[i])
      minval = ds_aff[i]/work.s[i];
  for (i = 0; i < 360; i++)
    if (dz_aff[i] < minval*work.z[i])
      minval = dz_aff[i]/work.z[i];
  /* Find alpha. */
  if (-1 < minval)
      alpha = 1;
  else
      alpha = -1/minval;
  sigma = 0;
  for (i = 0; i < 360; i++)
    sigma += (work.s[i] + alpha*ds_aff[i])*
      (work.z[i] + alpha*dz_aff[i]);
  sigma /= mu;
  sigma = sigma*sigma*sigma;
  /* Finish calculating mu now. */
  mu *= 0.002777777777777778;
  smu = sigma*mu;
  /* Fill-in the rhs. */
  for (i = 0; i < 270; i++)
    work.rhs[i] = 0;
  for (i = 630; i < 1170; i++)
    work.rhs[i] = 0;
  for (i = 0; i < 360; i++)
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
    for (i = 0; i < 1170; i++) {
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
    for (i = 0; i < 1170; i++) {
      var[i] -= new_var[i];
    }
  }
#ifndef ZERO_LIBRARY_MODE
  if (settings.verbose_refinement) {
    /* Check the residual once more, but only if we're reporting it, since */
    /* it's expensive. */
    norm2 = 0;
    matrix_multiply(residual, var);
    for (i = 0; i < 1170; i++) {
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
  for (i = 0; i < 360; i++)
    work.buffer[i] += -work.s[i] + work.h[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 360; i++)
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
  for (i = 0; i < 180; i++)
    work.buffer[i] += work.b[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 180; i++)
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
  for (i = 0; i < 360; i++)
    work.s_inv_z[i] = 1;
  fill_KKT();
  ldl_factor();
  fillrhs_start();
  /* Borrow work.lhs_aff for the solution. */
  ldl_solve(work.rhs, work.lhs_aff);
  /* Don't do any refinement for now. Precision doesn't matter too much. */
  x = work.lhs_aff;
  s = work.lhs_aff + 270;
  z = work.lhs_aff + 630;
  y = work.lhs_aff + 990;
  /* Just set x and y as is. */
  for (i = 0; i < 270; i++)
    work.x[i] = x[i];
  for (i = 0; i < 180; i++)
    work.y[i] = y[i];
  /* Now complete the initialization. Start with s. */
  /* Must have alpha > max(z). */
  alpha = -1e99;
  for (i = 0; i < 360; i++)
    if (alpha < z[i])
      alpha = z[i];
  if (alpha < 0) {
    for (i = 0; i < 360; i++)
      work.s[i] = -z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 360; i++)
      work.s[i] = -z[i] + alpha;
  }
  /* Now initialize z. */
  /* Now must have alpha > max(-z). */
  alpha = -1e99;
  for (i = 0; i < 360; i++)
    if (alpha < -z[i])
      alpha = -z[i];
  if (alpha < 0) {
    for (i = 0; i < 360; i++)
      work.z[i] = z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 360; i++)
      work.z[i] = z[i] + alpha;
  }
}
void fillrhs_start(void) {
  /* Fill rhs with (-q, 0, h, b). */
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 270;
  r3 = work.rhs + 630;
  r4 = work.rhs + 990;
  for (i = 0; i < 270; i++)
    r1[i] = -work.q[i];
  for (i = 0; i < 360; i++)
    r2[i] = 0;
  for (i = 0; i < 360; i++)
    r3[i] = work.h[i];
  for (i = 0; i < 180; i++)
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
    for (i = 0; i < 360; i++) {
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
    for (i = 0; i < 1170; i++)
      work.lhs_aff[i] += work.lhs_cc[i];
    /* Rename aff to reflect its new meaning. */
    dx = work.lhs_aff;
    ds = work.lhs_aff + 270;
    dz = work.lhs_aff + 630;
    dy = work.lhs_aff + 990;
    /* Find min(min(ds./s), min(dz./z)). */
    minval = 0;
    for (i = 0; i < 360; i++)
      if (ds[i] < minval*work.s[i])
        minval = ds[i]/work.s[i];
    for (i = 0; i < 360; i++)
      if (dz[i] < minval*work.z[i])
        minval = dz[i]/work.z[i];
    /* Find alpha. */
    if (-0.99 < minval)
      alpha = 1;
    else
      alpha = -0.99/minval;
    /* Update the primal and dual variables. */
    for (i = 0; i < 270; i++)
      work.x[i] += alpha*dx[i];
    for (i = 0; i < 360; i++)
      work.s[i] += alpha*ds[i];
    for (i = 0; i < 360; i++)
      work.z[i] += alpha*dz[i];
    for (i = 0; i < 180; i++)
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
