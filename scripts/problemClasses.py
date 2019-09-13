#!/usr/bin/env python
import sys
import rospy
from rendezvous_problem.srv import *
from rendezvous_problem.msg import Float32MultiArrayStamped
from std_msgs.msg import MultiArrayDimension
import rendezvous_problem       # For ROS srv
from helper_functions import shift_traj_msg, shift_trajectory, get_traj_dir, \
    get_cos_angle_between

import cvxpy as cp
import numpy as np
import scipy as sp
import osqp
from scipy.sparse import csc_matrix
import thread
import Queue
import time

# Supresses warning during division by 0. Division by zero will always occur
# in one of the functions, but it is correctly handled afterwards
# EDIT: Is this still true? TODO: Check it out
np.seterr(divide='ignore', invalid='ignore')

class CentralisedProblem():

    def __init__(self, T, A, B, Ab, Bb, Q, P, R, type, params):
        self.T = T
        self.A = A
        self.B = B
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.params = params
        self.type = type
        self.t_since_update = 100 # Arbitrary number larger than 0
        [self.nUAV, self.mUAV] = B.shape
        [self.nUSV, self.mUSV] = Bb.shape
        self.last_solution_duration = np.nan
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        if self.type == 'CVXGEN':
            self.ROS_init()

    def create_optimisation_matrices(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        params = self.params
        v_max = params.v_max

        # Cost Matrices
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUAV:(T+1)*nUAV, -nUAV:(T+1)*nUAV] = self.P  # Not double-checked
        self.R_big  = np.kron(np.eye(T),   self.R)

        # Dynamics Matrices
        self.Phi = np.zeros(( (T+1)*nUAV, nUAV ))
        self.Lambda = np.zeros(( (T+1)*nUAV, T*mUAV ))
        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))
        self.Phi_j = np.zeros(( (T+1)*nUAV, nUAV ))
        self.Lambda_j = np.zeros(( (T+1)*nUAV, T*mUAV ))

        J_mat = np.matrix([[0, 0, 1, 0], [0, 0, -1, 0],\
                           [0, 0, 0, 1], [0, 0, 0, -1]])

        temp_mat = np.matrix([[v_max],[-v_max],[v_max],[-v_max]])
        self.V_vec = np.kron( np.ones((T+1, 1)), temp_mat)

        for j in range(T+1):
            self.Phi[  j*nUAV:(j+1)*nUAV, :] = np.linalg.matrix_power(self.A, j)
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            self.Phi_j[j*nUSV:(j+1)*nUSV, :] = J_mat*np.linalg.matrix_power(self.A, j)

            for k in range(j):  # range(0) returns empty list
                self.Lambda[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    np.linalg.matrix_power(self.A, j-k-1)*self.B
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.linalg.matrix_power(self.Ab, j-k-1)*self.Bb
                self.Lambda_j[j*nUAV:(j+1)*nUAV, k*mUAV:(k+1)*mUAV] = \
                    J_mat*np.linalg.matrix_power(self.A, j-k-1)*self.B

        # ------------- OSQP Matrices --------------
        # Assumes nUAV = nUSV, mUAV = mUSV
        velocity_extractor = np.zeros(( 2*(T+1), nUAV*(T+1) ))
        for i in range(T+1):
            for j in range(2):
                velocity_extractor[ 2*i+j, nUAV*i+2+j ] = 1

        zeros = np.zeros((nUAV*(T+1), mUAV*T))
        zeros_sqr = np.zeros((mUAV*T, mUAV*T))
        zeros_tall = np.zeros((nUAV*(T+1), 1))
        zeros_short = np.zeros((mUAV*T, 1))
        self.C = np.full((1, 1), 10000*(T+1))
        P_temp = 2*np.bmat([
            [self.Q_big, zeros, -self.Q_big, zeros, zeros_tall],
            [zeros.T, self.R_big, zeros.T, zeros_sqr, zeros_short],
            [-self.Q_big, zeros, self.Q_big, zeros, zeros_tall],
            [zeros.T, zeros_sqr, zeros.T,  self.R_big, zeros_short],
            [zeros_tall.T, zeros_short.T, zeros_tall.T, zeros_short.T, self.C]
        ])
        # This matrix should be created straight from the dense counterpart,
        # because 1. the matrix is not diagonal, 2. it has a non-changing spartsity pattern
        self.P_OSQP = csc_matrix(P_temp)
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi, np.zeros((nUAV, 1)))],      # UAV Dynamics
            [np.full((T*mUAV, 1), params.amin)],          # UAV Input constraints
            [np.full((2*(T+1),   1), -params.v_max)],     # UAV Velocity constraints
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],    # USV Dynamics
            [np.full((T*mUSV, 1), params.amin_b)],        # USV Input constraints
            [np.full((2*(T+1),   1), -params.v_max_b)]    # USV Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi, np.zeros((nUAV, 1)))],      # UAV Dynamics
            [np.full((T*mUAV, 1), params.amax)],          # UAV Input constraints
            [np.full((2*(T+1),   1), params.v_max)],      # UAV Velocity constraints
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],    # USV Dynamics
            [np.full((T*mUSV, 1), params.amax_b)],        # USV Input constraints
            [np.full((2*(T+1),   1), -params.v_min_b)]    # USV Velocity constraints
        ])
        self.q_OSQP = 0
        A_temp_UAV = np.bmat([
            [np.eye(nUAV*(T+1)), -self.Lambda],                # Dynamics
            [np.zeros((T*mUAV, nUAV*(T+1))), np.eye(T*mUAV)],  # Input constraints
            [velocity_extractor, np.zeros((2*(T+1), T*mUAV))], # Velocity constraints
        ])
        A_temp_USV = np.bmat([
            [np.eye(nUSV*(T+1)), -self.Lambda_b, np.zeros( (nUSV*(T+1), 1) )],           # Dynamics
            [np.zeros((T*mUSV, nUSV*(T+1))), np.eye(T*mUSV), np.zeros( (T*mUSV, 1) )],   # Input constraints
            [velocity_extractor, np.zeros((2*(T+1), T*mUSV)), np.ones((2*(T+1), 1))],    # Velocity constraints
        ])
        zeros = np.zeros( (nUAV*(T+1) + mUAV*T + 2*(T+1), nUAV*(T+1) + mUAV*T) )
        # zeros = np.zeros( (nUAV*(T+1) + mUAV*T, nUAV*(T+1) + mUAV*T) )
        self.A_temp = np.bmat([
            [A_temp_UAV, zeros, np.zeros( (nUAV*(T+1) + T*mUAV + 2*(T+1), 1) )],
            [zeros, A_temp_USV]
        ])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        params = self.params
        self.x  = cp.Variable(( nUAV*(T+1), 1 ))
        self.xb = cp.Variable(( nUSV*(T+1), 1 ))
        self.u  = cp.Variable(( mUAV*T, 1 ))
        self.ub = cp.Variable(( mUSV*T, 1 ))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.s = cp.Variable((1, 1))

        objectiveCent = cp.quad_form(self.x-self.xb, self.Q_big) \
            + cp.quad_form(self.u, self.R_big) \
            + cp.quad_form(self.ub, self.R_big)
        constraintsCent  = [ self.x  ==  self.Phi*self.x_0 \
            + self.Lambda*self.u ]
        constraintsCent += [ self.xb == self.Phi_b*self.xb_0 \
            + self.Lambda_b*self.ub ]
        #constraintsCent += [self.Phi_j*self.x_0 + self.Lambda_j*self.u \
        #    <= self.V_vec]

        # COULD PROBABLY DELETE THIS, DOESN'T MAKE SENSE TO USE IT
        # Better approximation of true constraint set. Not worth computation.
        # constraintsCent += \
        #     [self.in_constr_matrix * self.u  <=  self.in_constr_vector]
        # constraintsCent += \
        #     [self.in_constr_matrix_b*self.ub <= self.in_constr_vector_b]

        # Multiplying it with square root of 0.5 makes it more conservative,
        # and bounds the admissible set within the true circular constraint set

        # Assumed mUAV = mUSV
        in_consr_matrix = np.bmat([[np.eye(mUAV*T)], [-np.eye(mUAV*T)]])
        constraintsCent += [in_consr_matrix*self.u  <= params.amax*np.sqrt(0.5)]    # TODO: Makes more sense to have amax
        constraintsCent += [in_consr_matrix*self.ub <= params.amax_b*np.sqrt(0.5)]  # already divided by sqrt(2)

        self.problemCent = cp.Problem(cp.Minimize(objectiveCent), constraintsCent)

        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 200)

    def ROS_init(self):
        print('Waiting for centralised problem solver')
        rospy.wait_for_service('centralised_problem')
        print('Finished waiting')
        self.service = rospy.ServiceProxy('centralised_problem', centralised_problem)

        x_0_msg = Float32MultiArrayStamped()
        x_0_msg.array.layout.dim.append(MultiArrayDimension())
        x_0_msg.array.layout.dim[0].size = self.nUAV
        x_0_msg.array.layout.dim[0].stride = 1
        x_0_msg.array.layout.dim[0].label = "x_0"
        self.x_0_msg = x_0_msg

        xb_0_msg = Float32MultiArrayStamped()
        xb_0_msg.array.layout.dim.append(MultiArrayDimension())
        xb_0_msg.array.layout.dim[0].size = self.nUAV
        xb_0_msg.array.layout.dim[0].stride = 1
        xb_0_msg.array.layout.dim[0].label = "xb_0"
        self.xb_0_msg = xb_0_msg

        self.req = centralised_problemRequest()

    def solve(self, x_m, xb_m):
        start = time.time()
        self.x_0.value = x_m
        self.xb_0.value = xb_m
        if self.type == 'CVXGEN':
            self.x_0_msg.array.data = np.asarray(x_m).flatten(order='F')   # TODO: Send in ndarray, then flatten will be enough
            self.xb_0_msg.array.data = np.asarray(xb_m).flatten(order='F') # TODO: Send in ndarray, then flatten will be enough
            self.req.x_0 = self.x_0_msg
            self.req.xb_0 = self.xb_0_msg
            resp = self.service(self.req)
            self.x.value = np.reshape(resp.x_traj.array.data,\
                (self.nUAV*(self.T+1), 1), order='F')
            self.xb.value = np.reshape(resp.xb_traj.array.data,\
                (self.nUSV*(self.T+1), 1), order='F')
            self.u.value = np.reshape(resp.u_traj.array.data,\
                (self.mUAV*self.T, 1), order='F')
            self.ub.value = np.reshape(resp.ub_traj.array.data,\
                (self.mUSV*self.T, 1), order='F')
        elif self.type == 'OSQP':
            self.update_OSQP(x_m, xb_m)
            results = self.problemOSQP.solve()
            T = self.T
            nUAV = self.nUAV
            mUAV = self.mUAV
            self.x.value = np.reshape(results.x[0:nUAV*(T+1)], (-1, 1))
            self.u.value = np.reshape(results.x[nUAV*(T+1):nUAV*(T+1)+mUAV*T], (-1, 1))
            self.xb.value = np.reshape(results.x[nUAV*(T+1)+mUAV*T:2*nUAV*(T+1)+mUAV*T], (-1, 1))
            self.ub.value = np.reshape(results.x[2*nUAV*(T+1)+mUAV*T:-1], (-1, 1))
            self.s.value = np.full((1,1), results.x[-1])
            # print results.info.status, results.info.iter, #DEBUG PRINT
            # if results.info.run_time > 0.01:
            #     print results.info.iter
            # else:
            #     print ""
        else:
            self.problemCent.solve(solver=cp.OSQP, warm_start=True, verbose=False)
        self.t_since_update = 0
        end = time.time()
        self.last_solution_duration = end - start

    def solve_threaded(self, x_m, xb_m):
        thread.start_new_thread(self.solve, (x_m, xb_m))

    def update_OSQP(self, x0, xb0):
        params = self.params
        T = self.T
        mUAV = self.mUAV
        mUSV = self.mUSV
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi, x0)],                       # UAV Dynamics
            [np.full((T*mUAV, 1), params.amin)],          # UAV Input constraints
            [np.full((2*(T+1),   1), -params.v_max)],     # UAV Velocity constraints
            [np.dot(self.Phi_b, xb0)],                    # USV Dynamics
            [np.full((T*mUSV, 1), params.amin_b)],        # USV Input constraints
            [np.full((2*(T+1),   1), -params.v_max_b)]    # USV Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi, x0)],                       # UAV Dynamics
            [np.full((T*mUAV, 1), params.amax)],          # UAV Input constraints
            [np.full((2*(T+1),   1), params.v_max)],      # UAV Velocity constraints
            [np.dot(self.Phi_b, xb0)],                    # USV Dynamics
            [np.full((T*mUSV, 1), params.amax_b)],        # USV Input constraints
            [np.full((2*(T+1),   1), -params.v_min_b)]    # USV Velocity constraints
        ])
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP)

