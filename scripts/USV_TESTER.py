#!/usr/bin/env python
import rospy
from IMPORT_ME import settings, NEXT_HORIZON
from matrices_and_parameters import dynamics_parameters
from helper_classes import Parameters
from helper_functions import mat_to_multiarray_stamped, get_dist_traj, get_travel_dir
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

global UAV_test_round, should_change_horizon, should_finish, quit_horizon, exp_index
UAV_test_round = np.inf
should_change_horizon = False
should_finish = False
quit_horizon = -1
exp_index = -1

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

def experiment_index_callback(msg):
    global exp_index
    exp_index = msg.data

rospy.init_node('USV_main')

round_pub = rospy.Publisher('USV_test_round', Int32, queue_size = 10, latch = True)
store_pub = rospy.Publisher('USV_has_stored_data', Int32, queue_size = 1, latch = True)
time_pub = rospy.Publisher('USV_time', Time, queue_size = 1, latch = False)
rospy.Subscriber('UAV_test_round', Int32, UAV_test_round_callback)
rospy.Subscriber('UAV_instruction', Int32, UAV_instruction_callback)
rospy.Subscriber('experiment_index', Int8, experiment_index_callback)
has_sent_time = False

class ProblemParams():
    def __init__(self):
        self.settings = settings
        self.params = dynamics_parameters
        self.T = 0
        self.T_inner = 0

problem_params = ProblemParams()

# -2, 1
xb_m = np.array([[-6], [6], [np.nan], [np.nan]])

reverse_dir = False
dir = get_travel_dir(xb_m, reverse_dir)
xb_m[2:4] = np.zeros((2, 1))#dir
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
NUM_TESTS = 1
if settings.PARALLEL:
    hor_max = 120#347#170#420#405#100
    hor_min = 120#347#170#420#300#100
elif settings.CENTRALISED:
    hor_max = 100#195#150#120
    hor_min = 100#80#120
elif settings.DISTRIBUTED:
    hor_max = 100#280#100
    hor_min = 100

hor_inner = 60#30#15

for N in range(hor_max, hor_min-1, -1):
    took_too_long = False
    USV_test_round = -1
    next_test_round = 0
    problem_params.T = N
    problem_params.T_inner = hor_inner

    it_mean_list = np.full((NUM_TESTS, 1), np.nan)
    it_median_list = np.full((NUM_TESTS, 1), np.nan)
    if not settings.CENTRALISED:
        hor_mean_list = np.full((NUM_TESTS, 1), np.nan)
        hor_median_list = np.full((NUM_TESTS, 1), np.nan)
    if settings.PARALLEL:
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

    if not has_sent_time:
        msg = Time()
        msg.data = rospy.Time.now()
        time_pub.publish(msg)
        print "TOTS PUBBED TIME!"

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

        my_usv_simulator.simulate_problem(settings.sim_len, xb_m)
        # time.sleep(20)
        # my_usv_simulator.store_data()
        # try:
        #     my_usv_simulator.plot_results(True)
        # except:
        #     pass


        it_mean_list[i] = np.mean(my_usv_simulator.iteration_durations)
        it_median_list[i] = np.median(my_usv_simulator.iteration_durations)
        if not settings.CENTRALISED:
            hor_mean_list[i] = np.mean(my_usv_simulator.hor_solution_durations)
            hor_median_list[i] = np.median(my_usv_simulator.hor_solution_durations)
        if settings.PARALLEL:
            hor_inner_mean_list[i] = np.mean(my_usv_simulator.hor_inner_solution_durations)
            hor_inner_median_list[i] = np.median(my_usv_simulator.hor_inner_solution_durations)

        print "Finished simulation round", i, "with horizon", N
        print "Mean iteration:", np.mean(my_usv_simulator.iteration_durations)
        if not settings.CENTRALISED:
            print "Mean solution:", np.mean(my_usv_simulator.hor_solution_durations)
        if settings.PARALLEL:
            print "Mean inner solution", np.mean(my_usv_simulator.hor_inner_solution_durations)
        if np.mean(my_usv_simulator.iteration_durations) > SAMPLING_TIME and \
            np.median(my_usv_simulator.iteration_durations) > SAMPLING_TIME:
            print "ITERATION TOOK TOO LONG"
            took_too_long = True
        # ------------- FOR PARALLEL ------------
        if settings.PARALLEL and \
            np.mean(my_usv_simulator.hor_solution_durations) > \
                settings.INTER_ITS*SAMPLING_TIME and\
            np.median(my_usv_simulator.hor_solution_durations) > \
                settings.INTER_ITS*SAMPLING_TIME:
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

while exp_index == -1:
    if rospy.is_shutdown():
        exp_index = -2
        break
    if random.randint(1, 101) == 100:
        print "Waiting for experiment index"
    time.sleep(0.01)

if quit_horizon >= 0 and exp_index != -2:
    print "Storing!"
    if N == quit_horizon:
        my_usv_simulator.store_data(exp_index)
    else:
        # It is possible that the outer loop increments N while the UAV tester
        # is still at the previous value of N. If the UAV-tester then quits,
        # my_usv_simulator will not be the correct simulator.
        prev_simulator.store_data(exp_index)
    if ever_took_too_long:
        print 'OMG HOW ON EARTH DID IT EVER TAKE TOO LONG????? Horizon:', took_too_long_horizon

    dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'
    dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
    if not dir_already_exists:
        os.mkdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
    # TODO: Why and when is UAV notified about that the USV has finished storing?
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEAN_USV.csv', it_mean_list, delimiter=',')
    np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/MEDIAN_USV.csv', it_median_list, delimiter=',')
    if not settings.CENTRALISED:
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEAN_USV.csv', hor_mean_list, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_MEDIAN_USV.csv', hor_median_list, delimiter=',')
    if settings.PARALLEL:
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEAN_USV.csv', hor_inner_mean_list, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/HOR_INNER_MEDIAN_USV.csv', hor_inner_median_list, delimiter=',')

else:
    print "nope, no storing", rospy.Time.now()

store_pub.publish(Int32(1))
