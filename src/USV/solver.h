/* Produced by CVXGEN, 2019-04-24 04:09:39 -0400.  */
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
  double x_0[4];
  double xb_0[4];
  double Q[16];
  double R[4];
  double x_1[4];
  double x_2[4];
  double x_3[4];
  double x_4[4];
  double x_5[4];
  double x_6[4];
  double x_7[4];
  double x_8[4];
  double x_9[4];
  double x_10[4];
  double x_11[4];
  double x_12[4];
  double x_13[4];
  double x_14[4];
  double x_15[4];
  double x_16[4];
  double x_17[4];
  double x_18[4];
  double x_19[4];
  double x_20[4];
  double x_21[4];
  double x_22[4];
  double x_23[4];
  double x_24[4];
  double x_25[4];
  double x_26[4];
  double x_27[4];
  double x_28[4];
  double x_29[4];
  double x_30[4];
  double x_31[4];
  double x_32[4];
  double x_33[4];
  double x_34[4];
  double x_35[4];
  double x_36[4];
  double x_37[4];
  double x_38[4];
  double x_39[4];
  double x_40[4];
  double x_41[4];
  double x_42[4];
  double x_43[4];
  double x_44[4];
  double x_45[4];
  double P[16];
  double A[16];
  double B[8];
  double amin[1];
  double amax[1];
  double vmax[1];
  double *x[46];
  double *xb[1];
} Params;
typedef struct Vars_t {
  double *ub_0; /* 2 rows. */
  double *xb_1; /* 4 rows. */
  double *ub_1; /* 2 rows. */
  double *xb_2; /* 4 rows. */
  double *ub_2; /* 2 rows. */
  double *xb_3; /* 4 rows. */
  double *ub_3; /* 2 rows. */
  double *xb_4; /* 4 rows. */
  double *ub_4; /* 2 rows. */
  double *xb_5; /* 4 rows. */
  double *ub_5; /* 2 rows. */
  double *xb_6; /* 4 rows. */
  double *ub_6; /* 2 rows. */
  double *xb_7; /* 4 rows. */
  double *ub_7; /* 2 rows. */
  double *xb_8; /* 4 rows. */
  double *ub_8; /* 2 rows. */
  double *xb_9; /* 4 rows. */
  double *ub_9; /* 2 rows. */
  double *xb_10; /* 4 rows. */
  double *ub_10; /* 2 rows. */
  double *xb_11; /* 4 rows. */
  double *ub_11; /* 2 rows. */
  double *xb_12; /* 4 rows. */
  double *ub_12; /* 2 rows. */
  double *xb_13; /* 4 rows. */
  double *ub_13; /* 2 rows. */
  double *xb_14; /* 4 rows. */
  double *ub_14; /* 2 rows. */
  double *xb_15; /* 4 rows. */
  double *ub_15; /* 2 rows. */
  double *xb_16; /* 4 rows. */
  double *ub_16; /* 2 rows. */
  double *xb_17; /* 4 rows. */
  double *ub_17; /* 2 rows. */
  double *xb_18; /* 4 rows. */
  double *ub_18; /* 2 rows. */
  double *xb_19; /* 4 rows. */
  double *ub_19; /* 2 rows. */
  double *xb_20; /* 4 rows. */
  double *ub_20; /* 2 rows. */
  double *xb_21; /* 4 rows. */
  double *ub_21; /* 2 rows. */
  double *xb_22; /* 4 rows. */
  double *ub_22; /* 2 rows. */
  double *xb_23; /* 4 rows. */
  double *ub_23; /* 2 rows. */
  double *xb_24; /* 4 rows. */
  double *ub_24; /* 2 rows. */
  double *xb_25; /* 4 rows. */
  double *ub_25; /* 2 rows. */
  double *xb_26; /* 4 rows. */
  double *ub_26; /* 2 rows. */
  double *xb_27; /* 4 rows. */
  double *ub_27; /* 2 rows. */
  double *xb_28; /* 4 rows. */
  double *ub_28; /* 2 rows. */
  double *xb_29; /* 4 rows. */
  double *ub_29; /* 2 rows. */
  double *xb_30; /* 4 rows. */
  double *ub_30; /* 2 rows. */
  double *xb_31; /* 4 rows. */
  double *ub_31; /* 2 rows. */
  double *xb_32; /* 4 rows. */
  double *ub_32; /* 2 rows. */
  double *xb_33; /* 4 rows. */
  double *ub_33; /* 2 rows. */
  double *xb_34; /* 4 rows. */
  double *ub_34; /* 2 rows. */
  double *xb_35; /* 4 rows. */
  double *ub_35; /* 2 rows. */
  double *xb_36; /* 4 rows. */
  double *ub_36; /* 2 rows. */
  double *xb_37; /* 4 rows. */
  double *ub_37; /* 2 rows. */
  double *xb_38; /* 4 rows. */
  double *ub_38; /* 2 rows. */
  double *xb_39; /* 4 rows. */
  double *ub_39; /* 2 rows. */
  double *xb_40; /* 4 rows. */
  double *ub_40; /* 2 rows. */
  double *xb_41; /* 4 rows. */
  double *ub_41; /* 2 rows. */
  double *xb_42; /* 4 rows. */
  double *ub_42; /* 2 rows. */
  double *xb_43; /* 4 rows. */
  double *ub_43; /* 2 rows. */
  double *xb_44; /* 4 rows. */
  double *ub_44; /* 2 rows. */
  double *xb_45; /* 4 rows. */
  double *ub[45];
  double *xb[46];
} Vars;
typedef struct Workspace_t {
  double h[360];
  double s_inv[360];
  double s_inv_z[360];
  double b[180];
  double q[270];
  double rhs[1170];
  double x[1170];
  double *s;
  double *z;
  double *y;
  double lhs_aff[1170];
  double lhs_cc[1170];
  double buffer[1170];
  double buffer2[1170];
  double KKT[3269];
  double L[2815];
  double d[1170];
  double v[1170];
  double d_inv[1170];
  double gap;
  double optval;
  double ineq_resid_squared;
  double eq_resid_squared;
  double block_33[1];
  /* Pre-op symbols. */
  double quad_513884164096[1];
  double quad_444665335808[1];
  double quad_58300387328[1];
  double quad_299659579392[1];
  double quad_364130152448[1];
  double quad_913533890560[1];
  double quad_856461352960[1];
  double quad_241630588928[1];
  double quad_14788370432[1];
  double quad_828395790336[1];
  double quad_963669229568[1];
  double quad_188360511488[1];
  double quad_828356825088[1];
  double quad_590068277248[1];
  double quad_134046646272[1];
  double quad_456149590016[1];
  double quad_374614888448[1];
  double quad_921483431936[1];
  double quad_213113778176[1];
  double quad_180686053376[1];
  double quad_177970065408[1];
  double quad_919324475392[1];
  double quad_320799019008[1];
  double quad_988567134208[1];
  double quad_449843810304[1];
  double quad_482645798912[1];
  double quad_102626074624[1];
  double quad_47443726336[1];
  double quad_758227316736[1];
  double quad_757530308608[1];
  double quad_188583526400[1];
  double quad_216730951680[1];
  double quad_562744274944[1];
  double quad_742353604608[1];
  double quad_195581906944[1];
  double quad_467803193344[1];
  double quad_544160227328[1];
  double quad_896070811648[1];
  double quad_414529871872[1];
  double quad_590027743232[1];
  double quad_252493217792[1];
  double quad_712756629504[1];
  double quad_255141339136[1];
  double quad_465764904960[1];
  double quad_266053423104[1];
  double quad_554815283200[1];
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