class UAVProblem():

    def __init__(self, T, A, B, Q, P, R, nUSV, type, params):
        self.T = T
        self.A = A
        self.B = B
        self.Q = Q
        self.P = P
        self.R = R
        self.nUSV = nUSV
        self.type = type
        self.params = params
        # When problem is solved in parallel, this variable makes it easier to access solution duration
        self.last_solution_duration = np.nan
        [self.nUAV, self.mUAV] = B.shape
        self.t_since_update = 100 # Arbitrary number larger than 0
        self.t_since_prev_update = 0
        self.last_solution_is_used = False
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        if self.type == 'CVXGEN':
            self.ROS_init()

    def create_optimisation_matrices(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        params = self.params

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

        # ------------- OSQP Matrices --------------
        velocity_extractor = np.zeros(( 2*(T+1), nUAV*(T+1) ))
        for i in range(T+1):
            for j in range(2):
                velocity_extractor[ 2*i+j, nUAV*i+2+j ] = 1

        P_temp = 2*np.bmat([[self.Q_big, np.zeros((nUAV*(T+1), mUAV*T))],\
            [np.zeros((mUAV*T, nUAV*(T+1))), self.R_big]])
        P_data = np.diagonal(P_temp)
        P_row = range(nUAV*(T+1) + mUAV*T)
        P_col = range(nUAV*(T+1) + mUAV*T)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, np.zeros(( (T+1)*self.nUSV, 1 )) )],
            [np.zeros((T*mUAV, 1))]
        ])
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi, np.zeros((nUAV, 1)))],      # Dynamics
            [np.full((T*mUAV, 1), params.amin)],          # Input constraints
            [np.full((2*(T+1),   1), -params.v_max)]             # Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi, np.zeros((nUAV, 1)))],      # Dynamics
            [np.full((T*mUAV, 1), params.amax)],          # Input constraints
            [np.full((2*(T+1),   1), params.v_max)]              # Velocity constraints
        ])
        self.A_temp = np.bmat([
            [np.eye(nUAV*(T+1)), -self.Lambda],                # Dynamics
            [np.zeros((T*mUAV, nUAV*(T+1))), np.eye(T*mUAV)],  # Input constraints
            [velocity_extractor, np.zeros((2*(T+1), T*mUAV))], # Velocity constraints
        ])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        self.x  = cp.Variable(( nUAV*(T+1), 1 ))
        self.u  = cp.Variable(( mUAV*T, 1 ))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.xb_hat = cp.Parameter(( nUSV*(T+1), 1 ))

        objectiveUAV = cp.quad_form(self.x-self.xb_hat, self.Q_big) \
            + cp.quad_form(self.u, self.R_big)
        constraintsUAV  = [ self.x  ==  self.Phi*self.x_0 \
            + self.Lambda*self.u ]

        temp_matrix = np.bmat([[np.eye(mUAV*T)], [-np.eye(mUAV*T)]])
        constraintsUAV += [temp_matrix*self.u <= self.params.amax]
        # constraintsUAV += [self.u  <= self.params.amax]
        # constraintsUAV += [self.u  >= self.params.amin]

        self.problemUAV = cp.Problem(cp.Minimize(objectiveUAV), constraintsUAV)

        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 500)

    def ROS_init(self):
        print('Waiting for uav problem solver')
        rospy.wait_for_service('uav_problem')
        print('Finished waiting')
        self.service = rospy.ServiceProxy('uav_problem', UAV_problem)

        x_0_msg = Float32MultiArrayStamped()
        x_0_msg.array.layout.dim.append(MultiArrayDimension())
        x_0_msg.array.layout.dim[0].size = self.nUAV
        x_0_msg.array.layout.dim[0].stride = 1
        x_0_msg.array.layout.dim[0].label = "x_0"
        self.x_0_msg = x_0_msg

        xb_traj_msg = Float32MultiArrayStamped()
        xb_traj_msg.array.layout.dim.extend([MultiArrayDimension(),\
            MultiArrayDimension()])
        xb_traj_msg.array.layout.dim[0].size = self.T+1
        xb_traj_msg.array.layout.dim[0].stride = self.nUSV*(self.T+1)
        xb_traj_msg.array.layout.dim[0].label = "Time"
        xb_traj_msg.array.layout.dim[1].size = self.nUSV
        xb_traj_msg.array.layout.dim[1].stride = self.nUSV
        xb_traj_msg.array.layout.dim[1].label = "State element"
        self.xb_traj_msg = xb_traj_msg

        self.req = UAV_problemRequest()

    def solve(self, x_m, xbhat_m):
        start = time.time()
        self.x_0.value = x_m
        # print self.xb_hat.value.shape
        # print ( self.nUSV*(self.T+1), 1 )
        # print xbhat_m.shape
        self.xb_hat.value = xbhat_m

        if self.type == 'CVXGEN':
            self.x_0_msg.array.data = np.asarray(x_m).flatten(order='F')  # TODO: Send in ndarray, then flatten will be enough
            self.xb_traj_msg.array.data = xbhat_m.flatten(order='F')
            self.req.x_0 = self.x_0_msg
            self.req.xb_traj = self.xb_traj_msg
            resp = self.service(self.req)
            self.u.value = np.reshape(resp.u_traj.array.data, (-1, 1), order='F')
            self.x.value = np.reshape(resp.x_traj.array.data, (-1, 1), order='F' )
        elif self.type == 'OSQP':
            self.update_OSQP(x_m, xbhat_m)
            results = self.problemOSQP.solve()
            self.x.value = np.reshape(results.x[0:self.nUAV*(self.T+1)], (-1, 1))
            self.u.value = np.reshape(results.x[self.nUAV*(self.T+1):], (-1, 1))
        else:   # self.type == 'CVXPy'
            self.problemUAV.solve(solver=cp.OSQP, warm_start=True, verbose=False)
            if self.x.value is None:
                print "x was None, u was", self.u.value #DEBUG
                # Sometimes a bug occurs where the solution returns only None
                # In that case, apply no control input
                self.u.value = np.zeros((self.mUAV*self.T, 1))
                self.x.value = self.predict_trajectory(x_m, self.u.value)
            # print 'Solve exit'  #DEBUG


        self.t_since_prev_update = self.t_since_update
        self.t_since_update = 0
        self.last_solution_is_used = False
        end = time.time()
        self.last_solution_duration = end - start

    def solve_threaded(self, x_m, xb_m):
        thread.start_new_thread(self.solve, (x_m, xb_m))

    def predict_trajectory(self, x_0, u_traj):
        return np.dot(self.Phi, x_0) + np.dot(self.Lambda, u_traj)

    def update_OSQP(self, x0, xb_traj):
        params = self.params
        T = self.T
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi, x0)],                       # Dynamics
            [np.full((T*self.mUAV, 1), params.amin)],     # Input constraints
            [np.full((2*(T+1),   1), -params.v_max)]      # Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi, x0)],                      # Dynamics
            [np.full((T*self.mUAV, 1), params.amax)],    # Input constraints
            [np.full((2*(T+1),   1), params.v_max)]      # Velocity constraints
        ])
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, xb_traj )],
            [np.zeros((T*self.mUAV, 1))]
        ])
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q=self.q_OSQP)

