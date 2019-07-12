#!/usr/bin/env python
import rospy
from Dynamics import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters, StateApproximator
from helper_functions import mat_to_multiarray_stamped, get_dist_traj
import Queue
import os
# from callbacks import *
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header, Int8, Int32
from geometry_msgs.msg import Vector3Stamped, QuaternionStamped, AccelStamped
from rendezvous_problem.msg import StateStamped
from dji_sdk.srv import SDKControlAuthority
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
import cvxpy as cp
#import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import datetime
import osqp
import thread
# import threading
from problemClasses import *
from UAV_simulation import UAV_simulator
from USV_simulation import USV_simulator
import pdb
import random

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"

lookahead = 0   # Only for parallel

global UAV_test_round, should_change_horizon, should_finish, quit_horizon
UAV_test_round = np.inf
should_change_horizon = False
should_finish = False
quit_horizon = -1

def UAV_test_round_callback(msg):
    global UAV_test_round
    UAV_test_round =  msg.data

def UAV_instruction_callback(msg):
    global should_change_horizon, should_finish, quit_horizon
    if msg.data == NEXT_HORIZON:
        should_change_horizon = True
    elif msg.data > NEXT_HORIZON:
        print "SHOULD STORE AFTER THIS!!!"
        quit_horizon = msg.data
        should_finish = True

rospy.init_node('USV_main')

round_pub = rospy.Publisher('USV_test_round', Int32, queue_size = 10, latch = True)
store_pub = rospy.Publisher('USV_has_stored_data', Int32, queue_size = 1, latch = True)
rospy.Subscriber('UAV_test_round', Int32, UAV_test_round_callback)
rospy.Subscriber('UAV_instruction', Int32, UAV_instruction_callback)

class ProblemParams():
    def __init__(self):
        self.CENTRALISED = CENTRALISED
        self.DISTRIBUTED = DISTRIBUTED
        self.PARALLEL = PARALLEL
        self.SAMPLING_RATE = SAMPLING_RATE
        self.SAMPLING_TIME = SAMPLING_TIME
        self.USE_ROS = USE_ROS
        self.INTER_ITS = INTER_ITS
        self.T = T
        self.T_inner = 1
        self.A = A
        self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.Av = Av
        self.Bv = Bv
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        self.used_solver = CVXPy
        self.lookahead = lookahead
        self.KUAV = KUAV
        self.KUSV = KUSV
        self.params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
            wmin, wmax, wmin_land, kl, vmax)
        self.delay_len = delay_len

problem_params = ProblemParams()

xb_m = np.matrix([[30.0], [15.0], [0.0], [0.0]])

# --------------- TESTING LOOP ------------------
# NUM_TESTS = 1 DOESN'T WORK, THE TESTERS FAIL WAITING FOR EACH OTHER
NUM_TESTS = 1
prev_simulator = None
my_usv_simulator = None

ever_took_too_long = False

# Need to create a simulator, because simulators call rospy.node_init(), and
# that function must be called before anything can be published, but it also
# can only be called once, so I can't call it here myself
# SHOULD BE ABLE TO REMOVE, I INIT NODE ABOVE NOW!
# my_usv_simulator = USV_simulator(problem_params)
# my_usv_simulator.deinitialise() # We don't want it to receive callbacks
if PARALLEL:
    hor_max = 180#260#120#150   212 was good I think
    hor_min = 180#260#180#120#100
    problem_params.T_inner = 30
else:
    hor_max = 79#80#37#63#80#56
    hor_min = 79#30#37#63#25#20

for N in range(hor_max, hor_min-1, -1):
    took_too_long = False
    USV_test_round = -1
    next_test_round = 0
    problem_params.T = N

    # Wait for UAV tester before creating next simulator
    # If the UAV and USV testers have simulators with different time horizons,
    # some of the callbacks between them will mess up
    round_pub.publish(Int32(-1))
    #while UAV_test_round != -1:
    # Sometimes other tester had time to switch to round 0 too quickly and round -1 was never registered
    while UAV_test_round > 0:
        if rospy.is_shutdown() or should_finish:
            break
        if random.randint(1, 101) == 100:
            print "Waiting in loop 1"
        time.sleep(0.01)
        # print 'Waiting at time', time.time(), 'with values', UAV_test_round, USV_test_round, next_test_round
    # In case there is some old horizon change request sent by the UAV
    should_change_horizon = False
    if my_usv_simulator is not None:
        # We deinitialise here because hopefully old messages have stopped arriving by now
        my_usv_simulator.deinitialise()
    prev_simulator = my_usv_simulator
    my_usv_simulator = USV_simulator(problem_params)

    for i in range(NUM_TESTS):
        USV_test_round += 1
        msg = Int32(USV_test_round)
        round_pub.publish(msg)

        # Wait for UAV tester to also be ready
        while UAV_test_round != next_test_round:
            if rospy.is_shutdown() or should_finish or should_change_horizon:
                break
            if random.randint(1, 101) == 100:
                print "Waiting in loop 2"
            time.sleep(0.01)
            # print 'Waiting at time', time.time(), 'with values', UAV_test_round, USV_test_round, next_test_round
        next_test_round += 1

        if rospy.is_shutdown() or should_finish:
            should_finish = True
            print "Asked to finish"
            break
        elif should_change_horizon:
            should_change_horizon = False
            print "Asked to change horizon"
            break

        my_usv_simulator.simulate_problem(sim_len, xb_m)
        # time.sleep(20)
        my_usv_simulator.store_data()
        try:
            my_usv_simulator.plot_results(True)
        except:
            pass
        print "Finished simulation round", i, "with horizon", N
        print np.mean(my_usv_simulator.iteration_durations)
        print np.median(my_usv_simulator.iteration_durations)
        # ------------- FOR PARALLEL ------------
        if PARALLEL and np.mean(my_usv_simulator.dist_solution_durations) > SAMPLING_TIME\
            and np.median(my_usv_simulator.dist_solution_durations) > SAMPLING_TIME:
            took_too_long = True
            break
        # ---------- FOR NON PARALLEL -----------
        if not PARALLEL and np.mean(my_usv_simulator.iteration_durations) > SAMPLING_TIME\
            and np.median(my_usv_simulator.iteration_durations) > SAMPLING_TIME:
            took_too_long = True
            break
    if took_too_long:
        print 'USV TEST ACTUALLY TOOK TOO LONG!!!!!!!!!!!!!!'
        ever_took_too_long = True
    if should_finish:
        should_finish = False
        print "Still asked to finish"
        break


print "started sleeping"
if not quit_horizon >= 0:
    # Sleep for a while, give UAV-tester a chance to finish
    time.sleep(30)

print "stopped sleeping"

store_pub.publish(Int32(1))
if quit_horizon >= 0:
    print "Storing!"
    if N == quit_horizon:
        my_usv_simulator.store_data()
    else:
        # It is possible that the outer loop increments N while the UAV tester
        # is still at the previous value of N. If the UAV-tester then quits,
        # my_usv_simulator will not be the correct simulator.
        prev_simulator.store_data()
    if ever_took_too_long:
        print 'OMG HOW ON EARTH DID IT EVER TAKE TOO LONG?????'
else:
    print "nope, no storing", rospy.Time.now()
