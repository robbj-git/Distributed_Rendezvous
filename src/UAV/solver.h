/* Produced by CVXGEN, 2019-04-24 04:05:41 -0400.  */
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
  double xb_1[4];
  double xb_2[4];
  double xb_3[4];
  double xb_4[4];
  double xb_5[4];
  double xb_6[4];
  double xb_7[4];
  double xb_8[4];
  double xb_9[4];
  double xb_10[4];
  double xb_11[4];
  double xb_12[4];
  double xb_13[4];
  double xb_14[4];
  double xb_15[4];
  double xb_16[4];
  double xb_17[4];
  double xb_18[4];
  double xb_19[4];
  double xb_20[4];
  double xb_21[4];
  double xb_22[4];
  double xb_23[4];
  double xb_24[4];
  double xb_25[4];
  double xb_26[4];
  double xb_27[4];
  double xb_28[4];
  double xb_29[4];
  double xb_30[4];
  double xb_31[4];
  double xb_32[4];
  double xb_33[4];
  double xb_34[4];
  double xb_35[4];
  double xb_36[4];
  double xb_37[4];
  double xb_38[4];
  double xb_39[4];
  double xb_40[4];
  double xb_41[4];
  double xb_42[4];
  double xb_43[4];
  double xb_44[4];
  double xb_45[4];
  double P[16];
  double A[16];
  double B[8];
  double amin[1];
  double amax[1];
  double vmax[1];
  double *x[1];
  double *xb[46];
} Params;
typedef struct Vars_t {
  double *u_0; /* 2 rows. */
  double *x_1; /* 4 rows. */
  double *u_1; /* 2 rows. */
  double *x_2; /* 4 rows. */
  double *u_2; /* 2 rows. */
  double *x_3; /* 4 rows. */
  double *u_3; /* 2 rows. */
  double *x_4; /* 4 rows. */
  double *u_4; /* 2 rows. */
  double *x_5; /* 4 rows. */
  double *u_5; /* 2 rows. */
  double *x_6; /* 4 rows. */
  double *u_6; /* 2 rows. */
  double *x_7; /* 4 rows. */
  double *u_7; /* 2 rows. */
  double *x_8; /* 4 rows. */
  double *u_8; /* 2 rows. */
  double *x_9; /* 4 rows. */
  double *u_9; /* 2 rows. */
  double *x_10; /* 4 rows. */
  double *u_10; /* 2 rows. */
  double *x_11; /* 4 rows. */
  double *u_11; /* 2 rows. */
  double *x_12; /* 4 rows. */
  double *u_12; /* 2 rows. */
  double *x_13; /* 4 rows. */
  double *u_13; /* 2 rows. */
  double *x_14; /* 4 rows. */
  double *u_14; /* 2 rows. */
  double *x_15; /* 4 rows. */
  double *u_15; /* 2 rows. */
  double *x_16; /* 4 rows. */
  double *u_16; /* 2 rows. */
  double *x_17; /* 4 rows. */
  double *u_17; /* 2 rows. */
  double *x_18; /* 4 rows. */
  double *u_18; /* 2 rows. */
  double *x_19; /* 4 rows. */
  double *u_19; /* 2 rows. */
  double *x_20; /* 4 rows. */
  double *u_20; /* 2 rows. */
  double *x_21; /* 4 rows. */
  double *u_21; /* 2 rows. */
  double *x_22; /* 4 rows. */
  double *u_22; /* 2 rows. */
  double *x_23; /* 4 rows. */
  double *u_23; /* 2 rows. */
  double *x_24; /* 4 rows. */
  double *u_24; /* 2 rows. */
  double *x_25; /* 4 rows. */
  double *u_25; /* 2 rows. */
  double *x_26; /* 4 rows. */
  double *u_26; /* 2 rows. */
  double *x_27; /* 4 rows. */
  double *u_27; /* 2 rows. */
  double *x_28; /* 4 rows. */
  double *u_28; /* 2 rows. */
  double *x_29; /* 4 rows. */
  double *u_29; /* 2 rows. */
  double *x_30; /* 4 rows. */
  double *u_30; /* 2 rows. */
  double *x_31; /* 4 rows. */
  double *u_31; /* 2 rows. */
  double *x_32; /* 4 rows. */
  double *u_32; /* 2 rows. */
  double *x_33; /* 4 rows. */
  double *u_33; /* 2 rows. */
  double *x_34; /* 4 rows. */
  double *u_34; /* 2 rows. */
  double *x_35; /* 4 rows. */
  double *u_35; /* 2 rows. */
  double *x_36; /* 4 rows. */
  double *u_36; /* 2 rows. */
  double *x_37; /* 4 rows. */
  double *u_37; /* 2 rows. */
  double *x_38; /* 4 rows. */
  double *u_38; /* 2 rows. */
  double *x_39; /* 4 rows. */
  double *u_39; /* 2 rows. */
  double *x_40; /* 4 rows. */
  double *u_40; /* 2 rows. */
  double *x_41; /* 4 rows. */
  double *u_41; /* 2 rows. */
  double *x_42; /* 4 rows. */
  double *u_42; /* 2 rows. */
  double *x_43; /* 4 rows. */
  double *u_43; /* 2 rows. */
  double *x_44; /* 4 rows. */
  double *u_44; /* 2 rows. */
  double *x_45; /* 4 rows. */
  double *u[45];
  double *x[46];
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
  double quad_788958081024[1];
  double quad_374560497664[1];
  double quad_606718136320[1];
  double quad_263870058496[1];
  double quad_323313410048[1];
  double quad_835447427072[1];
  double quad_866469752832[1];
  double quad_780297809920[1];
  double quad_929313640448[1];
  double quad_736882544640[1];
  double quad_685030031360[1];
  double quad_256231362560[1];
  double quad_239472939008[1];
  double quad_678005088256[1];
  double quad_67476746240[1];
  double quad_41528709120[1];
  double quad_914721599488[1];
  double quad_938668638208[1];
  double quad_200827822080[1];
  double quad_964538445824[1];
  double quad_498086375424[1];
  double quad_166526738432[1];
  double quad_849159483392[1];
  double quad_192161705984[1];
  double quad_727999463424[1];
  double quad_512511655936[1];
  double quad_484104499200[1];
  double quad_857027723264[1];
  double quad_49952149504[1];
  double quad_977066876928[1];
  double quad_554623475712[1];
  double quad_468130324480[1];
  double quad_112549814272[1];
  double quad_864864751616[1];
  double quad_885212905472[1];
  double quad_527754874880[1];
  double quad_542107860992[1];
  double quad_761311268864[1];
  double quad_434894467072[1];
  double quad_288263913472[1];
  double quad_934005862400[1];
  double quad_490908278784[1];
  double quad_401341784064[1];
  double quad_737798402048[1];
  double quad_431452737536[1];
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
