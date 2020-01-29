#!/usr/bin/env python
import rospy
import time
from std_msgs.msg import Bool
import numpy as np
from rendezvous_problem.msg import StateStamped
from geometry_msgs.msg import AccelStamped
from helper_classes import StampedMsgQueue
from helper_functions import get_dist_traj
from problemClasses import CentralisedProblem
from uav_simulator_2 import UAVSimulator2

class CentralisedUAVSimulator(UAVSimulator2):

    def __init__(self, problem_params, travel_dir = None):
        super(CentralisedUAVSimulator, self).__init__(problem_params)
        pp = problem_params

        self.problemCent = CentralisedProblem(self.T, self.A, self.B,\
            pp.params.Ab, pp.params.Bb, pp.params.Q, pp.params.P, \
            pp.params.R, pp.params.Q_vel, pp.params.P_vel, pp.params.Qb_vel,\
            pp.params.Pb_vel, pp.params, travel_dir = travel_dir)

        # USV_state_queue needs to be defined already here since it's used in callbacks
        self.USV_state_queue = StampedMsgQueue(self.delay_len)
        self.USV_input_pub = rospy.Publisher('USV_input', AccelStamped, queue_size = 10)
        self.USV_state_sub = rospy.Subscriber(\
            'USV_state', StateStamped, self.USV_state_callback)
        self.sim_stop_pub = rospy.Publisher('stop_sim', Bool, queue_size = 1)

    def reset(self, sim_len, x_0, xv_0):
        super(CentralisedUAVSimulator, self).reset(sim_len, x_0, xv_0)
        self.USV_state_queue = StampedMsgQueue(self.delay_len)
        self.s_UAV_log = np.full((self.problemCent.nUAV_s, sim_len), np.nan)
        self.s_USV_log = np.full((self.problemCent.nUSV_s, sim_len), np.nan)
        self.uUSV_log = np.full((self.mUSV, sim_len), np.nan)

    def simulate_problem(self, sim_len, x_val, xv_val):
        self.reset(sim_len, x_val, xv_val)
        self.x = x_val
        self.xv = xv_val

        self.get_initial_USV_state_estimate()

        start = time.time()
        for i in range(sim_len):
            if rospy.is_shutdown():
                return

            self.i = i
            # Get data from USV
            if i > 0:
                try:
                    xb_msg = self.USV_state_queue.get()
                    self.xb = np.array(\
                        [[xb_msg.pose.position.x], [xb_msg.pose.position.y],\
                        [xb_msg.twist.linear.x], [xb_msg.twist.linear.y]])
                except IndexError:
                    # Leave self.xb unchanged
                    pass

            # -------------- HORIZONTAL PROBLEM ----------------
            self.problemCent.solve(self.x, self.xb)
            self.x_traj  = self.problemCent.x.value
            self.xb_traj = self.problemCent.xb.value
            self.u_traj  = self.problemCent.u.value
            self.ub_traj = self.problemCent.ub.value
            self.uUAV = self.problemCent.u[ 0:self.mUAV, 0:1].value
            self.uUSV = self.problemCent.ub[0:self.mUSV, 0:1].value
            self.dist_traj = get_dist_traj(self.x_traj, self.xb_traj, self.T, \
                self.nUAV, self.nUSV)

            # --------------- VERTICAL PROBLEM ---------------------
            # TODO: Make dist_traj naturally be an array instead of a matrix
            self.problemVert.solve(self.xv, 0.0, np.asarray(self.dist_traj))
            self.wdes = self.problemVert.wdes[0:self.mv, 0:1].value
            if np.isnan(self.wdes).any() or np.isnan(self.problemVert.xv.value).any():
                # Failed to solve vertical problem, rise up to a safe height
                self.wdes = self.params.wmax
                self.wdes_traj = np.full((self.T*self.mv, 1), self.params.wmax)
                self.xv_traj = self.problemVert.predict_trajectory(self.xv, self.wdes_traj)
            else:
                self.xv_traj = self.problemVert.xv.value
                self.wdes_traj = self.problemVert.wdes.value

            self.update_logs(i)

            # -------------- DYNAMICS SIMULATION -----------------
            self.send_control_to_USV(self.uUSV)
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
        self.xb_log[:, sim_len:sim_len+1] = self.xb
        self.send_sim_stop()    # Tells USV to stop simulation
        return

    def get_initial_USV_state_estimate(self):
        xb_msg = None
        while xb_msg is None:
            try:
                xb_msg = self.USV_state_queue.get()
            except IndexError:
                pass
            if rospy.is_shutdown():
                return
            self.rate.sleep()
        self.xb = np.array(\
            [[xb_msg.pose.position.x], [xb_msg.pose.position.y],\
            [xb_msg.twist.linear.x], [xb_msg.twist.linear.y]])

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
        self.xb_log[:, i:i+1] = self.xb
        self.uUSV_log[:, i:i+1] = self.uUSV
        self.s_UAV_log[:, i:i+1] = self.problemCent.s_UAV.value
        self.s_USV_log[:, i:i+1] = self.problemCent.s_USV.value
        self.hor_solution_durations.append(self.problemCent.last_solution_duration)
        self.vert_solution_durations.append(self.problemVert.last_solution_duration)

    def send_control_to_USV(self, uUSV):
        USV_input_msg = AccelStamped()
        USV_input_msg.accel.linear.x = uUSV[0]
        USV_input_msg.accel.linear.y = uUSV[1]
        USV_input_msg.header.stamp = rospy.Time.now()
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            # DEBUG: Adds message droput
            pass
        else:
            self.USV_input_pub.publish(USV_input_msg)

    def send_sim_stop(self):
        msg = Bool()
        msg.data = True
        self.sim_stop_pub.publish(msg)

    def deinitialise(self):
        super(CentralisedUAVSimulator, self).deinitialise()
        self.USV_state_sub.unregister()

    def USV_state_callback(self, msg):
        self.USV_state_queue.put(msg)

    def store_data(self, test_info_str = None):
        # First argument equal to 0 means that the problem type is centralised
        return super(CentralisedUAVSimulator, self).store_data(0, test_info_str)
