#!/usr/bin/env python
import rospy
import numpy as np
import time
import os
from rendezvous_problem.msg import StateStamped
from geometry_msgs.msg import AccelStamped
from helper_classes import StampedMsgQueue
from usv_simulator_2 import USVSimulator2

class CentralisedUSVSimulator(USVSimulator2):

    def __init__(self, problem_params):
        super(CentralisedUSVSimulator, self).__init__(problem_params)
        self.state_pub = rospy.Publisher('USV_state', StateStamped, queue_size = 10)
        self.USV_input_sub = rospy.Subscriber(\
            'USV_input', AccelStamped, self.USV_input_callback)

    def reset(self, sim_len):
        super(CentralisedUSVSimulator, self).reset(sim_len)
        self.input_queue = StampedMsgQueue(self.delay_len)

    def simulate_problem(self, sim_len, xb_val):
        self.reset(sim_len)
        self.xb = xb_val
        self.i = 0  # Needs to be defined here since it's referenced in send_state_to_UAV()
        self.get_first_control_input()
        start = time.time()
        i = 0
        while not self.stop_sim or i < sim_len:
            # Even if UAV has finished simulation, it is important to let the
            # USV run sim_len iteration for data analysis purposes
            if rospy.is_shutdown(): return
            self.i = i
            self.send_state_to_UAV(self.xb)
            # ------------ GET DATA FROM UAV --------------
            if i > 0:
                try:
                    uUSV_msg = self.input_queue.get()
                    self.uUSV = np.array([[uUSV_msg.accel.linear.x],\
                        [uUSV_msg.accel.linear.y]])
                except IndexError:
                    self.uUSV = np.zeros((self.mUSV, 1))

            if i < sim_len:
                self.update_logs(self.i)

            # ---------------- DYNAMICS SIMULATION & SLEEP ----------------
            self.xb = np.dot(self.Ab,self.xb) + np.dot(self.Bb,self.uUSV)
            i += 1
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        # ----------------------- END OF LOOP -----------------------
        self.xb_log[:, sim_len:sim_len+1] = self.xb

    def get_first_control_input(self):
        uUSV_msg = None

        while uUSV_msg is None:
            self.send_state_to_UAV(self.xb)
            try:
                uUSV_msg = self.input_queue.get()
            except IndexError:
                pass
            if rospy.is_shutdown(): return
            self.rate.sleep()
        self.uUSV = np.array([[uUSV_msg.accel.linear.x],\
            [uUSV_msg.accel.linear.y]])

    def update_logs(self, i):
        self.xb_log[:, i:i+1] = self.xb
        self.uUSV_log[:, i:i+1] = self.uUSV
        self.USV_times[:, i:i+1] = rospy.get_time()

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

    def deinitialise(self):
        super(CentralisedUSVSimulator, self).deinitialise()
        self.USV_input_sub.unregister()

    def send_state_to_UAV(self, xb):
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            #DEBUG Adds message dropout
            pass
        else:
            state_msg = StateStamped()
            state_msg.pose.position.x = xb[0]
            state_msg.pose.position.y = xb[1]
            state_msg.twist.linear.x = xb[2]
            state_msg.twist.linear.y = xb[3]
            state_msg.header.stamp = rospy.Time.now()
            self.state_pub.publish(state_msg)

    def USV_input_callback(self, msg):
        self.input_queue.put(msg)
