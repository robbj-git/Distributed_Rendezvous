#!/usr/bin/env python
import rospy
from Dynamics import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
# from callbacks import *
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
from helper_classes import Parameters
from helper_functions import dist_traj

# from geometry_msgs.msg import Quaternion, Vector3Stamped
from math import sin, cos, atan, atan2, asin, pi, sqrt

def IMU_callback(msg):
    global w_1, w_2
    # TODO: FIGURE OUT WHAT MESSAGE TYPE THIS IS!!! TWIST PERHAPS???
    w_1 = msg.angular_velocity.x
    w_2 = msg.angular_velocity.y

def height_callback(msg):
    global xv_m
    xv_m[0] = msg.data

def velocity_callback(msg):
    global xv_m, x_m
    x_m[2]  = msg.vector.x
    x_m[3]  = msg.vector.y
    xv_m[1] = msg.vector.z

def pos_callback(msg):
    global x_m, long_ref, lat_ref
    R = 6378138.12

    if long_ref is None:
        long_ref = msg.longitude
    if lat_ref is None:
        lat_ref = msg.latitude

    phi_gps = msg.latitude
    phi_ref = lat_ref
    lambda_gps = msg.longitude
    lambda_ref = long_ref

    x_m[0:2] = lat_long_to_pos(phi_gps, lambda_gps, phi_ref, lambda_ref, R);

def attitude_callback(msg):
    global phi, theta
    qw = msg.quaternion.w
    qx = msg.quaternion.x
    qy = msg.quaternion.y
    qz = msg.quaternion.z
    phi = atan( 2*(qw*qx + qy*qz)/(1 - 2*(qx*qx + qy*qy)) )
    theta = asin(2*(qw*qy-qz*qx))

def lat_long_to_pos(phi, lambd, phi0, lambd0, R):

    # lambd is supposed to be called lambda, but that's a reserved keyword
    phi =     pi*phi    /180.0
    lambd =  pi*lambd /180.0
    phi0 =    pi*phi0   /180.0
    lambd0 = pi*lambd0/180.0

    delta_lambd = lambd - lambd0

    k1 = sin(delta_lambd)*cos(phi)
    k2 = cos(phi0)*sin(phi) - sin(phi0)*cos(phi)*cos(delta_lambd)
    k3 = sin((phi0 - phi)*0.5)
    k4 = sin((lambd0 - lambd)*0.5)

    zeta = atan2(k1, k2)
    d = 2*R*asin(sqrt( k3*k3 + cos(phi0)*cos(phi)*k4*k4 ))

    return np.matrix([[d*sin(zeta)], [d*cos(zeta)]])

# -------------------------- PROBLEM DEFINITION -------------------------

#  MAKE SURE TO IMPORT Dynamics.py and IMPORT_ME.py !!!!!!!!!!!!!!!!!!!!!!!

global x_m, xv_m, phi, theta, long_ref, lat_ref, w_1, w_2
long_ref = None
lat_ref = None
phi = 0.0
theta = 0.0
w_1 = 0.0
w_2 = 0.0

x_m = np.matrix([[0.0], [0.0], [0.0], [0.0]])
xb_m = np.matrix([[15.0], [30.0], [0.0], [0.0]])
xv_m = np.matrix([[12.0], [0.0]])
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
vmax = 5.0

# Inpired by https://osqp.org/docs/examples/mpc.html
xhat_traj_0  = np.empty((nUAV*(T+1), 1))
xbhat_traj_0 = np.empty((nUSV*(T+1), 1))
for i in range(T+1):
    xhat_traj_0[ i*nUAV : (i+1)*nUAV] = x_m
    xbhat_traj_0[i*nUSV : (i+1)*nUSV] = xb_m


# # CRAZY DEBUG TOTAL CRAZYNESS!!!!
# my_x = np.matrix([[10], [10], [10], [10]])
# my_u = np.matrix([[1], [1]])
# for t in range(10):
#     my_x = A*my_x + B*my_u
# print "final state:", my_x
# print B

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"

params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
    wmin, wmax, wmin_land, kl, vmax)
problemCent = CentralisedProblem(T, A, B, Ab, Bb, Q, 1*P, R, CVXPy, params)
problemDist = DistributedProblem(T, A, B, Ab, Bb, Q, P, R,\
    delay_len, xhat_traj_0, xbhat_traj_0, CVXPy, params)
problemVert = VerticalProblem(T, Av, Bv, Qv, Pv, Rv, CVXPy, params)
# --------------------------- ROS SETUP ----------------------------------

