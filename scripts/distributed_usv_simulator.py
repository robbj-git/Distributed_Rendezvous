#!/usr/bin/env python
import rospy
import numpy as np
import time
import os
from rendezvous_problem.msg import Float32MultiArrayStamped
from problemClasses import USVProblem
from helper_classes import StampedTrajQueue
from helper_functions import shift_trajectory, mat_to_multiarray_stamped
from usv_simulator_2 import USVSimulator2

class DistributedUSVSimulator(USVSimulator2):

    def __init__(self, problem_params, travel_dir = None):
        super(DistributedUSVSimulator, self).__init__(problem_params)
        pp = problem_params
        self.T = pp.T
        self.T_inner = pp.T_inner
        self.SHOULD_SHIFT_MESSAGES = pp.settings.SHOULD_SHIFT_MESSAGES
        self.problemUSV = USVProblem(self.T, self.Ab, self.Bb, pp.params.Q,\
            pp.params.P, pp.params.R, pp.params.Qb_vel, pp.params.Pb_vel,\
            self.nUAV, self.params, travel_dir = travel_dir)
        self.UAVApprox = StampedTrajQueue(self.delay_len, should_shift = self.SHOULD_SHIFT_MESSAGES)
        self.traj_pub = rospy.Publisher('USV_traj', Float32MultiArrayStamped, queue_size = 10)
        self.UAV_traj_sub = rospy.Subscriber(\
            'UAV_traj', Float32MultiArrayStamped, self.UAV_traj_callback)

    def reset(self, sim_len, xb_0):
        super(DistributedUSVSimulator, self).reset(sim_len)
        self.USV_traj_log = np.full((self.nUSV*(self.T+1), sim_len), np.nan)
        self.x_log = np.full((self.nUAV, sim_len+1), np.nan)
        self.UAV_traj_log = np.full( (self.nUAV*(self.T+1), sim_len),\
            np.nan )
        self.s_USV_log = np.full((2, sim_len), np.nan)
        self.hor_solution_durations = []
        # Initial predicted trajectory assumes no control signal applied
        self.ub_traj = np.zeros( (self.mUSV*self.T, 1) )
        self.xb_traj = self.problemUSV.predict_trajectory(xb_0, self.ub_traj)
        self.problemUSV.xb.value = self.xb_traj # TODO: Why do we need to set the value here??
        self.x_traj = None  # Always contains most up-to-date UAV predicted traj
        self.UAVApprox = StampedTrajQueue(self.delay_len, should_shift = self.SHOULD_SHIFT_MESSAGES)

    def simulate_problem(self, sim_len, xb_val):
        self.reset(sim_len, xb_val)
        self.xb = xb_val

        self.i = 0  # Needs to be defined here since it's referenced in send_traj_to_UAV()
        self.get_initial_UAV_trajectory_estimate()

        start = time.time()
        i = 0
        while not self.stop_sim or i < sim_len:
            if rospy.is_shutdown(): return

            self.i = i
            # ------------------- GET DATA FROM UAV --------------------
            if i > 0:
                try:
                    self.x_traj = self.UAVApprox.get_traj()
                    if self.SHOULD_SHIFT_MESSAGES:
                        # Trajectory is sent at the end of the USV iteration,
                        # so if we assume that the vehicles' iterations
                        # are synchronised, the message won't be received
                        # until the iteration after being sent
                        self.x_traj = shift_trajectory(self.x_traj, self.nUAV, 1)
                except IndexError:
                    # Use shifted old trajectory if no new trajectory is available
                    self.x_traj = shift_trajectory(self.x_traj, self.nUAV, 1)

            # ---------------- SOLVING PROBLEM -------------------
            self.problemUSV.solve(self.xb, self.x_traj)
            self.xb_traj = self.problemUSV.xb.value
            self.ub_traj = self.problemUSV.ub.value
            self.uUSV = self.problemUSV.ub[0:self.mUSV, 0:1].value
            if i < sim_len:
                self.update_logs(i)

            # ---------------- DYNAMICS SIMULATION & SLEEP ----------------
            self.send_traj_to_UAV(self.xb_traj)
            self.xb = np.dot(self.Ab,self.xb) + np.dot(self.Bb,self.uUSV)
            i += 1
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()
        # ------------ END OF LOOP ------------
        self.xb_log[:, sim_len:sim_len+1] = self.xb
        self.x_log[:, sim_len:sim_len+1] = self.x_traj[0:self.nUAV, 0:1]

    def get_initial_UAV_trajectory_estimate(self):
        while self.x_traj is None:
            # TODO: Sometimes self.xb_traj seems to be something other than an array, fix that
            self.send_traj_to_UAV(np.asarray(self.xb_traj))
            try:
                self.x_traj = self.UAVApprox.get_traj()
            except IndexError:
                # This happens if the queue is empty
                self.x_traj = None
            if rospy.is_shutdown(): return
            self.rate.sleep()

    def update_logs(self, i):
        self.xb_log[:, i:i+1] = self.xb
        self.uUSV_log[:, i:i+1] = self.uUSV
        self.USV_times[:, i:i+1] = rospy.get_time()
        self.USV_traj_log[:, i:i+1] = self.xb_traj
        self.UAV_traj_log[:, i:i+1] = self.x_traj
        self.x_log[:, i:i+1] = self.x_traj[0:self.nUAV, 0:1]
        self.s_USV_log[:, i:i+1] = self.problemUSV.s.value
        self.hor_solution_durations.append(self.problemUSV.last_solution_duration)

    def send_traj_to_UAV(self, xb_traj):
        traj_msg = mat_to_multiarray_stamped(xb_traj, self.T+1, self.nUSV)
        traj_msg.header.stamp = rospy.Time.now()
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            #DEBUG Adds message dropout
            pass
        else:
            self.traj_pub.publish(traj_msg)

    def store_data(self, exp_index):
        i = exp_index
        dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'

        if os.path.isdir(dir_path + 'Experiment_' + str(i)):
            # Directory exists, assumed to be created by UAV
            pass
        else:
            os.mkdir(dir_path + 'Experiment_' + str(i))

        np.savetxt(dir_path + 'Experiment_'+str(i)+'/xb_log.csv', self.xb_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUSV_log.csv', self.uUSV_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_iteration_durations.csv', self.iteration_durations, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_time_stamps.csv', self.USV_times, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_traj_log.csv', self.USV_traj_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_horizontal_durations.csv', self.hor_solution_durations, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_USV_log.csv', self.s_USV_log, delimiter=',')

    def deinitialise(self):
        super(DistributedUSVSimulator, self).deinitialise()
        self.UAV_traj_sub.unregister()

    def UAV_traj_callback(self, msg):
        nUAV = self.nUAV
        T = self.T
        xhat_m_traj = np.empty((nUAV, T+1))
        stride = msg.array.layout.dim[1].stride
        for t in range(T+1):
            for i in range(nUAV):
                xhat_m_traj[i][t] = msg.array.data[stride*t + i]

        temp = np.reshape(xhat_m_traj, (-1, 1), order='F')
        self.UAVApprox.put_traj(msg)
