#include "ros/ros.h"
#include "rendezvous_problem/centralised_problem.h"
extern "C"{
  #include "Centralised/solver.h"
}
//#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/MultiArrayDimension.h"
#include <math.h>

Vars vars;
Params params;
Workspace work;
Settings settings;
int T = 25;
int n = 4;
int m = 2;

void load_data(Params *params) {
  // A-matrix
  {
    params->A[0] = 1.0;
    params->A[1] = 0.0;
    params->A[2] = 0.0;
    params->A[3] = 0.0;

    params->A[4] = 0.0;
    params->A[5] = 1.0;
    params->A[6] = 0.0;
    params->A[7] = 0.0;

    params->A[8] = 0.0499;
    params->A[9] = 0.0;
    params->A[10] = 0.9950;
    params->A[11] = 0.0;

    params->A[12] = 0.0;
    params->A[13] = 0.0499;
    params->A[14] = 0.0;
    params->A[15] = 0.9950;
  }

  // Ab-matrix
  {
    params->Ab[0] = 1.0;
    params->Ab[1] = 0.0;
    params->Ab[2] = 0.0;
    params->Ab[3] = 0.0;

    params->Ab[4] = 0.0;
    params->Ab[5] = 1.0;
    params->Ab[6] = 0.0;
    params->Ab[7] = 0.0;

    params->Ab[8] = 0.0494;
    params->Ab[9] = 0.0;
    params->Ab[10] = 0.9753;
    params->Ab[11] = 0.0;

    params->Ab[12] = 0.0;
    params->Ab[13] = 0.0494;
    params->Ab[14] = 0.0;
    params->Ab[15] = 0.9753;
  }

  // B-matrix
  {
    params->B[0] = 0.0012;
    params->B[1] = 0.0;
    params->B[2] = 0.0499;
    params->B[3] = 0.0;

    params->B[4] = 0.0;
    params->B[5] = 0.0012;
    params->B[6] = 0.0;
    params->B[7] = 0.0499;
  }

  // Bb-matrix
  {
    params->Bb[0] = 0.0012;
    params->Bb[1] = 0.0;
    params->Bb[2] = 0.0494;
    params->Bb[3] = 0.0;

    params->Bb[4] = 0.0;
    params->Bb[5] = 0.0012;
    params->Bb[6] = 0.0;
    params->Bb[7] = 0.0494;
  }

  // Q-matrix
  {
    params->Q[0] = 1.0;
    params->Q[1] = 0.0;
    params->Q[2] = 0.0;
    params->Q[3] = 0.0;

    params->Q[4] = 0.0;
    params->Q[5] = 1.0;
    params->Q[6] = 0.0;
    params->Q[7] = 0.0;

    params->Q[8] = 0.0;
    params->Q[9] = 0.0;
    params->Q[10] = 0.0;
    params->Q[11] = 0.0;

    params->Q[12] = 0.0;
    params->Q[13] = 0.0;
    params->Q[14] = 0.0;
    params->Q[15] = 0.0;
  }

  // P-matrix
  {
    params->P[0] = 1.0;
    params->P[1] = 0.0;
    params->P[2] = 0.0;
    params->P[3] = 0.0;

    params->P[4] = 0.0;
    params->P[5] = 1.0;
    params->P[6] = 0.0;
    params->P[7] = 0.0;

    params->P[8] = 0.0;
    params->P[9] = 0.0;
    params->P[10] = 0.0;
    params->P[11] = 0.0;

    params->P[12] = 0.0;
    params->P[13] = 0.0;
    params->P[14] = 0.0;
    params->P[15] = 0.0;
  }

  // R-matrix
  {
    params->R[0] = 0.1;
    params->R[1] = 0.0;
    params->R[2] = 0.0;
    params->R[3] = 0.1;
  }

  params->vmax[0] = 5.0;
  params->amax[0] =  5.0;
  params->amin[0] = -5.0;
  params->amax_b[0] =  3.0;
  params->amin_b[0] = -3.0;
}

