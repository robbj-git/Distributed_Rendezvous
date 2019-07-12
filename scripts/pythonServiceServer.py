#!/usr/bin/env python

from rendezvous_problem.srv import *
import rospy

def handle_request(req):
    # print "Returning [%s + %s = %s]"%(req.a, req.b, (req.a + req.b))
    print "Totally got a request"
    return USV_problemResponse()

def USV_problem_server():
    rospy.init_node('USV_server')
    s = rospy.Service('usv_problem', USV_problem, handle_request)
    print "Ready to solve the problem."
    rospy.spin()

if __name__ == "__main__":
    USV_problem_server()
