#!/usr/bin/env python
import rospy
from matrices_and_parameters import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters
from helper_functions import mat_to_multiarray_stamped, get_dist_traj, get_travel_dir
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
from USV_simulation import USV_simulator
import pdb
import random

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

def get_USV_travel_dir(xb, reverse_dir = False):
    len = np.sqrt(np.sum(np.square(xb[0:2])))
    if len > 0:
        if reverse_dir:
            return -xb[0:2]/len
        else:
            return xb[0:2]/len
    else:
        raise ZeroDivisionError("First two elements of argument must have norm greater than zero")

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
        self.USE_HIL = USE_HIL
        self.INTER_ITS = INTER_ITS
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
        self.Qb_vel = Qb_vel
        self.Pb_vel = Pb_vel
        self.Q_vel = Q_vel
        self.P_vel = P_vel
        self.used_solver = used_hor_solver
        self.lookahead = lookahead
        self.KUAV = KUAV
        self.KUSV = KUSV
        self.params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
            wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max, ang_vel_max)
        self.delay_len = delay_len
        self.ADD_DROPOUT = ADD_DROPOUT
        self.PRED_PARALLEL_TRAJ = PRED_PARALLEL_TRAJ
        self.SHOULD_SHIFT_MESSAGES = SHOULD_SHIFT_MESSAGES
        self.dropout_lower_bound = dropout_lower_bound
        self.dropout_upper_bound = dropout_upper_bound

problem_params = ProblemParams()

# -2, 1
xb_m = np.array([[-5], [4], [np.nan], [np.nan]])

reverse_dir = False
dir = get_travel_dir(xb_m, reverse_dir)
xb_m[2:] = dir
 # 5 and 0.8

# TODO, REMOVE THIS, DO CALCULATIONS IN USV_SIMULATOR

# x1 = 5.0*dir[0]
# x2 = 0.8*dir[0]
# y1 = 5.0*dir[1]
# y2 = 0.8*dir[1]
# problem_params.params.v_max_x_b = max(x1, x2)
# problem_params.params.v_max_y_b = max(y1, y2)
# problem_params.params.v_min_x_b = min(x1, x2)
# problem_params.params.v_min_y_b = min(y1, y2)
# print "x:",min(x1, x2), 'to', max(x1, x2)
# print "y:",min(y1, y2), 'to', max(y1, y2)

# --------------- TESTING LOOP ------------------
# NUM_TESTS = 1 DOESN'T WORK, THE TESTERS FAIL WAITING FOR EACH OTHER
NUM_TESTS = 1#50
prev_simulator = None
my_usv_simulator = None

ever_took_too_long = False
took_too_long_horizon = -1

# Need to create a simulator, because simulators call rospy.node_init(), and
# that function must be called before anything can be published, but it also
# can only be called once, so I can't call it here myself
# SHOULD BE ABLE TO REMOVE, I INIT NODE ABOVE NOW!
# my_usv_simulator = USV_simulator(problem_params)
# my_usv_simulator.deinitialise() # We don't want it to receive callbacks
if PARALLEL:
    hor_max = 100#400#100
    hor_min = 100#200#100
elif CENTRALISED:
    hor_max = 60#120#130#120
    hor_min = 60#120#80#120
elif DISTRIBUTED:
    hor_max = 100#200#100
    hor_min = 100#100

hor_inner = 60#30#15

