#!/usr/bin/env python
import rospy
from Dynamics import *              # THESE ARE SUPER NECESSARY
from IMPORT_ME import *
from helper_classes import Parameters, StateApproximator
from helper_functions import mat_to_multiarray_stamped
import Queue
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
from rendezvous_problem.msg import StateStamped
from geometry_msgs.msg import AccelStamped
from std_msgs.msg import Int8
# import cvxpy as cp
# import scipy as sp
import matplotlib.pyplot as plt
import time
import datetime
import osqp
import thread
from problemClasses import *

# from geometry_msgs.msg import Quaternion, Vector3Stamped
from math import sin, cos, atan, atan2, asin, pi, sqrt

def UAV_traj_callback(msg):
    global UAVApprox, UAV_trajectories, x_log
    xhat_m_traj = np.empty((nUAV, T+1))
    stride = msg.array.layout.dim[1].stride
    for t in range(T+1):
        for i in range(nUAV):
            xhat_m_traj[i][t] = msg.array.data[stride*t + i]

    temp = np.reshape(xhat_m_traj, (-1, 1), order='F')
    num_times_to_add = 1
    if PARALLEL:
        num_times_to_add = INTER_ITS
    for i in range(num_times_to_add):
        UAV_trajectories = np.concatenate((UAV_trajectories, temp), axis=1)
        x_log = np.concatenate((x_log, temp[0:nUAV, 0:1]), axis=1)

    UAVApprox.put_traj(msg)

def USV_input_callback(msg):
    global uUSV
    uUSV = np.array([[msg.accel.linear.x],[msg.accel.linear.y]])

def experiment_index_callback(msg):
    global experiment_index
    experiment_index = msg.data

# -------------------------- PROBLEM DEFINITION -------------------------

#  MAKE SURE TO IMPORT Dynamics.py and IMPORT_ME.py !!!!!!!!!!!!!!!!!!!!!!!

global UAVApprox, UAV_trajectories, x_log, uUSV, experiment_index
experiment_index = -1   # -1 means that experiment index has not yet been set

xb_m = np.matrix([[15.0], [30.0], [0.0], [0.0]])
# xb_traj = np.zeros(( nUAV*(T+1), 1 ))

amin  =  0.0        # Only here to not break parameter class
amax  =  0.0        # Only here to not break parameter class
amin_b = -3.0
amax_b = 3.0
hs = 5.0            # Only here to not break parameter class
ds = 2.0            # Only here to not break parameter class
dl = 1.0            # Only here to not break parameter class
wmin = -1.0         # Only here to not break parameter class
wmax = 1.0          # Only here to not break parameter class
wmin_land = -0.3    # Only here to not break parameter class
# Additional allowed negative vertical velocity per unit height
kl = 0.2            # Only here to not break parameter class
vmax = 5.0          # Only here to not break parameter class

# TODO: I'm not sure shure what this is all about anymore!!!
# Inpired by https://osqp.org/docs/examples/mpc.html
# xhat_traj_0  = np.empty((nUAV*(T+1), 1))
# for i in range(T+1):
#     xhat_traj_0[ i*nUAV : (i+1)*nUAV] = x_m

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"
lookahead = 3   # Only for parallel

used_solver = CVXPy

params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
    wmin, wmax, wmin_land, kl, vmax)
problemUSV = USVProblem(T, Ab,  Bb,  Q, P, R, nUAV, used_solver, params)
UAVApprox = StateApproximator(nUAV, T, delay_len)

# --------------------------- ROS SETUP ----------------------------------
rospy.init_node('USV_main')
traj_pub = rospy.Publisher('USV_traj', Float32MultiArrayStamped, queue_size = 10)
state_pub = rospy.Publisher('USV_state', StateStamped, queue_size = 10)
rospy.Subscriber('UAV_traj', Float32MultiArrayStamped, UAV_traj_callback)
rospy.Subscriber('USV_input', AccelStamped, USV_input_callback)
rospy.Subscriber('experiment_index', Int8, experiment_index_callback)
rate = rospy.Rate(SAMPLING_RATE)

