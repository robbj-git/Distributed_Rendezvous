from classesTest import *

import numpy as np
from math import atan

SAMPLING_RATE = 20              # Dynamics change if this changes
SAMPLING_TIME = 1.0/SAMPLING_RATE
# Horizon
T = 45
# T = 200
sim_len = 400

def get_cmd_angle(u, ub, wdes, xv):
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

# ----------------- PARAMETERS -----------------
hs = 5.0;
ds = 2.0;
dl = 1.0;
wmin = -1.0;
wmax = 1.0;
wmin_land = -0.3;
# Additional allowed negative vertical velocity per unit height
kl = 0.2;

tau_w = 0.4
g = 9.8
kw  = 1.0
# ------------------- DYNAMICS -------------------

A = np.matrix([
    [1.0000,        0.,    0.0499,        0.],
    [    0.,    1.0000,        0.,    0.0499],
    [    0.,        0.,    0.9950,        0.],
    [    0.,        0.,        0.,    0.9950]
])

B = np.matrix([
    [0.0012,        0.],
    [    0.,    0.0012],
    [0.0499,        0.],
    [    0.,    0.0499]
])

Ab = np.matrix([
    [1.0000,        0.,    0.0494,        0.],
    [    0.,    1.0000,        0.,    0.0494],
    [    0.,        0.,    0.9753,        0.],
    [    0.,        0.,        0.,    0.9753]
])

Bb = np.matrix([
    [0.0012,        0.],
    [    0.,    0.0012],
    [0.0494,        0.],
    [    0.,    0.0494]
])

Av = np.matrix([
    [1.0000,    0.0470],
    [     0,    0.8825]
])

Bv = np.matrix([
    [0.0030],
    [0.1175]
])
# -------------------------- COST MATRICES -----------------------

Q = np.matrix([
    [ 1,     0.,      0.,      0.],
    [0.,      1,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.]
])

R = np.matrix([
    [0.1,         0.],
    [  0.,       0.1]
])

P = np.matrix([
    [1,     0.,      0.,      0.],
    [0.,     1,      0.,      0.],
    [0.,     0.,     0.,      0.],
    [0.,     0.,     0.,      0.]
])

class Parameters():
    def __init__(self, amin, amax, amin_b, amax_b):
        self.amin = amin
        self.amax = amax
        self.amin_b = amin_b
        self.amax_b = amax_b

params = Parameters(-5.0, 5.0, -3.0, 3.0)

x_m = np.zeros((4, 1))
xb_m = np.matrix([[15], [30], [0], [0]])

myProb = CentralisedProblem(T, A, B, Ab, Bb, Q, P, R, params)
myProb.solve(x_m, xb_m)