bool get_solution(rendezvous_problem::centralised_problem::Request  &req,
         rendezvous_problem::centralised_problem::Response &res)
{
  params.x[0][0] = req.x_0.array.data[0];
  params.x[0][1] = req.x_0.array.data[1];
  params.x[0][2] = req.x_0.array.data[2];
  params.x[0][3] = req.x_0.array.data[3];

  params.xb[0][0] = req.xb_0.array.data[0];
  params.xb[0][1] = req.xb_0.array.data[1];
  params.xb[0][2] = req.xb_0.array.data[2];
  params.xb[0][3] = req.xb_0.array.data[3];

  int num_iters = solve();

  res.u_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.u_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.u_traj.array.layout.dim[0].size = T;
  res.u_traj.array.layout.dim[0].stride = T*m;
  res.u_traj.array.layout.dim[0].label = "Time";
  res.u_traj.array.layout.dim[1].size = m;
  res.u_traj.array.layout.dim[1].stride = m;
  res.u_traj.array.layout.dim[1].label = "Input element";
  for (int t=0; t<T; ++t)
  {
    for (int i=0; i<m; ++i)
    {
      res.u_traj.array.data.push_back(vars.u[t][i]);
    }
  }

  res.ub_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.ub_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.ub_traj.array.layout.dim[0].size = T;
  res.ub_traj.array.layout.dim[0].stride = T*m;
  res.ub_traj.array.layout.dim[0].label = "Time";
  res.ub_traj.array.layout.dim[1].size = m;
  res.ub_traj.array.layout.dim[1].stride = m;
  res.ub_traj.array.layout.dim[1].label = "Input element";
  for (int t=0; t<T; ++t)
  {
    for (int i=0; i<m; ++i)
    {
      res.ub_traj.array.data.push_back(vars.ub[t][i]);
    }
  }

  res.x_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.x_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.x_traj.array.layout.dim[0].size = T+1;
  res.x_traj.array.layout.dim[0].stride = (T+1)*n;
  res.x_traj.array.layout.dim[0].label = "Time";
  res.x_traj.array.layout.dim[1].size = n;
  res.x_traj.array.layout.dim[1].stride = n;
  res.x_traj.array.layout.dim[1].label = "State element";

  for (int t=0; t<T+1; ++t)
  {
    for (int i=0; i<n; ++i)
    {
      if (t == 0) {
        res.x_traj.array.data.push_back(params.x[0][i]);
      }
      else {
        res.x_traj.array.data.push_back(vars.x[t][i]);
      }
    }
  }

  res.xb_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.xb_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.xb_traj.array.layout.dim[0].size = T+1;
  res.xb_traj.array.layout.dim[0].stride = (T+1)*n;
  res.xb_traj.array.layout.dim[0].label = "Time";
  res.xb_traj.array.layout.dim[1].size = n;
  res.xb_traj.array.layout.dim[1].stride = n;
  res.xb_traj.array.layout.dim[1].label = "State element";
  for (int t=0; t<T+1; ++t)
  {
    for (int i=0; i<n; ++i)
    {
      if (t == 0) {
        res.xb_traj.array.data.push_back(params.xb[0][i]);
      }
      else {
        res.xb_traj.array.data.push_back(vars.xb[t][i]);
      }
    }
  }

  return true;
}

void debug_prediction(double *x0, double *u0)
{
  double x[4];
  for (int t=0; t<10; ++t) {
    for (int i=0; i<4; ++i) {
      x[i] = 0;
      for (int j=0; j<4; ++j)
      {
        x[i] += x0[j]*params.A[i + j*4];
      }
      for (int j=0; j<2; ++j)
      {
        x[i] += u0[j]*params.B[4*j+i];
      }
    }
    for (int i=0; i < 4; ++i) {
      x0[i] = x[i];
    }
  }
  ROS_INFO("State: %f, %f, %f, %f", x0[0], x0[1], x0[2], x0[3]);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "centralised_problem_server");
  ros::NodeHandle n;


  // DEBUG: CVXGEN
  set_defaults();
  setup_indexing();
  load_data(&params);
  settings.verbose = 0;

  ros::ServiceServer service = n.advertiseService("centralised_problem", get_solution);
  ROS_INFO("Ready to solve centralised problem");

  // // DEBUG
  // double x0[4] = {10, 10, 10, 10};
  // double u0[2] = {1, 1};
  // debug_prediction(x0, u0);

  ros::spin();

  return 0;
}
