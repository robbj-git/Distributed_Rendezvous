#!/usr/bin/env python
import rospy
import time
import numpy as np
from rendezvous_problem.msg import Float32MultiArrayStamped
from problemClasses import UAVProblem, FastUAVProblem, FastVerticalProblem
from helper_classes import StampedTrajQueue
from helper_functions import mat_to_multiarray_stamped, get_dist_traj, shift_trajectory
from uav_simulator_2 import UAVSimulator2

class CascadingUAVSimulator(UAVSimulator2):

    def __init__(self, problem_params):
        super(CascadingUAVSimulator, self).__init__(problem_params)
        pp = problem_params

        self.problemUAV = UAVProblem(self.T, self.A,  self.B,  pp.params.Q,\
            pp.params.P, pp.params.R, pp.params.Q_vel, pp.params.P_vel,\
            self.nUSV, pp.params)
        Z_UAV = self.problemUAV.get_Z(None)
        self.problemUAVFast = FastUAVProblem(self.T_inner, self.A, self.B,\
            pp.params.Q, pp.params.R, Z_UAV, pp.params)
        self.problemVertFast = FastVerticalProblem(self.T_inner, self.Av,\
            self.Bv, pp.params.Qv, pp.params.Pv, pp.params.Rv, pp.params)

        self.USVApprox = StampedTrajQueue(self.delay_len,\
            should_shift = self.SHOULD_SHIFT_MESSAGES)
        self.USV_traj_sub = rospy.Subscriber(\
            'USV_traj', Float32MultiArrayStamped, self.USV_traj_callback)
        self.traj_pub = rospy.Publisher('UAV_traj', Float32MultiArrayStamped, queue_size = 10)

    def reset(self, sim_len, x_0, xv_0):
        super(CascadingUAVSimulator, self).reset(sim_len, x_0, xv_0)
        self.UAV_inner_traj_log = np.full((self.nUAV*(self.T_inner+1), sim_len)\
            , np.nan)
        self.vert_inner_traj_log = np.full((self.nv *(self.T_inner+1), sim_len)\
            , np.nan)
        self.USVApprox = StampedTrajQueue(self.delay_len,\
            should_shift = self.SHOULD_SHIFT_MESSAGES)

        self.hor_inner_solution_durations = []
        self.vert_inner_solution_durations = []
        self.u_traj = np.zeros( (self.mUAV*self.T, 1) )
        self.x_traj = self.problemUAV.predict_trajectory(x_0, self.u_traj)
        self.problemUAV.x.value = self.x_traj
        self.problemUAV.u.value = self.u_traj
        self.x_traj_inner = self.x_traj[:, 0:self.T_inner]
        self.xv_traj_inner = self.xv_traj[:, 0:self.T_inner]

    def simulate_problem(self, sim_len, x_val, xv_val):
        self.reset(sim_len, x_val, xv_val)

        self.x = x_val
        self.xv = xv_val

        self.get_initial_USV_trajectory_estimate()

        start = time.time()
        for i in range(sim_len):
            if rospy.is_shutdown(): return

            self.i = i
            # -------------- GET DATA FROM USV ----------------
            if i > 0:
                try:
                    self.xb_traj = self.USVApprox.get_traj()
                    if self.SHOULD_SHIFT_MESSAGES:
                        # Trajectory is sent at the end of the USV iteration,
                        # so if we assume that the vehicles' iterations
                        # are synchronised, the message won't be received
                        # until the iteration after being sent
                        self.xb_traj = shift_trajectory(self.xb_traj, self.nUSV, 1)
                except IndexError:
                    # Use shifted old trajectory if no new trajectory is available
                    self.xb_traj = shift_trajectory(self.xb_traj, self.nUSV, 1)

            # -------- GET RESULTS FROM LAST SOLUTION OF OUTER PROBLEM ---------
            if i > 0 and i%self.INTER_ITS == 0:
                self.problemUAV.end_process()
                self.problemVert.end_process()
                self.x_traj = self.problemUAV.x.value
                self.u_traj = self.problemUAV.u.value
                self.dist_traj = get_dist_traj(self.x_traj, self.xb_traj, self.T, \
                    self.nUAV, self.nUSV)

                if np.isnan(self.problemVert.xv.value).any()\
                    or np.isnan(self.problemVert.wdes.value).any():
                    # Failed to solve vertical problem, rise up to a safe height
                    self.wdes_traj = np.full((self.T*self.mv, 1), self.params.wmax)
                    self.xv_traj = self.problemVert.predict_trajectory(self.xv, self.wdes_traj)
                else:
                    self.wdes_traj = self.problemVert.wdes.value
                    self.xv_traj = self.problemVert.xv.value
                self.hor_solution_durations.append(self.problemUAV.last_solution_duration)
                self.vert_solution_durations.append(self.problemVert.last_solution_duration)

                self.send_traj_to_USV(self.x_traj)

            if self.i%self.INTER_ITS != 0:
                self.x_traj = shift_trajectory(self.x_traj, self.nUAV, 1)
                self.u_traj = shift_trajectory(self.u_traj, self.mUAV, 1)
                self.dist_traj = shift_trajectory(self.dist_traj, 1, 1)
                self.xv_traj = shift_trajectory(self.xv_traj, self.nv, 1)
                self.wdes_traj = shift_trajectory(self.wdes_traj, self.mv, 1)

            # ------------- START NEW SOLUTION OF OUTER PROBLEMS ---------------
            if i % self.INTER_ITS == 0:
                # -------------- HORIZONTAL PROBLEM --------------
                x0 = self.x_traj[self.INTER_ITS*self.nUAV\
                    :(self.INTER_ITS+1)*self.nUAV]
                # We want to pass the future predicted trajectory, so we shift
                # the current predicted trajectory an appropriate amount
                traj = shift_trajectory(self.xb_traj, self.nUSV, self.INTER_ITS)
                self.problemUAV.solve_in_parallel(x0, traj)

                # ----------------- VERTICAL PROBLEM ------------------
                xv0 = self.xv_traj[self.INTER_ITS*self.nv:\
                    (self.INTER_ITS+1)*self.nv]
                # TODO: Make dist_traj nartually an array instead of matrix
                dist_traj = shift_trajectory(np.asarray(self.dist_traj),\
                    1, self.INTER_ITS)
                self.problemVert.solve_in_parallel(xv0, 0.0, dist_traj)

            # --------------- SOLVES INNER PROBLEMS ---------------
            self.problemUAVFast.solve(self.x,\
                self.x_traj[0:(self.T_inner+1)*self.nUAV])
            self.x_traj_inner = self.problemUAVFast.x.value
            self.uUAV = self.u_traj[0:self.mUAV]\
                + np.dot(self.problemUAV.K, self.x-self.x_traj[0:self.nUAV])

            self.problemVertFast.solve(self.xv,
                self.xv_traj[0:(self.T_inner+1)*self.nv, 0:1])
            self.xv_traj_inner = self.problemVertFast.xv.value

            self.wdes = self.wdes_traj[0:self.mv]\
                + np.dot(self.problemVert.K, self.xv-self.xv_traj[0:self.nv])

            self.update_logs(self.i)

            # -------------- DYNAMICS SIMULATION -----------------
            if not self.USE_HIL:
                self.x = np.dot(self.A,self.x)  +  np.dot(self.B,self.uUAV)
                self.xv = np.dot(self.Av,self.xv) + np.dot(self.Bv,self.wdes)
            else:
                self.publish_HIL_control(self.uUAV, self.wdes)
            # ------------------ SLEEP ---------------------
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        # ------------ END OF LOOP ------------
        self.x_log[:, sim_len:sim_len+1] = self.x
        self.xv_log[:, sim_len:sim_len+1] = self.xv
        self.xb_log[:, sim_len:sim_len+1] = self.xb_traj[0:self.nUSV, 0:1]

    def get_initial_USV_trajectory_estimate(self):
        while self.xb_traj is None:
            # TODO: Sometimes self.xb_traj seems to be something other than an array, fix that
            self.send_traj_to_USV(np.asarray(self.x_traj))
            try:
                self.xb_traj = self.USVApprox.get_traj()
            except IndexError:
                # This happens if the queue is empty
                self.xb_traj = None
            if rospy.is_shutdown():
                return
            self.rate.sleep()

        self.dist_traj = get_dist_traj(self.x_traj, self.xb_traj, self.T, \
            self.nUAV, self.nUSV)

    def update_logs(self, i):
        self.x_log[ :, i:i+1] = self.x
        self.xv_log[:, i:i+1] = self.xv
        self.uUAV_log[:, i:i+1] = self.uUAV
        self.wdes_log[:, i:i+1] = self.wdes
        self.UAV_traj_log[:, i:i+1]  = self.x_traj
        self.vert_traj_log[:, i:i+1] = self.xv_traj
        self.USV_traj_log[:, i:i+1] = self.xb_traj
        self.s_vert_log[:, i:i+1] = self.problemVert.s.value
        self.obj_val_log[:, i:i+1] = self.problemVert.obj_val

        self.UAV_times[:, i:i+1] = rospy.get_time()
        self.xb_log[:, i:i+1] = self.xb_traj[0:self.nUSV, 0:1]

        self.UAV_inner_traj_log[:, i:i+1] = self.x_traj_inner
        self.vert_inner_traj_log[:, i:i+1] = self.xv_traj_inner
        self.hor_inner_solution_durations.append(self.problemUAVFast.last_solution_duration)
        self.vert_inner_solution_durations.append(self.problemVertFast.last_solution_duration)

    def send_traj_to_USV(self, x_traj):
        traj_msg = mat_to_multiarray_stamped(x_traj, self.T+1, self.nUAV)
        traj_msg.header.stamp = rospy.Time.now()
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            # DEBUG: Adds message droput
            pass
        else:
            self.traj_pub.publish(traj_msg)

    def store_data(self, test_info_str = None):
        # First argument equal to 2 means that the problem type is cascaded
        return super(CascadingUAVSimulator, self).store_data(2, test_info_str)

    def deinitialise(self):
        super(CascadingUAVSimulator, self).deinitialise()
        self.USV_traj_sub.unregister()
        self.traj_pub.unregister()

    def USV_traj_callback(self, msg):
        self.USVApprox.put_traj( msg )