class USVProblem():

    def __init__(self, T, Ab, Bb, Q, P, R, nUAV, type, params):
        self.T = T
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.nUAV = nUAV
        self.type = type
        self.params = params
        # When problem is solved in parallel, this variable makes it easier to access solution duration
        self.last_solution_duration = np.nan
        [self.nUSV, self.mUSV] = Bb.shape
        self.t_since_update = 100 # Arbitrary number larger than 0
        self.t_since_prev_update = 0
        self.last_solution_is_used = False
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        if type == 'CVXGEN':
            self.ROS_init()

    def create_optimisation_matrices(self):
        T = self.T
        nUAV = self.nUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        params = self.params

        # Cost Matrices
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = self.P  # Not double-checked
        self.Q_big_sparse = csc_matrix(self.Q_big)
        self.R_big  = np.kron(np.eye(T),   self.R)

        # Dynamics Matrices
        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))

        for j in range(T+1):
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.linalg.matrix_power(self.Ab, j-k-1)*self.Bb

        # ------------- OSQP Matrices --------------
        velocity_extractor = np.zeros(( 2*(T+1), nUSV*(T+1) ))
        for i in range(T+1):
            for j in range(2):
                velocity_extractor[ 2*i+j, nUSV*i+2+j ] = 1

        dim1 = nUSV*(T+1)
        dim2 = mUSV*T
        self.C = np.full((1,1), 10000*(T+1))
        P_temp = 2*np.bmat([[self.Q_big, np.zeros((dim1, dim2)), np.zeros((dim1, 1))],
            [np.zeros((dim2, dim1)), self.R_big, np.zeros((dim2, 1))],
            [np.zeros((1, dim1)), np.zeros((1, dim2)), self.C]
        ])
        P_data = np.diagonal(P_temp)
        P_row = range(nUSV*(T+1) + mUSV*T + 1)
        P_col = range(nUSV*(T+1) + mUSV*T + 1)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, np.zeros(( (T+1)*self.nUAV, 1 )) )],
            [np.zeros((T*mUSV+1, 1))]
        ])
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],      # Dynamics
            [np.full((T*mUSV, 1), params.amin_b)],          # Input constraints
            [np.full((2*(T+1),   1), -params.v_max_b)]      # Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi_b, np.zeros((nUSV, 1)))],      # Dynamics
            [np.full((T*mUSV, 1), params.amax_b)],        # Input constraints
            [np.full((2*(T+1),   1), -params.v_min_b)]      # Velocity constraints
        ])
        self.A_temp = np.bmat([
            [np.eye(nUSV*(T+1)), -self.Lambda_b, np.zeros((dim1, 1))],              # Dynamics
            [np.zeros((T*mUSV, nUSV*(T+1))), np.eye(dim2), np.zeros((dim2,1))],     # Input constraints
            [velocity_extractor, np.zeros((2*(T+1), dim2)), np.ones((2*(T+1), 1))], # Velocity constraints
        ])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        self.xb = cp.Variable(( nUSV*(T+1), 1 ))
        self.ub = cp.Variable(( mUSV*T, 1 ))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.x_hat  = cp.Parameter((nUAV*(T+1), 1))
        self.s  = cp.Parameter((1, 1))

        objectiveUSV = cp.quad_form(self.x_hat-self.xb, self.Q_big) \
            + cp.quad_form(self.ub, self.R_big)
        constraintsUSV = [ self.xb == self.Phi_b*self.xb_0 \
            + self.Lambda_b*self.ub ]
        temp_matrix = np.bmat([[np.eye(mUSV*T)], [-np.eye(mUSV*T)]])
        constraintsUSV += [temp_matrix*self.ub <= self.params.amax_b]
        # constraintsUSV += [self.ub <= self.params.amax_b]
        # constraintsUSV += [self.ub >= self.params.amin_b ]

        self.problemUSV = cp.Problem(cp.Minimize(objectiveUSV), constraintsUSV)

        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 500)

    def ROS_init(self):
        print('Waiting for usv problem solver')
        rospy.wait_for_service('usv_problem')
        print('Finished waiting')
        self.service = rospy.ServiceProxy('usv_problem', USV_problem)

        xb_0_msg = Float32MultiArrayStamped()
        xb_0_msg.array.layout.dim.append(MultiArrayDimension())
        xb_0_msg.array.layout.dim[0].size = self.nUSV
        xb_0_msg.array.layout.dim[0].stride = 1
        xb_0_msg.array.layout.dim[0].label = "xb_0"
        self.xb_0_msg = xb_0_msg

        x_traj_msg = Float32MultiArrayStamped()
        x_traj_msg.array.layout.dim.extend([MultiArrayDimension(),\
            MultiArrayDimension()])
        x_traj_msg.array.layout.dim[0].size = self.T+1
        x_traj_msg.array.layout.dim[0].stride = self.nUAV*(self.T+1)
        x_traj_msg.array.layout.dim[0].label = "Time"
        x_traj_msg.array.layout.dim[1].size = self.nUAV
        x_traj_msg.array.layout.dim[1].stride = self.nUAV
        x_traj_msg.array.layout.dim[1].label = "State element"
        self.x_traj_msg = x_traj_msg

        self.req = USV_problemRequest()

    def solve(self, xb_m, xhat_m, USV_should_stop = False):
        start = time.time()
        self.x_hat.value = xhat_m
        self.xb_0.value = xb_m
        # print xb_m[-2:]
        if USV_should_stop:
            self.ub.value = np.zeros((self.mUSV*self.T, 1))
            self.xb.value = self.predict_trajectory(xb_m, self.ub.value)
        elif self.type == 'CVXGEN':
            self.xb_0_msg.array.data = np.asarray(xb_m).flatten(order='F') # TODO: Send in ndarray, then flatten will be enough
            self.x_traj_msg.array.data = xhat_m.flatten(order='F')
            self.req.xb_0 = self.xb_0_msg
            self.req.x_traj = self.x_traj_msg
            resp = self.service(self.req)
            self.ub.value = np.reshape(resp.ub_traj.array.data, (-1, 1),\
                order='F')
            self.xb.value = np.reshape(resp.xb_traj.array.data, (-1, 1),\
                order='F' )
        elif self.type == 'OSQP':
            self.update_OSQP(xb_m, xhat_m)
            results = self.problemOSQP.solve()
            self.xb.value = np.reshape(results.x[0:self.nUSV*(self.T+1)], (-1, 1))
            self.ub.value = np.reshape(results.x[self.nUSV*(self.T+1):-1], (-1, 1))
            self.s.value  = np.full((1,1), results.x[-1])
        else:
            self.problemUSV.solve(solver=cp.OSQP, warm_start=True, verbose=False)
            if self.xb.value is None:
                # Sometimes a bug occurs where the solution returns only None
                # In that case, apply no control input
                self.ub.value = np.zeros((self.mUSV*self.T, 1))
                self.xb.value = self.predict_trajectory(xb_m, self.ub.value)
        self.t_since_prev_update = self.t_since_update
        self.t_since_update = 0
        self.last_solution_is_used = False
        end = time.time()
        self.last_solution_duration = end - start

    def solve_threaded(self, xb_m, x_hat, USV_should_stop = False):
        thread.start_new_thread(self.solve, (xb_m, x_hat, USV_should_stop))

    def predict_trajectory( self, xb_0, ub_traj):
        return np.dot(self.Phi_b, xb_0) + np.dot(self.Lambda_b, ub_traj)

    def update_OSQP(self, xb0, x_traj):
        params = self.params
        T = self.T
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi_b, xb0)],                      # Dynamics
            [np.full((T*self.mUSV, 1), params.amin_b)],     # Input constraints
            [np.full((2*(T+1),   1), -params.v_max_b)]      # Velocity constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi_b, xb0)],                     # Dynamics
            [np.full((T*self.mUSV, 1), params.amax_b)],    # Input constraints
            [np.full((2*(T+1),   1), -params.v_min_b)]     # Velocity constraints
        ])
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, x_traj )],
            [np.zeros((T*self.mUSV+1, 1))]
        ])

        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q=self.q_OSQP)

