#!/usr/bin/env python

import sys
import rospy
from rendezvous_problem.srv import *
import rendezvous_problem
import time
from std_msgs.msg import Float32MultiArray, MultiArrayDimension

T = 25
n = 4
m =  2

def rendezvous_client():
    rospy.wait_for_service('usv_problem')
    try:
        rospy.wait_for_service('usv_problem')
        solve_usv_problem = rospy.ServiceProxy('usv_problem', USV_problem)

        xb_0 = [0.0, 0.0, 0.0, 0.0]
        x_traj = [30.0, 15.0, 0.0, 0.0]*(T+1)

        xb_0_msg = Float32MultiArray()
        xb_0_msg.layout.dim.append(MultiArrayDimension())
        xb_0_msg.layout.dim[0].size = n
        xb_0_msg.layout.dim[0].stride = 1
        xb_0_msg.layout.dim[0].label = "xb_0"
        xb_0_msg.data = xb_0

        x_traj_msg = Float32MultiArray()
        x_traj_msg.layout.dim.extend([MultiArrayDimension(),\
            MultiArrayDimension()])
        x_traj_msg.layout.dim[0].size = T+1
        x_traj_msg.layout.dim[0].stride = n*(T+1)
        x_traj_msg.layout.dim[0].label = "Time"
        x_traj_msg.layout.dim[1].size = n
        x_traj_msg.layout.dim[1].stride = n
        x_traj_msg.layout.dim[1].label = "State element"
        x_traj_msg.data = x_traj

        #rospy.loginfo(x_traj_msg)

        req = USV_problemRequest()
        req.xb_0 = xb_0_msg
        req.x_traj = x_traj_msg
        resp = solve_usv_problem(req)
        return resp.ub_traj
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

if __name__ == "__main__":
    # if len(sys.argv) == 3:
    #     x = int(sys.argv[1])
    #     y = int(sys.argv[2])
    # else:
    #     print usage()
    #     sys.exit(1)
    rospy.init_node('USV_problem_client_node')
    print rendezvous_client()
