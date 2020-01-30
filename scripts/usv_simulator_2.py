#!/usr/bin/env python
import rospy
import numpy as np
from std_msgs.msg import Bool

class USVSimulator2(object):

    def __init__(self, problem_params):
        pp = problem_params
        self.Ab = pp.params.Ab
        self.Bb = pp.params.Bb
        self.params = pp.params
        self.delay_len = pp.settings.delay_len
        [self.nUAV, self.mUAV] = pp.params.B.shape
        [self.nUSV, self.mUSV] = self.Bb.shape
        self.SAMPLING_RATE = pp.settings.SAMPLING_RATE
        self.ADD_DROPOUT = pp.settings.ADD_DROPOUT
        self.dropout_lower_bound = pp.settings.dropout_lower_bound
        self.dropout_upper_bound = pp.settings.dropout_upper_bound
        self.rate = rospy.Rate(self.SAMPLING_RATE)
        self.stop_sim_sub = rospy.Subscriber('stop_sim', Bool, self.stop_sim_callback)

    def reset(self, sim_len):
        self.xb_log = np.full((self.nUSV, sim_len+1), np.nan)
        self.uUSV_log = np.full((self.mUSV, sim_len), np.nan)
        self.USV_times = np.full((1, sim_len), np.nan)
        self.iteration_durations = []
        self.stop_sim = False

    def stop_sim_callback(self, msg):
        self.stop_sim = msg.data

    # Allows for stopping an object from receiving ROS messages.
    # Useful if a new instance is created, but old object is still kept
    # for other purposes. If this function is not called, the old and new
    # instances will both be subscribed to the same topic.
    def deinitialise(self):
        self.stop_sim_sub.unregister()