if USE_ROS:
    rospy.init_node('rendezvous_simulator')

    rospy.Subscriber('dji12/dji_sdk/imu', Imu, IMU_callback)
    rospy.Subscriber('dji12/dji_sdk/height_above_takeoff', Float32, height_callback)
    rospy.Subscriber('dji12/dji_sdk/velocity', Vector3Stamped, velocity_callback)
    rospy.Subscriber('dji12/dji_sdk/gps_position', NavSatFix, pos_callback)
    rospy.Subscriber('dji12/dji_sdk/attitude', QuaternionStamped, attitude_callback)

    UAV_publisher = rospy.Publisher('/dji12/dji_sdk/flight_control_setpoint_generic',\
        Joy, queue_size = 10)

    print('Waiting for control authority serivce')
    rospy.wait_for_service('/dji12/dji_sdk/sdk_control_authority')
    print('Finished waiting')

    # TODO: Can I make this succeed somehow??
    try:
        authority_server = rospy.ServiceProxy(\
            '/dji12/dji_sdk/sdk_control_authority', SDKControlAuthority)
        control_response = authority_server(1)
    except:
        print "Failed reaching control authority. Sleeping for 3s."
        time.sleep(3)

    rate = rospy.Rate(SAMPLING_RATE)
# -------------- PROBLEM SIMULATION ---------------
x_log  = np.empty((nUAV, sim_len+1))
xb_log = np.empty((nUSV, sim_len+1))
xv_log = np.empty((nv,   sim_len+1))
uUAV_log = np.empty((mUAV, sim_len))
uUSV_log = np.empty((mUSV, sim_len))
UAV_trajectories = np.empty((nUAV*(T+1), sim_len))
USV_trajectories = np.empty((nUSV*(T+1), sim_len))
vert_trajectories = np.empty((2*(T+1), sim_len))
x_log.fill(np.nan)
xb_log.fill(np.nan)
xv_log.fill(np.nan)
uUAV_log.fill(np.nan)
uUSV_log.fill(np.nan)
UAV_trajectories.fill(np.nan)
USV_trajectories.fill(np.nan)
vert_trajectories.fill(np.nan)

# iteration_durations = [None]*sim_len
iteration_durations = [0]*sim_len
dist_solution_durations = [0]*sim_len
cent_solution_durations = [0]*sim_len
vert_solution_durations = [0]*sim_len

# DEBUG !!!!!!!!!!!
saved_fast_traj = False
saved_slow_traj = False

