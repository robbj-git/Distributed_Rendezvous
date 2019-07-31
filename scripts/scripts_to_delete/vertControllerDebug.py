#!/usr/bin/env python
import rospy
from Dynamics import *
# from callbacks import *
from math import ceil
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header
from geometry_msgs.msg import Vector3Stamped, QuaternionStamped
from dji_sdk.srv import SDKControlAuthority
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
import cvxpy as cp
#import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import osqp
import thread
# import threading
from problemClasses import *

USE_ROS = False
CENTRALISED = False
DISTRIBUTED = not CENTRALISED
PARALLEL = False
delay_time = 0.75
delay_len = int(ceil(delay_time/SAMPLING_TIME))
# delay_len = 5   # DEBUG

global x_m, xv_m, phi, theta, long_ref, lat_ref, w_1, w_2
long_ref = None
lat_ref = None
phi = 0.0
theta = 0.0
w_1 = 0.0
w_2 = 0.0

x_m = np.zeros((4, 1))
xb_m = np.matrix([[15], [30], [0], [0]])
xv_m = np.matrix([[12], [0]])
xhat_m = np.zeros(( nUAV*(T+1), 1 ))
xbhat_m = np.zeros(( nUSV*(T+1), 1 ))
for t in range(T + 1):
    xbhat_m[4*t:4*(t+1)] = xb_m

amin  =  -5.0
amax  =   5.0
amin_b = -3.0
amax_b =  3.0
hs = 5.0
ds = 2.0
dl = 1.0
wmin = -1.0
wmax = 1.0
wmin_land = -0.3
# Additional allowed negative vertical velocity per unit height
kl = 0.2

class Parameters():

    def __init__(self, amin, amax, amin_b, amax_b, hs, ds, dl, \
        wmin, wmax, wmin_land, kl):
        self.amin = amin
        self.amax = amax
        self.amin_b = amin_b
        self.amax_b = amax_b
        self.hs = hs
        self.ds = ds
        self.dl = dl
        self.wmin = wmin
        self.wmax = wmax
        self.wmin_land = wmin_land
        self.kl = kl

# Inpired by https://osqp.org/docs/examples/mpc.html
xhat_traj_0  = np.empty((nUAV*(T+1), 1))
xbhat_traj_0 = np.empty((nUSV*(T+1), 1))
for i in range(T+1):
    xhat_traj_0[ i*nUAV : (i+1)*nUAV] = x_m
    xbhat_traj_0[i*nUSV : (i+1)*nUSV] = xb_m

params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
    wmin, wmax, wmin_land, kl)
problemCent = CentralisedProblem(T, A, B, Ab, Bb, Q, P, R, params)
problemDist = DistributedProblem(T, A, B, Ab, Bb, Q, P, R,\
    delay_len, xhat_traj_0, xbhat_traj_0, params)
problemVert = VerticalProblem(T, Av, Bv, Qv, Pv, Rv, params)

x_log  = np.empty((nUAV, sim_len+1))
xb_log = np.empty((nUSV, sim_len+1))
xv_log = np.empty((nv,   sim_len+1))
UAV_trajectories = np.empty((nUAV*(T+1), sim_len))
USV_trajectories = np.empty((nUSV*(T+1), sim_len))
x_log.fill(np.nan)
xb_log.fill(np.nan)
xv_log.fill(np.nan)
UAV_trajectories.fill(np.nan)
USV_trajectories.fill(np.nan)

# iteration_durations = [None]*sim_len
iteration_durations = [0]*sim_len
dist_solution_durations = [0]*sim_len
cent_solution_durations = [0]*sim_len
vert_solution_durations = [0]*sim_len

# # DEBUG !!!!!!!!!!!
# saved_fast_traj = False
# saved_slow_traj = False

t_since_update = 0
loop_iter_time_sum = 0
USV_should_stop = True # Set to True if USV shoul

fast_file = "Fasttraj.txt"
slow_file = "Slowtraj.txt"

fast_traj = np.loadtxt(fast_file)
slow_traj = np.loadtxt(slow_file)
shape = fast_traj.shape
fast_traj = np.reshape(fast_traj, (shape[0], 1))
slow_traj = np.reshape(slow_traj, (shape[0], 1))

num_its = 100
fast_durations = np.empty((num_its, 1))
slow_durations = np.empty((num_its, 1))

for i in range(num_its):
    vert_start = time.time()
    problemVert.solve(np.matrix([[5+i], [0]]), 0.0, fast_traj)
    vert_end = time.time()
    fast_durations[i] = vert_end - vert_start

    vert_start = time.time()
    problemVert.solve(np.matrix([[5+i], [0]]), 0.0, slow_traj)
    vert_end = time.time()
    slow_durations[i] = vert_end - vert_start

# print fast_durations
print "Mean, fast:", np.mean(fast_durations), "slow:", np.mean(slow_durations)
print "Median:", np.median(fast_durations), "slow:", np.median(slow_durations)
print "Standard dev:", np.std(fast_durations), "slow:", np.std(slow_durations)
print "Max:", np.max(fast_durations), "slow:", np.max(slow_durations)
print "Min:", np.min(fast_durations), "slow:", np.min(slow_durations)
