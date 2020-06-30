import numpy as np

# --------------- Dynamics parameters of USV ------------------
# Altitude of USV, mostly assumed constant for entire simulation
# Useful to set to a value greater than 0 when landing a UAV without access
# to a boat. This will make the UAV "land" a few meters up in the air and
# avoid running into the ground. Running into the grond can be a problem since
# the UAV usually lands with some horizontal velocity, since the simulated
# boat is not stationary
hb = 0

# These parameters do not accurately reflect realistic dynamics of a USV
tau_wb = 0.4
k_psib = 0.5
tau_psib = 0.5
ddx = 0.5
ddy = 0.5
amin_b = -3.0
amax_b =  3.0
# Bounds on USV velocity and applied torque, only used in moreProblemClasses.py
vmax_b = 3.0
vmin_b = 0.8
T_max = 3
T_min = -1.5

# ----------------- Dynamics Matrices -------------------
# NOTE: Sampling rate must be 20hz for this to be accurate. Check IMPORT_MAIN
# for the current sampling rate

# Matrices for describing dynamics of linear system on the form
# x(t+1) = Ax(t) + Bu(t), where x is the state and u is the control input
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

# [n_USV, m_USV] = Bb.shape   # USV state and input dimensions

# ------------------- Cost Matrices ------------------
# Q denotes the stage state cost matrix, R the stage input cost matrix,
# and P the terminal state cost matrix
Qb = np.matrix([
    [ 1,     0.,      0.,      0.],
    [0.,      1,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.]
])

# When the USV has a secondary objective, the stage cost is Qb+Qb_vel. However,
# if no secondary objective is used, the stage cost is only Qb.
Qb_vel = np.matrix([
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      1000,      0.],
    [0.,     0.,      0.,      1000]
])

Rb = np.matrix([
    [0.1,         0.],
    [  0.,       0.1]
])

Pb = np.matrix([
    [1,     0.,      0.,      0.],
    [0.,     1,      0.,      0.],
    [0.,     0.,     0.,      0.],
    [0.,     0.,     0.,      0.]
])

# Same function as Qb_vel, but for terminal cost
Pb_vel = Qb_vel

class USVParameters():
    def __init__(self):
        self.hb = hb
        self.tau_wb = tau_wb
        self.k_psib = k_psib
        self.tau_psib = tau_psib
        self.ddx = ddx
        self.ddy = ddy
        self.amin_b = amin_b
        self.amax_b = amax_b
        self.v_max_b = vmax_b
        self.v_min_b = vmin_b
        self.T_max = T_max
        self.T_min = T_min
        self.Ab = Ab
        self.Bb = Bb
        self.Qb = Qb
        self.Qb_vel = Qb_vel
        self.Rb = Rb
        self.Pb = Pb
        self.Pb_vel = Pb_vel
        # self.n_USV = n_USV
        # self.m_USV = m_USV

USV_parameters = USVParameters()
