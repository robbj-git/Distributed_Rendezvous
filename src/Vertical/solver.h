/* Produced by CVXGEN, 2019-04-23 04:29:27 -0400.  */
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
  double *b[26];
  double *x[1];
  double *dist[26];
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
  double *u[25];
  double *x[26];
} Vars;
typedef struct Workspace_t {
  double h[150];
  double s_inv[150];
  double s_inv_z[150];
  double b[50];
  double q[75];
  double rhs[425];
  double x[425];
  double *s;
  double *z;
  double *y;
  double lhs_aff[425];
  double lhs_cc[425];
  double buffer[425];
  double buffer2[425];
  double KKT[921];
  double L[596];
  double d[425];
  double v[425];
  double d_inv[425];
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
  double quad_28331511808[4];
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
  double quad_654529605632[1];
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
