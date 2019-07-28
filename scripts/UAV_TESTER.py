#!/usr/bin/env python
import rospy
from Dynamics import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters
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
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import datetime
import osqp
import thread
import pdb
import random
# import threading
from problemClasses import *
# from UAV_simulation import UAV_simulator
from UAV_simulation_NEW import UAV_simulator
from USV_simulation import USV_simulator

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"
OSQP = "OSQP"

lookahead = 0   # Only for parallel. TODO: Move to IMPORT_ME.py???

global USV_test_round, USV_has_stored_data
USV_test_round = np.inf
USV_has_stored_data = 0

def USV_test_round_callback(msg):
    global USV_test_round
    USV_test_round = msg.data

def USV_store_callback(msg):
    global USV_has_stored_data
    USV_has_stored_data = msg.data

rospy.init_node('UAV_main')

round_pub = rospy.Publisher('UAV_test_round', Int32, queue_size = 10, latch = True)
instruct_pub = rospy.Publisher('UAV_instruction', Int32, queue_size = 10, latch = True)
rospy.Subscriber('USV_test_round', Int32, USV_test_round_callback)
rospy.Subscriber('USV_has_stored_data', Int32, USV_store_callback)

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
        self.vert_used_solver = CVXPy
        self.lookahead = lookahead
        self.KUAV = KUAV
        self.KUSV = KUSV
        self.KVert = KVert
        self.params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
            wmin, wmax, wmin_land, kl, vmax)
        self.delay_len = delay_len

problem_params = ProblemParams()
x_m = np.matrix([[0.0], [0.0], [0.0], [0.0]])
xv_m = np.matrix([[7.0], [0.0]])#np.matrix([[12.0], [0.0]])
prev_simulator = None
my_uav_simulator =  None

# -------------- TESTING LOOP ----------------
# NUM_TESTS = 1 DOESN'T WORK, THE TESTERS FAIL WAITING FOR EACH OTHER
NUM_TESTS = 1
if PARALLEL:
    hor_max = 180#260#120#150
    hor_min = 180#260#180#120#100
    problem_params.T_inner = 30
else:
    hor_max = 79#80#37#63#80#56
    hor_min = 79#30#37#63#25#20
cancelled = False

# Need to create a simulator, because simulators call rospy.node_init(), and
# that function must be called before anything can be published, but it also
# can only be called once, so I can't call it here myself
# SHOULD BE ABLE TO REMOVE, I INIT NODE ABOVE NOW!
# my_uav_simulator = UAV_simulator(problem_params)
# my_uav_simulator.deinitialise() # We don't want it to receive callbacks

