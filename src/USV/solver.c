/* Produced by CVXGEN, 2019-04-24 04:09:34 -0400.  */
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
  vars.ub_0 = work.x + 0;
  vars.ub_1 = work.x + 2;
  vars.ub_2 = work.x + 4;
  vars.ub_3 = work.x + 6;
  vars.ub_4 = work.x + 8;
  vars.ub_5 = work.x + 10;
  vars.ub_6 = work.x + 12;
  vars.ub_7 = work.x + 14;
  vars.ub_8 = work.x + 16;
  vars.ub_9 = work.x + 18;
  vars.ub_10 = work.x + 20;
  vars.ub_11 = work.x + 22;
  vars.ub_12 = work.x + 24;
  vars.ub_13 = work.x + 26;
  vars.ub_14 = work.x + 28;
  vars.ub_15 = work.x + 30;
  vars.ub_16 = work.x + 32;
  vars.ub_17 = work.x + 34;
  vars.ub_18 = work.x + 36;
  vars.ub_19 = work.x + 38;
  vars.ub_20 = work.x + 40;
  vars.ub_21 = work.x + 42;
  vars.ub_22 = work.x + 44;
  vars.ub_23 = work.x + 46;
  vars.ub_24 = work.x + 48;
  vars.ub_25 = work.x + 50;
  vars.ub_26 = work.x + 52;
  vars.ub_27 = work.x + 54;
  vars.ub_28 = work.x + 56;
  vars.ub_29 = work.x + 58;
  vars.ub_30 = work.x + 60;
  vars.ub_31 = work.x + 62;
  vars.ub_32 = work.x + 64;
  vars.ub_33 = work.x + 66;
  vars.ub_34 = work.x + 68;
  vars.ub_35 = work.x + 70;
  vars.ub_36 = work.x + 72;
  vars.ub_37 = work.x + 74;
  vars.ub_38 = work.x + 76;
  vars.ub_39 = work.x + 78;
  vars.ub_40 = work.x + 80;
  vars.ub_41 = work.x + 82;
  vars.ub_42 = work.x + 84;
  vars.ub_43 = work.x + 86;
  vars.ub_44 = work.x + 88;
  vars.xb_1 = work.x + 90;
  vars.xb_2 = work.x + 94;
  vars.xb_3 = work.x + 98;
  vars.xb_4 = work.x + 102;
  vars.xb_5 = work.x + 106;
  vars.xb_6 = work.x + 110;
  vars.xb_7 = work.x + 114;
  vars.xb_8 = work.x + 118;
  vars.xb_9 = work.x + 122;
  vars.xb_10 = work.x + 126;
  vars.xb_11 = work.x + 130;
  vars.xb_12 = work.x + 134;
  vars.xb_13 = work.x + 138;
  vars.xb_14 = work.x + 142;
  vars.xb_15 = work.x + 146;
  vars.xb_16 = work.x + 150;
  vars.xb_17 = work.x + 154;
  vars.xb_18 = work.x + 158;
  vars.xb_19 = work.x + 162;
  vars.xb_20 = work.x + 166;
  vars.xb_21 = work.x + 170;
  vars.xb_22 = work.x + 174;
  vars.xb_23 = work.x + 178;
  vars.xb_24 = work.x + 182;
  vars.xb_25 = work.x + 186;
  vars.xb_26 = work.x + 190;
  vars.xb_27 = work.x + 194;
  vars.xb_28 = work.x + 198;
  vars.xb_29 = work.x + 202;
  vars.xb_30 = work.x + 206;
  vars.xb_31 = work.x + 210;
  vars.xb_32 = work.x + 214;
  vars.xb_33 = work.x + 218;
  vars.xb_34 = work.x + 222;
  vars.xb_35 = work.x + 226;
  vars.xb_36 = work.x + 230;
  vars.xb_37 = work.x + 234;
  vars.xb_38 = work.x + 238;
  vars.xb_39 = work.x + 242;
  vars.xb_40 = work.x + 246;
  vars.xb_41 = work.x + 250;
  vars.xb_42 = work.x + 254;
  vars.xb_43 = work.x + 258;
  vars.xb_44 = work.x + 262;
  vars.xb_45 = work.x + 266;
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
  params.x[1] = params.x_1;
  params.x[2] = params.x_2;
  params.x[3] = params.x_3;
  params.x[4] = params.x_4;
  params.x[5] = params.x_5;
  params.x[6] = params.x_6;
  params.x[7] = params.x_7;
  params.x[8] = params.x_8;
  params.x[9] = params.x_9;
  params.x[10] = params.x_10;
  params.x[11] = params.x_11;
  params.x[12] = params.x_12;
  params.x[13] = params.x_13;
  params.x[14] = params.x_14;
  params.x[15] = params.x_15;
  params.x[16] = params.x_16;
  params.x[17] = params.x_17;
  params.x[18] = params.x_18;
  params.x[19] = params.x_19;
  params.x[20] = params.x_20;
  params.x[21] = params.x_21;
  params.x[22] = params.x_22;
  params.x[23] = params.x_23;
  params.x[24] = params.x_24;
  params.x[25] = params.x_25;
  params.x[26] = params.x_26;
  params.x[27] = params.x_27;
  params.x[28] = params.x_28;
  params.x[29] = params.x_29;
  params.x[30] = params.x_30;
  params.x[31] = params.x_31;
  params.x[32] = params.x_32;
  params.x[33] = params.x_33;
  params.x[34] = params.x_34;
  params.x[35] = params.x_35;
  params.x[36] = params.x_36;
  params.x[37] = params.x_37;
  params.x[38] = params.x_38;
  params.x[39] = params.x_39;
  params.x[40] = params.x_40;
  params.x[41] = params.x_41;
  params.x[42] = params.x_42;
  params.x[43] = params.x_43;
  params.x[44] = params.x_44;
  params.x[45] = params.x_45;
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
  vars.ub[0] = vars.ub_0;
  vars.xb[1] = vars.xb_1;
  vars.ub[1] = vars.ub_1;
  vars.xb[2] = vars.xb_2;
  vars.ub[2] = vars.ub_2;
  vars.xb[3] = vars.xb_3;
  vars.ub[3] = vars.ub_3;
  vars.xb[4] = vars.xb_4;
  vars.ub[4] = vars.ub_4;
  vars.xb[5] = vars.xb_5;
  vars.ub[5] = vars.ub_5;
  vars.xb[6] = vars.xb_6;
  vars.ub[6] = vars.ub_6;
  vars.xb[7] = vars.xb_7;
  vars.ub[7] = vars.ub_7;
  vars.xb[8] = vars.xb_8;
  vars.ub[8] = vars.ub_8;
  vars.xb[9] = vars.xb_9;
  vars.ub[9] = vars.ub_9;
  vars.xb[10] = vars.xb_10;
  vars.ub[10] = vars.ub_10;
  vars.xb[11] = vars.xb_11;
  vars.ub[11] = vars.ub_11;
  vars.xb[12] = vars.xb_12;
  vars.ub[12] = vars.ub_12;
  vars.xb[13] = vars.xb_13;
  vars.ub[13] = vars.ub_13;
  vars.xb[14] = vars.xb_14;
  vars.ub[14] = vars.ub_14;
  vars.xb[15] = vars.xb_15;
  vars.ub[15] = vars.ub_15;
  vars.xb[16] = vars.xb_16;
  vars.ub[16] = vars.ub_16;
  vars.xb[17] = vars.xb_17;
  vars.ub[17] = vars.ub_17;
  vars.xb[18] = vars.xb_18;
  vars.ub[18] = vars.ub_18;
  vars.xb[19] = vars.xb_19;
  vars.ub[19] = vars.ub_19;
  vars.xb[20] = vars.xb_20;
  vars.ub[20] = vars.ub_20;
  vars.xb[21] = vars.xb_21;
  vars.ub[21] = vars.ub_21;
  vars.xb[22] = vars.xb_22;
  vars.ub[22] = vars.ub_22;
  vars.xb[23] = vars.xb_23;
  vars.ub[23] = vars.ub_23;
  vars.xb[24] = vars.xb_24;
  vars.ub[24] = vars.ub_24;
  vars.xb[25] = vars.xb_25;
  vars.ub[25] = vars.ub_25;
  vars.xb[26] = vars.xb_26;
  vars.ub[26] = vars.ub_26;
  vars.xb[27] = vars.xb_27;
  vars.ub[27] = vars.ub_27;
  vars.xb[28] = vars.xb_28;
  vars.ub[28] = vars.ub_28;
  vars.xb[29] = vars.xb_29;
  vars.ub[29] = vars.ub_29;
  vars.xb[30] = vars.xb_30;
  vars.ub[30] = vars.ub_30;
  vars.xb[31] = vars.xb_31;
  vars.ub[31] = vars.ub_31;
  vars.xb[32] = vars.xb_32;
  vars.ub[32] = vars.ub_32;
  vars.xb[33] = vars.xb_33;
  vars.ub[33] = vars.ub_33;
  vars.xb[34] = vars.xb_34;
  vars.ub[34] = vars.ub_34;
  vars.xb[35] = vars.xb_35;
  vars.ub[35] = vars.ub_35;
  vars.xb[36] = vars.xb_36;
  vars.ub[36] = vars.ub_36;
  vars.xb[37] = vars.xb_37;
  vars.ub[37] = vars.ub_37;
  vars.xb[38] = vars.xb_38;
  vars.ub[38] = vars.ub_38;
  vars.xb[39] = vars.xb_39;
  vars.ub[39] = vars.ub_39;
  vars.xb[40] = vars.xb_40;
  vars.ub[40] = vars.ub_40;
  vars.xb[41] = vars.xb_41;
  vars.ub[41] = vars.ub_41;
  vars.xb[42] = vars.xb_42;
  vars.ub[42] = vars.ub_42;
  vars.xb[43] = vars.xb_43;
  vars.ub[43] = vars.ub_43;
  vars.xb[44] = vars.xb_44;
  vars.ub[44] = vars.ub_44;
  vars.xb[45] = vars.xb_45;
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
  objv += work.quad_513884164096[0]+work.quad_444665335808[0]+work.quad_58300387328[0]+work.quad_299659579392[0]+work.quad_364130152448[0]+work.quad_913533890560[0]+work.quad_856461352960[0]+work.quad_241630588928[0]+work.quad_14788370432[0]+work.quad_828395790336[0]+work.quad_963669229568[0]+work.quad_188360511488[0]+work.quad_828356825088[0]+work.quad_590068277248[0]+work.quad_134046646272[0]+work.quad_456149590016[0]+work.quad_374614888448[0]+work.quad_921483431936[0]+work.quad_213113778176[0]+work.quad_180686053376[0]+work.quad_177970065408[0]+work.quad_919324475392[0]+work.quad_320799019008[0]+work.quad_988567134208[0]+work.quad_449843810304[0]+work.quad_482645798912[0]+work.quad_102626074624[0]+work.quad_47443726336[0]+work.quad_758227316736[0]+work.quad_757530308608[0]+work.quad_188583526400[0]+work.quad_216730951680[0]+work.quad_562744274944[0]+work.quad_742353604608[0]+work.quad_195581906944[0]+work.quad_467803193344[0]+work.quad_544160227328[0]+work.quad_896070811648[0]+work.quad_414529871872[0]+work.quad_590027743232[0]+work.quad_252493217792[0]+work.quad_712756629504[0]+work.quad_255141339136[0]+work.quad_465764904960[0]+work.quad_266053423104[0]+work.quad_554815283200[0];
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
