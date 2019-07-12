/* Produced by CVXGEN, 2019-04-23 04:29:25 -0400.  */
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
  for (i = 0; i < 150; i++)
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
  work.y = work.x + 75;
  work.s = work.x + 125;
  work.z = work.x + 275;
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
  vars.x_1 = work.x + 25;
  vars.x_2 = work.x + 27;
  vars.x_3 = work.x + 29;
  vars.x_4 = work.x + 31;
  vars.x_5 = work.x + 33;
  vars.x_6 = work.x + 35;
  vars.x_7 = work.x + 37;
  vars.x_8 = work.x + 39;
  vars.x_9 = work.x + 41;
  vars.x_10 = work.x + 43;
  vars.x_11 = work.x + 45;
  vars.x_12 = work.x + 47;
  vars.x_13 = work.x + 49;
  vars.x_14 = work.x + 51;
  vars.x_15 = work.x + 53;
  vars.x_16 = work.x + 55;
  vars.x_17 = work.x + 57;
  vars.x_18 = work.x + 59;
  vars.x_19 = work.x + 61;
  vars.x_20 = work.x + 63;
  vars.x_21 = work.x + 65;
  vars.x_22 = work.x + 67;
  vars.x_23 = work.x + 69;
  vars.x_24 = work.x + 71;
  vars.x_25 = work.x + 73;
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
}
void setup_indexing(void) {
  setup_pointers();
  setup_indexed_params();
  setup_indexed_optvars();
}
void set_start(void) {
  int i;
  for (i = 0; i < 75; i++)
    work.x[i] = 0;
  for (i = 0; i < 50; i++)
    work.y[i] = 0;
  for (i = 0; i < 150; i++)
    work.s[i] = (work.h[i] > 0) ? work.h[i] : settings.s_init;
  for (i = 0; i < 150; i++)
    work.z[i] = settings.z_init;
}
double eval_objv(void) {
  int i;
  double objv;
  /* Borrow space in work.rhs. */
  multbyP(work.rhs, work.x);
  objv = 0;
  for (i = 0; i < 75; i++)
    objv += work.x[i]*work.rhs[i];
  objv *= 0.5;
  for (i = 0; i < 75; i++)
    objv += work.q[i]*work.x[i];
  objv += work.quad_783933743104[0]+work.quad_339902681088[0]+work.quad_135673548800[0]+work.quad_945197019136[0]+work.quad_21094948864[0]+work.quad_390374883328[0]+work.quad_311039037440[0]+work.quad_722651664384[0]+work.quad_73848643584[0]+work.quad_715760762880[0]+work.quad_619396980736[0]+work.quad_449708576768[0]+work.quad_644345716736[0]+work.quad_540410519552[0]+work.quad_271462109184[0]+work.quad_337763737600[0]+work.quad_454123520[0]+work.quad_15178178560[0]+work.quad_912311828480[0]+work.quad_525854347264[0]+work.quad_811378728960[0]+work.quad_956960821248[0]+work.quad_858261053440[0]+work.quad_79292780544[0]+work.quad_894503522304[0]+work.quad_654529605632[0];
  return objv;
}
void fillrhs_aff(void) {
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 75;
  r3 = work.rhs + 225;
  r4 = work.rhs + 375;
  /* r1 = -A^Ty - G^Tz - Px - q. */
  multbymAT(r1, work.y);
  multbymGT(work.buffer, work.z);
  for (i = 0; i < 75; i++)
    r1[i] += work.buffer[i];
  multbyP(work.buffer, work.x);
  for (i = 0; i < 75; i++)
    r1[i] -= work.buffer[i] + work.q[i];
  /* r2 = -z. */
  for (i = 0; i < 150; i++)
    r2[i] = -work.z[i];
  /* r3 = -Gx - s + h. */
  multbymG(r3, work.x);
  for (i = 0; i < 150; i++)
    r3[i] += -work.s[i] + work.h[i];
  /* r4 = -Ax + b. */
  multbymA(r4, work.x);
  for (i = 0; i < 50; i++)
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
  r2 = work.rhs + 75;
  ds_aff = work.lhs_aff + 75;
  dz_aff = work.lhs_aff + 225;
  mu = 0;
  for (i = 0; i < 150; i++)
    mu += work.s[i]*work.z[i];
  /* Don't finish calculating mu quite yet. */
  /* Find min(min(ds./s), min(dz./z)). */
  minval = 0;
  for (i = 0; i < 150; i++)
    if (ds_aff[i] < minval*work.s[i])
      minval = ds_aff[i]/work.s[i];
  for (i = 0; i < 150; i++)
    if (dz_aff[i] < minval*work.z[i])
      minval = dz_aff[i]/work.z[i];
  /* Find alpha. */
  if (-1 < minval)
      alpha = 1;
  else
      alpha = -1/minval;
  sigma = 0;
  for (i = 0; i < 150; i++)
    sigma += (work.s[i] + alpha*ds_aff[i])*
      (work.z[i] + alpha*dz_aff[i]);
  sigma /= mu;
  sigma = sigma*sigma*sigma;
  /* Finish calculating mu now. */
  mu *= 0.006666666666666667;
  smu = sigma*mu;
  /* Fill-in the rhs. */
  for (i = 0; i < 75; i++)
    work.rhs[i] = 0;
  for (i = 225; i < 425; i++)
    work.rhs[i] = 0;
  for (i = 0; i < 150; i++)
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
    for (i = 0; i < 425; i++) {
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
    for (i = 0; i < 425; i++) {
      var[i] -= new_var[i];
    }
  }
#ifndef ZERO_LIBRARY_MODE
  if (settings.verbose_refinement) {
    /* Check the residual once more, but only if we're reporting it, since */
    /* it's expensive. */
    norm2 = 0;
    matrix_multiply(residual, var);
    for (i = 0; i < 425; i++) {
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
  for (i = 0; i < 150; i++)
    work.buffer[i] += -work.s[i] + work.h[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 150; i++)
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
  for (i = 0; i < 50; i++)
    work.buffer[i] += work.b[i];
  /* Now find the squared norm. */
  norm2_squared = 0;
  for (i = 0; i < 50; i++)
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
  for (i = 0; i < 150; i++)
    work.s_inv_z[i] = 1;
  fill_KKT();
  ldl_factor();
  fillrhs_start();
  /* Borrow work.lhs_aff for the solution. */
  ldl_solve(work.rhs, work.lhs_aff);
  /* Don't do any refinement for now. Precision doesn't matter too much. */
  x = work.lhs_aff;
  s = work.lhs_aff + 75;
  z = work.lhs_aff + 225;
  y = work.lhs_aff + 375;
  /* Just set x and y as is. */
  for (i = 0; i < 75; i++)
    work.x[i] = x[i];
  for (i = 0; i < 50; i++)
    work.y[i] = y[i];
  /* Now complete the initialization. Start with s. */
  /* Must have alpha > max(z). */
  alpha = -1e99;
  for (i = 0; i < 150; i++)
    if (alpha < z[i])
      alpha = z[i];
  if (alpha < 0) {
    for (i = 0; i < 150; i++)
      work.s[i] = -z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 150; i++)
      work.s[i] = -z[i] + alpha;
  }
  /* Now initialize z. */
  /* Now must have alpha > max(-z). */
  alpha = -1e99;
  for (i = 0; i < 150; i++)
    if (alpha < -z[i])
      alpha = -z[i];
  if (alpha < 0) {
    for (i = 0; i < 150; i++)
      work.z[i] = z[i];
  } else {
    alpha += 1;
    for (i = 0; i < 150; i++)
      work.z[i] = z[i] + alpha;
  }
}
void fillrhs_start(void) {
  /* Fill rhs with (-q, 0, h, b). */
  int i;
  double *r1, *r2, *r3, *r4;
  r1 = work.rhs;
  r2 = work.rhs + 75;
  r3 = work.rhs + 225;
  r4 = work.rhs + 375;
  for (i = 0; i < 75; i++)
    r1[i] = -work.q[i];
  for (i = 0; i < 150; i++)
    r2[i] = 0;
  for (i = 0; i < 150; i++)
    r3[i] = work.h[i];
  for (i = 0; i < 50; i++)
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
    for (i = 0; i < 150; i++) {
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
    for (i = 0; i < 425; i++)
      work.lhs_aff[i] += work.lhs_cc[i];
    /* Rename aff to reflect its new meaning. */
    dx = work.lhs_aff;
    ds = work.lhs_aff + 75;
    dz = work.lhs_aff + 225;
    dy = work.lhs_aff + 375;
    /* Find min(min(ds./s), min(dz./z)). */
    minval = 0;
    for (i = 0; i < 150; i++)
      if (ds[i] < minval*work.s[i])
        minval = ds[i]/work.s[i];
    for (i = 0; i < 150; i++)
      if (dz[i] < minval*work.z[i])
        minval = dz[i]/work.z[i];
    /* Find alpha. */
    if (-0.99 < minval)
      alpha = 1;
    else
      alpha = -0.99/minval;
    /* Update the primal and dual variables. */
    for (i = 0; i < 75; i++)
      work.x[i] += alpha*dx[i];
    for (i = 0; i < 150; i++)
      work.s[i] += alpha*ds[i];
    for (i = 0; i < 150; i++)
      work.z[i] += alpha*dz[i];
    for (i = 0; i < 50; i++)
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
