#!/usr/bin/env python
import rospy
from matrices_and_parameters import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters
from helper_functions import mat_to_multiarray_stamped, get_dist_traj
import Queue
import os
# from callbacks import *
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header, Int8, Int32, Time
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
from UAV_simulation import UAV_simulator

lookahead = 0   # Only for parallel. TODO: Move to IMPORT_ME.py???

global USV_test_round, USV_has_stored_data, USV_time, UAV_time
USV_test_round = np.inf
USV_has_stored_data = 0
UAV_time = np.nan
USV_time = np.nan

def USV_test_round_callback(msg):
    global USV_test_round
    USV_test_round = msg.data

def USV_store_callback(msg):
    global USV_has_stored_data
    USV_has_stored_data = msg.data

def USV_time_callback(msg):
    global USV_time, UAV_time
    USV_time = msg.data
    UAV_time = rospy.Time.now()

rospy.init_node('UAV_main')

round_pub = rospy.Publisher('UAV_test_round', Int32, queue_size = 10, latch = True)
instruct_pub = rospy.Publisher('UAV_instruction', Int32, queue_size = 10, latch = True)
experiment_index_pub = rospy.Publisher('experiment_index', Int8, queue_size=1, latch=True)
rospy.Subscriber('USV_test_round', Int32, USV_test_round_callback)
rospy.Subscriber('USV_has_stored_data', Int32, USV_store_callback)
rospy.Subscriber('USV_time', Time, USV_time_callback)

# Altitude of the USV, currently assumed constant, which is why it is set here
hb = 0

class ProblemParams():
    def __init__(self):
        self.CENTRALISED = CENTRALISED
        self.DISTRIBUTED = DISTRIBUTED
        self.PARALLEL = PARALLEL
        self.SAMPLING_RATE = SAMPLING_RATE
        self.SAMPLING_TIME = SAMPLING_TIME
        self.USE_HIL = USE_HIL
        self.INTER_ITS = INTER_ITS
        self.USE_COMPLETE_HORIZONTAL = USE_COMPLETE_HORIZONTAL
        self.USE_COMPLETE_USV = USE_COMPLETE_USV
        self.A = A
        self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.Qb_vel = Qb_vel
        self.Pb_vel = Pb_vel
        self.Q_vel = Q_vel
        self.P_vel = P_vel
        self.Av = Av
        self.Bv = Bv
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        self.used_solver = used_hor_solver
        self.vert_used_solver = used_vert_solver
        self.lookahead = lookahead
        self.KUAV = KUAV
        self.KUSV = KUSV
        self.KVert = KVert
        self.params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
            wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max, ang_vel_max, psi_max, T_max, T_min)
        self.hb = hb
        self.delay_len = delay_len
        self.ADD_DROPOUT = ADD_DROPOUT
        self.PRED_PARALLEL_TRAJ = PRED_PARALLEL_TRAJ
        self.SHOULD_SHIFT_MESSAGES = SHOULD_SHIFT_MESSAGES
        self.dropout_lower_bound = dropout_lower_bound
        self.dropout_upper_bound = dropout_upper_bound

problem_params = ProblemParams()

if USE_COMPLETE_HORIZONTAL:
    nUAV = 8
else:
    nUAV = 4

x_m = np.zeros((nUAV, 1))
xv_m = np.array([[7.0], [0.0]])#np.matrix([[12.0], [0.0]])
prev_simulator = None
my_uav_simulator =  None

# In centralised case, this variable can be set to make the USV travel in the direction
# of the vector pointint to its starting position. However, you have to manually make
# sure that the xb below matches the initial state of the USV in USV_TESTER.py
# xb = None
#-2, 1
xb = np.array([[-5], [4], [np.nan], [np.nan]])
if xb is not None and CENTRALISED:
    reverse_dir = False
    dir = get_travel_dir(xb, reverse_dir)
else:
    dir = None
# -------------- TESTING LOOP ----------------
# NUM_TESTS = 1 DOESN'T ALWAYS WORK, THE TESTERS FAIL WAITING FOR EACH OTHER
NUM_TESTS = 100
if PARALLEL:
    hor_max = 420#405#100
    hor_min = 420#300#100
elif CENTRALISED:
    hor_max = 195#150#120
    hor_min = 100#80#120
elif DISTRIBUTED:
    hor_max = 250#100#280#100
    hor_min = 100

hor_inner = 60#30#15
cancelled = False

# Need to create a simulator, because simulators call rospy.node_init(), and
# that function must be called before anything can be published, but it also
# can only be called once, so I can't call it here myself
# SHOULD BE ABLE TO REMOVE, I INIT NODE ABOVE NOW!
# my_uav_simulator = UAV_simulator(problem_params)
# my_uav_simulator.deinitialise() # We don't want it to receive callbacks