class VerticalProblem():

    def __init__(self, T, Av, Bv, Qv, Pv, Rv, type, params):
        self.T = T
        self.Av = Av
        self.Bv = Bv
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        self.type = type
        self.params = params
        self.nv = 2
        self.mv = 1
        self.t_since_update = 100 # Arbitrary number larger than 0
        self.t_since_prev_update = 0    # TODO: Us this used still?
        self.last_solution_is_used = False
        # When problem is solved in parallel, this variable makes it easier to access solution duration
        self.last_solution_duration = np.nan
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        self.durations = [] #DEBUG
        self.num_iters_log = [] #DEBUG
        self.obj_val = np.nan
        self.state_obj_val = np.nan
        self.input_obj_val = np.nan
        self.slack_obj_val = np.nan
        if type == 'CVXGEN':
            self.ROS_init()

    def create_optimisation_matrices(self):
        T = self.T
        nv = self.nv
        mv = self.mv
        params = self.params

        # Dynamics Matrices
        self.Phi_v = np.zeros(( (T+1)*nv, nv ))
        self.Lambda_v =  np.zeros(( (T+1)*nv, T*mv ))

        for j in range(T+1):
            self.Phi_v[ j*nv :(j+1)*nv,   :] = np.linalg.matrix_power(self.Av, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda_v[  j*nv:(j+1)*nv,    k*mv:(k+1)*mv   ] = \
                    np.linalg.matrix_power(self.Av, j-k-1)*self.Bv

        # Cost Matrices
        self.Qv_big = np.kron(np.eye(T+1), self.Qv)       # I haven't double-checked that this is correct
        self.Qv_big[-nv:(T+1)*nv, -nv:(T+1)*nv] = self.Pv
        self.Rv_big = np.kron(np.eye(T),   self.Rv)

        # Constraint Matrices
        height_extractor = np.zeros(( T+1, nv*(T+1) ))
        for i in range(T+1):
            height_extractor[ i, nv*i ] = 1
        self.height_extractor = height_extractor

        velocity_extractor = np.zeros(( T+1, nv*(T+1) ))
        for i in range(T+1):
            velocity_extractor[ i, nv*i+1 ] = 1

        touchdown_matrix = np.zeros(( T+1, nv*(T+1) ))
        for i in range(T+1):
            touchdown_matrix[ i, nv*i ] = params.kl
            touchdown_matrix[ i, nv*i+1 ] = 1

        # Constraints appear in the following row order:
        # * Max velocity constraints
        # * Min velocity constraints
        # * Touchdown constraints
        # * Altitude constraints (height greater than 0)
        self.vert_constraints_matrix = np.bmat([\
            [velocity_extractor],\
            [-velocity_extractor],\
            [-touchdown_matrix],\
            [-height_extractor],\
        ])

        self.vert_constraints_vector = np.bmat([\
            [ params.wmax*np.ones((T+1, 1))],\
            [-params.wmin*np.ones((T+1, 1))],\
            [-params.wmin_land*np.ones((T+1, 1))], \
            [np.zeros((T+1, 1))],\
        ])

        # This matrix is separate from vert_constraints_matrix
        # since the constraints here depend on the distance,
        # which is a parameter and makes it impossible
        # to pre-compute the LHS of the constraints
        self.safety_matrix = np.bmat([\
            [(params.dl-params.ds)*height_extractor],\
            [(params.dl-params.ds)*height_extractor],\
        ])

        # ------------- OSQP Matrices --------------
        self.C = 10000*(T+1)
        P_temp = 2*np.bmat([[self.Qv_big, np.zeros((nv*(T+1), mv*T+1))],\
            [np.zeros((mv*T, nv*(T+1))), self.Rv_big, np.zeros((mv*T, 1)) ],\
            [np.zeros(( 1, nv*(T+1)+mv*T )), np.full((1,1), self.C) ]])
        P_data = np.diagonal(P_temp)
        P_row = range(nv*(T+1) + mv*T + 1)
        P_col = range(nv*(T+1) + mv*T + 1)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        self.q_OSQP = 0
        # Honestly, I can't quite remember wth I was doing here, remade it below
        # self.l_OSQP = np.bmat([[np.dot(self.Phi_v,np.zeros((nv, 1)))],\
        #     [np.full((4*(T+1), 1), -np.inf)],\
        #     [params.wmin*np.ones((mv*T, 1))]] )
        # self.u_OSQP = np.bmat([[np.dot(self.Phi_v,np.zeros((nv, 1)))],\
        #     [self.vert_constraints_vector],\
        #     [params.wmax*np.ones((mv*T, 1))]] )
        # A_temp = np.bmat([\
        #     [np.eye(nv*(T+1)), -self.Lambda_v],\
        #     [self.vert_constraints_matrix, np.zeros((4*(T+1), mv*T))],\
        #     [np.zeros((mv*T, nv*(T+1))), np.eye(mv*T)]
        #     ])
        # self.A_OSQP = csc_matrix(A_temp)
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi_v, np.zeros((nv, 1)))],    # Dynamics
            [np.dot(params.wmin,np.ones((2*T+1, 1)))],  # Velocity and input constraints
            [np.dot(params.wmin_land,np.ones((T+1, 1)))], # Touchdown constraints
            [np.zeros((T+1, 1))],                        # Altitude constraints
            [-np.full((T+1,1), np.inf)]                  # Safety constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi_v, np.zeros((nv, 1)))],      # Dynamics
            [np.full((T+1, 1), np.inf)],                  # Velocity constraints
            [np.full((T,   1), params.wmax)],             # Input constraints
            [np.full((T+1, 1), np.inf)],                  # Touchdown constraints
            [np.full((T+1, 1), np.inf)],                  # Altitude constraints
            [-np.dot(params.hs,np.zeros((T+1, 1))) + \
                np.dot(params.hs*params.dl, np.ones((T+1, 1)))] # Safety constraints
        ])
        # INCLUDES SOFT CONSTRAINTS
        self.A_temp = np.bmat([
            [np.eye(nv*(T+1)), -self.Lambda_v, np.zeros((nv*(T+1), 1))],        # Dynamics
            [velocity_extractor, np.zeros((T+1, T)), np.ones((T+1, 1))],   # Velocity constraints
            [np.zeros((T, nv*(T+1))), np.eye(T), np.ones((T, 1))],      # Input constraints
            [velocity_extractor + np.dot(params.kl,height_extractor),\
                np.zeros((T+1, T)), np.ones((T+1, 1))],                    # Touchdown constraints
            [height_extractor, np.zeros((T+1, T)), np.zeros((T+1, 1))],    # Altitude constraints
            [np.dot(params.dl-params.ds,height_extractor),\
                np.zeros((T+1, T)), np.zeros((T+1, 1))]                    # Safety constraints
        ])
        # DOES NOT INCLUDE SOFT CONSTRAINTS
        # self.A_temp = np.bmat([
        #     [np.eye(nv*(T+1)), -self.Lambda_v, np.zeros((nv*(T+1), 1))],        # Dynamics
        #     [velocity_extractor, np.zeros((T+1, T)), np.zeros((T+1, 1))],   # Velocity constraints
        #     [np.zeros((T, nv*(T+1))), np.eye(T), np.zeros((T, 1))],      # Input constraints
        #     [velocity_extractor + np.dot(params.kl,height_extractor),\
        #         np.zeros((T+1, T)), np.zeros((T+1, 1))],                    # Touchdown constraints
        #     [height_extractor, np.zeros((T+1, T)), np.zeros((T+1, 1))],    # Altitude constraints
        #     [np.dot(params.dl-params.ds,height_extractor),\
        #         np.zeros((T+1, T)), np.zeros((T+1, 1))]                    # Safety constraints
        # ])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nv = self.nv
        params = self.params
        self.xv = cp.Variable(( nv*(T+1), 1 ))
        self.wdes = cp.Variable(( T, 1 ))
        self.s = cp.Variable((1, 1))
        self.xb_v = cp.Parameter(( nv*(T+1), 1 ))
        self.xv_0 = cp.Parameter(( nv, 1 ))
        self.dist = cp.Parameter(( T+1, 1 ))
        self.b  = cp.Parameter(( T+1,  1))  # True if within landing distance
        self.b2 = cp.Parameter(( nv*(T+1),  ))

        safe_states_extractor = cp.diag( self.b2 )
        self.safe_states_extractor = safe_states_extractor  #DEBUG
        objectiveVert = cp.quad_form(self.wdes, self.Rv_big) +\
            cp.quad_form(safe_states_extractor*(self.xv-self.xb_v), self.Qv_big)
        # Dynamics constraint
        constraintsVert = [self.xv == self.Phi_v*self.xv_0 \
            + self.Lambda_v*self.wdes]
        # Velocity constraints, above 0-constraint, and touchdown constraints
        constraintsVert += [self.vert_constraints_matrix*self.xv \
            <= self.vert_constraints_vector]
        # Input constraints
        constraintsVert += [params.wmin <= self.wdes, self.wdes <= params.wmax]

        # Safety constraints
        constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
            <= cp.diag(self.b)*(params.hs*params.dl - params.hs*self.dist)]
        # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
        #     <= cp.diag(self.b)*(params.hs*params.dl + params.hs*self.dist)]
        # Safe height constraints
        constraintsVert += [-self.height_extractor*self.xv \
            <= -params.hs*(np.ones(( T+1, 1 )) - self.b)]

        # # RIDICULOUS DEBUG!!!!
        # new_mat = np.bmat([[self.vert_constraints_matrix, np.zeros((4*(T+1),T))], \
        #     [np.zeros((T, 2*(T+1))),  np.eye(T)],\
        #     [np.zeros((T, 2*(T+1))), -np.eye(T)]])
        # new_vec = np.bmat([[self.vert_constraints_vector],\
        #     [params.wmax*np.ones((T,1))],\
        #     [-params.wmin*np.ones((T,1))]])
        # constraintsVert += [new_mat*cp.bmat([[self.xv],[self.wdes]]) <= new_vec]

        self.problemVert = \
            cp.Problem(cp.Minimize(objectiveVert), constraintsVert)

        # max_iter = 400 if self.PARALLEL else 200
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 300)

    def ROS_init(self):
        if self.T == 100:
            print('Waiting for ultra-long vertical problem solver')
            rospy.wait_for_service('vertical_problem_ulong')
            print('Finished waiting')
            self.service = rospy.ServiceProxy('vertical_problem_ulong',\
                vertical_problem)
        elif self.T == 45:
            print('Waiting for long vertical problem solver')
            rospy.wait_for_service('vertical_problem_long')
            print('Finished waiting')
            self.service = rospy.ServiceProxy('vertical_problem_long',\
                vertical_problem)
        elif self.T == 25:
            print('Waiting for vertical problem solver')
            rospy.wait_for_service('vertical_problem')
            print('Finished waiting')
            self.service = rospy.ServiceProxy('vertical_problem',\
                vertical_problem)
        else:
            raise ValueError('The chosen prediction horizon T='+str(self.T)+\
                ' is not supported by any of the CVXGEN-solvers')

        xv_0_msg = Float32MultiArrayStamped()
        xv_0_msg.array.layout.dim.append(MultiArrayDimension())
        xv_0_msg.array.layout.dim[0].size = self.nv
        xv_0_msg.array.layout.dim[0].stride = 1
        xv_0_msg.array.layout.dim[0].label = "xv_0"
        self.xv_0_msg = xv_0_msg

        xbv_msg = Float32MultiArrayStamped()
        xbv_msg.array.layout.dim.append(MultiArrayDimension())
        xbv_msg.array.layout.dim[0].size = self.nv
        xbv_msg.array.layout.dim[0].stride = 1
        xbv_msg.array.layout.dim[0].label = "xb"
        # xbv_msg.data = [0.0, 0.0];
        self.xbv_msg = xbv_msg

        dist_traj_msg = Float32MultiArrayStamped()
        dist_traj_msg.array.layout.dim.append(MultiArrayDimension())
        dist_traj_msg.array.layout.dim[0].size = self.T+1
        dist_traj_msg.array.layout.dim[0].stride = self.T+1
        dist_traj_msg.array.layout.dim[0].label = "Time"
        self.dist_traj_msg = dist_traj_msg

        self.req = vertical_problemRequest()

    def solve(self, xv_m, xbv_m, dist):
        start = time.time()
        T = self.T
        nv = self.nv
        # TODO: Rename xv_m to just xv, or xv_0?
        self.xv_0.value = xv_m
        # USV vertical state assumed constant
        self.xb_v.value = np.ones((nv*(T+1), 1))*xbv_m
        self.dist.value = dist
        self.b.value = (dist <= self.params.ds).astype(int)
        # Each element in the binary vector is repeated twice,
        # since the vertical state has dimension 2. It is stored as an 1D-array
        # so that it can be used with cp.diag later on
        self.b2.value =  np.ravel( np.kron( self.b.value, np.ones((2, 1)))  )
        if self.type == 'CVXGEN':
            self.xv_0_msg.array.data = np.asarray(xv_m).flatten(order='F')  # TODO: Send in ndarray, then remove asarray
            self.xbv_msg.array.data = [xbv_m, 0.0]#*self.T  # For some reason I only send in a scalar for xbv_m...
            self.dist_traj_msg.array.data = dist.flatten(order='F')
            self.req.xv_0 = self.xv_0_msg
            self.req.xbv = self.xbv_msg
            self.req.dist_traj = self.dist_traj_msg
            resp = self.service(self.req)
            self.wdes.value = np.reshape(resp.wdes_traj.array.data, (self.T, 1),\
                order='F')
            self.xv.value = np.reshape(resp.xv_traj.array.data, \
                (self.nv*(self.T+1), 1), order='F')
        elif self.type == 'OSQP':
            start = time.time()
            self.update_OSQP(xv_m, dist, self.b.value)
            results = self.problemOSQP.solve()
            if results.x[0] is not None:
                self.xv.value = np.reshape(results.x[0:self.nv*(self.T+1)], (-1, 1))
                self.wdes.value = np.reshape(results.x[self.nv*(self.T+1):-1], (-1, 1))
                self.s.value  = np.full((1,1), results.x[-1])
                self.obj_val = results.info.obj_val
                # print self.s.value[0,0], self.obj_val
                # print results.info.iter # DEBUG PRINT
                # print self.xv.value[-2]
                # #DEBUG
                # print "CONSTRAINT SATISFACTION:"
                # self.print_constraints_satisfied(self.xv.value, self.wdes.value)
            else:
                # Optimisation failed
                print "STATUS:", results.info.status
                # Using np.full() doesn't seem to work, since "variables must be
                # real". Using this approach seems to circumvent that limitation
                # np.zeros() is used instead of np.empty() since np.empty()
                # sometimes contains non-real values, causing an exception
                self.wdes.value = np.zeros((self.T, 1))
                self.wdes.value.fill(np.nan)
                self.xv.value = np.zeros(((self.T+1)*self.nv, 1))
                self.xv.value.fill(np.nan)
            duration = time.time() - start
            self.num_iters_log.append(results.info.iter)
            self.durations.append(duration)
        else:   # self.type == 'CVXPY'
            try:
                start = time.time()
                self.problemVert.solve(solver=cp.OSQP, warm_start=False, verbose=False, max_iter = 5000)
                duration = time.time() - start
                stats = self.problemVert.solver_stats
                self.num_iters_log.append(stats.num_iters)
                self.durations.append(duration)
                # #DEBUG
                # print "CONSTRAINT SATISFACTION CVXPY:"
                # self.print_constraints_satisfied(self.xv.value, self.wdes.value)
            except cp.error.SolverError as e:
                print "Vertical problem:"
                print e
                # Using np.full() doesn't seem to work, since "variables must be
                # real". Using this approach seems to circumvent that limitation
                # np.zeros() is used instead of np.empty() since np.empty()
                # sometimes contains non-real values, causing an exception
                self.wdes.value = np.zeros((self.T, 1))
                self.wdes.value.fill(np.nan)
                self.xv.value = np.zeros( (self.nv*(self.T+1), 1))
                self.xv.value.fill(np.nan)
            # Exception is not thrown in problem was unbounded or infeasible
            if self.problemVert.status == 'unbounded' or\
                self.problemVert.status == 'infeasible':
                print "Vertical problem: Problem was unbounded or infeasible"
                # Using np.full() doesn't seem to work, since "variables must be
                # real". Using this approach seems to circumvent that limitation
                # np.zeros() is used instead of np.empty() since np.empty()
                # sometimes contains non-real values, causing an exception
                self.wdes.value = np.zeros((self.T, 1))
                self.wdes.value.fill(np.nan)
                self.xv.value = np.zeros( (self.nv*(self.T+1), 1))
                self.xv.value.fill(np.nan)

        self.t_since_prev_update = self.t_since_update
        self.t_since_update = 0
        self.last_solution_is_used = False
        end = time.time()
        self.last_solution_duration = end - start
        # # DEBUG DEBUG DEBUG DEBUG
        # params = self.params
        # SCLHS = (params.dl-params.ds)*np.dot(self.height_extractor,self.xv.value)
        # SCRHS = np.dot( np.diagflat(self.b.value), (np.reshape(params.hs*params.dl, (1, 1)) - params.hs*dist))
        # SHLHS = np.dot(self.height_extractor, self.xv.value)
        # SHRHS = params.hs*(np.ones(( T+1, 1 )) - self.b.value)
        # # print(SCLHS <= SCRHS)
        # print('--------')
        # print(SHLHS-SHRHS)
        # Safety constraints
        # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
        #     <= cp.diag(self.b)*(params.hs*params.dl - params.hs*self.dist)]

        # Safe height constraints
        # constraintsVert += [self.height_extractor*self.xv \
        #     >= params.hs*(np.ones(( T+1, 1 )) - self.b)]

    def solve_threaded(self, xv_m, xbv_m, dist):
        thread.start_new_thread(self.solve, (xv_m, xbv_m, dist))

    def predict_trajectory(self, xv_0, wdes_traj):
        return np.dot(self.Phi_v, xv_0) + np.dot(self.Lambda_v, wdes_traj)

    def update_OSQP(self, x0, dist_traj, binary_traj):
        b1 = np.diag(np.ravel(binary_traj))
        b2 = np.diag(np.ravel( np.kron( binary_traj, np.ones((2, 1)))  ))
        params = self.params
        T = self.T
        self.l_OSQP = np.bmat([
            [np.dot(self.Phi_v, x0)],             # Dynamics
            [np.dot(params.wmin,np.ones((2*T+1, 1)))],# Velocity and input constraints
            [np.dot(params.wmin_land,np.ones((T+1, 1)))], # Touchdown constraints
            [np.dot( (np.eye(T+1)-b1), np.full((T+1,1), params.hs) ) ], # Altitude constraints
            [-np.full((T+1, 1), np.inf)]            # Safety constraints
        ])
        self.u_OSQP = np.bmat([
            [np.dot(self.Phi_v, x0)],                     # Dynamics
            [np.full((T+1, 1), np.inf)],                  # Velocity constraints
            [np.full((T,   1), params.wmax)],             # Input constraints
            [np.full((T+1, 1), np.inf)],                  # Touchdown constraints
            [np.full((T+1, 1), np.inf)],                  # Altitude constraints
            [-np.dot(params.hs, np.dot(b1, dist_traj)) + \
                np.dot(params.hs*params.dl,np.ones((T+1, 1)))]# Safety constraints
        ])
        P_temp = 2*np.bmat([[np.dot(b2, self.Qv_big),\
                np.zeros((self.nv*(self.T+1), self.mv*(self.T+1)))],\
            [np.zeros((self.mv*self.T, self.nv*(self.T+1))), self.Rv_big,\
                np.zeros((self.mv*self.T, 1))],\
            [np.zeros(( 1, self.nv*(self.T+1)+self.mv*self.T )),\
                np.full((1,1), self.C) ]])
        P_data = np.diagonal(P_temp)
        # print P_data.shape
        # P is 225x225. Shouldn't there be just as many elements?
        # Or has setting some to zero during the first definition messed something up?

        # P_row = range(self.nv*(self.T+1) + self.mv*self.T)
        # P_col = range(self.nv*(self.T+1) + self.mv*self.T)
        # P_new = csc_matrix((P_data, (P_row, P_col)))
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP)
        self.problemOSQP.update(Px=P_data)

    # DEBUG: Checks if a solution satisfies all constraints
    def print_constraints_satisfied(self, xv_traj, uv_traj):
        # I'm not sure if this one works, it always seems to show that constraints
        # are violated, even when I think they're not
        vec = np.bmat([[xv_traj],[uv_traj]])
        lower = self.l_OSQP <= np.dot(self.A_temp, vec)
        upper = np.dot(self.A_temp, vec) <= self.u_OSQP
        # Get indices of rows where constraints where violated
        lower_violations = np.where(lower == False)[0]
        upper_violations = np.where(upper == False)[0]
        dynamics_violations_l = 0
        dynamics_violations_u = 0
        velocity_violations_l = 0
        velocity_violations_u = 0
        input_violations_l = 0
        input_violations_u = 0
        touchdown_violations_l = 0
        touchdown_violations_u = 0
        altitude_violations_l = 0
        altitude_violations_u = 0
        safety_violations_l = 0
        safety_violations_u = 0

        n = self.nv
        T = self.T

        for index in lower_violations:
            if index < n*(T+1):
                dynamics_violations_l += 1
            elif index < (n+1)*(T+1):
                velocity_violations_l += 1
            elif index < (n+1)*(T+1) + T:
                input_violations_l += 1
            elif index < (n+3)*(T+1):
                touchdown_violations_l += 1
            elif index < (n+4)*(T+1):
                altitude_violations_l += 1
            elif index < (n+5)*(T+1):
                safety_violations_l += 1

        for index in upper_violations:
            if index < n*(T+1):
                dynamics_violations_u += 1
            elif index < (n+1)*(T+1):
                velocity_violations_u += 1
            elif index < (n+1)*(T+1) + T:
                input_violations_u += 1
            elif index < (n+3)*(T+1):
                touchdown_violations_u += 1
            elif index < (n+4)*(T+1):
                altitude_violations_u += 1
            elif index < (n+5)*(T+1):
                safety_violations_u += 1

        print "Violated", dynamics_violations_l, "lower and", dynamics_violations_u, "upper dynamics constraints"
        print "Violated", velocity_violations_l, "lower and", velocity_violations_u, "upper velocity constraints"
        print "Violated", input_violations_l, "lower and", input_violations_u, "upper input constraints"
        print "Violated", touchdown_violations_l, "lower and", touchdown_violations_u, "upper touchdown constraints"
        print "Violated", altitude_violations_l, "lower and", altitude_violations_u, "upper altitude constraints"
        print "Violated", safety_violations_l, "lower and", safety_violations_u, "upper safety constraints"
        # print sum( lower ), 'of', self.A_temp.shape[0], 'satisfied'
        # print sum( upper ), 'of', self.A_temp.shape[0], 'satisfied'

