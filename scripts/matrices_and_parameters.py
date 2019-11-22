import numpy as np

# ------------------- PARAMETERS -------------------

hb = 0 # Altitude of USV, assumed constant for entire simulation

tau_wb = 0.4
k_psib = 0.5
tau_psib = 0.5  # TODO: SET THESE TO SOMETHING REASONABLE!!!

tau_w = 0.4
g = 9.8
kw  = 1.0
k_phi = 0.95
w_phi = 9.0
xi_phi =  0.72
k_theta = 1.02
w_theta = 11.0
xi_theta = 0.7
# Not identified, but set to the parameters sent by Linnea
kdx = 0.1
kdy = 0.1
kdz = 0.0
# Like kdx and kdy but for boat
ddx = 0.5
ddy = 0.5

amin  =  -5.0
amax  =   5.0
amin_b = -3.0
amax_b =  3.0
hs = 4.0
ds = 2.0
dl = 1.0
wmin = -1.0
wmax = 1.0
wmin_land = -0.3
# Additional allowed negative vertical velocity per unit height
kl = 0.2
vmax = 5.0
vmax_b = 3.0
vmin_b = 0.8
ang_max = np.radians(30)
ang_vel_max = np.radians(30)
psi_max = np.radians(10)
T_max = 3
T_min = -1.5
# vmax_x_b = vmax_b
# vmin_x_b = vmin_b
# vmax_y_b = vmax_b
# vmin_y_b = vmin_b

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

[n_UAV, m_UAV] = B.shape
[n_USV, m_USV] = Bb.shape
[nv, mv] = Bv.shape

# -------------------------- COST MATRICES -----------------------

Q = np.matrix([
    [ 1,     0.,      0.,      0.],
    [0.,      1,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.]
])

Qb_vel = np.matrix([
    [0.,     0.,      0.,      0.],
    [0.,     0.,      0.,      0.],
    [0.,     0.,      1000,      0.],
    [0.,     0.,      0.,      1000]
])

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

Pb_vel = Qb_vel

P_vel = Q_vel

Qv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])

Rv = 0.1

Pv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])

class DynamicsParameters():
    def __init__(self):
        self.A = A
        self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.Qb_vel = Qb_vel
        self.Pb_vel = Pb_vel
        self.Q_vel = Q_vel
        self.P_vel = P_vel
        self.Av = Av
        self.Bv = Bv
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        self.amin = amin
        self.amax = amax
        self.amin_b = amin_b
        self.amax_b = amax_b
        self.hs = hs
        self.ds = ds
        self.dl = dl
        self.wmin = wmin
        self.wmax = wmax
        self.wmin_land = wmin_land
        self.kl = kl
        self.v_max = vmax
        self.v_max_b = vmax_b
        self.v_min_b = vmin_b
        self.ang_max = ang_max
        self.ang_vel_max = ang_vel_max
        self.psi_max = psi_max
        self.T_max = T_max
        self.T_min = T_min
        self.hb = hb

dynamics_parameters = DynamicsParameters()