t_since_update = 0
loop_iter_time_sum = 0
USV_should_stop = False # Set to True if USV should stop acting and become passive
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3) # For plotting inside of loop
start = time.time()
for i in range(sim_len):
    if rospy.is_shutdown():
        break

    # Weird indexing to preserve dimensions
    x_log[:, i:i+1]  = x_m
    xb_log[:, i:i+1] = xb_m
    xv_log[:, i:i+1] = xv_m

    # ------------------- SOLVE OPTIMISATION PROBLEMS --------------------
    if i==0 or not PARALLEL:
        if CENTRALISED:
            start_cent = time.time()
            problemCent.solve(x_m, xb_m)
            cent_solution_durations[i] = time.time() - start_cent
            x_traj = problemCent.x.value
            xb_traj = problemCent.xb.value
            dist = dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
        elif DISTRIBUTED:
            start_dist = time.time()
            problemDist.solve(x_m, xb_m, USV_should_stop)
            dist_solution_durations[i] = time.time() - start_dist
            x_traj = problemDist.x.value
            xb_traj = problemDist.xb.value
            dist = dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
    elif i%10 == 0 and PARALLEL:
        if CENTRALISED:
            problemCent.solve_threaded(x_m, xb_m)
        elif DISTRIBUTED:
            problemDist.solve_threaded(x_m, xb_m)

    # ----------------------- VERTICAL PROBLEM ---------------------------
    # Updates  distance trajectory if problem has recently been solved
    if PARALLEL and CENTRALISED and problemCent.t_since_update == 0:
        dist = dist_traj(problemCent, T, nUAV, nUSV)
    elif PARALLEL and DISTRIBUTED and problemDist.t_since_update == 0:
        dist = dist_traj(problemDist, T, nUAV, nUSV)

    # Once UAV and USV are close enough, stop the USV to reduce fluctuations
    if dist[0] < ds and DISTRIBUTED:
        USV_should_stop = True

    vert_start = time.time()
    problemVert.solve(xv_m, 0.0, dist)
    vert_solution_durations[i] = time.time() - vert_start

    # # DEBUG
    # if vert_solution_durations[i] < 0.025 and not saved_fast_traj:
    #     # np.savetxt("Fasttraj.txt", dist)
    #     crazy_vert_debug(problemVert, xv_m, dist)
    #     saved_fast_traj = True
    #     print "FAST:", vert_solution_durations[i]
    # elif vert_solution_durations[i] > 0.04 and not saved_slow_traj:
    #     # np.savetxt("Slowtraj.txt", dist)
    #     crazy_vert_debug(problemVert, xv_m, dist)
    #     saved_slow_traj = True
    #     print "SLOW:", vert_solution_durations[i]


    # ----------------------- ASSIGN uUAV AND uUSV -----------------------
    if CENTRALISED:
        if not PARALLEL or problemCent.t_since_update == 0:
            uUAV = problemCent.u[ 0:mUAV, 0:1].value
            uUSV = problemCent.ub[0:mUSV, 0:1].value
        else:
            # Using linear feedback intermediate controller
            uUAV = KUAV*(x_m  -  problemCent.\
                x[t_since_update*nUAV:(t_since_update+1)*nUAV].value)
            uUSV = KUSV*(xb_m - problemCent.\
                xb[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
            uUAV = -np.clip(uUAV, amin,   amax)
            uUSV = -np.clip(uUSV, amin_b, amax_b)

        problemCent.t_since_update += 1
        t_since_update = problemCent.t_since_update
        UAV_trajectories[:, i:i+1] = problemCent.x.value
        USV_trajectories[:, i:i+1] = problemCent.xb.value
    elif DISTRIBUTED:
        if not PARALLEL or problemDist.t_since_update == 0:
            uUAV = problemDist.u[ 0:mUAV, 0:1].value
            uUSV = problemDist.ub[0:mUSV, 0:1].value
        else:
            # Using linear feedback intermediate controller
            uUAV = KUAV*(x_m  -  problemDist.\
                x[t_since_update*nUAV:(t_since_update+1)*nUAV].value)
            uUSV = KUSV*(xb_m - problemDist.\
                xb[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
            uUAV = -np.clip(uUAV, amin,   amax)
            uUSV = -np.clip(uUSV, amin_b, amax_b)

        problemDist.t_since_update += 1
        t_since_update = problemDist.t_since_update
        UAV_trajectories[:, i:i+1] = problemDist.x.value
        USV_trajectories[:, i:i+1] = problemDist.xb.value

    uUAV_log[:, i:i+1] = uUAV;
    uUSV_log[:, i:i+1] = uUSV;

    vert_trajectories[:, i:i+1] = problemVert.xv.value

    # ----------- SIMULATE DYNAMICS / PUBLISH CONTROL INPUTS -------------
    wdes_current = problemVert.wdes[0:mv, 0:1].value
    if wdes_current is None:
        wdes_current = 0
        print('Wdes was None, iteration:', i)
        break   # DEBUG !!!!

    # uUSV = np.matrix([[-1.0], [-1.0]])

    xb_m = Ab*xb_m + Bb*uUSV
    if not USE_ROS:
        x_m  =  A*x_m  +  B*uUAV
        xv_m = Av*xv_m + Bv*wdes_current
    if USE_ROS:
        phi_cmd, theta_cmd = get_cmd_angle(uUAV, uUSV, wdes_current, xv_m)
        axes = [phi_cmd, theta_cmd, wdes_current, 0.0, 0x02]
        UAV_msg = Joy(Header(), axes, [])
        UAV_publisher.publish(UAV_msg)

    # # # #  ----- PLOTTING, ruins performace, so only use it for debugging  -------
    # distance = np.sqrt( np.square(x_log[0, :] - xb_log[0, :])\
    #     + np.square(x_log[1, :] - xb_log[1, :]) )
    #
    # forbidden_area_1 = Polygon([ (dl, 0),\
    #                              (ds, hs),\
    #                              (10, hs),\
    #                              (10, 0)], True)
    # forbidden_area_2 = Polygon([ (-dl, 0),\
    #                              (-ds, hs),\
    #                              (-10, hs),\
    #                              (-10, 0)], True)
    # p2 = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)
    #
    # # REAL-TIME, not sure if try-except works
    # try:
    #     t = i
    #     safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
    #     p1 = PatchCollection([safe_circle], alpha=0.1)
    #     ax1.add_collection(p1)
    #     UAV_traj = np.reshape(UAV_trajectories[:,t], (nUAV, T+1), order='F')
    #     USV_traj = np.reshape(USV_trajectories[:,t], (nUSV, T+1), order='F')
    #     ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
    #     ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')
    #
    #     ax1.plot(x_log[0, 0:t+1], x_log[1, 0:t+1], 'bx')
    #     ax1.plot(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 'rx')
    #     ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
    #     ax1.grid(True)
    #     ax2.grid(True)
    #     plt.pause(0.01)
    #
    #     ax1.cla()
    # except:
    #     pass

    # ---------------------------- SLEEP ---------------------------------
    end = time.time()
    # print(end - start)
    # loop_iter_time_sum += end-start
    iteration_durations[i] = end-start
    if USE_ROS:
        rate.sleep()
    else:
        try:
            time.sleep(SAMPLING_TIME - end + start)
        except:
            pass
    start = time.time()

# print 'Mean iteration time:', np.mean(iteration_durations)
# print 'Median iteration time:', np.median(iteration_durations)
# print 'Standard deviation:', np.std(iteration_durations)
# print 'Centralised solution:', np.mean(cent_solution_durations)
# print 'Median centralised:', np.median(cent_solution_durations)
print 'Distributed solution:', np.mean(dist_solution_durations)
print 'Median distributed:', np.median(dist_solution_durations)
print 'Vertical solution:', np.mean(vert_solution_durations)
print "Median vertical:", np.median(vert_solution_durations)
# print 'Max vertical:', np.max(vert_solution_durations)

# Weird indexing to preserve dimensions
x_log[:, -nUAV:sim_len+1]  = x_m
xb_log[:, -nUSV:sim_len+1] = xb_m
xv_log[:, -2:sim_len+1] = xv_m
# ------------------------------ PLOTTING --------------------------------

distance = np.sqrt( np.square(x_log[0, :] - xb_log[0, :])\
    + np.square(x_log[1, :] - xb_log[1, :]) )

# fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
#
forbidden_area_1 = Polygon([ (dl, 0),\
                             (ds, hs),\
                             (10, hs),\
                             (10, 0)], True)
forbidden_area_2 = Polygon([ (-dl, 0),\
                             (-ds, hs),\
                             (-10, hs),\
                             (-10, 0)], True)
p2 = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)

# ### REAL-TIME, not sure if try-except works
# for t in range(sim_len):
#     safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
#     p1 = PatchCollection([safe_circle], alpha=0.1)
#     ax1.add_collection(p1)
#     UAV_traj = np.reshape(UAV_trajectories[:,t], (nUAV, T+1), order='F')
#     USV_traj = np.reshape(USV_trajectories[:,t], (nUSV, T+1), order='F')
#     vert_traj = np.reshape(vert_trajectories[:,t], (2, T+1), order='F')
#     ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
#     ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')
#
#     pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
#         (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )
#
#     ax1.plot(x_log[0, 0:t+1], x_log[1, 0:t+1], 'bx')
#     ax1.plot(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 'rx')
#     ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t])
#     ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
#     # ax2.plot(range(t+1), xv_log[0, 0:t+1], 'b')
#     ax2.plot(pred_dist, vert_traj[0, 0:T+1], 'y')
#     # ax2.plot(range(t+1, t+1 + T+1), vert_traj[0, 0:T+1], 'y')
#     ax2.add_collection(p2)
#
#     ax3.plot([SAMPLING_TIME*i for i in range(t+1)], distance[0:t+1], 'k')
#
#     #print "UAV speed:", np.sqrt(x_log[2,t]**2 + x_log[3,t]**2)
#     #print "UAV speeds:", x_log[2,t], " , ", x_log[3,t]
#
#     ax1.grid(True)
#     ax2.grid(True)
#     ax3.grid(True)
#     plt.pause(0.01)
#
#     ax1.cla()
#     ax2.cla()


# NOT REAL-TIME
ax1.plot(x_log[0, :], x_log[1, :], 'bx')
ax1.plot(xb_log[0, :], xb_log[1, :], 'rx')
ax2.plot(distance, xv_log[0, :], 'b')
UAV_traj = np.reshape(UAV_trajectories[:,213-1], (nUAV, T+1), order='F')    # TODO: REMOVE. I'M PRETTY SURE THIS DOES NOTHING USEFUL
USV_traj = np.reshape(USV_trajectories[:,213-1], (nUSV, T+1), order='F')
ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')
ax1.grid(True)
ax2.grid(True)

safe_circle = Circle((xb_log[0, sim_len], xb_log[1, sim_len]), ds)
p1 = PatchCollection([safe_circle], alpha=0.2)

ax1.add_collection(p1)
ax2.add_collection(p2)

plt.show()
