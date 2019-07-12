#!/usr/bin/env python
import rospy
from Dynamics import *
# from callbacks import *
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header
from geometry_msgs.msg import Vector3Stamped, QuaternionStamped
from dji_sdk.srv import SDKControlAuthority
import cvxpy as cp
#import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import time
import osqp
import thread
# import threading

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

def problemDistThreaded():
    global t_since_update, xbhat_m, xhat_m
    xbhat.value =  xbhat_m
    problemUAV.solve(solver=cp.OSQP, warm_start=True, verbose=True)
    xhat_m = x.value
    xhat.value = xhat_m
    problemUSV.solve(solver=cp.OSQP, warm_start=True, verbose=True)
    xbhat_m = xb.value
    xbhat_m = np.roll(xbhat_m, -1*nUSV)
    xbhat_m[-nUSV:nUSV*(T+1)] = xbhat_m[-2*nUSV:-nUSV]
    t_since_update = 0

def problemCentThreaded():
    global t_since_update
    problemCent.solve(solver=cp.OSQP, warm_start=True)
    t_since_update = 0

# --------------------- PROBLEM DEFINITION ---------------------

# Inpired by https://osqp.org/docs/examples/mpc.html

x  = cp.Variable(( nUAV*(T+1), 1 ))
xb = cp.Variable(( nUSV*(T+1), 1 ))
u  = cp.Variable(( mUAV*T, 1 ))
ub = cp.Variable(( mUSV*T, 1 ))
xhat  = cp.Parameter(( nUAV*(T+1), 1 ))
xbhat = cp.Parameter(( nUSV*(T+1), 1 ))
x_0  = cp.Parameter((nUAV, 1))
xb_0 = cp.Parameter((nUSV, 1))
amax  = cp.Parameter()
amin  = cp.Parameter()
amax_b = cp.Parameter()
amin_b = cp.Parameter()

xv = cp.Variable(( 2*(T+1), 1 ))
wdes = cp.Variable(( T, 1 ))
xb_v = cp.Parameter(( 2, 1 ))                 # Vertical state of USV
xv_0 = cp.Parameter(( 2, 1))
dist = cp.Parameter()

# ----------------------- CENTRALISED PROBLEM ----------------------

objectiveCent = cp.quad_form(x-xb, Q_big) + cp.quad_form(u, R_big) \
    + cp.quad_form(ub, R_big)
constraintsCent  = [ x  ==  Phi*x_0  +  Lambda*u ]
constraintsCent += [ xb == Phi_b*xb_0 + Lambda_b*ub ]
# TODO: THESE CONSTRAINTS ARE WHAT MAKES THE VEHICLES TAKE A PATH THAT'S NOT STRAIGHT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# TODO: Change into constraints on magnitude of u(k)? Or is that too tricky?
constraintsCent += [ u  <= amax,   u  >= amin   ]
constraintsCent += [ ub <= amax_b, ub >= amin_b ]

problemCent = cp.Problem(cp.Minimize(objectiveCent), constraintsCent)

t_since_update = 0

# ----------------------- DECENTRALISED UAV PROBLEM ----------------------------
objectiveUAV = cp.quad_form(x-xbhat, Q_big) + cp.quad_form(u, R_big)
constraintsUAV  = [ x  ==  Phi*x_0  +  Lambda*u ]
constraintsUAV += [ u  <= amax,   u  >= amin   ]

problemUAV = cp.Problem(cp.Minimize(objectiveUAV), constraintsUAV)

# ----------------------- DECENTRALISED USV PROBLEM ----------------------------
objectiveUSV = cp.quad_form(xb-xhat, Q_big) + cp.quad_form(ub, R_big)
constraintsUSV  = [ xb  ==  Phi_b*xb_0  +  Lambda_b*ub ]
constraintsUSV += [ ub  <= amax,   ub  >= amin   ]

problemUSV = cp.Problem(cp.Minimize(objectiveUSV), constraintsUSV)

# -------------------------- VERTICAL PROBLEM ----------------------------------

xb_v_vector = cp.kron(np.ones(( T+1, 1 )), xb_v)
objectiveVertLand = cp.quad_form(xv - xb_v_vector, Qv_big) + cp.quad_form(wdes, Rv_big)
constraintsVertLand =  [xv == Phi_v*xv_0 + Lambda_v*wdes]
constraintsVertLand += [wmin <= velocity_extractor*xv, \
    velocity_extractor*xv <= wmax]
constraintsVertLand += [wmin <= wdes, wdes <= wmax]
constraintsVertLand += [(dl-ds)*height_extractor*xv <= (hs*dl - hs*dist)]
constraintsVertLand += [(dl-ds)*height_extractor*xv <= (hs*dl + hs*dist)]

problemVertLand = cp.Problem(cp.Minimize(objectiveVertLand), constraintsVertLand)

objectiveVertSafe = cp.quad_form(wdes, Rv_big)
constraintsVertSafe =  [xv == Phi_v*xv_0 + Lambda_v*wdes]
constraintsVertSafe += [height_extractor*xv >= hs]

problemVertSafe = cp.Problem(cp.Minimize(objectiveVertSafe), constraintsVertSafe)

