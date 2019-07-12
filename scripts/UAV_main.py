#!/usr/bin/env python
import rospy
from Dynamics import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters, StateApproximator
from helper_functions import mat_to_multiarray_stamped, dist_traj
import Queue
import os
# from callbacks import *
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header, Int8
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

def USV_traj_callback(msg):
    global USVApprox, USV_trajectories, xb_log
    xbhat_m_traj = np.empty((nUSV, T+1))
    stride = msg.array.layout.dim[1].stride
    for t in range(T+1):
        for i in range(nUSV):
            temp = msg.array.data[stride*t + i]
            xbhat_m_traj[i][t] = temp

    temp = np.reshape(xbhat_m_traj, (-1, 1), order='F')

    num_times_to_add = 1
    if PARALLEL:
        num_times_to_add = INTER_ITS
    for i in range(num_times_to_add):
        USV_trajectories = np.concatenate((USV_trajectories, temp), axis=1)
        xb_log = np.concatenate((xb_log, temp[0:nUSV, 0:1]), axis=1)

    USVApprox.put_traj( msg )
    # USVApprox.put_traj(np.asmatrix(xbhat_m_traj).flatten(order='F').T)

def USV_state_callback(msg):
    global xb_m, xb_log
    xb_m = np.array([[msg.pose.position.x], [msg.pose.position.y],\
        [msg.twist.linear.x], [msg.twist.linear.y]])
    xb_log = np.concatenate((xb_log, xb_m), axis=1)

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

global x_m, xb_m, xv_m, phi, theta, long_ref, lat_ref, w_1, w_2, USVApprox, USV_trajectories, xb_log
long_ref = None
lat_ref = None
phi = 0.0
theta = 0.0
w_1 = 0.0
w_2 = 0.0

xb_m = np.matrix([[30.0], [15.0], [0.0], [0.0]])    # Only used for centralised problem
x_m = np.matrix([[0.0], [0.0], [0.0], [0.0]])
xv_m = np.matrix([[12.0], [0.0]])

# Inpired by https://osqp.org/docs/examples/mpc.html
# xhat_traj_0  = np.empty((nUAV*(T+1), 1))
# for i in range(T+1):
#     xhat_traj_0[ i*nUAV : (i+1)*nUAV] = x_m
x_traj  = np.empty((nUAV*(T+1), 1))
for i in range(T+1):
    x_traj[ i*nUAV : (i+1)*nUAV] = x_m

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"
lookahead = 3   # Only for parallel

used_solver = CVXPy

# ********************** CHANGE SOLVER HERE **************************
params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
    wmin, wmax, wmin_land, kl, vmax)
problemCent = CentralisedProblem(T, A, B, Ab, Bb, Q, P, R, used_solver, params)
problemUAV = UAVProblem(T, A,  B,  Q, P, R, nUSV, used_solver, params)
problemVert = VerticalProblem(T, Av, Bv, Qv, Pv, Rv, used_solver, params)
USVApprox = StateApproximator(nUSV, T,  delay_len)
# --------------------------- ROS SETUP ----------------------------------
rospy.init_node('UAV_main')
traj_pub = rospy.Publisher('UAV_traj', Float32MultiArrayStamped, queue_size = 10)
USV_input_pub = rospy.Publisher('USV_input', AccelStamped, queue_size = 10)
experiment_index_pub = rospy.Publisher('experiment_index', Int8, queue_size=1)
rospy.Subscriber('USV_traj', Float32MultiArrayStamped, USV_traj_callback)
rospy.Subscriber('USV_state', StateStamped, USV_state_callback)
rate = rospy.Rate(SAMPLING_RATE)
if USE_ROS:
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

    try:
        authority_server = rospy.ServiceProxy(\
            '/dji12/dji_sdk/sdk_control_authority', SDKControlAuthority)
        control_response = authority_server(1)
    except:
        print "Failed reaching control authority. Sleeping for 3s."
        time.sleep(3)

# -------------- PROBLEM SIMULATION ---------------
x_log  = np.empty((nUAV, sim_len+1))
xv_log = np.empty((nv,   sim_len+1))
uUAV_log = np.empty((mUAV, sim_len))
UAV_trajectories = np.empty((nUAV*(T+1), sim_len))
vert_trajectories = np.empty((2*(T+1), sim_len))
wdes_log = np.empty((mv, sim_len))
if CENTRALISED:
    USV_trajectories = np.empty((nUSV*(T+1), sim_len))
    xb_log = np.empty((nUSV, sim_len))