for N in range(hor_max, hor_min-1, -1):
    # print "N:", N
    took_too_long = False
    UAV_test_round = -1
    next_test_round = 0
    problem_params.T = N

    mean_list = np.empty((NUM_TESTS, 1))
    mean_list.fill(np.nan)
    median_list = np.empty((NUM_TESTS, 1))
    median_list.fill(np.nan)
    hor_mean_list = np.empty((NUM_TESTS, 1))
    hor_mean_list.fill(np.nan)
    hor_median_list = np.empty((NUM_TESTS, 1))
    hor_median_list.fill(np.nan)
    vert_mean_list = np.empty((NUM_TESTS, 1))
    vert_mean_list.fill(np.nan)
    vert_median_list = np.empty((NUM_TESTS, 1))
    vert_median_list.fill(np.nan)
    landing_list = np.empty((NUM_TESTS, 1))
    landing_list.fill(np.nan)

    # Wait for USV tester before creating next simulator
    # If the UAV and USV testers have simulators with different time horizons,
    # some of the callbacks between them will mess up
    round_pub.publish(Int32(-1))
    # while USV_test_round != -1:
    # Sometimes other tester had time to switch to round 0 too quickly and round -1 was never registered
    while USV_test_round > 0:
        if rospy.is_shutdown():
            break
        if random.randint(1, 101) == 100:
            print "Waiting in loop 1"
        time.sleep(0.01)

    if rospy.is_shutdown():
        break

    if my_uav_simulator is not None:
        # We deinitialise here because hopefully old messages have stopped arriving by now
        my_uav_simulator.deinitialise()
    prev_simulator = my_uav_simulator
    my_uav_simulator = UAV_simulator(problem_params)

    for i in range(NUM_TESTS):
        UAV_test_round += 1
        msg = Int32(UAV_test_round)
        round_pub.publish(msg)
        # Wait for USV tester to also be ready
        while USV_test_round != next_test_round:
            if rospy.is_shutdown():
                break
            if random.randint(1, 101) == 100:
                print "Waiting in loop 2"
            time.sleep(0.01)
            # print ('Waiting at time', time.time(), 'with values', UAV_test_round, USV_test_round, next_test_round)
        next_test_round += 1

        if rospy.is_shutdown():
            cancelled = True
            break

        my_uav_simulator.simulate_problem(sim_len, x_m, xv_m)
        print "FINISHED SIMULATING!"
        # # DEBUG storing
        # my_uav_simulator.store_data()
        # DEBUG plotting
        # try:
        #     my_uav_simulator.plot_results(True)
        # except Exception as e:
        #     print "Failed plotting:"
        #     print e
        xv_log = my_uav_simulator.xv_log
        z_traj = xv_log[0,:]
        # Calculate landing time
        land_time = 0
        UAV_time_stamps = my_uav_simulator.UAV_times
        t_0 = UAV_time_stamps[0, 0]
        UAV_time_stamps = UAV_time_stamps - t_0
        for j in range(len(z_traj)):
            if z_traj[j] > 0.1:
                land_time = UAV_time_stamps[0, j]
            else:
                break
        landing_list[i] = land_time
        mean_list[i] = np.mean(my_uav_simulator.iteration_durations)
        median_list[i] = np.median(my_uav_simulator.iteration_durations)
        hor_mean_list[i] = np.mean(my_uav_simulator.hor_solution_durations)
        hor_median_list[i] = np.median(my_uav_simulator.hor_solution_durations)
        vert_mean_list[i] = np.mean(my_uav_simulator.vert_solution_durations)
        vert_median_list[i] = np.median(my_uav_simulator.vert_solution_durations)
        print "Finished simulation round", i, "with horizon", N
        print hor_mean_list[i]
        # print hor_median_list[i]
        print vert_mean_list[i]
        # print vert_median_list[i]
        print mean_list[i]
        print mean_list[i] - hor_mean_list[i] - vert_mean_list[i]
        if PARALLEL and (hor_mean_list[i] > SAMPLING_TIME*INTER_ITS \
            or hor_median_list[i] > SAMPLING_TIME*INTER_ITS\
            or vert_mean_list[i] > SAMPLING_TIME*INTER_ITS \
            or vert_median_list[i] > SAMPLING_TIME*INTER_ITS):
            # took_too_long = True
            print "TOOK TO LONG!"
            # instruct_pub.publish(Int32(NEXT_HORIZON))
            # break
        if not PARALLEL and (np.mean(my_uav_simulator.iteration_durations) > SAMPLING_TIME\
            or np.median(my_uav_simulator.iteration_durations) > SAMPLING_TIME):
            print "Uh-oh, took too long!"
            took_too_long = True
            instruct_pub.publish(Int32(NEXT_HORIZON))
            # print np.mean(my_uav_simulator.iteration_durations)
            print np.median(my_uav_simulator.iteration_durations)
            # print hor_mean_list[i]
            # print vert_mean_list[i]
            break
    if not took_too_long:
        print "Best horizon: ", N
        instruct_pub.publish(Int32(N))
        break
    if cancelled:
        print "CANCELLED"
        instruct_pub.publish(Int32(N))
        break

#DEBUG
my_uav_simulator.plot_results(True)
instruct_pub.publish(Int32(N))
if not cancelled:
    print "ENTERING HERE! COMMUNICATION ISSUES AFTER THIS POINT AREN'T A BIG DEAL"
    # Store data from the last successfull simulation
    test_info_str = "min horizon: " + str(hor_min) + "\nmax horizon: " \
        + str(hor_max) + "\nnumber of trials: " + str(NUM_TESTS)
    exp_index = my_uav_simulator.store_data(test_info_str = test_info_str)

    dir_path = '/home/student/robbj_experiment_results/'
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/MEAN.txt', mean_list)
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/MEDIAN.txt', median_list)

    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/HOR_MEAN.txt', hor_mean_list)
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/HOR_MEDIAN.txt', hor_median_list)

    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/VERT_MEAN.txt', vert_mean_list)
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/VERT_MEDIAN.txt', vert_median_list)

    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/LANDING_TIMES.txt', landing_list)

    # Wait for USV to finish storing data. If we exit before this, USV will never receive experiment index
    while USV_has_stored_data == 0:
        if random.randint(1, 101) == 100:
            print "Waiting for USV to finish storing"
        if rospy.is_shutdown():
            break
        time.sleep(0.1)
