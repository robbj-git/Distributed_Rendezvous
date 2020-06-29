#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Bool, Int8, Time
from time import sleep
from IMPORT_MAIN import settings
from IMPORT_USV import USV_parameters
from IMPORT_UAV import B
from USV_simulation import USV_simulator
from random import randint
from helper_functions import get_travel_dir

class ProblemParams():
    def __init__(self):
        self.settings = settings
        self.params = USV_parameters
        self.T = 0
        self.T_inner = 0
        [self.nUAV, self.mUAV] = B.shape

def UAV_ready_callback(msg):
    global UAV_is_ready
    UAV_is_ready = msg.data

def experiment_index_callback(msg):
    global exp_index
    exp_index = msg.data

problem_params = ProblemParams()
problem_params.settings = settings
problem_params.params = USV_parameters

nUSV = problem_params.params.Ab.shape[0]
USV_ready_pub = rospy.Publisher('USV_ready', Bool, queue_size = 1, latch=True)
time_pub = rospy.Publisher('USV_time', Time, queue_size = 1, latch = False)
rospy.Subscriber('UAV_ready', Bool, UAV_ready_callback)
rospy.Subscriber('experiment_index', Int8, experiment_index_callback)

xb =  np.array([[-6], [6], [0], [0]])
if not settings.CENTRALISED and settings.ADD_USV_SECOND_OBJECTIVE:
    # Makes the UAV attempt to move at a constant velocity as a second
    # objective. This velocity is along the line between the USV's
    # initial position and the origin.

    # Should the velocity point from the USV initial position or not?
    reverse_dir = False
    dir = get_travel_dir(xb, reverse_dir)
else:
    dir = None

global UAV_is_ready, exp_index
UAV_is_ready = False
exp_index = -1

rospy.init_node('USV_main')

# ------- SET THESE ---------
# T: Prediction horizon
# T_inner: Inner prediction, only used in cascading case
if settings.CENTRALISED:
    problem_params.T = 70
    problem_params.T_inner = None
elif settings.DISTRIBUTED:
    problem_params.T = 100
    problem_params.T_inner = None
elif settings.PARALLEL:
    problem_params.T = 120
    problem_params.T_inner = 60
# ---------------------------

USV_simulator = USV_simulator(problem_params, travel_dir = dir)

USV_ready_pub.publish(Bool(True))

while not UAV_is_ready:
    if rospy.is_shutdown():
        break
    if randint(1, 101) == 100:
        print "Waiting for UAV to be ready"
    sleep(0.1)

# Sends current time to UAV for comparison, in case clocks are not synchronised
msg = Time()
msg.data = rospy.Time.now()
time_pub.publish(msg)

USV_simulator.simulate_problem(settings.sim_len, xb)
print "Mean iteration duration:", np.mean(USV_simulator.iteration_durations)

while exp_index == -1:
    if rospy.is_shutdown():
        exp_index = -2
        break
    if randint(1, 101) == 100:
        print "Waiting for experiment index"
    sleep(0.01)

if exp_index != -2:
    # Don't store anything if storing was cancelled
    USV_simulator.store_data(exp_index)
    print "Stored data with experiment index", exp_index