# Problem where only constraints are dynamics and input saturation (maybe)
# (no safety constraints).
class FastUAVProblem():

    def __init__(self, T, A, B, Q, P, R, type, params):
        self.T = T
        self.A = A
        self.B = B
        self.Q = Q
        self.P = P
        self.R = R
        self.type = type
        self.params = params
        self.last_solution_duration = np.nan
        [self.nUAV, self.mUAV] = B.shape
        # self.t_since_update = 0
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

        # ------------------ OSQP Matrices ------------------

        P_temp = 2*np.bmat([[self.Q_big, np.zeros(((T+1)*nUAV, T*mUAV))],
            [np.zeros((T*mUAV, (T+1)*nUAV,)), self.R_big]
        ])

        P_data = np.diagonal(P_temp)
        P_row = range(nUAV*(T+1) + mUAV*T)
        P_col = range(nUAV*(T+1) + mUAV*T)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, np.zeros(( (T+1)*self.nUAV, 1 )) )],
            [np.zeros((T*mUAV, 1))]
        ])
        self.l_OSQP = np.dot(self.Phi, np.zeros((nUAV, 1)))
        self.u_OSQP = np.dot(self.Phi, np.zeros((nUAV, 1)))
        self.A_temp = np.bmat([[np.eye(nUAV*(T+1)), -self.Lambda]])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nUAV = self.nUAV
        mUAV = self.mUAV
        self.x  = cp.Variable(( nUAV*(T+1), 1 ))
        self.u  = cp.Variable(( mUAV*T, 1 ))
        self.x_0  = cp.Parameter((nUAV, 1))
        self.x_des = cp.Parameter(( nUAV*(T+1), 1 ))

        objectiveUAV = cp.quad_form(self.x-self.x_des, self.Q_big) \
            + cp.quad_form(self.u, self.R_big)
        constraintsUAV  = [ self.x  ==  self.Phi*self.x_0 \
            + self.Lambda*self.u ]

        # TODO: Do we really need saturation constraints? Can't we expect the
        # optimal control inputs to be feasible, since the desired trajectory
        # was designed using feasible control inputs?
        # Try it out, I guess
        temp_matrix = np.bmat([[np.eye(mUAV*T)], [-np.eye(mUAV*T)]])
        constraintsUAV += [temp_matrix*self.u <= self.params.amax]
        # constraintsUAV += [self.u  <= self.params.amax]
        # constraintsUAV += [self.u  >= self.params.amin]

        self.problemUAV = cp.Problem(cp.Minimize(objectiveUAV), constraintsUAV)
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 500)

    def solve(self, x_m, x_des_m):
        start = time.time()
        self.x_0.value = x_m
        self.x_des.value = x_des_m

        if self.type == 'CVXPy':
            self.problemUAV.solve(solver=cp.OSQP, warm_start=True, verbose=False)
        elif self.type == 'OSQP':
            self.update_OSQP(x_m, x_des_m)
            results = self.problemOSQP.solve()
            self.x.value = np.reshape(results.x[0:self.nUAV*(self.T+1)], (-1, 1))
            self.u.value = np.reshape(results.x[self.nUAV*(self.T+1):], (-1, 1))

        # EDIT: I'm not sure this ever happens anymore
        if self.x.value is None:
            print "x was None, u was", self.u.value #DEBUG
            # Sometimes a bug occurs where the solution returns only None
            # In that case, apply no control input
            self.u.value = np.zeros((self.mUAV*self.T, 1))
            self.x.value = self.predict_trajectory(x_m, self.u.value)

        end = time.time()
        self.last_solution_duration = end - start

    def update_OSQP(self, x0, x_des):
        self.l_OSQP = np.dot(self.Phi, x0)
        self.u_OSQP = np.dot(self.Phi, x0)
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, x_des )],
            [np.zeros((self.T*self.mUAV, 1))]
        ])
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q=self.q_OSQP)

