import numpy as np

# ------------------- PARAMETERS -------------------

tau_w = 0.4
g = 9.8
kw  = 1.0

amin  =  -5.0
amax  =   5.0
amin_b = -3.0
amax_b =  3.0
hs = 5.0
ds = 2.0
dl = 1.0
wmin = -1.0
wmax = 1.0
wmin_land = -0.3
# Additional allowed negative vertical velocity per unit height
kl = 0.2
vmax = 5.0
vmax_b = 5.0
vmin_b = 0.8

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

Qv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])

Rv = 0.1

Pv = np.matrix([
    [1.0, 0.0],
    [0.0, 0.0]
])


# ------------- INNER CONTROLLERS ----------------
KUAV = np.matrix([
    [300.7506,         0.0,   32.4751,         0.0],
    [     0.0,    300.7506,       0.0,     32.4751]
])

KUSV = np.matrix([
    [303.7656,         0.0,   32.3763,         0.0],
    [     0.0,    303.7656,       0.0,     32.3763]
])

KVert = np.matrix([
    [127.6562,      12.7630]
])
