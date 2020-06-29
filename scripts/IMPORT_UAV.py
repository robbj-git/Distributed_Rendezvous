import numpy as np

# --------------- Dynamics parameters of UAV ------------------
# See section 5.2.2 in
# "Autonomous and Cooperative Landings Using Model Predictive Control",
# Licenciate Thesis by Linnea Persson , Royal Institute of Technology (KTH),
# Stockholm, Sweden, 2019
tau_w = 0.4
kw  = 1.0
k_phi = 0.95
w_phi = 9.0
xi_phi =  0.72
k_theta = 1.02
w_theta = 11.0
xi_theta = 0.7
# These parameters have not been set using system identification
kdx = 0.1
kdy = 0.1
kdz = 0.0

# --------------- Constraint parameters of UAV -------------------
# Bounds on acceleration
amin  =  -5.0
amax  =   5.0
# Parameters specifying forbidden region, see original paper for details
# ( Reference to paper can be found in readme.md )
hs = 4.0
ds = 2.0
dl = 1.0

# Bounds on UAV vertical velocity
wmin = -1.0
wmax = 1.0
wmin_land = -0.3
# Additional allowed negative vertical velocity per unit height
# More specifically: let v be the vertical velocity, positive when the UAV is
# rising. Then the touchdown vertical velocity constraint is given by
# -v <= kl*h - wmin_land,
# where h is the UAV altitude and wmin_land is the maximum allowed descent
# velocity at touchdown
kl = 0.2
# Maximum horizontal velocity of UAV, only used in moreProblemClasses.py
vmax = 5.0
# Bounds on UAV angles, only used in moreProblemClasses.py
ang_max = np.radians(30)
ang_vel_max = np.radians(30)
psi_max = np.radians(10)

# ----------------- Dynamics Matrices -------------------
# NOTE: Sampling rate must be 20hz for this to be accurate. Check IMPORT_MAIN
# for the current sampling rate

# Matrices for describing dynamics of linear system on the form
# x(t+1) = Ax(t) + Bu(t), where x is the state and u is the control input
# Horizontal dynamics
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

# Vertical Dynamics
Av = np.matrix([
    [1.0000,    0.0470],
    [     0,    0.8825]
])

Bv = np.matrix([
    [0.0030],
    [0.1175]
])

# [n_UAV, m_UAV] = B.shape    # UAV horizontal state and input dimensions
# [nv, mv] = Bv.shape         # UAV vertical state and input dimensions

# ------------------- Cost Matrices ------------------
# Q denotes the stage state cost matrix, R the stage input cost matrix,
# and P the terminal state cost matrix
# NOTE: It is these matrices that are used in the centralised problem

# Cost matrices for horizontal problem
Q = np.matrix([
    [ 1,     0.,      0.,      0.],
    [0.,      1,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.]
])

# Deprecated, should be removed
Q_vel = np.matrix([
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.],
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

# Deprecated, should be removed
P_vel = Q_vel

# Cost matrices for vertical problem:
Qv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])

Rv = 0.1

Pv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])

# Creates an object that can be imported that contains all the above parameters

class UAVParameters():
    def __init__(self):
        self.tau_w = tau_w
        self.kw = kw
        self.k_phi = k_phi
        self.w_phi = w_phi
        self.xi_phi = xi_phi
        self.k_theta = k_theta
        self.w_theta = w_theta
        self.xi_theta = xi_theta
        self.kdx = kdx
        self.kdy = kdy
        self.kdz = kdz
        self.amin = amin
        self.amax = amax
        self.hs = hs
        self.ds = ds
        self.dl = dl
        self.wmin = wmin
        self.wmax = wmax
        self.wmin_land = wmin_land
        self.kl = kl
        self.v_max = vmax
        self.ang_max = ang_max
        self.ang_vel_max = ang_vel_max
        self.psi_max = psi_max
        self.A = A
        self.B = B
        self.Av = Av
        self.Bv = Bv
        self.Q = Q
        self.P = P
        self.R = R
        self.Q_vel = Q_vel
        self.P_vel = P_vel
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        # self.n_UAV = n_UAV
        # self.m_UAV = m_UAV

UAV_parameters = UAVParameters()
