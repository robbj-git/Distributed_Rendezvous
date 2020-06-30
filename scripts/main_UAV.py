#!/usr/bin/env python
import rospy
import numpy as np
import os
from std_msgs.msg import Bool, Int8, Time
from time import sleep
from IMPORT_MAIN import settings
from IMPORT_UAV import UAV_parameters
from IMPORT_USV import Bb, hb
from UAV_simulation import UAV_simulator
from random import randint
from helper_functions import  get_travel_dir
if settings.CENTRALISED:
    from IMPORT_USV import USV_parameters

# Makes the USV try to follow a reference velocity instead of only helping the UAV to land
ADD_USV_SECOND_OBJECTIVE = True

class ProblemParams():
    def __init__(self):
        self.settings = settings
        self.params = UAV_parameters
        self.T = 0
        self.T_inner = 0
        [self.nUSV, self.mUSV] = Bb.shape
        self.hb = hb
        if settings.CENTRALISED:
            self.USV_params = USV_parameters
            # self.Ab = Ab
            # self.Bb = Bb
            # self.Qb_vel = Qb_vel
            # self.Pb_vel = Pb_vel
            # # self.amin_b = amin_b

def USV_ready_callback(msg):
    global USV_is_ready
    USV_is_ready = msg.data

def USV_time_callback(msg):
    global USV_time, UAV_time
    USV_time = msg.data
    UAV_time = rospy.Time.now()

problem_params = ProblemParams()
problem_params.settings = settings
problem_params.params = UAV_parameters

nUAV = problem_params.params.A.shape[0]
UAV_ready_pub = rospy.Publisher('UAV_ready', Bool, queue_size = 1, latch=True)
experiment_index_pub = rospy.Publisher('experiment_index', Int8, queue_size=1, latch=True)
rospy.Subscriber('USV_ready', Bool, USV_ready_callback)
rospy.Subscriber('USV_time', Time, USV_time_callback)
x = np.zeros((nUAV, 1))         # Initial UAV horizontal state
xv = np.array([[7.0], [0.0]])   # Initial USV horizontal state

if settings.CENTRALISED:
    xb =  np.array([[-6], [6], [0], [0]])
    if ADD_USV_SECOND_OBJECTIVE:
        # Makes the UAV attempt to move at a constant velocity as a second
        # objective. This velocity is along the line between the USV's
        # initial position and the origin.

        # Should the velocity point from the USV initial position or not?
        reverse_dir = False
        dir = get_travel_dir(xb, reverse_dir)
    else:
        dir = None

global USV_is_ready, UAV_time, USV_time
USV_is_ready = False
# Used to check time difference between UAV and USV in case the clocks on both
# machines are not synchronised
UAV_time = None
USV_time = None

rospy.init_node('UAV_main')

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

UAV_simulator = UAV_simulator(problem_params, travel_dir = dir)

UAV_ready_pub.publish(Bool(True))

while not USV_is_ready:
    if rospy.is_shutdown():
        break
    if randint(1, 101) == 100:
        print "Waiting for USV to be ready"
    sleep(0.1)

UAV_simulator.simulate_problem(settings.sim_len, x, xv)
print "Mean iteration duration:", np.mean(UAV_simulator.iteration_durations)
test_info_str = "A single trial with horizon", problem_params.T, "was performed"
exp_index = UAV_simulator.store_data(test_info_str = test_info_str)
experiment_index_pub.publish(Int8(exp_index))

dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'
dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
if not dir_already_exists:
    os.mkdir(dir_path + 'Experiment_' + str(exp_index) + '/TEST')
try:
    time_str = str((UAV_time - USV_time).secs) + "\n" + str((UAV_time - USV_time).nsecs)
except:
    print "Failed to store time difference between vehicles", UAV_time, USV_time
    time_str = "nan\nnan"
np.savetxt(dir_path + 'Experiment_'+str(exp_index)+'/TEST/time_diff.txt', [time_str], fmt="%s")
print "Stored data with experiment index", exp_index
