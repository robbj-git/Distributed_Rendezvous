import numpy as np
import scipy as sp
from scipy.linalg import expm
import osqp
from scipy.sparse import csc_matrix
from scipy.integrate import quad
from multiprocessing import Process, Pipe
from IMPORT_ME import SAMPLING_TIME
from time import time

# DEBUG
from matrices_and_parameters import g, k_phi, k_theta, w_phi, w_theta, xi_phi, xi_theta, kdx, kdy, ddx, ddy, k_psib, tau_psib
from matrices_and_parameters import Ab, Bb, Q, R, P, Qb_vel, Pb_vel, amin, amax, tau_wb,\
    amin_b, amax_b, hs, ds, dl, wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max, ang_vel_max
from helper_classes import Parameters
import cvxpy as cp

class CompleteCentralisedProblem():

    # def __init__(self, T, A, B, Ab, Bb, Q, P, R, Q_vel, P_vel, Qb_vel, Pb_vel, type, params, travel_dir = None):
    def __init__(self, T, Ab, Bb, Q, P, R, Rb, Qb_vel, Pb_vel, params):
        self.T = T
        # self.A = A
        # self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.Rb = Rb
        self.Qb_vel = Qb_vel
        self.Pb_vel = Pb_vel
        # # self.Q_vel = Q_vel
        # # self.P_vel = P_vel
        self.params = params
        self.nUAV_s = 6
        self.nUSV_s = 2
        # self.type = type
        # self.last_solution_duration = np.nan
        self.travel_dir = None #travel_dir
        self.create_optimisation_matrices()
        self.create_optimisation_problem()

    def create_optimisation_matrices(self):
        # Dynamics Matrices
        self.A_c =  np.array([
            [0, 0, 1,    0, 0,             0,              0,                   0],
            [0, 0, 0,    1, 0,             0,              0,                   0],
            [0, 0, -kdx, 0, 0,             0,              0,                   0],
            [0, 0, 0, -kdy, 0,             0,              0,                   0],
            [0, 0, 1,    0, 0,             0,              1,                   0],
            [0, 0, 1,    0, 0,             0,              0,                   1],
            [0, 0, 1,    0, -w_phi**2,     0,         -2*w_phi*xi_phi,          0],
            [0, 0, 1,    0, 0,             -w_theta**2,    0,             -2*w_theta*xi_theta]
        ])

        self.B_c = np.array([
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [k_phi*w_phi**2, 0],
            [0, k_theta*w_theta**2]
        ])

        self.C_c = np.zeros((8, 1))
        self.update_linearisation(0.0, 0.0)

        [self.nUAV, self.mUAV] = self.B_c.shape
        [self.nUSV, self.mUSV] = Bb.shape
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        nUAV_s = self.nUAV_s
        nUSV_s = self.nUSV_s
        params = self.params

        self.Phi = np.zeros(( (T+1)*nUAV, nUAV ))
        self.Lambda = np.zeros(( (T+1)*nUAV, T*mUAV ))
        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))
        for j in range(T+1):
            self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    np.dot(np.linalg.matrix_power(self.A, j-k-1),self.B)
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.dot(np.linalg.matrix_power(self.Ab, j-k-1),self.Bb)

        self.Xi = np.zeros((self.nUAV*(self.T+1), 1))
        for block_row in range(1, self.T+1):
            for i in range(block_row-1):
                self.Xi[block_row*self.nUAV:(block_row+1)*self.nUAV] += \
                    np.dot(np.linalg.matrix_power(self.A, block_row-1-i), self.C_d)

        # Cost Matrices
        Ex = np.block([[np.eye(4), np.zeros((4,4))]])
        # Ex = np.block([[np.eye(4), np.zeros((4,2))]])
        EQE = np.dot(Ex.T, np.dot(self.Q, Ex))
        EPE = np.dot(Ex.T, np.dot(self.P, Ex))
        self.Q_UAV = np.kron(np.eye(T+1), EQE)
        self.Q_UAV[-nUAV:(T+1)*nUAV, -nUAV:(T+1)*nUAV] = EPE
        self.QE = np.kron(np.eye(T+1), np.dot(Ex.T, self.Q))
        self.QE[-nUAV:, -nUSV:] = np.dot(Ex.T, self.P)
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = self.P
        self.R_big  = np.kron(np.eye(T),   self.R)
        self.Rb_big  = np.kron(np.eye(T),   self.Rb)
        self.Qb_big_vel  = np.kron(np.eye(T+1), self.Qb_vel)
        self.Qb_big_vel[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = self.Pb_vel
        self.C_mat = 1000*np.eye(self.nUAV_s)
        self.C_mat_USV = 1000*np.eye(self.nUSV_s)

        d1 = nUAV*(T+1)
        d2 = mUAV*T
        c1 = nUSV*(T+1)
        c2 = mUSV*T

        if self.travel_dir is None:
            Q_temp = self.Q_big
        else:
            Q_temp = self.Q_big + self.Qb_big_vel

        P_temp = 2*np.block([
            [self.Q_UAV,        np.zeros((d1,d2)), np.zeros((d1, nUAV_s)), -self.QE,        np.zeros((d1, c2)), np.zeros((d1, nUSV_s))],
            [np.zeros((d2,d1)), self.R_big,         np.zeros((d2, nUAV_s)), np.zeros((d2,c1)), np.zeros((d2,c2)), np.zeros((d2, nUSV_s))],
            [np.zeros((nUAV_s,d1)), np.zeros((nUAV_s, d2)), self.C_mat,  np.zeros((nUAV_s, c1)), np.zeros((nUAV_s, c2)), np.zeros((nUAV_s, nUSV_s))],
            [-self.QE.T,         np.zeros((c1,d2)), np.zeros((c1, nUAV_s)),   Q_temp,         np.zeros((c1,c2)),   np.zeros((c1, nUSV_s))],
            [np.zeros((c2,d1)), np.zeros((c2,d2)), np.zeros((c2, nUAV_s)),  np.zeros((c2,c1)), self.Rb_big,        np.zeros((c2, nUSV_s))],
            [np.zeros((nUSV_s,d1)), np.zeros((nUSV_s,d2)), np.zeros((nUSV_s, nUAV_s)), np.zeros((nUSV_s, c1)), np.zeros((nUSV_s,c2)), self.C_mat_USV]
        ])
        self.P_OSQP = csc_matrix(P_temp)

        if self.travel_dir is None:
            self.q_OSQP = np.zeros( (nUAV*(T+1) + mUAV*T + nUSV*(T+1) + mUSV*T + nUAV_s + nUSV_s, 1) )
        else:
            x1 = params.v_max_b*self.travel_dir[0, 0]
            x2 = params.v_min_b*self.travel_dir[0, 0]
            y1 = params.v_max_b*self.travel_dir[1, 0]
            y2 = params.v_min_b*self.travel_dir[1, 0]
            v_max_x_b = max(x1, x2)
            v_max_y_b = max(y1, y2)
            v_min_x_b = min(x1, x2)
            v_min_y_b = min(y1, y2)
            v_x_des = 0.9*v_min_x_b + 0.1*v_max_x_b
            v_y_des = 0.9*v_min_y_b + 0.1*v_max_y_b
            vel_state = np.array([[0], [0], [v_x_des], [v_y_des]])
            vel_vec = np.kron(np.ones((T+1, 1)), vel_state)
            self.q_OSQP = -2*np.block([
                [np.zeros((d1+d2+nUAV_s, 1))],
                [np.dot( self.Qb_big_vel, vel_vec)],
                [np.zeros((c2+nUSV_s, 1))]
            ])

        # Constraint Matrices
        Mvb = np.array([[0, 0, 1, 0],
                        [0, 0, 0, 1]])
        Mv = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0]])
        Ma = np.array([[0, 0, 0, 0, 1, 0, 0, 0],
                       [0, 0, 0, 0, 0, 1, 0, 0]])
        Mr = np.array([[0, 0, 0, 0, 0, 0, 1, 0],
                       [0, 0, 0, 0, 0, 0, 0, 1]])
        Mv_s = np.array([[1, 0, 0, 0, 0, 0],
                         [0, 1, 0, 0, 0, 0]])
        Ma_s = np.array([[0, 0, 1, 0, 0, 0],
                         [0, 0, 0, 1, 0, 0]])
        Mr_s = np.array([[0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1]])

        self.vel_extractor = np.kron(np.eye(T+1), Mv)
        self.vel_extractor_b = np.kron(np.eye(T+1), Mvb)
        self.ang_extractor = np.kron(np.eye(T+1), Ma)
        self.rate_extractor = np.kron(np.eye(T+1), Mr)
        self.cmd_extractor = np.kron(np.eye(T), np.eye(2))
        self.vel_s_extractor = np.kron(np.ones((T+1, 1)), Mv_s)
        self.ang_s_extractor = np.kron(np.ones((T+1, 1)), Ma_s)
        self.rate_s_extractor = np.kron(np.ones((T+1, 1)), Mr_s)
        self.USV_vel_s_extractor = np.kron(np.ones((T+1, 1)), np.eye(nUSV_s))

        self.set_A_OSQP()

        self.l_OSQP = np.block([
            [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
            [np.full((2*(T+1), 1), -params.v_max)],     # UAV Velocity
            [np.full((2*(T+1), 1), -params.ang_max)],   # UAV Angles
            [np.full((2*(T+1), 1), -params.ang_vel_max)],   # Angular rates
            [np.full((d2, 1), -params.ang_max)],        # UAV Inputs
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],  # USV Dynamics
            [np.full((c2, 1), params.amin_b)],          # USV Input constraints
            [np.full((2*(T+1),   1), -np.inf)]  # USV Velocity constraints
        ])

        self.u_OSQP = np.block([
            [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
            [np.full((2*(T+1), 1), params.v_max)],      # UAV Velocity
            [np.full((2*(T+1), 1), params.ang_max)],    # UAV Angles
            [np.full((2*(T+1), 1), params.ang_vel_max)],   # Angular rates
            [np.full((d2, 1), params.ang_max)],         # UAV Inputs
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],  # USV Dynamics
            [np.full((c2, 1), params.amax_b)],          # USV Input constraints
            [np.full((2*(T+1),   1), np.inf)]   # USV Velocity constraints
        ])

    def set_A_OSQP(self):
        T = self.T
        d1 = self.nUAV*(T+1)
        d2 = self.mUAV*T
        c1 = self.nUSV*(T+1)
        c2 = self.mUSV*T

        sparse_eye = csc_matrix(np.eye(d1))
        Lambda_sparse = self.get_Lambda_sparse()
        lower_left_mat_sparse = csc_matrix(np.block([
            [self.vel_extractor],                # UAV Velocity
            [self.ang_extractor],                # UAV Angles
            [self.rate_extractor],             # UAV Angular Rates
            [np.zeros((d2, d1))]            # UAV Input
        ]))
        lower_mid_mat_sparse = csc_matrix(np.block([
            [np.zeros((2*(T+1), d2))],      # UAV Velocity
            [np.zeros((2*(T+1), d2))],      # UAV Angles
            [np.zeros((2*(T+1), d2))],      # UAV Angular Rates
            [self.cmd_extractor]            # UAV Input
        ]))
        lower_right_mat_sparse = csc_matrix(np.block([
            [self.vel_s_extractor],       # UAV_Velocity
            [self.ang_s_extractor],       # UAV Angles
            [self.rate_s_extractor],          # UAV Angular Rates
            [np.zeros((d2, self.nUAV_s))]     # UAV Input
        ]))
        # I have tested that creating A_OSQP this way does NOT omit storing data
        # for elements of Lambda that happen to be zero. That is, even if some
        # elements of Lambda are zero now, they are still stored in the data vector
        # so if they become non-zero in the future, the spartisty pattern of
        # A_OSQP will not change
        self.A_UAV = sp.sparse.bmat([
            [sparse_eye, -Lambda_sparse, csc_matrix(np.zeros((d1, self.nUAV_s)))],  # UAV Dynamics
            [lower_left_mat_sparse, lower_mid_mat_sparse, lower_right_mat_sparse]
        ])
        self.A_USV = csc_matrix(np.block([
            [np.eye(c1), -self.Lambda_b, np.zeros((c1, self.nUSV_s))], # USV Dynamics
            [np.zeros((c2,c1)), np.eye(c2), np.zeros((c2, self.nUSV_s))], # USV Input
            [self.vel_extractor_b, np.zeros((2*(T+1), c2)), self.USV_vel_s_extractor]  # USV velocity
        ]))

        self.A_OSQP = sp.sparse.bmat([
            [self.A_UAV, None],
            [None, self.A_USV]
        ]).tocsc()

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        self.x  = cp.Variable(( nUAV*(T+1), 1 ))
        self.xb = cp.Variable(( nUSV*(T+1), 1 ))
        self.u  = cp.Variable(( mUAV*T, 1 ))
        self.ub = cp.Variable(( mUSV*T, 1 ))
        self.s_UAV = cp.Variable((self.nUAV_s, 1))
        self.s_USV = cp.Variable(( self.nUSV_s, 1))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, q = self.q_OSQP, A=self.A_OSQP, verbose=True, max_iter = 2000)

    def solve(self, x, xb):
        start = time()
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        nUAV_s = self.nUAV_s
        nUSV_s = self.nUSV_s
        # self.update_OSQP(x, xb)
        self.actually_update_linearisation(x, xb)
        print self.is_pos_semidef(self.P_OSQP.toarray()), ", ", self.is_symmetric(self.P_OSQP.toarray())
        # print "X:", x
        results = self.problemOSQP.solve()
        if results.x[0] is not None and results.info.status != 'maximum iterations reached':
            self.x.value = np.reshape(results.x[0:nUAV*(T+1)], (-1, 1))
            self.u.value = np.reshape(results.x[nUAV*(T+1):nUAV*(T+1)+mUAV*T], (-1, 1))
            self.s_UAV.value = np.reshape(results.x[nUAV*(T+1)+mUAV*T:nUAV*(T+1)+mUAV*T+nUAV_s], (-1, 1))
            self.xb.value = np.reshape(results.x[nUAV*(T+1)+mUAV*T+nUAV_s:(nUSV+nUAV)*(T+1)+mUAV*T+nUAV_s], (-1, 1))
            self.ub.value = np.reshape(results.x[(nUSV+nUAV)*(T+1)+mUAV*T+nUAV_s:(nUSV+nUAV)*(T+1)+(mUSV+mUAV)*T+nUAV_s], (-1, 1))
            self.s_USV.value = np.reshape(results.x[-nUSV_s:], (-1, 1))
        else:
            print "FAILED COMPLETE OPTIMISAITON"
            self.u.value = np.zeros((mUAV*T, 1))
            self.ub.value = np.zeros((mUSV*T, 1))
            self.x.value = self.predict_UAV_traj(x, self.u.value)
            self.xb.value = self.predict_USV_traj(xb, self.ub.value)

        end = time()
        self.last_solution_duration = end-start

    def update_OSQP(self, x0, xb0):
        T = self.T
        mUAV = self.mUAV
        mUSV = self.mUSV
        nUAV = self.nUAV
        nUSV = self.nUSV
        nUAV_s = self.nUAV_s

        self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.l_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
        self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.u_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)

        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP)

    def update_linearisation(self, phi, theta):
        self.A_c[2:4, 4:6] = np.array([
            [0, g/np.cos(theta)**2],
            [-g/( np.cos(theta)*(np.cos(phi)**2) ), -g*np.tan(phi)*np.tan(theta)/np.cos(theta)]
        ])

        self.C_c[2:4, 0:1] = np.array([
            [g*( np.tan(theta) - theta/(np.cos(theta))**2 )],
            [(g/np.cos(theta)) * ( -np.tan(phi) + phi/(np.cos(phi)**2) + np.tan(phi)*np.tan(theta)*theta )]
        ])

        self.A = expm(self.A_c*SAMPLING_TIME)

        self.B = np.full(self.A_c.shape, np.nan)
        for row in range(self.A_c.shape[0]):
            for col in range(self.A_c.shape[1]):
                integrand = lambda tau: expm(self.A_c*(SAMPLING_TIME-tau))[row, col]
                self.B[row, col] = quad(integrand, 0, SAMPLING_TIME)[0]
        self.B = np.dot(self.B, self.B_c)

        self.C_d = self.C_c*SAMPLING_TIME

    def actually_update_linearisation(self, x0, xb0):
        T = self.T
        mUAV = self.mUAV
        mUSV = self.mUSV
        nUAV = self.nUAV
        nUSV = self.nUSV
        nUAV_s = self.nUAV_s
        phi = x0[4, 0]
        theta = x0[5, 0]

        self.A_c[2:4, 4:6] = np.array([
            [0, g/np.cos(theta)**2],
            [-g/( np.cos(theta)*(np.cos(phi)**2) ), -g*np.tan(phi)*np.tan(theta)/np.cos(theta)]
        ])

        self.A = expm(self.A_c*SAMPLING_TIME)

        self.B = np.full(self.A_c.shape, np.nan)
        for row in range(self.A_c.shape[0]):
            for col in range(self.A_c.shape[1]):
                integrand = lambda tau: expm(self.A_c*(SAMPLING_TIME-tau))[row, col]
                self.B[row, col] = quad(integrand, 0, SAMPLING_TIME)[0]
        self.B = np.dot(self.B, self.B_c)

        self.C_c[2:4, 0:1] = np.array([
            [g*( np.tan(theta) - theta/(np.cos(theta))**2 )],
            [(g/np.cos(theta)) * ( -np.tan(phi) + phi/(np.cos(phi)**2) + np.tan(phi)*np.tan(theta)*theta )]
        ])

        self.C_d = self.C_c*SAMPLING_TIME

        # Updating Big Matrices
        for j in range(T+1):
            self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    np.dot(np.linalg.matrix_power(self.A, j-k-1),self.B)

        for block_row in range(1, self.T+1):
            for i in range(block_row-1):
                self.Xi[block_row*self.nUAV:(block_row+1)*self.nUAV] += \
                    np.dot(np.linalg.matrix_power(self.A, block_row-1-i), self.C_d)

        # Update OSQP Matrices

        self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.l_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
        self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.u_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)

        self.set_A_OSQP()
        A_data = self.A_OSQP.data
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, Ax=A_data)

    def get_Lambda_sparse(self):
        num_entries = self.nUAV*self.mUAV*self.T*(self.T+1)//2
        data = np.full((num_entries,), np.nan)
        col_inds = np.full((num_entries,), np.nan)
        row_inds = np.full((num_entries,), np.nan)
        i = 0
        for block_row in range(self.T+1):
            num_cols = block_row*self.mUAV
            for col in range(num_cols):
                for row in range(block_row*self.nUAV, (block_row+1)*self.nUAV):
                    data[i] = self.Lambda[row, col]
                    row_inds[i] = row
                    col_inds[i] = col
                    # print row, col
                    i += 1

        self.Lambda_data = data
        self.Lambda_rows = row_inds
        self.Lambda_cols = col_inds
        return csc_matrix((data, (row_inds, col_inds)), shape=(self.nUAV*(self.T+1),self.mUAV*self.T))

    def predict_UAV_traj(self, x0, u_traj):
        return np.dot(self.Phi, x0) + np.dot(self.Lambda, u_traj)

    def predict_USV_traj(self, xb0, ub_traj):
        return np.dot(self.Phi_b, xb0) + np.dot(self.Lambda_b, ub_traj)

    # DEBUG: FROM https://github.com/oxfordcontrol/osqp/issues/10
    def is_pos_semidef(self, x):
        return np.all(np.linalg.eigvals(x) >= 0)

    def is_symmetric(self, a, tol=1e-8):
        return np.allclose(a, a.T, atol=tol)

