from geometry_msgs.msg import Quaternion, Vector3Stamped
from math import sin, cos, atan, atan2, asin, pi, sqrt
import numpy as np
from Dynamics import nUSV, T, delay_len
from IMPORT_ME import PARALLEL
from helper_classes import StateApproximator

global w_1, w_2, xv_m, x_m, xb_m, xb_log, long_ref, lat_ref, phi, theta,\
    USVApprox, USV_trajectories

xb_log = np.zeros((nUSV, 1))
USV_trajectories = np.zeros((nUSV*(T+1), 1))
USVApprox = StateApproximator(nUSV, T,  delay_len)

# ------------- UAV CALLBACKS -------------

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

# ------------------ USV CALLBACKS ------------------
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
