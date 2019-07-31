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
