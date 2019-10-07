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
from matrices_and_parameters import g, k_phi, k_theta, w_phi, w_theta, xi_phi, xi_theta, kdx, kdy
from matrices_and_parameters import Ab, Bb, Q, R, P, Qb_vel, Pb_vel, amin, amax,\
    amin_b, amax_b, hs, ds, dl, wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max
from helper_classes import Parameters
import cvxpy as cp

class CompleteCentralisedProblem():

    # def __init__(self, T, A, B, Ab, Bb, Q, P, R, Q_vel, P_vel, Qb_vel, Pb_vel, type, params, travel_dir = None):
    def __init__(self, T, Ab, Bb, Q, R, P, Rb, Qb_vel, Pb_vel, params):
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
        # self.type = type
        # self.last_solution_duration = np.nan
        self.travel_dir = None #travel_dir
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        # if self.type == 'CVXGEN':
        #     self.ROS_init()

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
        self.ns = 4
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        ns = self.ns
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
        self.C_mat = 1000*np.eye(self.ns)

        d1 = nUAV*(T+1)
        d2 = mUAV*T
        c1 = nUSV*(T+1)
        c2 = mUSV*T

        if self.travel_dir is None:
            Q_temp = self.Q_big
        else:
            Q_temp = self.Q_big + self.Qb_big_vel

        P_temp = 2*np.block([
            [self.Q_UAV,        np.zeros((d1,d2)), np.zeros((d1, ns)), -self.QE,        np.zeros((d1, c2))],
            [np.zeros((d2,d1)), self.R_big,         np.zeros((d2, ns)), np.zeros((d2,c1)), np.zeros((d2,c2))],
            [np.zeros((ns,d1)), np.zeros((ns, d2)), self.C_mat,       np.zeros((ns, c1)), np.zeros((ns, c2))],
            [-self.QE.T,         np.zeros((c1,d2)), np.zeros((c1, ns)), Q_temp,         np.zeros((c1,c2))],
            [np.zeros((c2,d1)), np.zeros((c2,d2)), np.zeros((c2, ns)),         np.zeros((c2,c1)), self.Rb_big]
        ])
        self.P_OSQP = csc_matrix(P_temp)

        if self.travel_dir is None:
            self.q_OSQP = np.zeros( (nUAV*(T+1) + mUAV*T + nUSV*(T+1) + mUSV*T + ns, 1) )
        else:
            x1 = params.v_max_b*self.travel_dir[0]
            x2 = params.v_min_b*self.travel_dir[0]
            y1 = params.v_max_b*self.travel_dir[1]
            y2 = params.v_min_b*self.travel_dir[1]
            v_max_x_b = max(x1, x2)
            v_max_y_b = max(y1, y2)
            v_min_x_b = min(x1, x2)
            v_min_y_b = min(y1, y2)
            v_x_des = 0.9*v_min_x_b + 0.1*v_max_x_b
            v_y_des = 0.9*v_min_y_b + 0.1*v_max_y_b
            vel_state = np.array([[0], [0], [v_x_des], [v_y_des]])
            vel_vec = np.kron(np.ones((T+1, 1)), vel_state)
            self.q_OSQP = -2*np.block([
                [np.zeros((d1+d2+ns, 1))],
                [np.dot( self.Qb_big_vel, vel_vec)],
                [np.zeros((c2, 1))]
            ])

        # Constraint Matrices
        Mvb = np.array([[0, 0, 1, 0],
                        [0, 0, 0, 1]])
        Mv = np.array([[0, 0, 1, 0, 0, 0, 0, 0],
                       [0, 0, 0, 1, 0, 0, 0, 0]])
        Ma = np.array([[0, 0, 0, 0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0, 1, 0, 0]])
        Mv_s = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])
        Ma_s = np.array([[0, 0, 1, 0],
                         [0, 0, 0, 1]])

        vel_extractor = np.kron(np.eye(T+1), Mv)
        vel_extractor_b = np.kron(np.eye(T+1), Mvb)
        ang_extractor = np.kron(np.eye(T+1), Ma)
        cmd_extractor = np.kron(np.eye(T), np.eye(2))
        vel_s_extractor = np.kron(np.ones((T+1, 1)), Mv_s)
        ang_s_extractor = np.kron(np.ones((T+1, 1)), Ma_s)

        sparse_eye = csc_matrix(np.eye(d1))
        Lambda_sparse = self.get_Lambda_sparse()
        lower_left_mat_sparse = csc_matrix(np.block([
            # [vel_extractor],                # UAV Velocity
            [ang_extractor],                # UAV Angles
            # [np.zeros((d2, d1))]            # UAV Input
        ]))
        lower_mid_mat_sparse = csc_matrix(np.block([
            # [np.zeros((2*(T+1), d2))],      # UAV Velocity
            [np.zeros((2*(T+1), d2))],      # UAV Angles
            # [cmd_extractor]                 # UAV Input
        ]))
        lower_right_mat_sparse = csc_matrix(np.block([
            [ang_s_extractor]       # UAV Angles
        ]))
        self.A_UAV = sp.sparse.bmat([
            [sparse_eye, -Lambda_sparse, csc_matrix(np.zeros((d1, ns)))],                # UAV Dynamics
            [lower_left_mat_sparse, lower_mid_mat_sparse, lower_right_mat_sparse]
        ])
        # self.A_USV = csc_matrix(np.block([
        #     [np.eye(c1), -self.Lambda_b],               # USV Dynamics
        #     [np.zeros((c2,c1)), np.eye(c2)],            # USV Input
        #     [vel_extractor_b, np.zeros((2*(T+1), c2))]  # USV velocity
        # ]))
        self.A_USV = csc_matrix(np.block([
            [np.eye(c1), -self.Lambda_b]               # USV Dynamics
        ]))

        self.A_OSQP = sp.sparse.bmat([
            [self.A_UAV, None],
            [None, self.A_USV]
        ]).tocsc()

        # self.A_OSQP = csc_matrix(np.block([
        #     [np.eye(d1), -self.Lambda, np.zeros()],
        #     [np.zeros(), np.eye(c1), -self.Lambdab]
        # ]))

        # self.l_OSQP = np.block([
        #     [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
        #     [np.full((2*(T+1), 1), -params.v_max)],     # UAV Velocity
        #     [np.full((2*(T+1), 1), -params.ang_max)],   # UAV Angles
        #     [np.full((d2, 1), -params.ang_max)],        # UAV Inputs
        #     [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],  # USV Dynamics
        #     [np.full((c2, 1), params.amin_b)],          # USV Input constraints
        #     [np.full((2*(T+1),   1), -params.v_max_b)]  # USV Velocity constraints
        # ])
        #
        # self.u_OSQP = np.block([
        #     [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
        #     [np.full((2*(T+1), 1), params.v_max)],      # UAV Velocity
        #     [np.full((2*(T+1), 1), params.ang_max)],    # UAV Angles
        #     [np.full((d2, 1), params.ang_max)],         # UAV Inputs
        #     [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],  # USV Dynamics
        #     [np.full((c2, 1), params.amax_b)],          # USV Input constraints
        #     [np.full((2*(T+1),   1), params.v_max_b)]   # USV Velocity constraints
        # ])


        self.l_OSQP = np.block([
            [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
            [np.full((2*(T+1), 1), -params.ang_max)],   # UAV Angles
            # [np.full((d2, 1), -params.ang_max)],        # UAV Inputs
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))]  # USV Dynamics
        ])

        self.u_OSQP = np.block([
            [np.dot(self.Phi, np.zeros((nUAV, 1))) + self.Xi],    # UAV Dynamics
            [np.full((2*(T+1), 1), params.ang_max)],    # UAV Angles
            # [np.full((d2, 1), params.ang_max)],         # UAV Inputs
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))]  # USV Dynamics
        ])

        print "PAMS", params.ang_max    # DEBUG PRINT

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
        self.s_UAV = cp.Variable(( 1, 1 ))
        self.s_USV = cp.Variable(( 1, 1 ))
        self.s_UAV_new = cp.Variable((self.ns, 1))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, q = self.q_OSQP, A=self.A_OSQP, verbose=False, max_iter = 200)

    def solve(self, x, xb):
        start = time()
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        ns = self.ns
        self.update_OSQP(x, xb)
        results = self.problemOSQP.solve()
        self.x.value = np.reshape(results.x[0:nUAV*(T+1)], (-1, 1))
        self.u.value = np.reshape(results.x[nUAV*(T+1):nUAV*(T+1)+mUAV*T], (-1, 1))
        self.xb.value = np.reshape(results.x[nUAV*(T+1)+mUAV*T+ns:(nUSV+nUAV)*(T+1)+mUAV*T+ns], (-1, 1))
        self.ub.value = np.reshape(results.x[(nUSV+nUAV)*(T+1)+mUAV*T+ns:(nUSV+nUAV)*(T+1)+(mUSV+mUAV)*T+ns], (-1, 1))
        end = time()
        self.last_solution_duration = end-start

    def update_OSQP(self, x0, xb0):
        T = self.T
        mUAV = self.mUAV
        mUSV = self.mUSV
        nUAV = self.nUAV
        nUSV = self.nUSV

        self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.l_OSQP[(T+1)*(nUAV+2):(T+1)*(nUAV+nUSV+2)] = np.dot(self.Phi_b, xb0)
        self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        self.u_OSQP[(T+1)*(nUAV+2):(T+1)*(nUAV+nUSV+2)] = np.dot(self.Phi_b, xb0)

        # self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.l_OSQP[(T+1)*(nUAV+2)+mUAV*T:(T+1)*(nUAV+nUSV+2)+mUAV*T] = np.dot(self.Phi_b, xb0)
        # self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.u_OSQP[(T+1)*(nUAV+2)+mUAV*T:(T+1)*(nUAV+nUSV+2)+mUAV*T] = np.dot(self.Phi_b, xb0)
        # AREN'T THESE INDICES WRONG??? WHERE'S 2*(T+1)???
        # self.l_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.l_OSQP[(T+1)*(nUAV)+T*mUAV:(T+1)*(nUAV+nUSV)+T*mUAV] = np.dot(self.Phi_b, xb0)
        # self.u_OSQP[0:(T+1)*nUAV] = np.dot(self.Phi, x0) + self.Xi
        # self.u_OSQP[(T+1)*(nUAV)+T*mUAV:(T+1)*(nUAV+nUSV)+T*mUAV] = np.dot(self.Phi_b, xb0)

        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP)

    def update_linearisation(self, theta, phi):
        # TODO: DELETE ME
        # self.A_c = np.array([
        #     [0, 0, 1,    0, 0, 0],
        #     [0, 0, 0,    1, 0, 0],
        #     [0, 0, -0.1, 0, 0, 9.8],
        #     [0, 0, 0, -0.1, -9.8, 0],
        #     [0, 0, 0,   0,    0,  0],
        #     [0, 0, 0,   0,    0,  0]
        # ])
        #
        # self.B_c = np.array([
        #     [0, 0],
        #     [0, 0],
        #     [0, 0],
        #     [0, 0],
        #     [1, 0],
        #     [0, 1]
        # ])

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

if __name__ == '__main__':
    params = Parameters(amin, amax, amin_b, amax_b, hs, ds, dl, \
        wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max = ang_max)
    my_prob = CompleteCentralisedProblem(100, Ab, Bb, Q, R, P, R, Qb_vel, Pb_vel, params)
