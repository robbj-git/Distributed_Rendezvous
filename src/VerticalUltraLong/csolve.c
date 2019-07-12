/* Produced by CVXGEN, 2019-05-01 05:35:47 -0400.  */
/* CVXGEN is Copyright (C) 2006-2017 Jacob Mattingley, jem@cvxgen.com. */
/* The code in this file is Copyright (C) 2006-2017 Jacob Mattingley. */
/* CVXGEN, or solvers produced by CVXGEN, cannot be used for commercial */
/* applications without prior written permission from Jacob Mattingley. */

/* Filename: csolve.c. */
/* Description: mex-able file for running cvxgen solver. */
#include "mex.h"
#include "solver.h"
Vars vars;
Params params;
Workspace work;
Settings settings;
void mexFunction(int nlhs, mxArray *plhs[], int nrhs, const mxArray *prhs[]) {
  int i, j;
  mxArray *xm, *cell, *xm_cell;
  double *src;
  double *dest;
  double *dest_cell;
  int valid_vars;
  int steps;
  int this_var_errors;
  int warned_diags;
  int prepare_for_c = 0;
  int extra_solves;
  const char *status_names[] = {"optval", "gap", "steps", "converged"};
  mwSize dims1x1of1[1] = {1};
  mwSize dims[1];
  const char *var_names[] = {"u_0", "u_1", "u_2", "u_3", "u_4", "u_5", "u_6", "u_7", "u_8", "u_9", "u_10", "u_11", "u_12", "u_13", "u_14", "u_15", "u_16", "u_17", "u_18", "u_19", "u_20", "u_21", "u_22", "u_23", "u_24", "u_25", "u_26", "u_27", "u_28", "u_29", "u_30", "u_31", "u_32", "u_33", "u_34", "u_35", "u_36", "u_37", "u_38", "u_39", "u_40", "u_41", "u_42", "u_43", "u_44", "u_45", "u_46", "u_47", "u_48", "u_49", "u_50", "u_51", "u_52", "u_53", "u_54", "u_55", "u_56", "u_57", "u_58", "u_59", "u_60", "u_61", "u_62", "u_63", "u_64", "u_65", "u_66", "u_67", "u_68", "u_69", "u_70", "u_71", "u_72", "u_73", "u_74", "u_75", "u_76", "u_77", "u_78", "u_79", "u_80", "u_81", "u_82", "u_83", "u_84", "u_85", "u_86", "u_87", "u_88", "u_89", "u_90", "u_91", "u_92", "u_93", "u_94", "u_95", "u_96", "u_97", "u_98", "u_99", "x_1", "x_2", "x_3", "x_4", "x_5", "x_6", "x_7", "x_8", "x_9", "x_10", "x_11", "x_12", "x_13", "x_14", "x_15", "x_16", "x_17", "x_18", "x_19", "x_20", "x_21", "x_22", "x_23", "x_24", "x_25", "x_26", "x_27", "x_28", "x_29", "x_30", "x_31", "x_32", "x_33", "x_34", "x_35", "x_36", "x_37", "x_38", "x_39", "x_40", "x_41", "x_42", "x_43", "x_44", "x_45", "x_46", "x_47", "x_48", "x_49", "x_50", "x_51", "x_52", "x_53", "x_54", "x_55", "x_56", "x_57", "x_58", "x_59", "x_60", "x_61", "x_62", "x_63", "x_64", "x_65", "x_66", "x_67", "x_68", "x_69", "x_70", "x_71", "x_72", "x_73", "x_74", "x_75", "x_76", "x_77", "x_78", "x_79", "x_80", "x_81", "x_82", "x_83", "x_84", "x_85", "x_86", "x_87", "x_88", "x_89", "x_90", "x_91", "x_92", "x_93", "x_94", "x_95", "x_96", "x_97", "x_98", "x_99", "x_100", "u", "x"};
  const int num_var_names = 202;
  /* Avoid compiler warnings of unused variables by using a dummy assignment. */
  warned_diags = j = 0;
  extra_solves = 0;
  set_defaults();
  /* Check we got the right number of arguments. */
  if (nrhs == 0)
    mexErrMsgTxt("Not enough arguments: You need to specify at least the parameters.\n");
  if (nrhs > 1) {
    /* Assume that the second argument is the settings. */
    if (mxGetField(prhs[1], 0, "eps") != NULL)
      settings.eps = *mxGetPr(mxGetField(prhs[1], 0, "eps"));
    if (mxGetField(prhs[1], 0, "max_iters") != NULL)
      settings.max_iters = *mxGetPr(mxGetField(prhs[1], 0, "max_iters"));
    if (mxGetField(prhs[1], 0, "refine_steps") != NULL)
      settings.refine_steps = *mxGetPr(mxGetField(prhs[1], 0, "refine_steps"));
    if (mxGetField(prhs[1], 0, "verbose") != NULL)
      settings.verbose = *mxGetPr(mxGetField(prhs[1], 0, "verbose"));
    if (mxGetField(prhs[1], 0, "better_start") != NULL)
      settings.better_start = *mxGetPr(mxGetField(prhs[1], 0, "better_start"));
    if (mxGetField(prhs[1], 0, "verbose_refinement") != NULL)
      settings.verbose_refinement = *mxGetPr(mxGetField(prhs[1], 0,
            "verbose_refinement"));
    if (mxGetField(prhs[1], 0, "debug") != NULL)
      settings.debug = *mxGetPr(mxGetField(prhs[1], 0, "debug"));
    if (mxGetField(prhs[1], 0, "kkt_reg") != NULL)
      settings.kkt_reg = *mxGetPr(mxGetField(prhs[1], 0, "kkt_reg"));
    if (mxGetField(prhs[1], 0, "s_init") != NULL)
      settings.s_init = *mxGetPr(mxGetField(prhs[1], 0, "s_init"));
    if (mxGetField(prhs[1], 0, "z_init") != NULL)
      settings.z_init = *mxGetPr(mxGetField(prhs[1], 0, "z_init"));
    if (mxGetField(prhs[1], 0, "resid_tol") != NULL)
      settings.resid_tol = *mxGetPr(mxGetField(prhs[1], 0, "resid_tol"));
    if (mxGetField(prhs[1], 0, "extra_solves") != NULL)
      extra_solves = *mxGetPr(mxGetField(prhs[1], 0, "extra_solves"));
    else
      extra_solves = 0;
    if (mxGetField(prhs[1], 0, "prepare_for_c") != NULL)
      prepare_for_c = *mxGetPr(mxGetField(prhs[1], 0, "prepare_for_c"));
  }
  valid_vars = 0;
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "A");
  if (xm == NULL) {
    printf("could not find params.A.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 2))) {
      printf("A must be size (2,2), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter A must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter A must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter A must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.A;
      src = mxGetPr(xm);
      for (i = 0; i < 4; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "B");
  if (xm == NULL) {
    printf("could not find params.B.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 1))) {
      printf("B must be size (2,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter B must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter B must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter B must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.B;
      src = mxGetPr(xm);
      for (i = 0; i < 2; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "P");
  if (xm == NULL) {
    printf("could not find params.P.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 2))) {
      printf("P must be size (2,2), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter P must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter P must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter P must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.P;
      src = mxGetPr(xm);
      for (i = 0; i < 4; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "Q");
  if (xm == NULL) {
    printf("could not find params.Q.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 2))) {
      printf("Q must be size (2,2), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter Q must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter Q must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter Q must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.Q;
      src = mxGetPr(xm);
      for (i = 0; i < 4; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "R");
  if (xm == NULL) {
    printf("could not find params.R.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("R must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter R must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter R must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter R must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.R;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_0");
  if (xm == NULL) {
    printf("could not find params.b_0.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_0 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_0 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_0 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_0 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_0;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_1");
  if (xm == NULL) {
    /* Attempt to pull b_1 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 0);
  }
  if (xm == NULL) {
    printf("could not find params.b_1 or params.b{1}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_1 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_1 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_1 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_1 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_1;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_2");
  if (xm == NULL) {
    /* Attempt to pull b_2 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 1);
  }
  if (xm == NULL) {
    printf("could not find params.b_2 or params.b{2}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_2 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_2 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_2 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_2 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_2;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_3");
  if (xm == NULL) {
    /* Attempt to pull b_3 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 2);
  }
  if (xm == NULL) {
    printf("could not find params.b_3 or params.b{3}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_3 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_3 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_3 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_3 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_3;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_4");
  if (xm == NULL) {
    /* Attempt to pull b_4 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 3);
  }
  if (xm == NULL) {
    printf("could not find params.b_4 or params.b{4}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_4 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_4 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_4 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_4 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_4;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_5");
  if (xm == NULL) {
    /* Attempt to pull b_5 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 4);
  }
  if (xm == NULL) {
    printf("could not find params.b_5 or params.b{5}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_5 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_5 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_5 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_5 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_5;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_6");
  if (xm == NULL) {
    /* Attempt to pull b_6 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 5);
  }
  if (xm == NULL) {
    printf("could not find params.b_6 or params.b{6}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_6 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_6 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_6 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_6 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_6;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_7");
  if (xm == NULL) {
    /* Attempt to pull b_7 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 6);
  }
  if (xm == NULL) {
    printf("could not find params.b_7 or params.b{7}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_7 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_7 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_7 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_7 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_7;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_8");
  if (xm == NULL) {
    /* Attempt to pull b_8 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 7);
  }
  if (xm == NULL) {
    printf("could not find params.b_8 or params.b{8}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_8 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_8 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_8 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_8 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_8;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_9");
  if (xm == NULL) {
    /* Attempt to pull b_9 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 8);
  }
  if (xm == NULL) {
    printf("could not find params.b_9 or params.b{9}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_9 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_9 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_9 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_9 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_9;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_10");
  if (xm == NULL) {
    /* Attempt to pull b_10 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 9);
  }
  if (xm == NULL) {
    printf("could not find params.b_10 or params.b{10}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_10 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_10 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_10 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_10 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_10;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_11");
  if (xm == NULL) {
    /* Attempt to pull b_11 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 10);
  }
  if (xm == NULL) {
    printf("could not find params.b_11 or params.b{11}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_11 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_11 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_11 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_11 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_11;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_12");
  if (xm == NULL) {
    /* Attempt to pull b_12 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 11);
  }
  if (xm == NULL) {
    printf("could not find params.b_12 or params.b{12}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_12 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_12 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_12 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_12 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_12;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_13");
  if (xm == NULL) {
    /* Attempt to pull b_13 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 12);
  }
  if (xm == NULL) {
    printf("could not find params.b_13 or params.b{13}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_13 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_13 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_13 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_13 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_13;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_14");
  if (xm == NULL) {
    /* Attempt to pull b_14 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 13);
  }
  if (xm == NULL) {
    printf("could not find params.b_14 or params.b{14}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_14 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_14 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_14 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_14 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_14;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_15");
  if (xm == NULL) {
    /* Attempt to pull b_15 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 14);
  }
  if (xm == NULL) {
    printf("could not find params.b_15 or params.b{15}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_15 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_15 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_15 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_15 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_15;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_16");
  if (xm == NULL) {
    /* Attempt to pull b_16 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 15);
  }
  if (xm == NULL) {
    printf("could not find params.b_16 or params.b{16}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_16 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_16 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_16 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_16 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_16;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_17");
  if (xm == NULL) {
    /* Attempt to pull b_17 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 16);
  }
  if (xm == NULL) {
    printf("could not find params.b_17 or params.b{17}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_17 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_17 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_17 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_17 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_17;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_18");
  if (xm == NULL) {
    /* Attempt to pull b_18 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 17);
  }
  if (xm == NULL) {
    printf("could not find params.b_18 or params.b{18}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_18 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_18 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_18 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_18 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_18;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_19");
  if (xm == NULL) {
    /* Attempt to pull b_19 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 18);
  }
  if (xm == NULL) {
    printf("could not find params.b_19 or params.b{19}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_19 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_19 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_19 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_19 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_19;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_20");
  if (xm == NULL) {
    /* Attempt to pull b_20 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 19);
  }
  if (xm == NULL) {
    printf("could not find params.b_20 or params.b{20}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_20 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_20 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_20 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_20 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_20;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_21");
  if (xm == NULL) {
    /* Attempt to pull b_21 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 20);
  }
  if (xm == NULL) {
    printf("could not find params.b_21 or params.b{21}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_21 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_21 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_21 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_21 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_21;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_22");
  if (xm == NULL) {
    /* Attempt to pull b_22 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 21);
  }
  if (xm == NULL) {
    printf("could not find params.b_22 or params.b{22}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_22 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_22 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_22 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_22 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_22;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_23");
  if (xm == NULL) {
    /* Attempt to pull b_23 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 22);
  }
  if (xm == NULL) {
    printf("could not find params.b_23 or params.b{23}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_23 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_23 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_23 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_23 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_23;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_24");
  if (xm == NULL) {
    /* Attempt to pull b_24 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 23);
  }
  if (xm == NULL) {
    printf("could not find params.b_24 or params.b{24}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_24 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_24 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_24 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_24 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_24;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_25");
  if (xm == NULL) {
    /* Attempt to pull b_25 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 24);
  }
  if (xm == NULL) {
    printf("could not find params.b_25 or params.b{25}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_25 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_25 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_25 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_25 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_25;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_26");
  if (xm == NULL) {
    /* Attempt to pull b_26 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 25);
  }
  if (xm == NULL) {
    printf("could not find params.b_26 or params.b{26}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_26 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_26 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_26 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_26 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_26;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_27");
  if (xm == NULL) {
    /* Attempt to pull b_27 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 26);
  }
  if (xm == NULL) {
    printf("could not find params.b_27 or params.b{27}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_27 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_27 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_27 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_27 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_27;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_28");
  if (xm == NULL) {
    /* Attempt to pull b_28 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 27);
  }
  if (xm == NULL) {
    printf("could not find params.b_28 or params.b{28}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_28 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_28 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_28 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_28 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_28;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_29");
  if (xm == NULL) {
    /* Attempt to pull b_29 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 28);
  }
  if (xm == NULL) {
    printf("could not find params.b_29 or params.b{29}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_29 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_29 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_29 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_29 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_29;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_30");
  if (xm == NULL) {
    /* Attempt to pull b_30 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 29);
  }
  if (xm == NULL) {
    printf("could not find params.b_30 or params.b{30}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_30 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_30 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_30 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_30 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_30;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_31");
  if (xm == NULL) {
    /* Attempt to pull b_31 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 30);
  }
  if (xm == NULL) {
    printf("could not find params.b_31 or params.b{31}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_31 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_31 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_31 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_31 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_31;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_32");
  if (xm == NULL) {
    /* Attempt to pull b_32 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 31);
  }
  if (xm == NULL) {
    printf("could not find params.b_32 or params.b{32}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_32 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_32 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_32 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_32 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_32;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_33");
  if (xm == NULL) {
    /* Attempt to pull b_33 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 32);
  }
  if (xm == NULL) {
    printf("could not find params.b_33 or params.b{33}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_33 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_33 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_33 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_33 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_33;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_34");
  if (xm == NULL) {
    /* Attempt to pull b_34 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 33);
  }
  if (xm == NULL) {
    printf("could not find params.b_34 or params.b{34}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_34 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_34 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_34 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_34 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_34;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_35");
  if (xm == NULL) {
    /* Attempt to pull b_35 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 34);
  }
  if (xm == NULL) {
    printf("could not find params.b_35 or params.b{35}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_35 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_35 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_35 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_35 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_35;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_36");
  if (xm == NULL) {
    /* Attempt to pull b_36 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 35);
  }
  if (xm == NULL) {
    printf("could not find params.b_36 or params.b{36}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_36 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_36 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_36 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_36 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_36;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_37");
  if (xm == NULL) {
    /* Attempt to pull b_37 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 36);
  }
  if (xm == NULL) {
    printf("could not find params.b_37 or params.b{37}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_37 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_37 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_37 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_37 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_37;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_38");
  if (xm == NULL) {
    /* Attempt to pull b_38 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 37);
  }
  if (xm == NULL) {
    printf("could not find params.b_38 or params.b{38}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_38 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_38 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_38 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_38 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_38;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_39");
  if (xm == NULL) {
    /* Attempt to pull b_39 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 38);
  }
  if (xm == NULL) {
    printf("could not find params.b_39 or params.b{39}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_39 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_39 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_39 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_39 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_39;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_40");
  if (xm == NULL) {
    /* Attempt to pull b_40 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 39);
  }
  if (xm == NULL) {
    printf("could not find params.b_40 or params.b{40}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_40 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_40 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_40 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_40 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_40;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_41");
  if (xm == NULL) {
    /* Attempt to pull b_41 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 40);
  }
  if (xm == NULL) {
    printf("could not find params.b_41 or params.b{41}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_41 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_41 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_41 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_41 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_41;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_42");
  if (xm == NULL) {
    /* Attempt to pull b_42 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 41);
  }
  if (xm == NULL) {
    printf("could not find params.b_42 or params.b{42}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_42 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_42 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_42 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_42 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_42;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_43");
  if (xm == NULL) {
    /* Attempt to pull b_43 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 42);
  }
  if (xm == NULL) {
    printf("could not find params.b_43 or params.b{43}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_43 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_43 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_43 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_43 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_43;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_44");
  if (xm == NULL) {
    /* Attempt to pull b_44 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 43);
  }
  if (xm == NULL) {
    printf("could not find params.b_44 or params.b{44}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_44 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_44 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_44 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_44 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_44;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_45");
  if (xm == NULL) {
    /* Attempt to pull b_45 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 44);
  }
  if (xm == NULL) {
    printf("could not find params.b_45 or params.b{45}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_45 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_45 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_45 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_45 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_45;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_46");
  if (xm == NULL) {
    /* Attempt to pull b_46 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 45);
  }
  if (xm == NULL) {
    printf("could not find params.b_46 or params.b{46}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_46 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_46 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_46 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_46 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_46;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_47");
  if (xm == NULL) {
    /* Attempt to pull b_47 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 46);
  }
  if (xm == NULL) {
    printf("could not find params.b_47 or params.b{47}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_47 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_47 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_47 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_47 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_47;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_48");
  if (xm == NULL) {
    /* Attempt to pull b_48 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 47);
  }
  if (xm == NULL) {
    printf("could not find params.b_48 or params.b{48}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_48 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_48 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_48 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_48 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_48;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_49");
  if (xm == NULL) {
    /* Attempt to pull b_49 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 48);
  }
  if (xm == NULL) {
    printf("could not find params.b_49 or params.b{49}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_49 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_49 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_49 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_49 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_49;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_50");
  if (xm == NULL) {
    /* Attempt to pull b_50 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 49);
  }
  if (xm == NULL) {
    printf("could not find params.b_50 or params.b{50}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_50 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_50 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_50 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_50 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_50;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_51");
  if (xm == NULL) {
    /* Attempt to pull b_51 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 50);
  }
  if (xm == NULL) {
    printf("could not find params.b_51 or params.b{51}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_51 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_51 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_51 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_51 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_51;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_52");
  if (xm == NULL) {
    /* Attempt to pull b_52 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 51);
  }
  if (xm == NULL) {
    printf("could not find params.b_52 or params.b{52}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_52 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_52 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_52 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_52 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_52;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_53");
  if (xm == NULL) {
    /* Attempt to pull b_53 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 52);
  }
  if (xm == NULL) {
    printf("could not find params.b_53 or params.b{53}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_53 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_53 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_53 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_53 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_53;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_54");
  if (xm == NULL) {
    /* Attempt to pull b_54 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 53);
  }
  if (xm == NULL) {
    printf("could not find params.b_54 or params.b{54}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_54 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_54 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_54 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_54 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_54;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_55");
  if (xm == NULL) {
    /* Attempt to pull b_55 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 54);
  }
  if (xm == NULL) {
    printf("could not find params.b_55 or params.b{55}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_55 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_55 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_55 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_55 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_55;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_56");
  if (xm == NULL) {
    /* Attempt to pull b_56 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 55);
  }
  if (xm == NULL) {
    printf("could not find params.b_56 or params.b{56}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_56 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_56 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_56 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_56 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_56;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_57");
  if (xm == NULL) {
    /* Attempt to pull b_57 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 56);
  }
  if (xm == NULL) {
    printf("could not find params.b_57 or params.b{57}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_57 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_57 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_57 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_57 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_57;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_58");
  if (xm == NULL) {
    /* Attempt to pull b_58 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 57);
  }
  if (xm == NULL) {
    printf("could not find params.b_58 or params.b{58}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_58 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_58 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_58 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_58 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_58;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_59");
  if (xm == NULL) {
    /* Attempt to pull b_59 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 58);
  }
  if (xm == NULL) {
    printf("could not find params.b_59 or params.b{59}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_59 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_59 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_59 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_59 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_59;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_60");
  if (xm == NULL) {
    /* Attempt to pull b_60 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 59);
  }
  if (xm == NULL) {
    printf("could not find params.b_60 or params.b{60}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_60 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_60 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_60 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_60 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_60;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_61");
  if (xm == NULL) {
    /* Attempt to pull b_61 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 60);
  }
  if (xm == NULL) {
    printf("could not find params.b_61 or params.b{61}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_61 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_61 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_61 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_61 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_61;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_62");
  if (xm == NULL) {
    /* Attempt to pull b_62 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 61);
  }
  if (xm == NULL) {
    printf("could not find params.b_62 or params.b{62}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_62 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_62 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_62 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_62 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_62;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_63");
  if (xm == NULL) {
    /* Attempt to pull b_63 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 62);
  }
  if (xm == NULL) {
    printf("could not find params.b_63 or params.b{63}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_63 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_63 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_63 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_63 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_63;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_64");
  if (xm == NULL) {
    /* Attempt to pull b_64 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 63);
  }
  if (xm == NULL) {
    printf("could not find params.b_64 or params.b{64}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_64 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_64 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_64 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_64 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_64;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_65");
  if (xm == NULL) {
    /* Attempt to pull b_65 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 64);
  }
  if (xm == NULL) {
    printf("could not find params.b_65 or params.b{65}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_65 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_65 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_65 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_65 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_65;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_66");
  if (xm == NULL) {
    /* Attempt to pull b_66 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 65);
  }
  if (xm == NULL) {
    printf("could not find params.b_66 or params.b{66}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_66 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_66 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_66 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_66 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_66;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_67");
  if (xm == NULL) {
    /* Attempt to pull b_67 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 66);
  }
  if (xm == NULL) {
    printf("could not find params.b_67 or params.b{67}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_67 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_67 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_67 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_67 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_67;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_68");
  if (xm == NULL) {
    /* Attempt to pull b_68 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 67);
  }
  if (xm == NULL) {
    printf("could not find params.b_68 or params.b{68}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_68 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_68 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_68 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_68 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_68;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_69");
  if (xm == NULL) {
    /* Attempt to pull b_69 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 68);
  }
  if (xm == NULL) {
    printf("could not find params.b_69 or params.b{69}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_69 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_69 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_69 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_69 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_69;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_70");
  if (xm == NULL) {
    /* Attempt to pull b_70 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 69);
  }
  if (xm == NULL) {
    printf("could not find params.b_70 or params.b{70}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_70 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_70 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_70 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_70 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_70;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_71");
  if (xm == NULL) {
    /* Attempt to pull b_71 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 70);
  }
  if (xm == NULL) {
    printf("could not find params.b_71 or params.b{71}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_71 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_71 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_71 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_71 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_71;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_72");
  if (xm == NULL) {
    /* Attempt to pull b_72 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 71);
  }
  if (xm == NULL) {
    printf("could not find params.b_72 or params.b{72}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_72 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_72 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_72 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_72 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_72;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_73");
  if (xm == NULL) {
    /* Attempt to pull b_73 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 72);
  }
  if (xm == NULL) {
    printf("could not find params.b_73 or params.b{73}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_73 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_73 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_73 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_73 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_73;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_74");
  if (xm == NULL) {
    /* Attempt to pull b_74 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 73);
  }
  if (xm == NULL) {
    printf("could not find params.b_74 or params.b{74}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_74 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_74 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_74 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_74 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_74;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_75");
  if (xm == NULL) {
    /* Attempt to pull b_75 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 74);
  }
  if (xm == NULL) {
    printf("could not find params.b_75 or params.b{75}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_75 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_75 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_75 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_75 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_75;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_76");
  if (xm == NULL) {
    /* Attempt to pull b_76 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 75);
  }
  if (xm == NULL) {
    printf("could not find params.b_76 or params.b{76}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_76 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_76 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_76 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_76 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_76;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_77");
  if (xm == NULL) {
    /* Attempt to pull b_77 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 76);
  }
  if (xm == NULL) {
    printf("could not find params.b_77 or params.b{77}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_77 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_77 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_77 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_77 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_77;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_78");
  if (xm == NULL) {
    /* Attempt to pull b_78 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 77);
  }
  if (xm == NULL) {
    printf("could not find params.b_78 or params.b{78}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_78 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_78 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_78 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_78 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_78;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_79");
  if (xm == NULL) {
    /* Attempt to pull b_79 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 78);
  }
  if (xm == NULL) {
    printf("could not find params.b_79 or params.b{79}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_79 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_79 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_79 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_79 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_79;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_80");
  if (xm == NULL) {
    /* Attempt to pull b_80 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 79);
  }
  if (xm == NULL) {
    printf("could not find params.b_80 or params.b{80}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_80 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_80 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_80 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_80 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_80;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_81");
  if (xm == NULL) {
    /* Attempt to pull b_81 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 80);
  }
  if (xm == NULL) {
    printf("could not find params.b_81 or params.b{81}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_81 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_81 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_81 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_81 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_81;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_82");
  if (xm == NULL) {
    /* Attempt to pull b_82 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 81);
  }
  if (xm == NULL) {
    printf("could not find params.b_82 or params.b{82}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_82 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_82 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_82 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_82 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_82;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_83");
  if (xm == NULL) {
    /* Attempt to pull b_83 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 82);
  }
  if (xm == NULL) {
    printf("could not find params.b_83 or params.b{83}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_83 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_83 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_83 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_83 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_83;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_84");
  if (xm == NULL) {
    /* Attempt to pull b_84 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 83);
  }
  if (xm == NULL) {
    printf("could not find params.b_84 or params.b{84}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_84 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_84 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_84 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_84 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_84;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_85");
  if (xm == NULL) {
    /* Attempt to pull b_85 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 84);
  }
  if (xm == NULL) {
    printf("could not find params.b_85 or params.b{85}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_85 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_85 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_85 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_85 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_85;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_86");
  if (xm == NULL) {
    /* Attempt to pull b_86 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 85);
  }
  if (xm == NULL) {
    printf("could not find params.b_86 or params.b{86}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_86 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_86 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_86 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_86 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_86;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_87");
  if (xm == NULL) {
    /* Attempt to pull b_87 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 86);
  }
  if (xm == NULL) {
    printf("could not find params.b_87 or params.b{87}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_87 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_87 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_87 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_87 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_87;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_88");
  if (xm == NULL) {
    /* Attempt to pull b_88 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 87);
  }
  if (xm == NULL) {
    printf("could not find params.b_88 or params.b{88}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_88 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_88 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_88 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_88 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_88;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_89");
  if (xm == NULL) {
    /* Attempt to pull b_89 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 88);
  }
  if (xm == NULL) {
    printf("could not find params.b_89 or params.b{89}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_89 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_89 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_89 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_89 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_89;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_90");
  if (xm == NULL) {
    /* Attempt to pull b_90 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 89);
  }
  if (xm == NULL) {
    printf("could not find params.b_90 or params.b{90}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_90 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_90 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_90 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_90 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_90;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_91");
  if (xm == NULL) {
    /* Attempt to pull b_91 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 90);
  }
  if (xm == NULL) {
    printf("could not find params.b_91 or params.b{91}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_91 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_91 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_91 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_91 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_91;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_92");
  if (xm == NULL) {
    /* Attempt to pull b_92 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 91);
  }
  if (xm == NULL) {
    printf("could not find params.b_92 or params.b{92}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_92 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_92 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_92 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_92 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_92;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_93");
  if (xm == NULL) {
    /* Attempt to pull b_93 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 92);
  }
  if (xm == NULL) {
    printf("could not find params.b_93 or params.b{93}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_93 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_93 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_93 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_93 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_93;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_94");
  if (xm == NULL) {
    /* Attempt to pull b_94 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 93);
  }
  if (xm == NULL) {
    printf("could not find params.b_94 or params.b{94}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_94 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_94 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_94 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_94 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_94;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_95");
  if (xm == NULL) {
    /* Attempt to pull b_95 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 94);
  }
  if (xm == NULL) {
    printf("could not find params.b_95 or params.b{95}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_95 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_95 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_95 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_95 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_95;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_96");
  if (xm == NULL) {
    /* Attempt to pull b_96 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 95);
  }
  if (xm == NULL) {
    printf("could not find params.b_96 or params.b{96}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_96 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_96 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_96 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_96 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_96;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_97");
  if (xm == NULL) {
    /* Attempt to pull b_97 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 96);
  }
  if (xm == NULL) {
    printf("could not find params.b_97 or params.b{97}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_97 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_97 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_97 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_97 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_97;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_98");
  if (xm == NULL) {
    /* Attempt to pull b_98 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 97);
  }
  if (xm == NULL) {
    printf("could not find params.b_98 or params.b{98}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_98 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_98 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_98 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_98 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_98;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_99");
  if (xm == NULL) {
    /* Attempt to pull b_99 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 98);
  }
  if (xm == NULL) {
    printf("could not find params.b_99 or params.b{99}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_99 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_99 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_99 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_99 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_99;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "b_100");
  if (xm == NULL) {
    /* Attempt to pull b_100 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "b");
    if (cell != NULL)
      xm = mxGetCell(cell, 99);
  }
  if (xm == NULL) {
    printf("could not find params.b_100 or params.b{100}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("b_100 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter b_100 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter b_100 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter b_100 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.b_100;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_1");
  if (xm == NULL) {
    /* Attempt to pull dist_1 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 0);
  }
  if (xm == NULL) {
    printf("could not find params.dist_1 or params.dist{1}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_1 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_1 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_1 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_1 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_1;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_2");
  if (xm == NULL) {
    /* Attempt to pull dist_2 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 1);
  }
  if (xm == NULL) {
    printf("could not find params.dist_2 or params.dist{2}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_2 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_2 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_2 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_2 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_2;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_3");
  if (xm == NULL) {
    /* Attempt to pull dist_3 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 2);
  }
  if (xm == NULL) {
    printf("could not find params.dist_3 or params.dist{3}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_3 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_3 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_3 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_3 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_3;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_4");
  if (xm == NULL) {
    /* Attempt to pull dist_4 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 3);
  }
  if (xm == NULL) {
    printf("could not find params.dist_4 or params.dist{4}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_4 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_4 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_4 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_4 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_4;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_5");
  if (xm == NULL) {
    /* Attempt to pull dist_5 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 4);
  }
  if (xm == NULL) {
    printf("could not find params.dist_5 or params.dist{5}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_5 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_5 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_5 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_5 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_5;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_6");
  if (xm == NULL) {
    /* Attempt to pull dist_6 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 5);
  }
  if (xm == NULL) {
    printf("could not find params.dist_6 or params.dist{6}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_6 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_6 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_6 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_6 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_6;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_7");
  if (xm == NULL) {
    /* Attempt to pull dist_7 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 6);
  }
  if (xm == NULL) {
    printf("could not find params.dist_7 or params.dist{7}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_7 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_7 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_7 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_7 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_7;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_8");
  if (xm == NULL) {
    /* Attempt to pull dist_8 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 7);
  }
  if (xm == NULL) {
    printf("could not find params.dist_8 or params.dist{8}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_8 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_8 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_8 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_8 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_8;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_9");
  if (xm == NULL) {
    /* Attempt to pull dist_9 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 8);
  }
  if (xm == NULL) {
    printf("could not find params.dist_9 or params.dist{9}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_9 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_9 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_9 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_9 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_9;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_10");
  if (xm == NULL) {
    /* Attempt to pull dist_10 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 9);
  }
  if (xm == NULL) {
    printf("could not find params.dist_10 or params.dist{10}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_10 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_10 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_10 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_10 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_10;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_11");
  if (xm == NULL) {
    /* Attempt to pull dist_11 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 10);
  }
  if (xm == NULL) {
    printf("could not find params.dist_11 or params.dist{11}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_11 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_11 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_11 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_11 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_11;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_12");
  if (xm == NULL) {
    /* Attempt to pull dist_12 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 11);
  }
  if (xm == NULL) {
    printf("could not find params.dist_12 or params.dist{12}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_12 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_12 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_12 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_12 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_12;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_13");
  if (xm == NULL) {
    /* Attempt to pull dist_13 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 12);
  }
  if (xm == NULL) {
    printf("could not find params.dist_13 or params.dist{13}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_13 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_13 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_13 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_13 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_13;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_14");
  if (xm == NULL) {
    /* Attempt to pull dist_14 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 13);
  }
  if (xm == NULL) {
    printf("could not find params.dist_14 or params.dist{14}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_14 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_14 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_14 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_14 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_14;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_15");
  if (xm == NULL) {
    /* Attempt to pull dist_15 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 14);
  }
  if (xm == NULL) {
    printf("could not find params.dist_15 or params.dist{15}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_15 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_15 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_15 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_15 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_15;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_16");
  if (xm == NULL) {
    /* Attempt to pull dist_16 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 15);
  }
  if (xm == NULL) {
    printf("could not find params.dist_16 or params.dist{16}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_16 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_16 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_16 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_16 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_16;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_17");
  if (xm == NULL) {
    /* Attempt to pull dist_17 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 16);
  }
  if (xm == NULL) {
    printf("could not find params.dist_17 or params.dist{17}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_17 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_17 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_17 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_17 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_17;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_18");
  if (xm == NULL) {
    /* Attempt to pull dist_18 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 17);
  }
  if (xm == NULL) {
    printf("could not find params.dist_18 or params.dist{18}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_18 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_18 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_18 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_18 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_18;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_19");
  if (xm == NULL) {
    /* Attempt to pull dist_19 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 18);
  }
  if (xm == NULL) {
    printf("could not find params.dist_19 or params.dist{19}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_19 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_19 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_19 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_19 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_19;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_20");
  if (xm == NULL) {
    /* Attempt to pull dist_20 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 19);
  }
  if (xm == NULL) {
    printf("could not find params.dist_20 or params.dist{20}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_20 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_20 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_20 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_20 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_20;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_21");
  if (xm == NULL) {
    /* Attempt to pull dist_21 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 20);
  }
  if (xm == NULL) {
    printf("could not find params.dist_21 or params.dist{21}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_21 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_21 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_21 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_21 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_21;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_22");
  if (xm == NULL) {
    /* Attempt to pull dist_22 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 21);
  }
  if (xm == NULL) {
    printf("could not find params.dist_22 or params.dist{22}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_22 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_22 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_22 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_22 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_22;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_23");
  if (xm == NULL) {
    /* Attempt to pull dist_23 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 22);
  }
  if (xm == NULL) {
    printf("could not find params.dist_23 or params.dist{23}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_23 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_23 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_23 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_23 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_23;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_24");
  if (xm == NULL) {
    /* Attempt to pull dist_24 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 23);
  }
  if (xm == NULL) {
    printf("could not find params.dist_24 or params.dist{24}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_24 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_24 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_24 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_24 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_24;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_25");
  if (xm == NULL) {
    /* Attempt to pull dist_25 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 24);
  }
  if (xm == NULL) {
    printf("could not find params.dist_25 or params.dist{25}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_25 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_25 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_25 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_25 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_25;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_26");
  if (xm == NULL) {
    /* Attempt to pull dist_26 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 25);
  }
  if (xm == NULL) {
    printf("could not find params.dist_26 or params.dist{26}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_26 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_26 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_26 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_26 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_26;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_27");
  if (xm == NULL) {
    /* Attempt to pull dist_27 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 26);
  }
  if (xm == NULL) {
    printf("could not find params.dist_27 or params.dist{27}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_27 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_27 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_27 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_27 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_27;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_28");
  if (xm == NULL) {
    /* Attempt to pull dist_28 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 27);
  }
  if (xm == NULL) {
    printf("could not find params.dist_28 or params.dist{28}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_28 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_28 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_28 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_28 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_28;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_29");
  if (xm == NULL) {
    /* Attempt to pull dist_29 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 28);
  }
  if (xm == NULL) {
    printf("could not find params.dist_29 or params.dist{29}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_29 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_29 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_29 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_29 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_29;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_30");
  if (xm == NULL) {
    /* Attempt to pull dist_30 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 29);
  }
  if (xm == NULL) {
    printf("could not find params.dist_30 or params.dist{30}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_30 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_30 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_30 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_30 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_30;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_31");
  if (xm == NULL) {
    /* Attempt to pull dist_31 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 30);
  }
  if (xm == NULL) {
    printf("could not find params.dist_31 or params.dist{31}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_31 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_31 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_31 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_31 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_31;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_32");
  if (xm == NULL) {
    /* Attempt to pull dist_32 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 31);
  }
  if (xm == NULL) {
    printf("could not find params.dist_32 or params.dist{32}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_32 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_32 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_32 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_32 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_32;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_33");
  if (xm == NULL) {
    /* Attempt to pull dist_33 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 32);
  }
  if (xm == NULL) {
    printf("could not find params.dist_33 or params.dist{33}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_33 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_33 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_33 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_33 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_33;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_34");
  if (xm == NULL) {
    /* Attempt to pull dist_34 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 33);
  }
  if (xm == NULL) {
    printf("could not find params.dist_34 or params.dist{34}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_34 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_34 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_34 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_34 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_34;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_35");
  if (xm == NULL) {
    /* Attempt to pull dist_35 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 34);
  }
  if (xm == NULL) {
    printf("could not find params.dist_35 or params.dist{35}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_35 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_35 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_35 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_35 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_35;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_36");
  if (xm == NULL) {
    /* Attempt to pull dist_36 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 35);
  }
  if (xm == NULL) {
    printf("could not find params.dist_36 or params.dist{36}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_36 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_36 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_36 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_36 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_36;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_37");
  if (xm == NULL) {
    /* Attempt to pull dist_37 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 36);
  }
  if (xm == NULL) {
    printf("could not find params.dist_37 or params.dist{37}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_37 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_37 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_37 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_37 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_37;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_38");
  if (xm == NULL) {
    /* Attempt to pull dist_38 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 37);
  }
  if (xm == NULL) {
    printf("could not find params.dist_38 or params.dist{38}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_38 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_38 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_38 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_38 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_38;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_39");
  if (xm == NULL) {
    /* Attempt to pull dist_39 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 38);
  }
  if (xm == NULL) {
    printf("could not find params.dist_39 or params.dist{39}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_39 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_39 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_39 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_39 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_39;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_40");
  if (xm == NULL) {
    /* Attempt to pull dist_40 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 39);
  }
  if (xm == NULL) {
    printf("could not find params.dist_40 or params.dist{40}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_40 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_40 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_40 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_40 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_40;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_41");
  if (xm == NULL) {
    /* Attempt to pull dist_41 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 40);
  }
  if (xm == NULL) {
    printf("could not find params.dist_41 or params.dist{41}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_41 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_41 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_41 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_41 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_41;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_42");
  if (xm == NULL) {
    /* Attempt to pull dist_42 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 41);
  }
  if (xm == NULL) {
    printf("could not find params.dist_42 or params.dist{42}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_42 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_42 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_42 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_42 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_42;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_43");
  if (xm == NULL) {
    /* Attempt to pull dist_43 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 42);
  }
  if (xm == NULL) {
    printf("could not find params.dist_43 or params.dist{43}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_43 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_43 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_43 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_43 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_43;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_44");
  if (xm == NULL) {
    /* Attempt to pull dist_44 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 43);
  }
  if (xm == NULL) {
    printf("could not find params.dist_44 or params.dist{44}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_44 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_44 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_44 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_44 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_44;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_45");
  if (xm == NULL) {
    /* Attempt to pull dist_45 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 44);
  }
  if (xm == NULL) {
    printf("could not find params.dist_45 or params.dist{45}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_45 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_45 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_45 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_45 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_45;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_46");
  if (xm == NULL) {
    /* Attempt to pull dist_46 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 45);
  }
  if (xm == NULL) {
    printf("could not find params.dist_46 or params.dist{46}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_46 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_46 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_46 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_46 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_46;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_47");
  if (xm == NULL) {
    /* Attempt to pull dist_47 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 46);
  }
  if (xm == NULL) {
    printf("could not find params.dist_47 or params.dist{47}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_47 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_47 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_47 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_47 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_47;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_48");
  if (xm == NULL) {
    /* Attempt to pull dist_48 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 47);
  }
  if (xm == NULL) {
    printf("could not find params.dist_48 or params.dist{48}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_48 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_48 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_48 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_48 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_48;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_49");
  if (xm == NULL) {
    /* Attempt to pull dist_49 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 48);
  }
  if (xm == NULL) {
    printf("could not find params.dist_49 or params.dist{49}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_49 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_49 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_49 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_49 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_49;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_50");
  if (xm == NULL) {
    /* Attempt to pull dist_50 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 49);
  }
  if (xm == NULL) {
    printf("could not find params.dist_50 or params.dist{50}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_50 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_50 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_50 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_50 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_50;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_51");
  if (xm == NULL) {
    /* Attempt to pull dist_51 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 50);
  }
  if (xm == NULL) {
    printf("could not find params.dist_51 or params.dist{51}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_51 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_51 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_51 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_51 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_51;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_52");
  if (xm == NULL) {
    /* Attempt to pull dist_52 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 51);
  }
  if (xm == NULL) {
    printf("could not find params.dist_52 or params.dist{52}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_52 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_52 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_52 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_52 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_52;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_53");
  if (xm == NULL) {
    /* Attempt to pull dist_53 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 52);
  }
  if (xm == NULL) {
    printf("could not find params.dist_53 or params.dist{53}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_53 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_53 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_53 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_53 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_53;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_54");
  if (xm == NULL) {
    /* Attempt to pull dist_54 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 53);
  }
  if (xm == NULL) {
    printf("could not find params.dist_54 or params.dist{54}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_54 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_54 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_54 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_54 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_54;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_55");
  if (xm == NULL) {
    /* Attempt to pull dist_55 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 54);
  }
  if (xm == NULL) {
    printf("could not find params.dist_55 or params.dist{55}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_55 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_55 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_55 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_55 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_55;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_56");
  if (xm == NULL) {
    /* Attempt to pull dist_56 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 55);
  }
  if (xm == NULL) {
    printf("could not find params.dist_56 or params.dist{56}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_56 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_56 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_56 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_56 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_56;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_57");
  if (xm == NULL) {
    /* Attempt to pull dist_57 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 56);
  }
  if (xm == NULL) {
    printf("could not find params.dist_57 or params.dist{57}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_57 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_57 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_57 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_57 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_57;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_58");
  if (xm == NULL) {
    /* Attempt to pull dist_58 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 57);
  }
  if (xm == NULL) {
    printf("could not find params.dist_58 or params.dist{58}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_58 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_58 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_58 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_58 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_58;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_59");
  if (xm == NULL) {
    /* Attempt to pull dist_59 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 58);
  }
  if (xm == NULL) {
    printf("could not find params.dist_59 or params.dist{59}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_59 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_59 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_59 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_59 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_59;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_60");
  if (xm == NULL) {
    /* Attempt to pull dist_60 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 59);
  }
  if (xm == NULL) {
    printf("could not find params.dist_60 or params.dist{60}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_60 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_60 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_60 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_60 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_60;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_61");
  if (xm == NULL) {
    /* Attempt to pull dist_61 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 60);
  }
  if (xm == NULL) {
    printf("could not find params.dist_61 or params.dist{61}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_61 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_61 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_61 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_61 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_61;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_62");
  if (xm == NULL) {
    /* Attempt to pull dist_62 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 61);
  }
  if (xm == NULL) {
    printf("could not find params.dist_62 or params.dist{62}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_62 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_62 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_62 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_62 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_62;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_63");
  if (xm == NULL) {
    /* Attempt to pull dist_63 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 62);
  }
  if (xm == NULL) {
    printf("could not find params.dist_63 or params.dist{63}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_63 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_63 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_63 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_63 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_63;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_64");
  if (xm == NULL) {
    /* Attempt to pull dist_64 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 63);
  }
  if (xm == NULL) {
    printf("could not find params.dist_64 or params.dist{64}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_64 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_64 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_64 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_64 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_64;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_65");
  if (xm == NULL) {
    /* Attempt to pull dist_65 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 64);
  }
  if (xm == NULL) {
    printf("could not find params.dist_65 or params.dist{65}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_65 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_65 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_65 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_65 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_65;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_66");
  if (xm == NULL) {
    /* Attempt to pull dist_66 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 65);
  }
  if (xm == NULL) {
    printf("could not find params.dist_66 or params.dist{66}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_66 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_66 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_66 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_66 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_66;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_67");
  if (xm == NULL) {
    /* Attempt to pull dist_67 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 66);
  }
  if (xm == NULL) {
    printf("could not find params.dist_67 or params.dist{67}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_67 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_67 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_67 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_67 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_67;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_68");
  if (xm == NULL) {
    /* Attempt to pull dist_68 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 67);
  }
  if (xm == NULL) {
    printf("could not find params.dist_68 or params.dist{68}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_68 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_68 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_68 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_68 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_68;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_69");
  if (xm == NULL) {
    /* Attempt to pull dist_69 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 68);
  }
  if (xm == NULL) {
    printf("could not find params.dist_69 or params.dist{69}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_69 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_69 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_69 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_69 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_69;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_70");
  if (xm == NULL) {
    /* Attempt to pull dist_70 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 69);
  }
  if (xm == NULL) {
    printf("could not find params.dist_70 or params.dist{70}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_70 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_70 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_70 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_70 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_70;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_71");
  if (xm == NULL) {
    /* Attempt to pull dist_71 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 70);
  }
  if (xm == NULL) {
    printf("could not find params.dist_71 or params.dist{71}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_71 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_71 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_71 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_71 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_71;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_72");
  if (xm == NULL) {
    /* Attempt to pull dist_72 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 71);
  }
  if (xm == NULL) {
    printf("could not find params.dist_72 or params.dist{72}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_72 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_72 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_72 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_72 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_72;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_73");
  if (xm == NULL) {
    /* Attempt to pull dist_73 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 72);
  }
  if (xm == NULL) {
    printf("could not find params.dist_73 or params.dist{73}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_73 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_73 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_73 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_73 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_73;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_74");
  if (xm == NULL) {
    /* Attempt to pull dist_74 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 73);
  }
  if (xm == NULL) {
    printf("could not find params.dist_74 or params.dist{74}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_74 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_74 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_74 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_74 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_74;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_75");
  if (xm == NULL) {
    /* Attempt to pull dist_75 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 74);
  }
  if (xm == NULL) {
    printf("could not find params.dist_75 or params.dist{75}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_75 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_75 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_75 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_75 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_75;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_76");
  if (xm == NULL) {
    /* Attempt to pull dist_76 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 75);
  }
  if (xm == NULL) {
    printf("could not find params.dist_76 or params.dist{76}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_76 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_76 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_76 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_76 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_76;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_77");
  if (xm == NULL) {
    /* Attempt to pull dist_77 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 76);
  }
  if (xm == NULL) {
    printf("could not find params.dist_77 or params.dist{77}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_77 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_77 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_77 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_77 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_77;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_78");
  if (xm == NULL) {
    /* Attempt to pull dist_78 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 77);
  }
  if (xm == NULL) {
    printf("could not find params.dist_78 or params.dist{78}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_78 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_78 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_78 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_78 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_78;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_79");
  if (xm == NULL) {
    /* Attempt to pull dist_79 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 78);
  }
  if (xm == NULL) {
    printf("could not find params.dist_79 or params.dist{79}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_79 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_79 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_79 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_79 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_79;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_80");
  if (xm == NULL) {
    /* Attempt to pull dist_80 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 79);
  }
  if (xm == NULL) {
    printf("could not find params.dist_80 or params.dist{80}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_80 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_80 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_80 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_80 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_80;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_81");
  if (xm == NULL) {
    /* Attempt to pull dist_81 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 80);
  }
  if (xm == NULL) {
    printf("could not find params.dist_81 or params.dist{81}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_81 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_81 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_81 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_81 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_81;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_82");
  if (xm == NULL) {
    /* Attempt to pull dist_82 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 81);
  }
  if (xm == NULL) {
    printf("could not find params.dist_82 or params.dist{82}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_82 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_82 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_82 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_82 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_82;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_83");
  if (xm == NULL) {
    /* Attempt to pull dist_83 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 82);
  }
  if (xm == NULL) {
    printf("could not find params.dist_83 or params.dist{83}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_83 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_83 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_83 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_83 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_83;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_84");
  if (xm == NULL) {
    /* Attempt to pull dist_84 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 83);
  }
  if (xm == NULL) {
    printf("could not find params.dist_84 or params.dist{84}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_84 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_84 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_84 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_84 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_84;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_85");
  if (xm == NULL) {
    /* Attempt to pull dist_85 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 84);
  }
  if (xm == NULL) {
    printf("could not find params.dist_85 or params.dist{85}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_85 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_85 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_85 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_85 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_85;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_86");
  if (xm == NULL) {
    /* Attempt to pull dist_86 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 85);
  }
  if (xm == NULL) {
    printf("could not find params.dist_86 or params.dist{86}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_86 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_86 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_86 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_86 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_86;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_87");
  if (xm == NULL) {
    /* Attempt to pull dist_87 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 86);
  }
  if (xm == NULL) {
    printf("could not find params.dist_87 or params.dist{87}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_87 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_87 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_87 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_87 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_87;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_88");
  if (xm == NULL) {
    /* Attempt to pull dist_88 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 87);
  }
  if (xm == NULL) {
    printf("could not find params.dist_88 or params.dist{88}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_88 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_88 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_88 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_88 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_88;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_89");
  if (xm == NULL) {
    /* Attempt to pull dist_89 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 88);
  }
  if (xm == NULL) {
    printf("could not find params.dist_89 or params.dist{89}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_89 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_89 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_89 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_89 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_89;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_90");
  if (xm == NULL) {
    /* Attempt to pull dist_90 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 89);
  }
  if (xm == NULL) {
    printf("could not find params.dist_90 or params.dist{90}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_90 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_90 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_90 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_90 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_90;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_91");
  if (xm == NULL) {
    /* Attempt to pull dist_91 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 90);
  }
  if (xm == NULL) {
    printf("could not find params.dist_91 or params.dist{91}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_91 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_91 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_91 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_91 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_91;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_92");
  if (xm == NULL) {
    /* Attempt to pull dist_92 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 91);
  }
  if (xm == NULL) {
    printf("could not find params.dist_92 or params.dist{92}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_92 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_92 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_92 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_92 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_92;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_93");
  if (xm == NULL) {
    /* Attempt to pull dist_93 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 92);
  }
  if (xm == NULL) {
    printf("could not find params.dist_93 or params.dist{93}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_93 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_93 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_93 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_93 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_93;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_94");
  if (xm == NULL) {
    /* Attempt to pull dist_94 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 93);
  }
  if (xm == NULL) {
    printf("could not find params.dist_94 or params.dist{94}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_94 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_94 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_94 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_94 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_94;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_95");
  if (xm == NULL) {
    /* Attempt to pull dist_95 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 94);
  }
  if (xm == NULL) {
    printf("could not find params.dist_95 or params.dist{95}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_95 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_95 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_95 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_95 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_95;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_96");
  if (xm == NULL) {
    /* Attempt to pull dist_96 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 95);
  }
  if (xm == NULL) {
    printf("could not find params.dist_96 or params.dist{96}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_96 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_96 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_96 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_96 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_96;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_97");
  if (xm == NULL) {
    /* Attempt to pull dist_97 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 96);
  }
  if (xm == NULL) {
    printf("could not find params.dist_97 or params.dist{97}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_97 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_97 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_97 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_97 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_97;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_98");
  if (xm == NULL) {
    /* Attempt to pull dist_98 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 97);
  }
  if (xm == NULL) {
    printf("could not find params.dist_98 or params.dist{98}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_98 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_98 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_98 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_98 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_98;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_99");
  if (xm == NULL) {
    /* Attempt to pull dist_99 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 98);
  }
  if (xm == NULL) {
    printf("could not find params.dist_99 or params.dist{99}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_99 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_99 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_99 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_99 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_99;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dist_100");
  if (xm == NULL) {
    /* Attempt to pull dist_100 from a cell array, as an additional option. */
    cell = mxGetField(prhs[0], 0, "dist");
    if (cell != NULL)
      xm = mxGetCell(cell, 99);
  }
  if (xm == NULL) {
    printf("could not find params.dist_100 or params.dist{100}.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dist_100 must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dist_100 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dist_100 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dist_100 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dist_100;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "dl");
  if (xm == NULL) {
    printf("could not find params.dl.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("dl must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter dl must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter dl must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter dl must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.dl;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "ds");
  if (xm == NULL) {
    printf("could not find params.ds.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("ds must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter ds must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter ds must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter ds must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.ds;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "hs");
  if (xm == NULL) {
    printf("could not find params.hs.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("hs must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter hs must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter hs must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter hs must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.hs;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "kl");
  if (xm == NULL) {
    printf("could not find params.kl.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("kl must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter kl must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter kl must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter kl must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.kl;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "wmax");
  if (xm == NULL) {
    printf("could not find params.wmax.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("wmax must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter wmax must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter wmax must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter wmax must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.wmax;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "wmin");
  if (xm == NULL) {
    printf("could not find params.wmin.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("wmin must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter wmin must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter wmin must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter wmin must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.wmin;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "wmin_land");
  if (xm == NULL) {
    printf("could not find params.wmin_land.\n");
  } else {
    if (!((mxGetM(xm) == 1) && (mxGetN(xm) == 1))) {
      printf("wmin_land must be size (1,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter wmin_land must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter wmin_land must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter wmin_land must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.wmin_land;
      src = mxGetPr(xm);
      for (i = 0; i < 1; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "x_0");
  if (xm == NULL) {
    printf("could not find params.x_0.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 1))) {
      printf("x_0 must be size (2,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter x_0 must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter x_0 must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter x_0 must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.x_0;
      src = mxGetPr(xm);
      for (i = 0; i < 2; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  this_var_errors = 0;
  xm = mxGetField(prhs[0], 0, "xb");
  if (xm == NULL) {
    printf("could not find params.xb.\n");
  } else {
    if (!((mxGetM(xm) == 2) && (mxGetN(xm) == 1))) {
      printf("xb must be size (2,1), not (%d,%d).\n", mxGetM(xm), mxGetN(xm));
      this_var_errors++;
    }
    if (mxIsComplex(xm)) {
      printf("parameter xb must be real.\n");
      this_var_errors++;
    }
    if (!mxIsClass(xm, "double")) {
      printf("parameter xb must be a full matrix of doubles.\n");
      this_var_errors++;
    }
    if (mxIsSparse(xm)) {
      printf("parameter xb must be a full matrix.\n");
      this_var_errors++;
    }
    if (this_var_errors == 0) {
      dest = params.xb;
      src = mxGetPr(xm);
      for (i = 0; i < 2; i++)
        *dest++ = *src++;
      valid_vars++;
    }
  }
  if (valid_vars != 215) {
    printf("Error: %d parameters are invalid.\n", 215 - valid_vars);
    mexErrMsgTxt("invalid parameters found.");
  }
  if (prepare_for_c) {
    printf("settings.prepare_for_c == 1. thus, outputting for C.\n");
    for (i = 0; i < 1; i++)
      printf("  params.b_0[%d] = %.6g;\n", i, params.b_0[i]);
    for (i = 0; i < 2; i++)
      printf("  params.x_0[%d] = %.6g;\n", i, params.x_0[i]);
    for (i = 0; i < 2; i++)
      printf("  params.xb[%d] = %.6g;\n", i, params.xb[i]);
    for (i = 0; i < 4; i++)
      printf("  params.Q[%d] = %.6g;\n", i, params.Q[i]);
    for (i = 0; i < 1; i++)
      printf("  params.R[%d] = %.6g;\n", i, params.R[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_1[%d] = %.6g;\n", i, params.b_1[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_2[%d] = %.6g;\n", i, params.b_2[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_3[%d] = %.6g;\n", i, params.b_3[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_4[%d] = %.6g;\n", i, params.b_4[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_5[%d] = %.6g;\n", i, params.b_5[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_6[%d] = %.6g;\n", i, params.b_6[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_7[%d] = %.6g;\n", i, params.b_7[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_8[%d] = %.6g;\n", i, params.b_8[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_9[%d] = %.6g;\n", i, params.b_9[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_10[%d] = %.6g;\n", i, params.b_10[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_11[%d] = %.6g;\n", i, params.b_11[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_12[%d] = %.6g;\n", i, params.b_12[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_13[%d] = %.6g;\n", i, params.b_13[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_14[%d] = %.6g;\n", i, params.b_14[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_15[%d] = %.6g;\n", i, params.b_15[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_16[%d] = %.6g;\n", i, params.b_16[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_17[%d] = %.6g;\n", i, params.b_17[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_18[%d] = %.6g;\n", i, params.b_18[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_19[%d] = %.6g;\n", i, params.b_19[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_20[%d] = %.6g;\n", i, params.b_20[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_21[%d] = %.6g;\n", i, params.b_21[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_22[%d] = %.6g;\n", i, params.b_22[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_23[%d] = %.6g;\n", i, params.b_23[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_24[%d] = %.6g;\n", i, params.b_24[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_25[%d] = %.6g;\n", i, params.b_25[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_26[%d] = %.6g;\n", i, params.b_26[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_27[%d] = %.6g;\n", i, params.b_27[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_28[%d] = %.6g;\n", i, params.b_28[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_29[%d] = %.6g;\n", i, params.b_29[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_30[%d] = %.6g;\n", i, params.b_30[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_31[%d] = %.6g;\n", i, params.b_31[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_32[%d] = %.6g;\n", i, params.b_32[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_33[%d] = %.6g;\n", i, params.b_33[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_34[%d] = %.6g;\n", i, params.b_34[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_35[%d] = %.6g;\n", i, params.b_35[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_36[%d] = %.6g;\n", i, params.b_36[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_37[%d] = %.6g;\n", i, params.b_37[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_38[%d] = %.6g;\n", i, params.b_38[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_39[%d] = %.6g;\n", i, params.b_39[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_40[%d] = %.6g;\n", i, params.b_40[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_41[%d] = %.6g;\n", i, params.b_41[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_42[%d] = %.6g;\n", i, params.b_42[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_43[%d] = %.6g;\n", i, params.b_43[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_44[%d] = %.6g;\n", i, params.b_44[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_45[%d] = %.6g;\n", i, params.b_45[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_46[%d] = %.6g;\n", i, params.b_46[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_47[%d] = %.6g;\n", i, params.b_47[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_48[%d] = %.6g;\n", i, params.b_48[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_49[%d] = %.6g;\n", i, params.b_49[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_50[%d] = %.6g;\n", i, params.b_50[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_51[%d] = %.6g;\n", i, params.b_51[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_52[%d] = %.6g;\n", i, params.b_52[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_53[%d] = %.6g;\n", i, params.b_53[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_54[%d] = %.6g;\n", i, params.b_54[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_55[%d] = %.6g;\n", i, params.b_55[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_56[%d] = %.6g;\n", i, params.b_56[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_57[%d] = %.6g;\n", i, params.b_57[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_58[%d] = %.6g;\n", i, params.b_58[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_59[%d] = %.6g;\n", i, params.b_59[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_60[%d] = %.6g;\n", i, params.b_60[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_61[%d] = %.6g;\n", i, params.b_61[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_62[%d] = %.6g;\n", i, params.b_62[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_63[%d] = %.6g;\n", i, params.b_63[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_64[%d] = %.6g;\n", i, params.b_64[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_65[%d] = %.6g;\n", i, params.b_65[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_66[%d] = %.6g;\n", i, params.b_66[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_67[%d] = %.6g;\n", i, params.b_67[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_68[%d] = %.6g;\n", i, params.b_68[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_69[%d] = %.6g;\n", i, params.b_69[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_70[%d] = %.6g;\n", i, params.b_70[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_71[%d] = %.6g;\n", i, params.b_71[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_72[%d] = %.6g;\n", i, params.b_72[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_73[%d] = %.6g;\n", i, params.b_73[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_74[%d] = %.6g;\n", i, params.b_74[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_75[%d] = %.6g;\n", i, params.b_75[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_76[%d] = %.6g;\n", i, params.b_76[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_77[%d] = %.6g;\n", i, params.b_77[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_78[%d] = %.6g;\n", i, params.b_78[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_79[%d] = %.6g;\n", i, params.b_79[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_80[%d] = %.6g;\n", i, params.b_80[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_81[%d] = %.6g;\n", i, params.b_81[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_82[%d] = %.6g;\n", i, params.b_82[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_83[%d] = %.6g;\n", i, params.b_83[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_84[%d] = %.6g;\n", i, params.b_84[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_85[%d] = %.6g;\n", i, params.b_85[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_86[%d] = %.6g;\n", i, params.b_86[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_87[%d] = %.6g;\n", i, params.b_87[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_88[%d] = %.6g;\n", i, params.b_88[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_89[%d] = %.6g;\n", i, params.b_89[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_90[%d] = %.6g;\n", i, params.b_90[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_91[%d] = %.6g;\n", i, params.b_91[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_92[%d] = %.6g;\n", i, params.b_92[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_93[%d] = %.6g;\n", i, params.b_93[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_94[%d] = %.6g;\n", i, params.b_94[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_95[%d] = %.6g;\n", i, params.b_95[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_96[%d] = %.6g;\n", i, params.b_96[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_97[%d] = %.6g;\n", i, params.b_97[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_98[%d] = %.6g;\n", i, params.b_98[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_99[%d] = %.6g;\n", i, params.b_99[i]);
    for (i = 0; i < 1; i++)
      printf("  params.b_100[%d] = %.6g;\n", i, params.b_100[i]);
    for (i = 0; i < 4; i++)
      printf("  params.P[%d] = %.6g;\n", i, params.P[i]);
    for (i = 0; i < 4; i++)
      printf("  params.A[%d] = %.6g;\n", i, params.A[i]);
    for (i = 0; i < 2; i++)
      printf("  params.B[%d] = %.6g;\n", i, params.B[i]);
    for (i = 0; i < 1; i++)
      printf("  params.wmin[%d] = %.6g;\n", i, params.wmin[i]);
    for (i = 0; i < 1; i++)
      printf("  params.wmax[%d] = %.6g;\n", i, params.wmax[i]);
    for (i = 0; i < 1; i++)
      printf("  params.kl[%d] = %.6g;\n", i, params.kl[i]);
    for (i = 0; i < 1; i++)
      printf("  params.wmin_land[%d] = %.6g;\n", i, params.wmin_land[i]);
    for (i = 0; i < 1; i++)
      printf("  params.hs[%d] = %.6g;\n", i, params.hs[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_1[%d] = %.6g;\n", i, params.dist_1[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dl[%d] = %.6g;\n", i, params.dl[i]);
    for (i = 0; i < 1; i++)
      printf("  params.ds[%d] = %.6g;\n", i, params.ds[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_2[%d] = %.6g;\n", i, params.dist_2[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_3[%d] = %.6g;\n", i, params.dist_3[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_4[%d] = %.6g;\n", i, params.dist_4[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_5[%d] = %.6g;\n", i, params.dist_5[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_6[%d] = %.6g;\n", i, params.dist_6[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_7[%d] = %.6g;\n", i, params.dist_7[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_8[%d] = %.6g;\n", i, params.dist_8[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_9[%d] = %.6g;\n", i, params.dist_9[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_10[%d] = %.6g;\n", i, params.dist_10[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_11[%d] = %.6g;\n", i, params.dist_11[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_12[%d] = %.6g;\n", i, params.dist_12[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_13[%d] = %.6g;\n", i, params.dist_13[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_14[%d] = %.6g;\n", i, params.dist_14[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_15[%d] = %.6g;\n", i, params.dist_15[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_16[%d] = %.6g;\n", i, params.dist_16[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_17[%d] = %.6g;\n", i, params.dist_17[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_18[%d] = %.6g;\n", i, params.dist_18[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_19[%d] = %.6g;\n", i, params.dist_19[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_20[%d] = %.6g;\n", i, params.dist_20[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_21[%d] = %.6g;\n", i, params.dist_21[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_22[%d] = %.6g;\n", i, params.dist_22[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_23[%d] = %.6g;\n", i, params.dist_23[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_24[%d] = %.6g;\n", i, params.dist_24[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_25[%d] = %.6g;\n", i, params.dist_25[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_26[%d] = %.6g;\n", i, params.dist_26[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_27[%d] = %.6g;\n", i, params.dist_27[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_28[%d] = %.6g;\n", i, params.dist_28[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_29[%d] = %.6g;\n", i, params.dist_29[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_30[%d] = %.6g;\n", i, params.dist_30[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_31[%d] = %.6g;\n", i, params.dist_31[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_32[%d] = %.6g;\n", i, params.dist_32[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_33[%d] = %.6g;\n", i, params.dist_33[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_34[%d] = %.6g;\n", i, params.dist_34[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_35[%d] = %.6g;\n", i, params.dist_35[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_36[%d] = %.6g;\n", i, params.dist_36[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_37[%d] = %.6g;\n", i, params.dist_37[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_38[%d] = %.6g;\n", i, params.dist_38[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_39[%d] = %.6g;\n", i, params.dist_39[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_40[%d] = %.6g;\n", i, params.dist_40[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_41[%d] = %.6g;\n", i, params.dist_41[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_42[%d] = %.6g;\n", i, params.dist_42[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_43[%d] = %.6g;\n", i, params.dist_43[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_44[%d] = %.6g;\n", i, params.dist_44[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_45[%d] = %.6g;\n", i, params.dist_45[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_46[%d] = %.6g;\n", i, params.dist_46[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_47[%d] = %.6g;\n", i, params.dist_47[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_48[%d] = %.6g;\n", i, params.dist_48[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_49[%d] = %.6g;\n", i, params.dist_49[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_50[%d] = %.6g;\n", i, params.dist_50[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_51[%d] = %.6g;\n", i, params.dist_51[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_52[%d] = %.6g;\n", i, params.dist_52[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_53[%d] = %.6g;\n", i, params.dist_53[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_54[%d] = %.6g;\n", i, params.dist_54[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_55[%d] = %.6g;\n", i, params.dist_55[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_56[%d] = %.6g;\n", i, params.dist_56[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_57[%d] = %.6g;\n", i, params.dist_57[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_58[%d] = %.6g;\n", i, params.dist_58[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_59[%d] = %.6g;\n", i, params.dist_59[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_60[%d] = %.6g;\n", i, params.dist_60[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_61[%d] = %.6g;\n", i, params.dist_61[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_62[%d] = %.6g;\n", i, params.dist_62[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_63[%d] = %.6g;\n", i, params.dist_63[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_64[%d] = %.6g;\n", i, params.dist_64[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_65[%d] = %.6g;\n", i, params.dist_65[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_66[%d] = %.6g;\n", i, params.dist_66[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_67[%d] = %.6g;\n", i, params.dist_67[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_68[%d] = %.6g;\n", i, params.dist_68[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_69[%d] = %.6g;\n", i, params.dist_69[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_70[%d] = %.6g;\n", i, params.dist_70[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_71[%d] = %.6g;\n", i, params.dist_71[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_72[%d] = %.6g;\n", i, params.dist_72[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_73[%d] = %.6g;\n", i, params.dist_73[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_74[%d] = %.6g;\n", i, params.dist_74[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_75[%d] = %.6g;\n", i, params.dist_75[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_76[%d] = %.6g;\n", i, params.dist_76[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_77[%d] = %.6g;\n", i, params.dist_77[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_78[%d] = %.6g;\n", i, params.dist_78[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_79[%d] = %.6g;\n", i, params.dist_79[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_80[%d] = %.6g;\n", i, params.dist_80[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_81[%d] = %.6g;\n", i, params.dist_81[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_82[%d] = %.6g;\n", i, params.dist_82[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_83[%d] = %.6g;\n", i, params.dist_83[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_84[%d] = %.6g;\n", i, params.dist_84[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_85[%d] = %.6g;\n", i, params.dist_85[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_86[%d] = %.6g;\n", i, params.dist_86[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_87[%d] = %.6g;\n", i, params.dist_87[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_88[%d] = %.6g;\n", i, params.dist_88[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_89[%d] = %.6g;\n", i, params.dist_89[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_90[%d] = %.6g;\n", i, params.dist_90[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_91[%d] = %.6g;\n", i, params.dist_91[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_92[%d] = %.6g;\n", i, params.dist_92[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_93[%d] = %.6g;\n", i, params.dist_93[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_94[%d] = %.6g;\n", i, params.dist_94[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_95[%d] = %.6g;\n", i, params.dist_95[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_96[%d] = %.6g;\n", i, params.dist_96[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_97[%d] = %.6g;\n", i, params.dist_97[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_98[%d] = %.6g;\n", i, params.dist_98[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_99[%d] = %.6g;\n", i, params.dist_99[i]);
    for (i = 0; i < 1; i++)
      printf("  params.dist_100[%d] = %.6g;\n", i, params.dist_100[i]);
  }
  /* Perform the actual solve in here. */
  steps = solve();
  /* For profiling purposes, allow extra silent solves if desired. */
  settings.verbose = 0;
  for (i = 0; i < extra_solves; i++)
    solve();
  /* Update the status variables. */
  plhs[1] = mxCreateStructArray(1, dims1x1of1, 4, status_names);
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[1], 0, "optval", xm);
  *mxGetPr(xm) = work.optval;
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[1], 0, "gap", xm);
  *mxGetPr(xm) = work.gap;
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[1], 0, "steps", xm);
  *mxGetPr(xm) = steps;
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[1], 0, "converged", xm);
  *mxGetPr(xm) = work.converged;
  /* Extract variable values. */
  plhs[0] = mxCreateStructArray(1, dims1x1of1, num_var_names, var_names);
  /* Create cell arrays for indexed variables. */
  dims[0] = 99;
  cell = mxCreateCellArray(1, dims);
  mxSetField(plhs[0], 0, "u", cell);
  dims[0] = 100;
  cell = mxCreateCellArray(1, dims);
  mxSetField(plhs[0], 0, "x", cell);
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_0", xm);
  dest = mxGetPr(xm);
  src = vars.u_0;
  for (i = 0; i < 1; i++) {
    *dest++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_1", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 0, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_1;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_2", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 1, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_2;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_3", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 2, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_3;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_4", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 3, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_4;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_5", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 4, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_5;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_6", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 5, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_6;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_7", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 6, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_7;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_8", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 7, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_8;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_9", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 8, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_9;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_10", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 9, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_10;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_11", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 10, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_11;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_12", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 11, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_12;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_13", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 12, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_13;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_14", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 13, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_14;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_15", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 14, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_15;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_16", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 15, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_16;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_17", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 16, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_17;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_18", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 17, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_18;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_19", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 18, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_19;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_20", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 19, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_20;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_21", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 20, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_21;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_22", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 21, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_22;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_23", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 22, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_23;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_24", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 23, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_24;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_25", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 24, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_25;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_26", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 25, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_26;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_27", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 26, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_27;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_28", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 27, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_28;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_29", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 28, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_29;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_30", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 29, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_30;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_31", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 30, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_31;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_32", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 31, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_32;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_33", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 32, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_33;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_34", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 33, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_34;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_35", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 34, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_35;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_36", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 35, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_36;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_37", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 36, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_37;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_38", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 37, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_38;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_39", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 38, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_39;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_40", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 39, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_40;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_41", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 40, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_41;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_42", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 41, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_42;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_43", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 42, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_43;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_44", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 43, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_44;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_45", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 44, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_45;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_46", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 45, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_46;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_47", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 46, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_47;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_48", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 47, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_48;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_49", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 48, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_49;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_50", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 49, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_50;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_51", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 50, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_51;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_52", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 51, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_52;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_53", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 52, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_53;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_54", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 53, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_54;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_55", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 54, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_55;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_56", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 55, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_56;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_57", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 56, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_57;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_58", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 57, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_58;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_59", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 58, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_59;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_60", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 59, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_60;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_61", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 60, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_61;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_62", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 61, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_62;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_63", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 62, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_63;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_64", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 63, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_64;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_65", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 64, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_65;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_66", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 65, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_66;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_67", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 66, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_67;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_68", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 67, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_68;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_69", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 68, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_69;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_70", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 69, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_70;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_71", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 70, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_71;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_72", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 71, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_72;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_73", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 72, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_73;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_74", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 73, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_74;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_75", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 74, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_75;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_76", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 75, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_76;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_77", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 76, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_77;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_78", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 77, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_78;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_79", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 78, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_79;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_80", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 79, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_80;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_81", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 80, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_81;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_82", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 81, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_82;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_83", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 82, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_83;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_84", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 83, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_84;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_85", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 84, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_85;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_86", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 85, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_86;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_87", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 86, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_87;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_88", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 87, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_88;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_89", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 88, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_89;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_90", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 89, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_90;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_91", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 90, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_91;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_92", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 91, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_92;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_93", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 92, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_93;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_94", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 93, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_94;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_95", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 94, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_95;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_96", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 95, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_96;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_97", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 96, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_97;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_98", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 97, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_98;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(1, 1, mxREAL);
  mxSetField(plhs[0], 0, "u_99", xm);
  xm_cell = mxCreateDoubleMatrix(1, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "u");
  mxSetCell(cell, 98, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.u_99;
  for (i = 0; i < 1; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_1", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 0, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_1;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_2", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 1, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_2;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_3", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 2, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_3;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_4", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 3, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_4;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_5", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 4, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_5;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_6", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 5, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_6;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_7", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 6, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_7;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_8", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 7, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_8;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_9", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 8, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_9;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_10", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 9, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_10;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_11", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 10, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_11;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_12", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 11, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_12;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_13", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 12, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_13;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_14", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 13, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_14;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_15", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 14, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_15;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_16", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 15, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_16;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_17", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 16, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_17;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_18", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 17, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_18;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_19", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 18, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_19;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_20", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 19, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_20;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_21", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 20, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_21;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_22", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 21, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_22;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_23", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 22, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_23;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_24", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 23, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_24;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_25", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 24, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_25;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_26", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 25, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_26;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_27", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 26, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_27;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_28", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 27, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_28;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_29", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 28, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_29;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_30", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 29, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_30;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_31", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 30, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_31;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_32", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 31, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_32;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_33", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 32, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_33;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_34", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 33, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_34;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_35", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 34, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_35;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_36", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 35, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_36;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_37", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 36, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_37;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_38", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 37, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_38;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_39", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 38, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_39;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_40", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 39, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_40;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_41", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 40, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_41;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_42", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 41, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_42;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_43", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 42, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_43;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_44", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 43, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_44;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_45", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 44, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_45;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_46", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 45, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_46;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_47", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 46, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_47;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_48", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 47, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_48;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_49", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 48, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_49;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_50", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 49, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_50;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_51", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 50, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_51;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_52", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 51, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_52;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_53", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 52, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_53;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_54", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 53, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_54;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_55", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 54, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_55;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_56", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 55, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_56;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_57", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 56, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_57;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_58", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 57, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_58;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_59", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 58, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_59;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_60", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 59, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_60;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_61", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 60, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_61;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_62", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 61, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_62;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_63", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 62, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_63;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_64", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 63, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_64;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_65", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 64, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_65;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_66", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 65, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_66;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_67", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 66, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_67;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_68", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 67, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_68;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_69", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 68, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_69;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_70", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 69, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_70;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_71", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 70, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_71;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_72", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 71, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_72;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_73", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 72, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_73;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_74", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 73, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_74;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_75", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 74, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_75;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_76", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 75, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_76;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_77", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 76, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_77;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_78", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 77, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_78;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_79", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 78, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_79;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_80", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 79, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_80;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_81", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 80, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_81;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_82", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 81, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_82;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_83", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 82, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_83;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_84", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 83, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_84;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_85", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 84, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_85;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_86", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 85, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_86;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_87", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 86, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_87;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_88", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 87, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_88;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_89", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 88, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_89;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_90", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 89, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_90;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_91", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 90, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_91;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_92", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 91, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_92;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_93", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 92, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_93;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_94", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 93, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_94;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_95", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 94, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_95;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_96", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 95, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_96;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_97", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 96, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_97;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_98", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 97, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_98;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_99", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 98, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_99;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
  xm = mxCreateDoubleMatrix(2, 1, mxREAL);
  mxSetField(plhs[0], 0, "x_100", xm);
  xm_cell = mxCreateDoubleMatrix(2, 1, mxREAL);
  cell = mxGetField(plhs[0], 0, "x");
  mxSetCell(cell, 99, xm_cell);
  dest = mxGetPr(xm);
  dest_cell = mxGetPr(xm_cell);
  src = vars.x_100;
  for (i = 0; i < 2; i++) {
    *dest++ = *src;
    *dest_cell++ = *src++;
  }
}
