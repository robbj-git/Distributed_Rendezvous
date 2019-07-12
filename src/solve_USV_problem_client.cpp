#include "ros/ros.h"
#include "rendezvous/USV_problem.h"
#include <cstdlib>


int main(int argc, char **argv)
{
  ros::init(argc, argv, "usv_problem_client");
  if (argc != 2)
  {
    ROS_INFO("usage: usv_problem_client xb_0");
    return 1;
  }

  ros::NodeHandle n;
  ros::ServiceClient client = n.serviceClient<rendezvous::USV_problem>("usv_problem");
  rendezvous::USV_problem srv;
  srv.request.xb_0.data = atoll(argv[1]);
  if (client.call(srv))
  {
    ROS_INFO("Response: %f", srv.response.ub_traj.data[0]);
  }
  else
  {
    ROS_ERROR("Failed to call service usv_problem");
    return 1;
  }

  return 0;
}
