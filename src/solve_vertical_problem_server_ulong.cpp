#include "ros/ros.h"
#include "rendezvous_problem/vertical_problem.h"
extern "C"{
  #include "VerticalUltraLong/solver.h"
}
//#include "std_msgs/Float32MultiArray.h"
#include "std_msgs/MultiArrayDimension.h"

Vars vars;
Params params;
Workspace work;
Settings settings;
int T = 100;
int n = 2;
int m = 1;

void load_data(Params *params) {
  // A-matrix
  {
    params->A[0] = 1.0;
    params->A[1] = 0.0;
    params->A[2] = 0.0470;
    params->A[3] = 0.8825;
  }

  // B-matrix
  {
    params->B[0] = 0.0030;
    params->B[1] = 0.1175;
  }

  // Q-matrix
  {
    params->Q[0] = 1.0;
    params->Q[1] = 0.0;
    params->Q[2] = 0.0;
    params->Q[3] = 0.0;
  }

  // P-matrix
  {
    params->P[0] = 1.0;
    params->P[1] = 0.0;
    params->P[2] = 0.0;
    params->P[3] = 0.0;
  }

  params->R[0] = 0.1;

  params->hs[0] = 5.0;
  params->ds[0] = 2.0;
  params->dl[0] = 1.0;
  params->wmin[0] = -1.0;
  params->wmax[0] = 1.0;
  params->wmin_land[0] = -0.3;
  params->kl[0] = 0.2;

}

bool get_solution(rendezvous_problem::vertical_problem::Request  &req,
         rendezvous_problem::vertical_problem::Response &res)
{
  for (int i=0; i<n; ++i)
  {
    params.x[0][i] = req.xv_0.array.data[i];
    params.xb[i]   = req.xbv.array.data[i];
  }

  for (int t=0; t<T+1; ++t)
  {
    if (t > 0) {
      // Parameter dist[0][0] is unused, so CVXgen doesn't allocate any memory for it
      params.dist[t][0] = req.dist_traj.array.data[t];
    }
    params.b[t][0] = (req.dist_traj.array.data[t] <= params.ds[0]) ? 1.0 : 0.0;
  }

  int num_iters = solve();

  res.wdes_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.wdes_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.wdes_traj.array.layout.dim[0].size = T;
  res.wdes_traj.array.layout.dim[0].stride = T*m;
  res.wdes_traj.array.layout.dim[0].label = "Time";
  res.wdes_traj.array.layout.dim[1].size = m;
  res.wdes_traj.array.layout.dim[1].stride = m;
  res.wdes_traj.array.layout.dim[1].label = "Input element";
  for (int t=0; t<T; ++t)
  {
    for (int i=0; i<m; ++i)
    {
      res.wdes_traj.array.data.push_back(vars.u[t][i]);
    }
  }

  res.xv_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.xv_traj.array.layout.dim.push_back(std_msgs::MultiArrayDimension());
  res.xv_traj.array.layout.dim[0].size = T+1;
  res.xv_traj.array.layout.dim[0].stride = (T+1)*n;
  res.xv_traj.array.layout.dim[0].label = "Time";
  res.xv_traj.array.layout.dim[1].size = n;
  res.xv_traj.array.layout.dim[1].stride = n;
  res.xv_traj.array.layout.dim[1].label = "State element";
  for (int t=0; t<T+1; ++t)
  {
    for (int i=0; i<n; ++i)
    {
      if (t == 0) {
        res.xv_traj.array.data.push_back(params.x[0][i]);
      }
      else {
        res.xv_traj.array.data.push_back(vars.x[t][i]);
      }
    }
  }

  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "vertical_problem_server_ulong");
  ros::NodeHandle n;

  set_defaults();
  setup_indexing();
  load_data(&params);
  settings.verbose = 0;

  ros::ServiceServer service = n.advertiseService("vertical_problem_ulong", get_solution);
  ROS_INFO("Ready to solve ultra-long vertical problem");
  ros::spin();

  return 0;
}
