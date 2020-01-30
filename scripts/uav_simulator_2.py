#!/usr/bin/env python
import rospy
import time
import datetime
import numpy as np
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header, Bool
from geometry_msgs.msg import Vector3Stamped, QuaternionStamped
from dji_sdk.srv import SDKControlAuthority
from problemClasses import VerticalProblem
import os
from helper_functions import lat_long_to_pos, get_cmd_angle
from math import atan, asin

class UAVSimulator2(object):

    def __init__(self, problem_params):
        pp = problem_params
        self.T = pp.T
        self.T_inner = pp.T_inner
        self.A = pp.params.A
        self.B = pp.params.B
        self.Av = pp.params.Av
        self.Bv = pp.params.Bv
        [self.nUAV, self.mUAV] = pp.params.B.shape
        [self.nUSV, self.mUSV] = pp.params.Bb.shape
        [self.nv, self.mv] = pp.params.Bv.shape
        self.hb = pp.params.hb
        self.params = pp.params
        self.SAMPLING_RATE = pp.settings.SAMPLING_RATE
        self.SAMPLING_TIME = pp.settings.SAMPLING_TIME
        self.SHOULD_SHIFT_MESSAGES = pp.settings.SHOULD_SHIFT_MESSAGES
        self.USE_HIL = pp.settings.USE_HIL
        self.INTER_ITS = pp.settings.INTER_ITS
        self.ADD_DROPOUT = pp.settings.ADD_DROPOUT
        self.PRED_PARALLEL_TRAJ = pp.settings.PRED_PARALLEL_TRAJ
        self.dropout_lower_bound = pp.settings.dropout_lower_bound
        self.dropout_upper_bound = pp.settings.dropout_upper_bound
        self.delay_len = pp.settings.delay_len
        self.long_ref = None
        self.lat_ref = None

        self.i = 0
        self.problemVert = VerticalProblem(self.T, self.Av, self.Bv, pp.params.Qv,\
            pp.params.Pv, pp.params.Rv, pp.params, self.params.hb, num_its = 300)

        self.x = np.full((self.nUAV, 1), np.nan)
        self.xv = np.full((self.nv, 1), np.nan)

        # --------------------------- ROS SETUP ----------------------------------
        self.rate = rospy.Rate(self.SAMPLING_RATE)
        if self.USE_HIL:
            self.imu_sub = \
                rospy.Subscriber('dji12/dji_sdk/imu', Imu, self.IMU_callback)
            self.height_sub = rospy.Subscriber(\
                'dji12/dji_sdk/height_above_takeoff', Float32, self.height_callback)
            self.vel_sub = rospy.Subscriber(\
                'dji12/dji_sdk/velocity', Vector3Stamped, self.velocity_callback)
            self.gps_sub = rospy.Subscriber(\
                'dji12/dji_sdk/gps_position', NavSatFix, self.pos_callback)
            self.attitude_sub = rospy.Subscriber(\
                'dji12/dji_sdk/attitude', QuaternionStamped, self.attitude_callback)

            self.UAV_publisher = rospy.Publisher('/dji12/dji_sdk/flight_control_setpoint_generic',\
                Joy, queue_size = 10)

            print('Waiting for control authority serivce')
            rospy.wait_for_service('/dji12/dji_sdk/sdk_control_authority')
            print('Finished waiting')

            try:
                authority_server = rospy.ServiceProxy(\
                    '/dji12/dji_sdk/sdk_control_authority', SDKControlAuthority)
                control_response = authority_server(1)
            except:
                print "Failed reaching control authority. Sleeping for 3s."
                time.sleep(3)

    def reset(self, sim_len, x_0, xv_0):
        self.x_log = np.full((self.nUAV, sim_len+1), np.nan)
        self.xv_log = np.full((self.nv,   sim_len+1), np.nan)
        self.xb_log = np.full((self.nUSV, sim_len+1), np.nan)
        self.uUAV_log = np.full((self.mUAV, sim_len), np.nan)
        self.wdes_log = np.full((self.mv,   sim_len), np.nan)
        self.UAV_traj_log = np.full((self.nUAV*(self.T+1), sim_len), np.nan)
        self.vert_traj_log = np.full((self.nv *(self.T+1), sim_len), np.nan)
        self.USV_traj_log = np.full((self.nUSV*(self.T+1), sim_len), np.nan)
        self.s_vert_log = np.full((1, sim_len), np.nan)
        self.obj_val_log = np.full((1, sim_len), np.nan)
        # Associate one time value with each iteration of the simulation
        self.UAV_times = np.full((1, sim_len), np.nan)
        self.iteration_durations = []
        self.hor_solution_durations = []
        self.vert_solution_durations = []

        self.wdes_traj = np.zeros( (self.mv*self.T, 1) )
        self.xv_traj = self.problemVert.predict_trajectory(xv_0, self.wdes_traj) # Always contains most up-to-date predicted vertical traj
        self.problemVert.xv.value = self.xv_traj
        self.problemVert.wdes.value = self.wdes_traj
        self.xb_traj = None # Always contains most up-to-date USV predicted traj
        # Always contains most up-to-date predicted horizontal distance between vehicles
        self.dist_traj = None

    def publish_HIL_control(self, uUAV, wdes):
        phi_cmd, theta_cmd = get_cmd_angle(uUAV, wdes, self.xv)
        axes = [phi_cmd, theta_cmd, wdes, 0.0, 0x02]
        UAV_msg = Joy(Header(), axes, [])
        self.UAV_publisher.publish(UAV_msg)

    def store_data(self, type, test_info_str = None):
        CENTRALISED = 0
        DISTRIBUTED = 1
        PARALLEL    = 2
        T = self.T
        SAMPLING_RATE = self.SAMPLING_RATE

        [_, sim_len] = self.x_log.shape
        sim_len -= 1
        i = 0
        dir_already_exists = True
        dir_path = os.path.expanduser("~") + '/robbj_experiment_results/'
        # print "DIR PATH:", dir_path
        # dir_path = '/home/student/robbj_experiment_results/'
        while dir_already_exists:
            i += 1
            dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(i))

        os.mkdir(dir_path + 'Experiment_' + str(i))
        os.mkdir(dir_path + 'Experiment_' + str(i) + '/UAV')
        os.mkdir(dir_path + 'Experiment_' + str(i) + '/TEST')
        # experiment_index_pub.publish(Int8(i))

        info_str = str(datetime.datetime.now()) + '\ntype: '
        if type == CENTRALISED:
            info_str += 'Centralised\n'
        elif type ==  DISTRIBUTED:
            info_str+= 'Distributed\n'
        elif type == PARALLEL:
            info_str += 'Parallel\n'

        info_str += 'simulation length: ' + str(sim_len) + '\n'
        info_str += 'horizon: ' + str(T) + '\n'
        info_str += 'sampling rate: ' + str(SAMPLING_RATE) + '\n'
        info_str += 'Delay length [iterations]: ' + str(self.delay_len) + '\n'
        info_str += ("HIL setup" if self.USE_HIL else "Local setup") + " was used\n"
        info_str += "USV was at altitude: " + str(self.hb) + "\n"
        info_str += "Dropout was used\n" if self.ADD_DROPOUT else "Dropout was NOT used\n"
        if self.ADD_DROPOUT:
            info_str += "Dropout bounds: " + str(self.dropout_lower_bound) + " to " + str(self.dropout_upper_bound) + "\n"
        info_str += "dl: " + str(self.params.dl) + "\n"
        info_str += "ds: " + str(self.params.ds) + "\n"
        info_str += "hs: " + str(self.params.hs) + "\n"
        info_str += "Received messages WERE shifted to account for delay\n" \
            if self.SHOULD_SHIFT_MESSAGES else "Received messages were NOT shifted to account for delay\n"
        if type == PARALLEL:
            info_str += "Parallel DID predict initial state for outer problem\n" \
                if self.PRED_PARALLEL_TRAJ else "Parallel did NOT predict initial state for outer problem\n"
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/info.txt', [info_str], fmt="%s")
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/x_log.csv', self.x_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/xv_log.csv', self.xv_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_traj_log.csv', self.UAV_traj_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_traj_log.csv', self.vert_traj_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUAV_log.csv', self.uUAV_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/wdes_log.csv', self.wdes_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_iteration_durations.csv', self.iteration_durations, delimiter=',')
        # print np.sum(np.array(self.iteration_durations) >= 0.05)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_time_stamps.csv', self.UAV_times, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_solution_durations.csv', self.vert_solution_durations, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.csv', self.hor_solution_durations, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_vert_log.csv', self.s_vert_log, delimiter=',')
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/obj_val_log.csv', self.obj_val_log, delimiter=',')
        if type == CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_traj_log.csv', self.USV_traj_log, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_UAV_log.csv', self.s_UAV_log, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_USV_log.csv', self.s_USV_log, delimiter=',')
        if type == PARALLEL:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_hor_inner_durations.csv', self.hor_inner_solution_durations, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_inner_durations.csv', self.vert_inner_solution_durations, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_inner_traj_log.csv', self.UAV_inner_traj_log, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_inner_traj_log.csv', self.vert_inner_traj_log, delimiter=',')
        if test_info_str is not None:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/test_info.txt', [test_info_str], fmt="%s")

        if type == CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/xb_log.csv', self.xb_log, delimiter=',')
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/uUSV_log.csv', self.uUSV_log, delimiter=',')
        if type != CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/USV_traj_log.csv', self.USV_traj_log, delimiter=',')

        return i

    # Allows for stopping an object from receiving ROS messages.
    # Useful if a new instance is created, but old object is still kept
    # for other purposes. If this function is not called, the old and new
    # instances will both be subscribed to the same topic. I can't remember
    # right now why that is a problem, but it did cause me issues previously.
    def deinitialise(self):
        if self.USE_HIL:
            self.imu_sub.unregister()
            self.height_sub.unregister()
            self.vel_sub.unregister()
            self.gps_sub.unregister()
            self.attitude_sub.unregister()

    def send_sim_stop(self):
        msg = Bool()
        msg.data = True
        self.sim_stop_pub.publish(msg)

    def IMU_callback(self, msg):
        # global w_1, w_2
        self.w_1 = msg.angular_velocity.x
        self.w_2 = msg.angular_velocity.y

    def height_callback(self, msg):
        # global xv
        self.xv[0] = msg.data

    def velocity_callback(self, msg):
        # global xv, x
        self.x[2]  = msg.vector.x
        self.x[3]  = msg.vector.y
        self.xv[1] = msg.vector.z

    def pos_callback(self, msg):
        # global x, long_ref, lat_ref
        R = 6378138.12

        if self.long_ref is None:
            self.long_ref = msg.longitude
        if self.lat_ref is None:
            self.lat_ref = msg.latitude

        phi_gps = msg.latitude
        phi_ref = self.lat_ref
        lambda_gps = msg.longitude
        lambda_ref = self.long_ref

        self.x[0:2] = lat_long_to_pos(phi_gps, lambda_gps, phi_ref, lambda_ref, R);

    def attitude_callback(self, msg):
        # global phi, theta
        qw = msg.quaternion.w
        qx = msg.quaternion.x
        qy = msg.quaternion.y
        qz = msg.quaternion.z
        self.phi = atan( 2*(qw*qx + qy*qz)/(1 - 2*(qx*qx + qy*qy)) )
        self.theta = asin(2*(qw*qy-qz*qx))