else:
    USV_trajectories = np.zeros((nUSV*(T+1), 1))
    xb_log  = np.zeros((nUSV, 1))
    # USV_trajectories.fill(np.nan) Do I even need this???
    # xb_log.fill(np.nan)
# Times for all the data in all of the logs. Matches iteration to data-piece
UAV_times = np.empty((1, sim_len+1))
x_log.fill(np.nan)
xv_log.fill(np.nan)
wdes_log.fill(np.nan)
uUAV_log.fill(np.nan)
UAV_trajectories.fill(np.nan)
vert_trajectories.fill(np.nan)

# iteration_durations = [None]*sim_len
iteration_durations = [0]*sim_len
dist_solution_durations = [0]*sim_len
cent_solution_durations = [0]*sim_len
vert_solution_durations = [0]*sim_len

# # For parallel case: Once the optimisation problem is solved, which happens
# # about 1 every INTER_ITS iterations, we want to
# use_optimisation_solution = True
t_since_update = 0
loop_iter_time_sum = 0
start = time.time()
for i in range(sim_len):
    if rospy.is_shutdown():
        break

    # Weird indexing to preserve dimensions
    x_log[:, i:i+1]  = x_m
    xv_log[:, i:i+1] = xv_m

    # ------------------- SOLVE OPTIMISATION PROBLEMS --------------------
    if i==0 or not PARALLEL:
        if CENTRALISED:
            start_cent = time.time()
            problemCent.solve(x_m, xb_m)
            cent_solution_durations[i] = time.time() - start_cent
            x_traj = problemCent.x.value
            xb_traj = problemCent.xb.value
            uUAV = problemCent.u[  0:mUAV, 0:1].value
            uUSV = problemCent.ub[ 0:mUSV, 0:1].value
            dist = dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
            USV_trajectories[:, i:i+1] = xb_traj
            xb_log[:, i:i+1] = xb_m
        elif DISTRIBUTED:
            xbhat_m = USVApprox.get_traj()
            if np.isnan(xbhat_m).any():
                # We don't know where USV is, apply no control input
                uUAV = np.matrix([[0], [0]])
                x_traj = np.asarray(\
                    problemUAV.predict_trajectory( x_m, np.zeros((mUAV*T,1)) ))
                dist = [np.nan]*nUAV*(T+1)
                # Needed for parallel
                problemUAV.x.value = x_traj
                problemUAV.u.value = np.zeros((mUAV*T, 1))
            else:
                start_dist = time.time()
                problemUAV.solve(x_m, np.asarray(xbhat_m))  # TODO: Make naturally array, not matrix
                dist_solution_durations[i] = time.time() - start_dist
                x_traj = problemUAV.x.value
                dist = dist_traj(x_traj, \
                    np.reshape(USVApprox.traj_msg.array.data, (-1,1)),\
                    T, nUAV, nUSV)

                uUAV = problemUAV.u[ 0:mUAV, 0:1].value

    elif i%INTER_ITS == 0 and PARALLEL:
        if CENTRALISED:
            problemCent.solve_threaded(x_m, xb_m)
        elif DISTRIBUTED:
            xbhat_m = USVApprox.get_traj()
            if np.isnan(xbhat_m).any():
                # We don't know where USV is, apply no control input
                uUAV = np.matrix([[0], [0]])
                x_traj = np.asarray(\
                    problemUAV.predict_trajectory( x_m, np.zeros((mUAV*T,1)) ))
                dist = [np.nan]*nUAV*(T+1)
                # Needed for parallel
                problemUAV.x.value = x_traj
                problemUAV.u.value = np.zeros((mUAV*T, 1))
                # For parallel: t_since_update increases with each iteration
                # If it's not reset to 0 here, it can grow arbitrarily large
                # without the problem ever being solved (happens if UAV never
                # receives information about the USV). The intermediate
                # controller further on will fail to work if it thinks that the
                # knows x_traj is too outdated. Therefore, by setting
                # t_since_update to 0, we're telling it that this x_traj is
                # actually up to date
                problemUAV.t_since_update = 0
                t_since_update = problemUAV.t_since_update
            else:
                problemUAV.solve_threaded(x_m, xbhat_m)

    # ----------------- SET CONTROL INPUTS -------------------
    if CENTRALISED and PARALLEL:
        xb_log[:, i:i+1] = xb_m
        USV_trajectories[:, i:i+1] = xb_traj    # TODO: Add shifting and such?
        if problemCent.t_since_update == 0:
            uUAV = problemCent.u[ 0:mUAV, 0:1].value
            uUSV = problemCent.ub[0:mUSV, 0:1].value
            x_traj = problemCent.x.value
            xb_traj = problemCent.xb.value
            dist = dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
        else:
            # Using linear feedback intermediate controller
            # uUAV = KUAV*(x_m  -  problemCent.\
            #     x[t_since_update*nUAV:(t_since_update+1)*nUAV].value)
            # uUSV = KUSV*(xb_m - problemCent.\
            #     xb[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
            uUAV = KUAV*(x_m  -  x_traj[(t_since_update+lookahead)*nUAV:\
                (t_since_update+1+lookahead)*nUAV])
            uUSV = KUSV*(xb_m - xb_traj[(t_since_update+lookahead)*nUSV\
            :(t_since_update+1+lookahead)*nUSV])
            uUAV = -np.clip(uUAV, amin,   amax)
            uUSV = -np.clip(uUSV, amin_b, amax_b)

        problemCent.t_since_update += 1
        t_since_update = problemCent.t_since_update
    elif DISTRIBUTED and PARALLEL:
        if problemUAV.t_since_update == 0:
            uUAV = problemUAV.u[ 0:mUAV, 0:1].value
            x_traj = problemUAV.x.value
            dist = dist_traj(x_traj, \
                np.reshape(USVApprox.traj_msg.array.data, (-1,1)),\
                T, nUAV, nUSV)
        else:
            uUAV = KUAV*(x_m  -  x_traj[(t_since_update+lookahead)*nUAV:\
                (t_since_update+1+lookahead)*nUAV])
            uUAV = -np.clip(uUAV, amin,   amax)

        problemUAV.t_since_update += 1
        t_since_update = problemUAV.t_since_update

    UAV_trajectories[:, i:i+1] = x_traj # TODO: Should I update this by shifting or something, in parallel case?

    # ----------------------- VERTICAL PROBLEM ---------------------------
    vert_start = time.time()
    if not np.isnan(dist).any():
        problemVert.solve(xv_m, 0.0, np.asarray(dist))  # TODO: Make dist naturally array, not matrix
        wdes_current = problemVert.wdes[0:mv, 0:1].value
        vert_trajectories[:, i:i+1] = problemVert.xv.value
        # TODO: Should anything else be done if the position of the USV is unknown?
    else:
        wdes_current = 0
        # TODO: Update vert_trajectories somehow? This is incorrect, not shifted
        if i > 0:
            vert_trajectories[:, i:i+1] = vert_trajectories[:, i-1:i]
        else:
            vert_trajectories[:, i:i+1] = np.kron( np.ones((T+1,1)), xv_m )
    vert_solution_durations[i] = time.time() - vert_start

    wdes_log[:, i:i+1] = wdes_current
    uUAV_log[:, i:i+1] = uUAV;

    UAV_times[:, i:i+1] = rospy.get_time()

    # ----------- SIMULATE DYNAMICS / PUBLISH CONTROL INPUTS -------------
    if wdes_current is None:
        wdes_current = 0
        print('Wdes was None, iteration:', i)
        break   # DEBUG !!!!

    if CENTRALISED:
        USV_input_msg = AccelStamped()
        USV_input_msg.accel.linear.x = uUSV[0]
        USV_input_msg.accel.linear.y = uUSV[1]
        USV_input_pub.publish(USV_input_msg)
        # xb_m = Ab*xb_m + Bb*uUSV  # REMOVE, publish message for USV node instead
    if not USE_ROS:
        x_m  =  A*x_m  +  B*uUAV
        xv_m = Av*xv_m + Bv*wdes_current
    if USE_ROS:
        phi_cmd, theta_cmd = get_cmd_angle(uUAV, uUSV, wdes_current, xv_m)
        axes = [phi_cmd, theta_cmd, wdes_current, 0.0, 0x02]
        UAV_msg = Joy(Header(), axes, [])
        UAV_publisher.publish(UAV_msg)
    # I guess this is at the right indentation level? We want to publish even
    # if we're not actually using the drone
    # if not np.isnan(dist):
        # Publish trajectory if it was successfully found
    traj_msg = mat_to_multiarray_stamped(x_traj, T+1, nUAV)
    traj_msg.header.stamp = rospy.Time.now()
    if not PARALLEL or t_since_update == 1:
        traj_pub.publish(traj_msg)  # TODO: CHANGE THIS. JUST DON'T USE A QUEUE
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