for N in range(hor_max, hor_min-1, -1):
    took_too_long = False
    UAV_test_round = -1
    next_test_round = 0
    problem_params.T = N
    problem_params.T_inner = hor_inner

    mean_list = np.full((NUM_TESTS, 1), np.nan)
    median_list = np.full((NUM_TESTS, 1), np.nan)
    hor_mean_list = np.full((NUM_TESTS, 1), np.nan)
    hor_median_list = np.full((NUM_TESTS, 1), np.nan)
    vert_mean_list = np.full((NUM_TESTS, 1), np.nan)
    vert_median_list = np.full((NUM_TESTS, 1), np.nan)
    landing_list = np.full((NUM_TESTS, 1), np.nan)
    if PARALLEL:
        hor_inner_mean_list = np.full((NUM_TESTS, 1), np.nan)
        hor_inner_median_list = np.full((NUM_TESTS, 1), np.nan)
        vert_inner_mean_list = np.full((NUM_TESTS, 1), np.nan)
        vert_inner_median_list = np.full((NUM_TESTS, 1), np.nan)

    # Wait for USV tester before creating next simulator
    # If the UAV and USV testers have simulators with different time horizons,
    # some of the callbacks between them will mess up
    round_pub.publish(Int32(-1))
    # Sometimes other tester had time to switch to round 0 too quickly and round -1 was never registered
    # while USV_test_round > 0:
    while USV_test_round != -1:
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
    my_uav_simulator = UAV_simulator(problem_params, travel_dir = dir)

    # Makes sure that UAV receives info about round being -1 before the round changes to 0
    time.sleep(0.5)

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
        print "Mean iteration:", np.mean(my_uav_simulator.iteration_durations)
        print "Mean horizontal:", np.mean(my_uav_simulator.hor_solution_durations)
        print "Mean vertical", np.mean(my_uav_simulator.vert_solution_durations)
        if PARALLEL:
            print "Mean horizontal inner:", np.mean(my_uav_simulator.hor_inner_solution_durations)
            print "Median horizontal inner:", np.median(my_uav_simulator.hor_inner_solution_durations)
            print "Mean vertical inner:", np.mean(my_uav_simulator.vert_inner_solution_durations)
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
        for j in range(len(z_traj)-1):
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
        if PARALLEL:
            hor_inner_mean_list[i] = np.mean(my_uav_simulator.hor_inner_solution_durations)
            hor_inner_median_list[i] = np.median(my_uav_simulator.hor_inner_solution_durations)
            vert_inner_mean_list[i] = np.mean(my_uav_simulator.vert_inner_solution_durations)
            vert_inner_median_list[i] = np.median(my_uav_simulator.vert_inner_solution_durations)
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
            took_too_long = True
            print "TOOK TO LONG!"
            instruct_pub.publish(Int32(NEXT_HORIZON))
            break
        if (np.mean(my_uav_simulator.iteration_durations) > SAMPLING_TIME\
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

# #DEBUG
# try:
#     my_uav_simulator.plot_results(True)
# except Exception as e:
#     # Exception is sometimes thrown when window is closed
#     print e
#     pass

instruct_pub.publish(Int32(N))
if not cancelled:
    print "ENTERING HERE! COMMUNICATION ISSUES AFTER THIS POINT AREN'T A BIG DEAL"
    # Store data from the last successfull simulation
    test_info_str = "min horizon: " + str(hor_min) + "\nmax horizon: " \
        + str(hor_max) + "\nnumber of trials: " + str(NUM_TESTS)
    exp_index = my_uav_simulator.store_data(test_info_str = test_info_str)
    experiment_index_pub.publish(Int8(exp_index))
    print "SENT EXPERIMENT INDEX", exp_index

    # dir_path = '/home/student/robbj_experiment_results/'
    dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEAN.csv', mean_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEDIAN.csv', median_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEAN.csv', hor_mean_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEDIAN.csv', hor_median_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/VERT_MEAN.csv', vert_mean_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/VERT_MEDIAN.csv', vert_median_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/LANDING_TIMES.csv', landing_list, delimiter=',')
    time_str = str((UAV_time - USV_time).secs) + "\n" + str((UAV_time - USV_time).nsecs)
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/time_diff.txt', [time_str], fmt="%s")

    if PARALLEL:
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEAN.csv', hor_inner_mean_list, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEDIAN.csv', hor_inner_median_list, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/VERT_INNER_MEAN.csv', vert_inner_mean_list, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/VERT_INNER_MEDIAN.csv', vert_inner_median_list, delimiter=',')

    # Wait for USV to finish storing data. If we exit before this, USV will never receive experiment index
    while USV_has_stored_data == 0:
        if random.randint(1, 101) == 100:
            print "Waiting for USV to finish storing"
        if rospy.is_shutdown():
            break
        time.sleep(0.1)

print "SENDING -2"
experiment_index_pub.publish(Int8(-2))