# DO WE REALLY NEED TO INCLUDE INPUT IN COST FUNCTION? PROBABLY FOR GOOD MEASURE

class FastUSVProblem():

    def __init__(self, T, Ab, Bb, Q, P, R, type, params):
        self.T = T
        self.Ab = Ab
        self.Bb = Bb
        self.Q = Q
        self.P = P
        self.R = R
        self.type = type
        self.params = params
        self.last_solution_duration = np.nan # Most recent time taken to solve problem
        [self.nUSV, self.mUSV] = Bb.shape
        self.create_optimisation_matrices()
        self.create_optimisation_problem()

    def create_optimisation_matrices(self):
        T = self.T
        nUSV = self.nUSV
        mUSV = self.mUSV

        # Cost Matrices
        self.Q_big  = np.kron(np.eye(T+1), self.Q)
        self.Q_big[-nUSV:(T+1)*nUSV, -nUSV:(T+1)*nUSV] = self.P  # Not double-checked
        self.Q_big_sparse = csc_matrix(self.Q_big)
        self.R_big  = np.kron(np.eye(T),   self.R)

        # Dynamics Matrices
        self.Phi_b = np.zeros(( (T+1)*nUSV, nUSV ))
        self.Lambda_b = np.zeros(( (T+1)*nUSV, T*mUSV ))

        for j in range(T+1):
            self.Phi_b[j*nUSV:(j+1)*nUSV, :] = np.linalg.matrix_power(self.Ab, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda_b[j*nUSV:(j+1)*nUSV, k*mUSV:(k+1)*mUSV] = \
                    np.linalg.matrix_power(self.Ab, j-k-1)*self.Bb

        # ------------------ OSQP Matrices ------------------

        P_temp = 2*np.bmat([[self.Q_big, np.zeros(((T+1)*nUSV, T*mUSV))],
            [np.zeros((T*mUSV, (T+1)*nUSV,)), self.R_big]
        ])
        P_data = np.diagonal(P_temp)
        P_row = range(nUSV*(T+1) + mUSV*T)
        P_col = range(nUSV*(T+1) + mUSV*T)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        self.q_OSQP = -2*np.bmat([
            [np.dot( self.Q_big, np.zeros(( (T+1)*self.nUSV, 1 )) )],
            [np.zeros((T*mUSV, 1))]
        ])
        self.l_OSQP = np.dot(self.Phi_b, np.zeros((nUSV, 1)))
        self.u_OSQP = np.dot(self.Phi_b, np.zeros((nUSV, 1)))
        self.A_temp = np.bmat([[np.eye(nUSV*(T+1)), -self.Lambda_b]])
        self.A_OSQP = csc_matrix(self.A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nUSV = self.nUSV
        mUSV = self.mUSV
        self.xb = cp.Variable(( nUSV*(T+1), 1 ))
        self.ub = cp.Variable(( mUSV*T, 1 ))
        self.xb_0 = cp.Parameter((nUSV, 1))
        self.xb_des  = cp.Parameter((nUSV*(T+1), 1))

        objectiveUSV = cp.quad_form(self.xb_des-self.xb, self.Q_big) \
            + cp.quad_form(self.ub, self.R_big)
        constraintsUSV = [ self.xb == self.Phi_b*self.xb_0 \
            + self.Lambda_b*self.ub ]
        # MAYBE NOT NECESSARY, I'M NOT SURE
        temp_matrix = np.bmat([[np.eye(mUSV*T)], [-np.eye(mUSV*T)]])
        constraintsUSV += [temp_matrix*self.ub <= self.params.amax_b]
        # constraintsUSV += [self.ub <= self.params.amax_b]
        # constraintsUSV += [self.ub >= self.params.amin_b ]

        self.problemUSV = cp.Problem(cp.Minimize(objectiveUSV), constraintsUSV)
        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 500)

    def solve(self, xb_m, xb_des_m, USV_should_stop = False):
        start = time.time()
        # print self.x_hat.value.shape
        # print (self.nUAV*(self.T+1), 1)
        # print xhat_m.shape
        self.xb_des.value = xb_des_m
        self.xb_0.value = xb_m
        if USV_should_stop:
            self.ub.value = np.zeros((self.mUSV*self.T, 1))
            self.xb.value = self.predict_trajectory(xb_m, self.ub.value)
        elif self.type == 'CVXPy':
            self.problemUSV.solve(solver=cp.OSQP, warm_start=True, verbose=False)
        elif self.type == 'OSQP':
            # start1 = time.time()
            self.update_OSQP(xb_m, xb_des_m)
            # start2 = time.time()
            results = self.problemOSQP.solve()
            self.xb.value = np.reshape(results.x[0:self.nUSV*(self.T+1)], (-1, 1))
            self.ub.value = np.reshape(results.x[self.nUSV*(self.T+1):], (-1, 1))

        # EDIT: I'm not sure this happens anymore
        if self.xb.value is None:
            # Sometimes a bug occurs where the solution returns only None
            # In that case, apply no control input
            self.ub.value = np.zeros((self.mUSV*self.T, 1))
            self.xb.value = self.predict_trajectory(xb_m, self.ub.value)

        end = time.time()
        self.last_solution_duration = end - start

    def predict_trajectory( self, xb_0, ub_traj):
        return np.dot(self.Phi_b, xb_0) + np.dot(self.Lambda_b, ub_traj)

    def update_OSQP(self, xb0, xb_des):
        self.l_OSQP = np.dot(self.Phi_b, xb0)
        self.u_OSQP = np.dot(self.Phi_b, xb0)
        # temp = -2*np.dot( self.Q_big, xb_des )
        # print self.xb_des.shape
        # print self.Q_big_sparse.dot(-2*xb_des.T).toarray().shape
        self.q_OSQP = np.block([[self.Q_big_sparse.dot(-2*xb_des)],\
            [np.zeros((self.T*self.mUSV, 1))]])
        # np.put(self.q_OSQP, range(self.nUSV*(self.T+1)), self.Q_big_sparse.multiply(-2*xb_des).toarray())
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q=self.q_OSQP)