# # # # # I DON'T THINK ANY OF THIS IS REALLY NEEDED. HOWEVER, MIGHT BE GREAT FOR DEBUG-ING!!!!
print 'Mean iteration time:', np.mean(iteration_durations)
print 'Median iteration time:', np.median(iteration_durations)
print 'Standard deviation:', np.std(iteration_durations)
print 'Centralised solution:', np.mean(cent_solution_durations)
print 'Distributed solution:', np.mean(dist_solution_durations)
print 'Vertical solution:', np.mean(vert_solution_durations)
print 'Max vertical:', np.max(vert_solution_durations)
# Weird indexing to preserve dimensions
x_log[:, -nUAV:sim_len+1]  = x_m
xv_log[:, -2:sim_len+1] = xv_m

# ------------------ STORES DATA -----------------
i = 0
dir_already_exists = True
dir_path = '/home/student/robbj_experiment_results/'
while dir_already_exists:
    i += 1
    dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(i))

os.mkdir(dir_path + 'Experiment_' + str(i))
experiment_index_pub.publish(Int8(i))

info_str = str(datetime.datetime.now()) + '\ntype: '
if CENTRALISED:
    info_str += 'Centralised\n'
else:
    info_str+= 'Distributed\n'
info_str += 'parallel: '
if PARALLEL:
    info_str += 'True\n'