# -------------- PROBLEM SIMULATION ---------------
xb_log  = np.empty((nUSV, sim_len+1))
x_log = np.zeros((nUAV, 1))
# xv_log = np.empty((nv,   sim_len+1))
uUSV_log = np.empty((mUSV, sim_len))
USV_trajectories = np.empty((nUSV*(T+1), sim_len))
UAV_trajectories = np.zeros((nUAV*(T+1), 1))
USV_times = np.empty((1, sim_len))
xb_log.fill(np.nan)
# xv_log.fill(np.nan)
uUSV_log.fill(np.nan)
USV_trajectories.fill(np.nan)
# vert_trajectories.fill(np.nan)

# iteration_durations = [None]*sim_len
iteration_durations = [0]*sim_len
dist_solution_durations = [0]*sim_len
uUSV = np.zeros((mUSV, 1))
USV_stopped_at_iter = -1

t_since_update = 0
loop_iter_time_sum = 0
start = time.time()
for i in range(sim_len):        # TODO: Change to keep on going sort of for ever?
    if rospy.is_shutdown():
        break

    # Weird indexing to preserve dimensions
    xb_log[:, i:i+1]  = xb_m
    # xv_log[:, i:i+1] = xv_m

    # ------------------- SOLVE OPTIMISATION PROBLEMS --------------------
    if i==0 or not PARALLEL:
        if DISTRIBUTED:
            xhat_m = UAVApprox.get_traj()
            if np.isnan(xhat_m).any():
                # We don't know where UAV is, apply no control input
                uUSV = np.matrix([[0], [0]])
                xb_traj = np.asarray(\
                    problemUSV.predict_trajectory( xb_m, np.zeros((mUSV*T, 1)) ))
                # Needed for parallel
                problemUSV.xb.value = xb_traj
                problemUSV.ub.value = np.zeros((mUSV*T, 1))
                # For parallel case: Since problemUSV wasn't actually solved,
                # we need to have non-zero t_since_update so that rest of
                # program doesn't think the problem was just solved and will
                # therefore try to access solution variables
                problemUSV.t_since_update = 0
                t_since_update = problemUSV.t_since_update
            else:
                start_dist = time.time()
                problemUSV.solve(xb_m, xhat_m)
                dist_solution_durations[i] = time.time() - start_dist
                xb_traj = problemUSV.xb.value

                if not PARALLEL or t_since_update == 0:
                    uUSV = problemUSV.ub[ 0:mUSV, 0:1].value
                else:
                    # Using linear feedback intermediate controller
                    uUSV = KUSV*(xb_m  -  problemUSV.\
                        x[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
                    uUSV = -np.clip(uUSV, amin_b, amax_b)

    elif i%INTER_ITS == 0 and PARALLEL:
        if DISTRIBUTED:
            xhat_m = UAVApprox.get_traj()
            if np.isnan(xhat_m).any():
                # We don't know where UAV is, apply no control input
                uUSV = np.matrix([[0], [0]])
                xb_traj = np.asarray(\
                    problemUSV.predict_trajectory( xb_m, np.zeros((mUSV*T,1)) ))
                # Needed for parallel
                problemUSV.xb.value = xb_traj
                problemUSV.ub.value = np.zeros((mUSV*T, 1))
                # In general, t_since_update increases with each iteration
                # If it's not reset to 1 here, it can grow arbitrarily large
                # without the problem ever being solved (happens if USV never
                # receives information about the UAV). The intermediate
                # controller further on will fail to work if it thinks that the
                # knows xb_traj is too outdated. Therefore, by setting
                # t_since_update to 1, we're telling it that this xb_traj is
                # actually up to date
                problemUSV.t_since_update = 0
                t_since_update = problemUSV.t_since_update
            else:
                problemUSV.solve_threaded(xb_m, xhat_m)

    if DISTRIBUTED and PARALLEL:
        if problemUSV.t_since_update == 0:
            uUSV = problemUSV.ub[ 0:mUSV, 0:1].value
            xb_traj = problemUSV.xb.value
        else:
            uUSV = KUSV*(xb_m  -  xb_traj[(t_since_update+lookahead)*nUSV:\
                (t_since_update+1+lookahead)*nUSV])
            uUSV = -np.clip(uUSV, amin_b,   amax_b)

        problemUSV.t_since_update += 1
        t_since_update = problemUSV.t_since_update

    if DISTRIBUTED:
        # We only have access to predicted trajectory in distributed caseself.
        # In centralised case, it is UAV_main that calculates it
        USV_trajectories[:, i:i+1] = xb_traj
    uUSV_log[:, i:i+1] = uUSV;
    USV_times[:, i:i+1] = rospy.get_time()

    xb_m = Ab*xb_m + Bb*uUSV

    if CENTRALISED:
        # Publish state to UAV
        state_msg = StateStamped()
        state_msg.pose.position.x = xb_m[0]
        state_msg.pose.position.y = xb_m[1]
        state_msg.twist.linear.x = xb_m[2]
        state_msg.twist.linear.y = xb_m[3]
        state_pub.publish(state_msg)
    elif DISTRIBUTED and (not PARALLEL or t_since_update == 1):
        traj_msg = mat_to_multiarray_stamped(xb_traj, T+1, nUSV)
        traj_msg.header.stamp = rospy.Time.now()
        traj_pub.publish(traj_msg)  # TODO: CHANGE THIS. JUST DON'T USE A QUEUE

    # ---------------------------- SLEEP ---------------------------------
    end = time.time()
    # print(end - start)
    # loop_iter_time_sum += end-start
    iteration_durations[i] = end-start
    rate.sleep()
    # if USE_ROS:
    #     rate.sleep()
    # else:
    #     try:
    #         time.sleep(SAMPLING_TIME - end + start)
    #     except:
    #         pass
    start = time.time()

# # # # # I DON'T THINK ANY OF THIS IS REALLY NEEDED. HOWEVER, MIGHT BE GREAT FOR DEBUG-ING!!!!
print 'Mean iteration time:', np.mean(iteration_durations)
print 'Median iteration time:', np.median(iteration_durations)
print 'Standard deviation:', np.std(iteration_durations)
print 'Distributed solution:', np.mean(dist_solution_durations)
# Weird indexing to preserve dimensions
xb_log[:, -nUSV:sim_len+1]  = xb_m
# xv_log[:, -2:sim_len+1] = xv_m

# ----------------------- STORES DATA ---------------------
# Waits for UAV to send over experiment index
while experiment_index < 0:
    if rospy.is_shutdown():
        break
    pass

i = experiment_index
dir_path = '/home/student/robbj_experiment_results/'
info_str = 'USV used solver: ' + used_solver + '\n'
info_str += 'USV stopped at iteration: ' + str(USV_stopped_at_iter)

np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_info.txt', [info_str], fmt="%s")
np.savetxt(dir_path + 'Experiment_'+str(i)+'/xb_log.txt', xb_log)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUSV_log.txt', uUSV_log)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_iteration_durations.txt', iteration_durations)
np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_time_stamps.txt', USV_times)
if DISTRIBUTED:
    np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_trajectories.txt', USV_trajectories)
    np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_horizontal_durations.txt', dist_solution_durations)
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

# np.savetxt("USV_local_traj_X.txt", xb_log[0, :])
# np.savetxt("USV_local_traj_Y.txt", xb_log[1, :])

### REAL-TIME, not sure if try-except works
[_, num_UAV_trajs] = UAV_trajectories.shape
for t in range(sim_len):
    if rospy.is_shutdown():
        break
    safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
    p1 = PatchCollection([safe_circle], alpha=0.1)
    ax1.add_collection(p1)
    if num_UAV_trajs > t:
        UAV_traj = np.reshape(UAV_trajectories[:,t], (nUAV, T+1), order='F')
        ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
    USV_traj = np.reshape(USV_trajectories[:,t], (nUSV, T+1), order='F')
    ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')

    # pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
    #     (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )

    # ax1.plot(x_log[0, 0:t+1], x_log[1, 0:t+1], 'bx')
    ax1.plot(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 'rx')
    # ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t]) # <--- ACCELERATION, AWESOME STUFF!
    # ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
    # ax2.plot(range(t+1), xv_log[0, 0:t+1], 'b')
    # ax2.plot(pred_dist, vert_traj[0, 0:T+1], 'y')
    # ax2.plot(range(t+1, t+1 + T+1), vert_traj[0, 0:T+1], 'y')
    # ax2.add_collection(p2)

    # ax3.plot([SAMPLING_TIME*i for i in range(t+1)], distance[0:t+1], 'k')

    #print "UAV speed:", np.sqrt(x_log[2,t]**2 + x_log[3,t]**2)
    #print "UAV speeds:", x_log[2,t], " , ", x_log[3,t]

    ax1.grid(True)
    # ax2.grid(True)
    # ax3.grid(True)
    plt.pause(0.01)

    ax1.cla()
    # ax2.cla()


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
