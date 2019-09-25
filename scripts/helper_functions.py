import rospy
import numpy as np
from rendezvous_problem.msg import Float32MultiArrayStamped
from std_msgs.msg import MultiArrayDimension
from math import sin, cos, atan, atan2, asin, pi, sqrt
from matrices_and_parameters import g, tau_w, kw

def shift_traj_msg(traj_msg, n, samp_time):
    delta_time = rospy.Time.now() - traj_msg.header.stamp
    d = int(delta_time.nsecs / (1000000000*samp_time)) # I used to have +1, not sure if that made sense though
    # print "delay:", d
    traj_msg.array.data = np.roll(traj_msg.array.data, -n*d, 0)
    for t in range(d):
        for i in range(n):
            # Fill the i:th state components of all future states with the i:th
            # component of the previously (before the shift) last state.
            traj_msg.array.data[-(t+1)*n+i] = traj_msg.array.data[-(d+1)*n+i]

    traj_msg.header.stamp = rospy.Time.now()
    return traj_msg

def shift_trajectory(traj, n, d):
    # n: State Size
    # d: Number of time steps of shift
    traj = np.roll(traj, -n*d, 0)
    [len, _] = traj.shape
    if d > 0:
        for i in range(n):
            # Fill the i:th state components of all future states with the i:th
            # component of the previously (before the shift) last state.
            traj[-n*d+i:len:n, :].fill(traj[-n*(d+1)+i, 0])
    return traj

def get_traj_dir(traj, n):
    return traj[0:2, 0:1] - traj[-n:-n+2, 0:1]

def get_travel_dir(x, reverse_dir = False):
    len = np.sqrt(np.sum(np.square(x[0:2])))
    if len > 0:
        if reverse_dir:
            return -x[0:2]/len
        else:
            return x[0:2]/len
    else:
        raise ZeroDivisionError("First two elements of argument must have norm greater than zero")

def get_cos_angle_between(v1, v2):
    return np.clip(np.asscalar(\
        np.dot(v1.transpose(), v2)/(np.linalg.norm(v1)*np.linalg.norm(v2))),-1,1)

# Expects x_traj and xb_traj to be 2d numpy arrays
def get_dist_traj(x_traj, xb_traj, T, nUAV, nUSV, signed=False):
    if not signed:
        return np.sqrt( \
            np.square(x_traj[0:nUAV*(T+1):nUAV] - xb_traj[0:nUSV*(T+1):nUSV]) +\
            np.square(x_traj[1:nUAV*(T+1):nUAV] - xb_traj[1:nUSV*(T+1):nUSV])  )
    else:
        dist = np.sqrt( \
            np.square(x_traj[0:nUAV*(T+1):nUAV] - xb_traj[0:nUSV*(T+1):nUSV]) +\
            np.square(x_traj[1:nUAV*(T+1):nUAV] - xb_traj[1:nUSV*(T+1):nUSV])  )
        signs = np.sign(x_traj[0:nUAV*(T+1):nUAV] - xb_traj[0:nUSV*(T+1):nUSV])
        return np.dot(np.diag(dist.flatten()), signs)

def mat_to_multiarray_stamped(matrix, time_span, n):
    stamped_arr = Float32MultiArrayStamped()
    stamped_arr.array.layout.dim.extend([MultiArrayDimension(),\
        MultiArrayDimension()])
    stamped_arr.array.layout.dim[0].size = time_span;
    stamped_arr.array.layout.dim[0].stride = time_span*n;
    stamped_arr.array.layout.dim[0].label = "Time";
    stamped_arr.array.layout.dim[1].size = n;
    stamped_arr.array.layout.dim[1].stride = n;
    stamped_arr.array.layout.dim[1].label = "State/Input element";
    stamped_arr.array.data = matrix.flatten(order='F')
    return stamped_arr

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

def fill_lost_values(matrix):
    (rows, cols) = matrix.shape
    non_nan_val = np.full((rows, 1), np.nan)
    for col in range(cols):
        if not np.isnan(matrix[:, col:col+1]).any():
            non_nan_val = matrix[:, col:col+1]
            break

    for col in range(cols):
        if np.isnan(matrix[:, col]).any():
            matrix[:, col:col+1] = non_nan_val
        else:
            non_nan_val = matrix[:, col:col+1]

    return matrix

def get_cmd_angle(u, wdes, xv):
    # The angles that we want now, not to be confused with angle_cmd
    phi_des =   atan( -u[1] / ( g + (1.0/tau_w)*(kw*wdes - xv[1]) ) )
    theta_des = atan(  u[0] / ( g + (1.0/tau_w)*(kw*wdes - xv[1]) ) )
    return phi_des, theta_des
    # Predict angles we need at next time step
    # phi_next   = atan( -varsUAV.u{1}(2) / ...
    #     ( g + (1/tau_w)*(kw*varsVert.u{1} - varsVert.x{1}(2)) ) );
    # theta_next = atan(  varsUAV.u{1}(1) / ...
    #     ( g + (1/tau_w)*(kw*varsVert.u{1} - varsVert.x{1}(2)) ) );
    # % Chose control signal to achieve desired angles at next time step
    # phi_cmd   = (phi_next   - Aphi(1, 1)  *  phi - Aphi(1, 2)  * w_1 )/Bphi(1);
    # theta_cmd = (theta_next - Atheta(1, 1)*theta  - Atheta(1, 2)*w_2)/Btheta(1);
