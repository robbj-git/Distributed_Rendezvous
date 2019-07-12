import numpy as np
from math import atan
from IMPORT_ME import *

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

# ----------------- PARAMETERS -----------------
# hs = 5.0;
# ds = 2.0;
# dl = 1.0;
# wmin = -1.0;
# wmax = 1.0;
# wmin_land = -0.3;
# # Additional allowed negative vertical velocity per unit height
# kl = 0.2;

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

[nUAV, mUAV] = B.shape
[nUSV, mUSV] = Bb.shape
[nv, mv]     = Bv.shape

Phi = np.zeros(( (T+1)*nUAV, nUAV ))
Lambda = np.zeros(( (T+1)*nUAV, T*mUAV ))
Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))
Phi_v = np.zeros(( (T+1)*nv, nv ))
Lambda_v =  np.zeros(( (T+1)*nv, T*mv ))

for j in range(T+1):
    Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(A, j)
    Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(Ab, j)
    Phi_v[ j*nv :(j+1)*nv,   :] = np.linalg.matrix_power(Av, j)
    for k in range(j):  # range(0) returns empty list
        Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
            np.linalg.matrix_power(A, j-k-1)*B
        Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
            np.linalg.matrix_power(Ab, j-k-1)*Bb
        Lambda_v[  j*nv:(j+1)*nv,    k*mv:(k+1)*mv   ] = \
            np.linalg.matrix_power(Av, j-k-1)*Bv

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

Q_big  = np.kron(np.eye(T+1), Q)
Q_big[-nUAV:(T+1)*nUAV, -nUAV:(T+1)*nUAV] = P
R_big  = np.kron(np.eye(T),   R)
Qv_big = np.kron(np.eye(T+1), Qv)       # I haven't double-checked that this is correct
Qv_big[-nv:(T+1)*nv, -nv:(T+1)*nv] = Pv
Rv_big = np.kron(np.eye(T),   Rv)

# ---------------------------- VERTICAL CONSTRAINTS ----------------------------
# TODO: Consider using sparse matrices
height_extractor = np.zeros(( T+1, 2*(T+1) ))
for i in range(T+1):
    height_extractor[ i, 2*i ] = 1

velocity_extractor = np.zeros(( T+1, 2*(T+1) ))
for i in range(T+1):
    velocity_extractor[ i, 2*i+1 ] = 1

touchdown_matrix = np.zeros(( T+1, 2*(T+1) ))
for i in range(T+1):
    touchdown_matrix[ i, 2*i ] = kl
    touchdown_matrix[ i, 2*i+1 ] = 1

# TODO: dl AND ds CAN*T BE PARAMETERS THEN!!!!!!

# Constraints appear in the following row order:
# * Max velocity constraints
# * Min velocity constraints
# * Touchdown constraints
# * Altitude constraints (height greater than 0)
# * Left (or right) safety constraints          REMOVED
# * Right (or left) safety constraints          REMOVED
vert_constraints_matrix = np.bmat([\
    [velocity_extractor],\
    [-velocity_extractor],\
    [-touchdown_matrix],\
    [height_extractor],\
])

# TODO: Last two rows have to separate as they depend on distance, which is a parameter

vert_constraints_vector = np.bmat([\
    [ wmax*np.ones((T+1, 1))],\
    [-wmin*np.ones((T+1, 1))],\
    [-wmin_land*np.ones((T+1, 1))], \
    [np.zeros((T+1, 1))],\
])

safety_matrix = np.bmat([\
    [(dl-ds)*height_extractor],\
    [(dl-ds)*height_extractor],\
])

# ------------- INTERMEDIATE CONTROLLERS ----------------
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