# ------------------ ROS SETUP ----------------------
USE_ROS = False
CENTRALISED = True
DISTRIBUTED = not CENTRALISED
PARALLEL = False

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
if USE_ROS:
    rospy.init_node('rendezvous_simulator')

    rospy.Subscriber('dji12/dji_sdk/imu', Imu, IMU_callback)
    rospy.Subscriber('dji12/dji_sdk/height_above_takeoff', Float32, height_callback)
    rospy.Subscriber('dji12/dji_sdk/velocity', Vector3Stamped, velocity_callback)
    rospy.Subscriber('dji12/dji_sdk/gps_position', NavSatFix, pos_callback)
    rospy.Subscriber('dji12/dji_sdk/attitude', QuaternionStamped, attitude_callback)

    UAV_publisher = rospy.Publisher('/dji12/dji_sdk/flight_control_setpoint_generic',\
     Joy, queue_size = 10)

    rospy.wait_for_service('/dji12/dji_sdk/sdk_control_authority')

    # TODO: Can I make this succeed somehow??
    try:
        authority_server = rospy.ServiceProxy(\
            '/dji12/dji_sdk/sdk_control_authority', SDKControlAuthority)
        control_response = sdk_control_authority(1)
    except:
        print "Failed reaching control authority. Sleeping for 3s."
        time.sleep(3)

    rate = rospy.Rate(SAMPLING_RATE)
# -------------- PROBLEM SIMULATION ---------------

x_log  = np.empty((nUAV, sim_len+1))
xb_log = np.empty((nUSV, sim_len+1))
xv_log = np.empty((nv,   sim_len+1))
x_log.fill(np.nan)
xb_log.fill(np.nan)
xv_log.fill(np.nan)

amin.value   = -5.0     # TODO: These don't really have to be parameters, they don't change
amax.value   =  5.0
amin_b.value = -3.0
amax_b.value =  3.0
xb_v.value = np.zeros((2, 1))
start = time.time()
for i in range(sim_len):
    if rospy.is_shutdown():
        break

    x_0.value = x_m
    xb_0.value = xb_m
    xv_0.value = xv_m
    dist.value = np.asscalar(np.sqrt( (x_m[0]-xb_m[0])**2 + (x_m[1]-xb_m[1])**2 ))
    # Weird indexing to preserve dimensions
    x_log[:, i:i+1]  = x_m
    xb_log[:, i:i+1] = xb_m
    xv_log[:, i:i+1] = xv_m

    if i==0 or not PARALLEL:
        if CENTRALISED:
            problemCent.solve(solver=cp.OSQP, warm_start=True)
        elif DISTRIBUTED:
            xbhat.value =  xbhat_m
            problemUAV.solve(solver=cp.OSQP, warm_start=True)
            xhat_m = x.value
            xhat.value = xhat_m
            problemUSV.solve(solver=cp.OSQP, warm_start=True)
            xbhat_m = xb.value
            xbhat_m = np.roll(xbhat_m, -1*nUSV)
            xbhat_m[-nUSV:nUSV*(T+1)] = xbhat_m[-2*nUSV:-nUSV]
    elif i%10 == 0 and PARALLEL:
        if CENTRALISED:
            thread.start_new_thread( problemCentThreaded, ())
        elif DISTRIBUTED:
            thread.start_new_thread( problemDistThreaded, ())

    if dist.value >= ds:
        problemVertSafe.solve(solver=cp.OSQP, warm_start=True)
    else:
        problemVertLand.solve(solver=cp.OSQP, warm_start=True)

    if not PARALLEL or t_since_update == 0:
        uUAV = u[ 0:mUAV, 0:1].value
        uUSV = ub[0:mUSV, 0:1].value
    else:
        # Using linear feedback intermediate controller
        uUAV = KUAV*(x_m  -  x[t_since_update*nUAV:(t_since_update+1)*nUAV].value)
        uUSV = KUSV*(xb_m - xb[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
        uUAV = -np.clip(uUAV, amin.value,   amax.value)
        uUSV = -np.clip(uUSV, amin_b.value, amax_b.value)

    t_since_update += 1     # TODO: Avoid race conditions somehow?
    wdes_current = wdes[ 0:mv,  0:1].value
    xb_m = Ab*xb_m + Bb*uUSV
    if not USE_ROS:
        x_m  =  A*x_m  +  B*uUAV
        xv_m = Av*xv_m + Bv*wdes_current

    if USE_ROS:
        phi_cmd, theta_cmd = get_cmd_angle(uUAV, uUSV, wdes_current, xv_m)
        axes = [phi_cmd, theta_cmd, wdes_current, 0.0, 0x02]
        UAV_msg = Joy(Header(), axes, [])
        UAV_publisher.publish(UAV_msg)


    end = time.time()
    print(end - start)
    if USE_ROS:
        rate.sleep()
    else:
        try:
            time.sleep(SAMPLING_TIME - end + start)
        except:
            pass
    start = time.time()
# Weird indexing to preserve dimensions
x_log[:, -nUAV:sim_len+1]  = x_m
xb_log[:, -nUSV:sim_len+1] = xb_m
xv_log[:, -2:sim_len+1] = xv_m
# ------------------ PLOTTING ---------------------

distance = np.sqrt( np.square(x_log[0, :] - xb_log[0, :])\
    + np.square(x_log[0, :] - xb_log[0, :]) )

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

# REAL-TIME, not sure if try-except works
try:
    for t in range(sim_len):
        ax1.plot(x_log[0, 0:t+1], x_log[1, 0:t+1], 'bx')
        ax1.plot(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 'rx')
        ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
        ax1.grid(True)
        ax2.grid(True)
        plt.pause(0.01)
except:
    pass

# NOT REAL-TIME
ax1.plot(x_log[0, :], x_log[1, :], 'bx')
ax1.plot(xb_log[0, :], xb_log[1, :], 'rx')
ax2.plot(distance, xv_log[0, :], 'b')
ax1.grid(True)
ax2.grid(True)

plt.show()