else:
    info_str += 'False\n'
info_str += 'simulation length: ' + str(sim_len) + '\n'
info_str += 'horizon: ' + str(T) + '\n'
info_str += 'sampling rate: ' + str(SAMPLING_RATE) + '\n'
info_str += 'UAV used solver: ' + used_solver
# TODO: Add simulated delay info???
np.savetxt(dir_path + 'Experiment_'+str(i)+'/info.txt', [info_str], fmt="%s")
np.savetxt(dir_path + 'Experiment_'+str(i)+'/x_log.txt', x_log)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/xv_log.txt', xv_log)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_trajectories.txt', UAV_trajectories)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUAV_log.txt', uUAV_log)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_iteration_durations.txt', iteration_durations)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/vertical_durations.txt', vert_solution_durations)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_time_stamps.txt', UAV_times)
if CENTRALISED:
    np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_trajectories.txt', USV_trajectories)
    np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.txt', cent_solution_durations)
else:
    np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.txt', dist_solution_durations)
# ------------------------------ PLOTTING --------------------------------

# distance = np.sqrt( np.square(x_log[0, :] - xb_log[0, :])\
#     + np.square(x_log[1, :] - xb_log[1, :]) )

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
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

# np.savetxt("USV_external_traj_X.txt", xb_log[0, :])
# np.savetxt("USV_external_traj_Y.txt", xb_log[1, :])

## REAL-TIME, not sure if try-except works
# [_, num_USV_trajs] = USV_trajectories.shape
# for t in range(sim_len):
#     # safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
#     # p1 = PatchCollection([safe_circle], alpha=0.1)
#     # ax1.add_collection(p1)
#     if num_USV_trajs > t:
#         USV_traj = np.reshape(USV_trajectories[:,t], (nUSV, T+1), order='F')
#         ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')
#     UAV_traj = np.reshape(UAV_trajectories[:,t], (nUAV, T+1), order='F')
#     ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
#
#     vert_traj = np.reshape(vert_trajectories[:,t], (2, T+1), order='F')
#
#     # pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
#     #     (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )
#
#     ax1.plot(x_log[0, 0:t+1], x_log[1, 0:t+1], 'bx')
#     ax1.plot(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 'rx')
#     # ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t]) # <--- ACCELERATION, AWESOME STUFF!
#     # ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
#     # # ax2.plot(range(t+1), xv_log[0, 0:t+1], 'b')
#     # ax2.plot(pred_dist, vert_traj[0, 0:T+1], 'y')
#     # # ax2.plot(range(t+1, t+1 + T+1), vert_traj[0, 0:T+1], 'y')
#     # ax2.add_collection(p2)
#     #
#     # ax3.plot([SAMPLING_TIME*i for i in range(t+1)], distance[0:t+1], 'k')
#
#     #print "UAV speed:", np.sqrt(x_log[2,t]**2 + x_log[3,t]**2)
#     #print "UAV speeds:", x_log[2,t], " , ", x_log[3,t]
#
#     ax1.grid(True)
#     # ax2.grid(True)
#     # ax3.grid(True)
#     plt.pause(0.01)
#
#     ax1.cla()
#     # ax2.cla()


# NOT REAL-TIME
ax1.plot(x_log[0, :], x_log[1, :], 'bx')
ax1.plot(xb_log[0, :], xb_log[1, :], 'rx')
# ax2.plot(distance, xv_log[0, :], 'b')
ax1.grid(True)
ax2.grid(True)

# safe_circle = Circle((xb_log[0, sim_len], xb_log[1, sim_len]), ds)
# p1 = PatchCollection([safe_circle], alpha=0.2)

# ax1.add_collection(p1)
ax2.add_collection(p2)

plt.show()