class CompleteUSVProblem():

    # def __init__(self, T, A, B, Ab, Bb, Q, P, R, Q_vel, P_vel, Qb_vel, Pb_vel, type, params, travel_dir = None):
    def __init__(self, T, Qb, Pb, Rb, Qb_vel, Pb_vel, nUAV, params, travel_dir = None):
        self.T = T
        self.Qb = Q
        self.Pb = P
        self.Rb = R
        self.Rb = Rb
        self.Qb_vel = Qb_vel
        self.Pb_vel = Pb_vel
        self.params = params
        self.nUSV_s = 2
        self.nUAV = nUAV
        # self.type = type
        # self.last_solution_duration = np.nan
        self.travel_dir = travel_dir
        psi_0 = 0
        T_0 = 0.5
        self.set_initial_dynamics()
        self.create_optimisation_matrices(psi_0, T_0)
        self.create_optimisation_problem()

    def create_optimisation_matrices(self, psi_0, T_0):
        self.update_linearisation_slow(T_0, psi_0)
        [self.nUSV, self.mUSV] = self.Bb.shape
        self.nUSV_s = 2

        self.M_vel = np.array([[0, 0, 1, 0, 0, 0],
                               [0, 0, 0, 1, 0, 0]])
        self.M_T = np.array([[1, 0]])

        self.vel_extractor = np.kron(np.eye(self.T+1), self.M_vel)
        self.T_extractor = np.kron(np.eye(self.T), self.M_T)
        self.vel_s_extractor = np.kron(np.ones((self.T+1, 1)), np.eye(self.nUSV_s))
        self.create_cost_matrices()
        self.create_constraint_matrices()

    def create_cost_matrices(self):
        # Cost Matrices
        T = self.T
        nUSV = self.nUSV
        mUSV = self.mUSV
        nUSV_s = self.nUSV_s
        params = self.params

        # Cost Matrices
        Ex = np.block([[np.eye(4), np.zeros((4,nUSV-4))]])
        # Ex = np.block([[np.eye(4), np.zeros((4,2))]])
        EQE = np.dot(Ex.T, np.dot(self.Qb, Ex))
        EPE = np.dot(Ex.T, np.dot(self.Pb, Ex))
        EQE_vel = np.dot(Ex.T, np.dot(self.Qb_vel, Ex))
        EPE_vel = np.dot(Ex.T, np.dot(self.Pb_vel, Ex))
        self.QE = np.kron(np.eye(T+1), np.dot(self.Qb, Ex))
        self.QE[-self.nUAV:, -nUSV:] = np.dot(self.Pb, Ex)
        self.QE_vel = np.kron(np.eye(T+1), np.dot(self.Qb_vel, Ex))
        self.QE_vel[-self.nUAV:, -nUSV:] = np.dot(self.Pb_vel, Ex)

        self.Qb_big  = 0*np.kron(np.eye(T+1), self.Qb)
        self.Qb_big[-4:(T+1)*4, -4:(T+1)*4] = 0*self.Pb
        self.Qb_big_vel  = np.kron(np.eye(T+1), self.Qb_vel)
        self.Qb_big_vel[-4:(T+1)*4, -4:(T+1)*4] = self.Pb_vel
        self.Rb_big  = np.kron(np.eye(T),   self.Rb)
        self.Qb_big_E  = 0*np.kron(np.eye(T+1), EQE)
        self.Qb_big_E[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = 0*EPE
        self.Qb_big_vel_E  = 0*np.kron(np.eye(T+1), EQE_vel)
        self.Qb_big_vel_E[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = 0*EPE_vel
        # ------------- OSQP Matrices --------------
        velocity_extractor = np.zeros(( 2*(T+1), nUSV*(T+1) ))
        for i in range(T+1):
            for j in range(2):
                velocity_extractor[ 2*i+j, nUSV*i+2+j ] = 1

        dim1 = nUSV*(T+1)
        dim2 = mUSV*T

        self.C = 10*(T+1)*np.eye(nUSV_s)

        if self.travel_dir is None:
            P_temp = 2*np.bmat([[self.Qb_big_E, np.zeros((dim1, dim2)), np.zeros((dim1, nUSV_s))],
                [np.zeros((dim2, dim1)), self.Rb_big, np.zeros((dim2, nUSV_s))],
                [np.zeros((nUSV_s, dim1)), np.zeros((nUSV_s, dim2)), self.C]
            ])
        else:
            # Allows the USV to also track a reference velocity trajectory
            P_temp = 2*np.bmat([[self.Qb_big_E+self.Qb_big_vel_E, np.zeros((dim1, dim2)), np.zeros((dim1, nUSV_s))],
                [np.zeros((dim2, dim1)), 2*self.Rb_big, np.zeros((dim2, nUSV_s))],
                [np.zeros((nUSV_s, dim1)), np.zeros((nUSV_s, dim2)), self.C]
            ])
        P_data = np.diagonal(P_temp)
        P_row = range(nUSV*(T+1) + mUSV*T + 2)
        P_col = range(nUSV*(T+1) + mUSV*T + 2)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        if self.travel_dir is None:
            self.q_OSQP = -2*np.block([
                [np.dot( self.QE, np.zeros(( (T+1)*self.nUAV, 1 )) )],
                [np.zeros((T*mUSV+nUSV_s, 1))]
            ])
        else:
            x1 = params.v_max_b*self.travel_dir[0, 0]
            x2 = params.v_min_b*self.travel_dir[0, 0]
            y1 = params.v_max_b*self.travel_dir[1, 0]
            y2 = params.v_min_b*self.travel_dir[1, 0]
            v_max_x_b = max(x1, x2)
            v_max_y_b = max(y1, y2)
            v_min_x_b = min(x1, x2)
            v_min_y_b = min(y1, y2)
            # print "X:", v_min_x_b, "to", v_max_x_b
            # print "Y:", v_min_y_b, "to", v_max_y_b
            v_x_des = 0.9*v_min_x_b + 0.1*v_max_x_b
            v_y_des = 0.9*v_min_y_b + 0.1*v_max_y_b
            vel_state = np.zeros((4, 1))
            vel_state[2:4, 0:1] = np.array([[v_x_des], [v_y_des]])
            vel_vec = np.kron(np.ones((T+1, 1)), vel_state)
            self.vel_cost_vec = np.dot( self.QE_vel.T, vel_vec)
            self.q_OSQP = -2*np.bmat([
                [0*np.dot( self.QE.T, np.zeros(( (T+1)*self.nUAV, 1 )) ) + \
                    self.vel_cost_vec],
                [np.zeros((T*mUSV+nUSV_s, 1))]
            ])
            # DEBUG
            self.vel_cost = np.dot(vel_vec.T, np.dot(self.Qb_big_vel, vel_vec))

    def create_constraint_matrices(self):
        T = self.T
        nUSV = self.nUSV
        mUSV = self.mUSV
        nUSV_s = self.nUSV_s
        params = self.params

        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))
        for j in range(T+1):
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.dot(np.linalg.matrix_power(self.Ab, j-k-1),self.Bb)

        self.Xi_b = np.zeros((nUSV*(T+1), 1))
        for block_row in range(1, T+1):
            for i in range(block_row-1):
                self.Xi_b[block_row*nUSV:(block_row+1)*nUSV] += \
                    np.dot(np.linalg.matrix_power(self.Ab, block_row-1-i), self.Cb)

        self.l_OSQP = np.block([
            [np.dot(self.Phi_b, np.zeros((nUSV, 1))) + self.Xi_b],      # Dynamics
            [np.full((2*(T+1), 1), -params.v_max_b)],               # Velocity
            [np.full((T, 1), params.T_min)],                        # Input
        ])

        self.u_OSQP = np.block([
            [np.dot(self.Phi_b, np.zeros((nUSV, 1))) + self.Xi_b],  # Dynamics
            [np.full((2*(T+1), 1), params.v_max_b)],                # Velocity
            [np.full((T, 1), params.T_max)],                        # Input
        ])

        sparse_eye = csc_matrix(np.eye(nUSV*(T+1)))
        Lambda_sparse = self.get_Lambda_sparse(self.Lambda_b)
        lower_left_sparse = csc_matrix(np.block([
            [self.vel_extractor],
            [np.zeros((T, nUSV*(T+1)))]
        ]))
        lower_mid_sparse = csc_matrix(np.block([
            [np.zeros((2*(T+1), mUSV*T))],
            [self.T_extractor]
        ]))
        lower_right_sparse = csc_matrix(np.block([
            [self.vel_s_extractor],
            [np.zeros((T, nUSV_s))]
        ]))
        self.A_OSQP = sp.sparse.bmat([
            [np.eye(nUSV*(T+1)), -Lambda_sparse, None],
            [lower_left_sparse, lower_mid_sparse, lower_right_sparse]
        ]).tocsc()

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        self.xb = cp.Variable(( nUSV*(T+1), 1 ))
        self.ub = cp.Variable(( mUSV*T, 1 ))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.x_hat  = cp.Parameter((nUAV*(T+1), 1))
        self.s  = cp.Variable((2, 1))
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, q=self.q_OSQP, verbose=False, max_iter = 500)

    def solve(self, xb, x_traj, USV_should_stop = False):
        start = time()
        self.x_hat.value = x_traj
        self.xb_0.value = xb
        # print xb_m[-2:]
        if USV_should_stop:
            self.ub.value = np.zeros((self.mUSV*self.T, 1))
            self.xb.value = self.predict_trajectory(xb, self.ub.value)
        else:
            self.update_OSQP(xb, x_traj)
            results = self.problemOSQP.solve()
            print "OBJECTIVE:", results.info.obj_val + self.vel_cost[0,0] + self.state_cost[0,0]
            if not results.x[0] is None:
                self.xb.value = np.reshape(results.x[0:self.nUSV*(self.T+1)], (-1, 1))
                self.ub.value = np.reshape(results.x[self.nUSV*(self.T+1):-self.nUSV_s], (-1, 1))
                self.s.value  = np.reshape(results.x[-self.nUSV_s:], (-1, 1))
            else:
                print "USV problem failed:", results.info.status
                self.ub.value = np.zeros((self.mUSV*self.T, 1))
                self.xb.value = self.predict_trajectory(xb, self.ub.value)
                self.s.value = np.zeros((self.nUSV_s,1))
                self.s.value.fill(np.nan)
        end = time()
        self.last_solution_duration = end - start

    def update_OSQP(self, xb0, x_traj):
        # T = self.T
        # mUAV = self.mUAV
        # mUSV = self.mUSV
        # nUAV = self.nUAV
        # nUSV = self.nUSV
        # nUAV_s = self.nUAV_s
        #
        # self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.l_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
        # self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.u_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
        #
        # self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP)

        params = self.params
        T = self.T
        self.l_OSQP[0:(T+1)*self.nUSV, 0:1] = np.dot(self.Phi_b, xb0)
        self.u_OSQP[0:(T+1)*self.nUSV, 0:1] = np.dot(self.Phi_b, xb0)
        # print "AIGHT", self.q_OSQP[0:(T+1)*self.nUSV, 0:1].shape, np.dot( self.Qb_big, x_traj ).shape, self.vel_cost_vec.shape
        self.q_OSQP[0:(T+1)*self.nUSV, 0:1] = -2*(0*np.dot( self.QE.T, x_traj ) + self.vel_cost_vec)

        self.state_cost = np.dot(x_traj.T, np.dot(self.Qb_big, x_traj))

        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q=self.q_OSQP)

    def update_linearisation(self, T_0, psi_0):
        a1 = -np.sin(psi_0)*T_0
        a2 = np.cos(psi_0)*T_0
        a3 = -1/tau_wb  # TODO: Undefined
        h = SAMPLING_TIME
        self.Ab = np.array([
            [1, 0, a1*h, -a1*h/a3 + a1*(np.exp(a3*h)-1)/a3**2],
            [0, 1, a2*h, -a2*h/a3 + a2*(np.exp(a3*h)-1)/a3**2],
            [0, 0, 1, (np.exp(a3*h)-1)/a3],
            [0, 0, 0, np.exp(a3*h)]
        ])

        self.Ab = np.block([
            [np.zeros((2,2)), np.eye(2), np.zeros((2,2))],
            [np.zeros((4,2)), self.Ab]
        ])

        integral = np.array([
            [h, 0, 0.5*a1*(h**2), -0.5*a1*(h**2)/a3 + a1*np.exp(a3*h)*(1-np.exp(-a3*h))/a3**3 - a1*h/a3**2],
            [0, h, 0.5*a2*(h**2), -0.5*a2*(h**2)/a3 + a2*np.exp(a3*h)*(1-np.exp(-a3*h))/a3**3 - a2*h/a3**2],
            [0, 0, h, np.exp(a3*h)*(1-np.exp(-a3*h))/a3**2 - h/a3],
            [0, 0, 0, np.exp(a3*h)*(1-np.exp(-a3*h))/a3]
        ])

        B_c = np.array([[np.cos(psi_0), 0],
                        [np.sin(psi_0), 0],
                        [0, 0],
                        [0, k_psib/tau_psib]])
        self.Bb = np.dot(integral, B_c)
        self.Bb = np.block([
            [np.zeros((2,2))],
            [self.Bb]
        ])

        self.Cb = np.array([[0],
                            [0],
                            [np.sin(psi_0)*T_0*psi_0*h],
                            [-np.cos(psi_0)*T_0*psi_0*h],
                            [0],
                            [0]])

    def set_initial_dynamics(self):
        self.A_c = np.array([
            [0, 0, 1,    0,    0, 0],
            [0, 0, 0,    1,    0, 0],
            [0, 0, -ddx, 0,    0, 0],
            [0, 0, 1,    -ddy, 0, 0],
            [0, 0, 1,    0,    0, 0],
            [0, 0, 1,    0,    0, -1/tau_wb]
        ])

        self.B_c = np.array([
            [0,             0],
            [0,             0],
            [0,             0],
            [0,             0],
            [0,             0],
            [0, k_psib/tau_psib]
        ])

        self.C_c = np.zeros((6,1))

    def update_linearisation_slow(self, T_0, psi_0):
        self.A_c[2:4, 4:5] = np.array([
            [-T_0*np.sin(psi_0)],
            [ T_0*np.cos(psi_0)]
        ])

        self.B_c[2:4, 0:1] = np.array([
            [np.cos(psi_0)],
            [np.sin(psi_0)]
        ])

        self.C_c[2:4, 0:1] = np.array([
            [T_0*psi_0*np.sin(psi_0)],
            [-T_0*psi_0*np.cos(psi_0)]
        ])

        self.Ab = expm(self.A_c*SAMPLING_TIME)

        self.Bb = np.full(self.A_c.shape, np.nan)

        for row in range(self.A_c.shape[0]):
            for col in range(self.A_c.shape[1]):
                integrand = lambda tau: expm(self.A_c*(SAMPLING_TIME-tau))[row, col]
                self.Bb[row, col] = quad(integrand, 0, SAMPLING_TIME)[0]
        self.Bb = np.dot(self.Bb, self.B_c)

        self.Cb = self.C_c*SAMPLING_TIME

    def actually_update_linearisation(self, x0, xb0):
    #     T = self.T
    #     mUAV = self.mUAV
    #     mUSV = self.mUSV
    #     nUAV = self.nUAV
    #     nUSV = self.nUSV
    #     nUAV_s = self.nUAV_s
    #     phi = x0[4, 0]
    #     theta = x0[5, 0]
    #
    #     self.A_c[2:4, 4:6] = np.array([
    #         [0, g/np.cos(theta)**2],
    #         [-g/( np.cos(theta)*(np.cos(phi)**2) ), -g*np.tan(phi)*np.tan(theta)/np.cos(theta)]
    #     ])
    #
    #     self.A = expm(self.A_c*SAMPLING_TIME)
    #
    #     self.B = np.full(self.A_c.shape, np.nan)
    #     for row in range(self.A_c.shape[0]):
    #         for col in range(self.A_c.shape[1]):
    #             integrand = lambda tau: expm(self.A_c*(SAMPLING_TIME-tau))[row, col]
    #             self.B[row, col] = quad(integrand, 0, SAMPLING_TIME)[0]
    #     self.B = np.dot(self.B, self.B_c)
    #
    #     self.C_c[2:4, 0:1] = np.array([
    #         [g*( np.tan(theta) - theta/(np.cos(theta))**2 )],
    #         [(g/np.cos(theta)) * ( -np.tan(phi) + phi/(np.cos(phi)**2) + np.tan(phi)*np.tan(theta)*theta )]
    #     ])
    #
    #     self.C_d = self.C_c*SAMPLING_TIME
    #
    #     # Updating Big Matrices
    #     for j in range(T+1):
    #         self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
    #         for k in range(j):  # range(0) returns empty list
    #             self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
    #                 np.dot(np.linalg.matrix_power(self.A, j-k-1),self.B)
    #
    #     for block_row in range(1, self.T+1):
    #         for i in range(block_row-1):
    #             self.Xi[block_row*self.nUAV:(block_row+1)*self.nUAV] += \
    #                 np.dot(np.linalg.matrix_power(self.A, block_row-1-i), self.C_d)
    #
    #     # Update OSQP Matrices
    #
    #     self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
    #     self.l_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
    #     self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
    #     self.u_OSQP[(T+1)*(nUAV+nUAV_s)+mUAV*T:(T+1)*(nUAV+nUSV+nUAV_s)+mUAV*T] = np.dot(self.Phi_b, xb0)
    #
    #     self.set_A_OSQP()
    #     A_data = self.A_OSQP.data
    #     self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, Ax=A_data)
        return

    def get_Lambda_sparse(self, Lambda):
        num_entries = self.nUSV*self.mUSV*self.T*(self.T+1)//2
        data = np.full((num_entries,), np.nan)
        col_inds = np.full((num_entries,), np.nan)
        row_inds = np.full((num_entries,), np.nan)
        i = 0
        for block_row in range(self.T+1):
            num_cols = block_row*self.mUSV
            for col in range(num_cols):
                for row in range(block_row*self.nUSV, (block_row+1)*self.nUSV):
                    data[i] = Lambda[row, col]
                    row_inds[i] = row
                    col_inds[i] = col
                    # print row, col
                    i += 1

        self.Lambda_data = data
        self.Lambda_rows = row_inds
        self.Lambda_cols = col_inds
        return csc_matrix((data, (row_inds, col_inds)), shape=(self.nUSV*(self.T+1),self.mUSV*self.T))

    def predict_trajectory(self, xb0, ub_traj):
        return np.dot(self.Phi_b, xb0) + np.dot(self.Lambda_b, ub_traj)

# if __name__ == '__main__':
#     params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
#         wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max, ang_vel_max)
#     my_prob = CompleteCentralisedProblem(100, Ab, Bb, Q, R, P, R, Qb_vel, Pb_vel, params)