for N in range(hor_max, hor_min-1, -1):
    took_too_long = False
    USV_test_round = -1
    next_test_round = 0
    problem_params.T = N
    problem_params.T_inner = hor_inner

    it_mean_list = np.full((NUM_TESTS, 1), np.nan)
    it_median_list = np.full((NUM_TESTS, 1), np.nan)
    if not CENTRALISED:
        hor_mean_list = np.full((NUM_TESTS, 1), np.nan)
        hor_median_list = np.full((NUM_TESTS, 1), np.nan)
    if PARALLEL:
        hor_inner_mean_list = np.full((NUM_TESTS, 1), np.nan)
        hor_inner_median_list = np.full((NUM_TESTS, 1), np.nan)

    # Wait for UAV tester before creating next simulator
    # If the UAV and USV testers have simulators with different time horizons,
    # some of the callbacks between them will mess up
    round_pub.publish(Int32(-1))
    # Sometimes other tester had time to switch to round 0 too quickly and round -1 was never registered
    # while UAV_test_round > 0:
    while UAV_test_round != -1:
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
    my_usv_simulator = USV_simulator(problem_params, travel_dir = dir)

    # Makes sure that UAV receives info about round being -1 before the round changes to 0
    time.sleep(0.5)

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
        # my_usv_simulator.store_data()
        # try:
        #     my_usv_simulator.plot_results(True)
        # except:
        #     pass


        it_mean_list[i] = np.mean(my_usv_simulator.iteration_durations)
        it_median_list[i] = np.median(my_usv_simulator.iteration_durations)
        if not CENTRALISED:
            hor_mean_list[i] = np.mean(my_usv_simulator.hor_solution_durations)
            hor_median_list[i] = np.median(my_usv_simulator.hor_solution_durations)
        if PARALLEL:
            hor_inner_mean_list[i] = np.mean(my_usv_simulator.hor_inner_solution_durations)
            hor_inner_median_list[i] = np.median(my_usv_simulator.hor_inner_solution_durations)

        print "Finished simulation round", i, "with horizon", N
        print "Mean iteration:", np.mean(my_usv_simulator.iteration_durations)
        if not CENTRALISED:
            print "Mean solution:", np.mean(my_usv_simulator.hor_solution_durations)
        if PARALLEL:
            print "Mean inner solution", np.mean(my_usv_simulator.hor_inner_solution_durations)
        if np.mean(my_usv_simulator.iteration_durations) > SAMPLING_TIME and \
            np.median(my_usv_simulator.iteration_durations) > SAMPLING_TIME:
            print "ITERATION TOOK TOO LONG"
            took_too_long = True
        # ------------- FOR PARALLEL ------------
        if PARALLEL and \
            np.mean(my_usv_simulator.hor_solution_durations) > \
                INTER_ITS*SAMPLING_TIME and\
            np.median(my_usv_simulator.hor_solution_durations) > \
                INTER_ITS*SAMPLING_TIME:
            print "SOLUTION TOOK TOO LONG"
            took_too_long = True
    if took_too_long:
        print 'USV TEST ACTUALLY TOOK TOO LONG!!!!!!!!!!!!!!'
        ever_took_too_long = True
        took_too_long_horizon = N
    if should_finish:
        should_finish = False
        print "Still asked to finish"
        break


print "started sleeping"
if not quit_horizon >= 0:
    # Sleep for a while, give UAV-tester a chance to finish
    time.sleep(20)

print "stopped sleeping"

# try:
#     my_usv_simulator.plot_results(True)
# except Exception as e:
#     # Sometimes exception is thrown when plotting window is closed
#     print "Error while plotting:"
#     print e
#     pass

store_pub.publish(Int32(1))
if quit_horizon >= 0:
    print "Storing!"
    if N == quit_horizon:
        exp_index = my_usv_simulator.store_data()
    else:
        # It is possible that the outer loop increments N while the UAV tester
        # is still at the previous value of N. If the UAV-tester then quits,
        # my_usv_simulator will not be the correct simulator.
        exp_index = prev_simulator.store_data()
    if ever_took_too_long:
        print 'OMG HOW ON EARTH DID IT EVER TAKE TOO LONG????? Horizon:', took_too_long_horizon

    dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'
    dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
    if not dir_already_exists:
        os.mkdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
    # TODO: Why and when is UAV notified about that the USV has finished storing?
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEAN_USV.txt', it_mean_list)
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEDIAN_USV.txt', it_median_list)
    if not CENTRALISED:
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEAN_USV.txt', hor_mean_list)
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEDIAN_USV.txt', hor_median_list)
    if PARALLEL:
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEAN_USV.txt', hor_inner_mean_list)
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEDIAN_USV.txt', hor_inner_median_list)

else:
    print "nope, no storing", rospy.Time.now()