class FastVerticalProblem():

    def __init__(self, T, Av, Bv, Qv, Pv, Rv, type, params):
        self.T = T
        self.Av = Av
        self.Bv = Bv
        self.Qv = Qv
        self.Pv = Pv
        self.Rv = Rv
        self.type = type
        self.params = params
        self.nv = 2
        self.mv = 1
        self.t_since_update = 100 # Arbitrary number larger than 0
        self.last_solution_duration = np.nan
        self.create_optimisation_matrices()
        self.create_optimisation_problem()
        self.durations = [] #DEBUG
        self.num_iters_log = [] #DEBUG

    def create_optimisation_matrices(self):
        T = self.T
        nv = self.nv
        mv = self.mv
        params = self.params

        # Dynamics Matrices
        self.Phi_v = np.zeros(( (T+1)*nv, nv ))
        self.Lambda_v =  np.zeros(( (T+1)*nv, T*mv ))

        for j in range(T+1):
            self.Phi_v[ j*nv :(j+1)*nv,   :] = np.linalg.matrix_power(self.Av, j)
            for k in range(j):  # range(0) returns empty list
                self.Lambda_v[  j*nv:(j+1)*nv,    k*mv:(k+1)*mv   ] = \
                    np.linalg.matrix_power(self.Av, j-k-1)*self.Bv

        # Cost Matrices
        self.Qv_big = np.kron(np.eye(T+1), self.Qv)       # I haven't double-checked that this is correct
        self.Qv_big[-nv:(T+1)*nv, -nv:(T+1)*nv] = self.Pv
        self.Rv_big = np.kron(np.eye(T),   self.Rv)

        velocity_extractor = np.zeros(( T+1, nv*(T+1) ))
        for i in range(T+1):
            velocity_extractor[ i, nv*i+1 ] = 1

        touchdown_matrix = np.zeros(( T+1, nv*(T+1) ))
        for i in range(T+1):
            touchdown_matrix[ i, nv*i ] = params.kl
            touchdown_matrix[ i, nv*i+1 ] = 1

        # Constraints appear in the following row order:
        # * Max velocity constraints
        # * Min velocity constraints
        # * Touchdown constraints
        self.vert_constraints_matrix = np.bmat([\
            [velocity_extractor],\
            [-velocity_extractor],\
            [-touchdown_matrix],\
        ])

        self.vert_constraints_vector = np.bmat([\
            [ params.wmax*np.ones((T+1, 1))],\
            [-params.wmin*np.ones((T+1, 1))],\
            [-params.wmin_land*np.ones((T+1, 1))], \
        ])

        # ------------- OSQP Matrices --------------
        P_temp = 2*np.bmat([[self.Qv_big, np.zeros((nv*(T+1), mv*T))],\
            [np.zeros((mv*T, nv*(T+1))), self.Rv_big]])
        P_data = np.diagonal(P_temp)
        P_row = range(nv*(T+1) + mv*T)
        P_col = range(nv*(T+1) + mv*T)
        self.P_OSQP = csc_matrix((P_data, (P_row, P_col)))
        # self.l_OSQP = np.bmat([\
        #     [np.dot(self.Phi_v,np.zeros((nv, 1)))],\
        #     [np.full((3*(T+1), 1), -np.inf)]] )
        # self.u_OSQP = np.bmat([\
        #     [np.dot(self.Phi_v,np.zeros((nv, 1)))],\
        #     [self.vert_constraints_vector]] )
        # self.q_OSQP = np.bmat([\
        #     [-2*np.dot(self.Qv_big, np.zeros((nv*(T+1), 1)))],\
        #     [np.zeros((T*mv, 1))]])
        # # I have added velocity constraints, but not constraints on wdes. Will this be enough?
        # A_temp = np.bmat([\
        #     [np.eye(nv*(T+1)), -self.Lambda_v],\
        #     [self.vert_constraints_matrix, np.zeros((3*(T+1), mv*T))]] )
        self.l_OSQP = np.dot(self.Phi_v,np.zeros((nv, 1)))
        self.u_OSQP = np.dot(self.Phi_v,np.zeros((nv, 1)))
        self.q_OSQP = np.bmat([\
            [-2*np.dot(self.Qv_big, np.zeros((nv*(T+1), 1)))],\
            [np.zeros((T*mv, 1))]])
        # I have added velocity constraints, but not constraints on wdes. Will this be enough?
        A_temp = np.bmat([\
            [np.eye(nv*(T+1)), -self.Lambda_v]] )
        self.A_OSQP = csc_matrix(A_temp)

    def create_optimisation_problem(self):
        T = self.T
        nv = self.nv
        params = self.params
        self.xv = cp.Variable(( nv*(T+1), 1 ))
        self.wdes = cp.Variable(( T, 1 ))
        self.xv_des = cp.Parameter(( nv*(T+1), 1 ))
        self.xv_0 = cp.Parameter(( nv, 1 ))

        objectiveVert = cp.quad_form(self.wdes, self.Rv_big) +\
            cp.quad_form(self.xv-self.xv_des, self.Qv_big)
        # Dynamics constraint
        constraintsVert = [self.xv == self.Phi_v*self.xv_0 \
            + self.Lambda_v*self.wdes]
        # Velocity constraints and touchdown constraints
        constraintsVert += [self.vert_constraints_matrix*self.xv \
            <= self.vert_constraints_vector]


        self.problemVert = \
            cp.Problem(cp.Minimize(objectiveVert), constraintsVert)

        self.problemOSQP = osqp.OSQP()
        self.problemOSQP.setup(P=self.P_OSQP, l=self.l_OSQP, u=self.u_OSQP, A=self.A_OSQP, verbose=False, max_iter = 300)

    def solve(self, xv_m, xv_des_m):
        start = time.time()
        T = self.T
        nv = self.nv
        self.xv_0.value = xv_m
        self.xv_des.value = xv_des_m
        if self.type == 'OSQP':
            start = time.time()
            self.update_OSQP(xv_m, xv_des_m)
            results = self.problemOSQP.solve()
            if results.x[0] is not None:
                self.xv.value = np.reshape(results.x[0:self.nv*(self.T+1)], (-1, 1))
                self.wdes.value = np.reshape(results.x[self.nv*(self.T+1):], (-1, 1))
            else:
                # Optimisation failed
                # Using np.full() doesn't seem to work, since "variables must be
                # real". Using this approach seems to circumvent that limitation
                # np.zeros() is used instead of np.empty() since np.empty()
                # sometimes contains non-real values, causing an exception
                self.wdes.value = np.zeros((self.T, 1))
                self.wdes.value.fill(np.nan)
                self.xv.value = np.zeros(((self.T+1)*self.nv, 1))
                self.xv.value.fill(np.nan)
            duration = time.time() - start
            self.num_iters_log.append(results.info.iter)
            self.durations.append(duration)
        else:   # self.type == 'CVXPY'
            try:
                start = time.time()
                self.problemVert.solve(solver=cp.OSQP, warm_start=False, verbose=False, max_iter = 5000)
                duration = time.time() - start
                stats = self.problemVert.solver_stats
                self.num_iters_log.append(stats.num_iters)
                self.durations.append(duration)
            except cp.error.SolverError as e:
                print "Vertical problem:"
                print e
                self.wdes.value = np.zeros((self.T, 1))
                self.wdes.value.fill(np.nan)
        end = time.time()
        self.last_solution_duration = end - start

    def update_OSQP(self, x0, x_des):
        # self.l_OSQP = np.bmat([\
        #     [np.dot(self.Phi_v, x0)],\
        #     [np.full((3*(self.T+1), 1), -np.inf)]] )
        # self.u_OSQP = np.bmat([\
        #     [np.dot(self.Phi_v, x0)],\
        #     [self.vert_constraints_vector]] )
        # self.q_OSQP = np.bmat([[np.dot(-2*self.Qv_big, x_des)],\
        #     [np.zeros((self.T*self.mv, 1))]])
        self.l_OSQP = np.dot(self.Phi_v, x0)
        self.u_OSQP = np.dot(self.Phi_v, x0)
        self.q_OSQP = np.bmat([[np.dot(-2*self.Qv_big, x_des)],\
            [np.zeros((self.T*self.mv, 1))]])
        # P_temp = 2*np.bmat([[np.dot(safe_states_extractor, self.Qv_big),\
        #     np.zeros((self.nv*(self.T+1), self.mv*self.T))],\
        #     [np.zeros((self.mv*self.T, self.nv*(self.T+1))), self.Rv_big]])
        # P_data = np.diagonal(P_temp)
        self.problemOSQP.update(l=self.l_OSQP, u=self.u_OSQP, q = self.q_OSQP)
        # self.problemOSQP.update(Px=P_data)
