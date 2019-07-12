import cvxpy as cp
import numpy as np
import scipy as sp
import thread       # TODO: TEST THE THREADING!!!!!!

class CentralisedProblem():

    def __init__(self, T, A, B, Ab, Bb, Q, P, R, params):
        self.T = T
        self.A = A
        self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.params = params
        [self.nUAV, self.mUAV] = B.shape
        [self.nUSV, self.mUSV] = Bb.shape
        self.create_optimisation_matrices()
        self.create_optimisation_problem()

    def create_optimisation_matrices(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV

        # Cost Matrices
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUAV:(T+1)*nUAV, -nUAV:(T+1)*nUAV] = self.P  # Not double-checked
        self.R_big  = np.kron(np.eye(T),   self.R)

        # Dynamics Matrices
        self.Phi = np.zeros(( (T+1)*nUAV, nUAV ))
        self.Lambda = np.zeros(( (T+1)*nUAV, T*mUAV ))
        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))

        for j in range(T+1):
            self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    np.linalg.matrix_power(self.A, j-k-1)*self.B
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.linalg.matrix_power(self.Ab, j-k-1)*self.Bb

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
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_0 = cp.Parameter((nUSV, 1))

        objectiveCent = cp.quad_form(self.x-self.xb, self.Q_big) \
            + cp.quad_form(self.u, self.R_big) \
            + cp.quad_form(self.ub, self.R_big)
        constraintsCent  = [ self.x  ==  self.Phi*self.x_0 \
            + self.Lambda*self.u ]
        constraintsCent += [ self.xb == self.Phi_b*self.xb_0 \
            + self.Lambda_b*self.ub ]
        constraintsCent += [self.u  <= self.params.amax]
        constraintsCent += [self.u  >= self.params.amin]
        constraintsCent += [self.ub <= self.params.amax_b]
        constraintsCent += [self.ub >= self.params.amin_b ]

        self.problemCent = cp.Problem(cp.Minimize(objectiveCent), constraintsCent)

    def solve(self, x_m, xb_m):
        self.x_0.value = x_m
        self.xb_0.value = xb_m

        self.problemCent.solve(solver=cp.OSQP, warm_start=True)
        self.t_since_update = 0

    def solve_threaded(self, x_m, xb_m):
        thread.start_new_thread(self.solve, (self, x_m, xb_m))

class UAVProblem():

    def __init__(self, T, A, B, Q, P, R, nUSV, params):
        self.T = T
        self.A = A
        self.B = B
        self.Q = Q
        self.P = P
        self.R = R
        self.nUSV = nUSV
        self.params = params
        [self.nUAV, self.mUAV] = B.shape
        self.create_optimisation_matrices()
        self.create_optimisation_problem()

    def create_optimisation_matrices(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV

        # Cost Matrices
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUAV:(T+1)*nUAV, -nUAV:(T+1)*nUAV] = self.P  # Not double-checked
        self.R_big  = np.kron(np.eye(T),   self.R)

        # Dynamics Matrices
        self.Phi = np.zeros(( (T+1)*nUAV, nUAV ))
        self.Lambda = np.zeros(( (T+1)*nUAV, T*mUAV ))

        for j in range(T+1):
            self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    np.linalg.matrix_power(self.A, j-k-1)*self.B

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        self.x  = cp.Variable(( nUAV*(T+1), 1 ))
        self.u  = cp.Variable(( mUAV*T, 1 ))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_hat = cp.Parameter(( nUSV*(T+1), 1 ))

        # TODO: FINISH FROM HERE!!!!

        objectiveCent = cp.quad_form(self.x-self.xb, self.Q_big) \
            + cp.quad_form(self.u, self.R_big) \
            + cp.quad_form(self.ub, self.R_big)
        constraintsCent  = [ self.x  ==  self.Phi*self.x_0 \
            + self.Lambda*self.u ]
        constraintsCent += [ self.xb == self.Phi_b*self.xb_0 \
            + self.Lambda_b*self.ub ]
        constraintsCent += [self.u  <= self.params.amax]
        constraintsCent += [self.u  >= self.params.amin]
        constraintsCent += [self.ub <= self.params.amax_b]
        constraintsCent += [self.ub >= self.params.amin_b ]

        self.problemCent = cp.Problem(cp.Minimize(objectiveCent), constraintsCent)

    def solve(self, x_m, xb_m):
        self.x_0.value = x_m
        self.xb_0.value = xb_m

        self.problemCent.solve(solver=cp.OSQP, warm_start=True)
        self.t_since_update = 0

    def solve_threaded(self, x_m, xb_m):
        thread.start_new_thread(self.solve, (self, x_m, xb_m))
