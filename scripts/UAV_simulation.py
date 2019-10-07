#!/usr/bin/env python
import rospy
import time
import datetime
import numpy as np
from sensor_msgs.msg import Imu, NavSatFix, Joy
from std_msgs.msg import Float32, Header
from geometry_msgs.msg import Vector3Stamped, QuaternionStamped
from dji_sdk.srv import SDKControlAuthority
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
import os
from problemClasses import CentralisedProblem, UAVProblem, VerticalProblem
from problemClasses import FastUAVProblem, FastVerticalProblem
from moreProblemClasses import CompleteCentralisedProblem
from helper_classes import StampedTrajQueue, StampedMsgQueue
from helper_functions import get_dist_traj, mat_to_multiarray_stamped, shift_trajectory, lat_long_to_pos, fill_lost_values, get_cmd_angle
from math import atan, asin, acos
# from new_callbacks import *
from rendezvous_problem.msg import Float32MultiArrayStamped, StateStamped
from geometry_msgs.msg import AccelStamped
from std_msgs.msg import Int8

class UAV_simulator():

    def __init__(self, problem_params, travel_dir = None):
        pp = problem_params
        self.T = pp.T
        self.T_inner = pp.T_inner
        self.A = pp.A
        self.B = pp.B
        self.Av = pp.Av
        self.Bv = pp.Bv
        self.used_solver = pp.used_solver
        self.vert_used_solver = pp.vert_used_solver
        self.delay_len = pp.delay_len
        [self.nUAV, self.mUAV] = pp.B.shape
        [self.nUSV, self.mUSV] = pp.Bb.shape
        [self.nv, self.mv] = pp.Bv.shape
        self.KUAV = pp.KUAV
        self.KVert = pp.KVert
        self.lookahead = pp.lookahead
        self.params = pp.params
        self.CENTRALISED = pp.CENTRALISED
        self.DISTRIBUTED = pp.DISTRIBUTED
        self.PARALLEL = pp.PARALLEL
        self.SAMPLING_RATE = pp.SAMPLING_RATE
        self.SAMPLING_TIME = pp.SAMPLING_TIME
        self.USE_HIL = pp.USE_HIL
        self.INTER_ITS = pp.INTER_ITS
        self.USE_COMPLETE_HORIZONTAL = pp.USE_COMPLETE_HORIZONTAL
        self.ADD_DROPOUT = pp.ADD_DROPOUT
        self.PRED_PARALLEL_TRAJ = pp.PRED_PARALLEL_TRAJ
        self.SHOULD_SHIFT_MESSAGES = pp.SHOULD_SHIFT_MESSAGES
        self.dropout_lower_bound = pp.dropout_lower_bound
        self.dropout_upper_bound = pp.dropout_upper_bound
        self.long_ref = None
        self.lat_ref = None
        self.hb = pp.hb

        self.problemCent = CentralisedProblem(pp.T, pp.A, pp.B, pp.Ab, pp.Bb,\
            pp.Q, pp.P, pp.R, pp.Q_vel, pp.P_vel, pp.Qb_vel, pp.Pb_vel, pp.used_solver, pp.params, travel_dir = travel_dir)
        self.problemUAV = UAVProblem(pp.T, pp.A,  pp.B,  pp.Q, pp.P, pp.R,\
            pp.Q_vel, pp.P_vel, self.nUSV, pp.used_solver, pp.params)
        self.problemVert = VerticalProblem(pp.T, pp.Av, pp.Bv, pp.Qv, pp.Pv,\
            pp.Rv, pp.vert_used_solver, pp.params, self.hb)

        self.problemUAVFast = FastUAVProblem(pp.T_inner, pp.A, pp.B, pp.Q, pp.P,\
            pp.R, self.used_solver, pp.params)
        self.problemVertFast = FastVerticalProblem(pp.T_inner, pp.Av, pp.Bv,\
            pp.Qv, pp.Pv, pp.Rv, pp.vert_used_solver, pp.params)

        if self.USE_COMPLETE_HORIZONTAL:
            self.problemCent = CompleteCentralisedProblem(pp.T, pp.Ab, pp.Bb,\
                pp.Q, pp.R, pp.P, pp.R, pp.Qb_vel, pp.Pb_vel, pp.params)
            self.nUAV = self.problemCent.nUAV
            self.mUAV = self.problemCent.mUAV
            self.A = self.problemCent.A
            self.B = self.problemCent.B

        self.i = 0
        # These must be created already in the constructor since they are used in ROS callbacks
        self.USVApprox = StampedTrajQueue(self.delay_len, should_shift = self.SHOULD_SHIFT_MESSAGES)
        self.USV_state_queue = StampedMsgQueue(self.delay_len)

        self.x = np.full((self.nUAV, 1), np.nan)
        self.xv = np.full((self.nv, 1), np.nan)
        self.xv.fill(np.nan)

        # --------------------------- ROS SETUP ----------------------------------
        # rospy.init_node('UAV_main')
        self.rate = rospy.Rate(self.SAMPLING_RATE)
        self.USV_input_pub = rospy.Publisher('USV_input', AccelStamped, queue_size = 10)
        self.experiment_index_pub = rospy.Publisher('experiment_index', Int8, queue_size=1, latch=True)
        if self.CENTRALISED:
            self.USV_state_sub = rospy.Subscriber(\
                'USV_state', StateStamped, self.USV_state_callback)
        else:
            self.USV_traj_sub = rospy.Subscriber(\
                'USV_traj', Float32MultiArrayStamped, self.USV_traj_callback)
            self.traj_pub = rospy.Publisher('UAV_traj', Float32MultiArrayStamped, queue_size = 10)
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
        self.UAV_inner_traj_log = np.full((self.nUAV*(self.T_inner+1), sim_len)\
            , np.nan)
        self.vert_inner_traj_log = np.full((self.nv *(self.T_inner+1), sim_len)\
            , np.nan)
        self.USV_traj_log = np.full((self.nUSV*(self.T+1), sim_len), np.nan)
        self.s_vert_log = np.full((1, sim_len), np.nan)
        self.obj_val_log = np.full((1, sim_len), np.nan)
        # Associate one time value with each iteration of the simulation
        self.UAV_times = np.full((1, sim_len), np.nan)
        self.iteration_durations = []
        self.hor_solution_durations = []
        self.vert_solution_durations = []
        if self.PARALLEL:
            self.hor_inner_solution_durations = []
            self.vert_inner_solution_durations = []

        # Initial predicted UAV trajectory assumes no control signal applied
        if not self.CENTRALISED:
            self.x_traj = self.problemUAV.predict_trajectory(x_0, \
                np.zeros( (self.mUAV*self.T, 1) ))
            self.problemUAV.x.value = self.x_traj
        self.xv_traj = self.problemVert.predict_trajectory(xv_0, \
            np.zeros( (self.mv*self.T, 1) )) # Always contains most up-to-date predicted vertical traj
        self.problemVert.xv.value = self.xv_traj
        self.xb_traj = None # Always contains most up-to-date USV predicted traj
        if self.PARALLEL:
            self.x_traj_inner = self.x_traj[:, 0:self.T_inner]
            self.xv_traj_inner = self.xv_traj[:, 0:self.T_inner]
        # Always contains most up-to-date predicted horizontal distance between vehicles
        self.dist_traj = None
        if not self.CENTRALISED:
            # Stores both positive and negative distances, for nicer plotting
            self.dist_traj_signed = None
        else: # if self.CENTRALISED
            self.s_UAV_log = np.full((2, sim_len), np.nan)
            self.s_USV_log = np.full((2, sim_len), np.nan)
            self.uUSV_log = np.full((self.mUSV, sim_len), np.nan)

        self.USVApprox = StampedTrajQueue(self.delay_len, should_shift = self.SHOULD_SHIFT_MESSAGES)
        self.USV_state_queue = StampedMsgQueue(self.delay_len)

    def simulate_problem(self, sim_len, x_val, xv_val):
        self.reset(sim_len, x_val, xv_val)

        self.x = x_val
        self.xv = xv_val

        # If centralised, get initial USV state estimate
        if self.CENTRALISED:
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

        # If distributed or parallel, get initial USV trajectory estimation
        if not self.CENTRALISED:
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

        start = time.time()
        for i in range(sim_len):
            self.i = i
            if rospy.is_shutdown():
                return

            # Receive data from USV
            if not i == 0:
                if self.CENTRALISED:
                    try:
                        xb_msg = self.USV_state_queue.get()
                        self.xb = np.array(\
                            [[xb_msg.pose.position.x], [xb_msg.pose.position.y],\
                            [xb_msg.twist.linear.x], [xb_msg.twist.linear.y]])
                    except IndexError:
                        # Leave self.xb unchanged
                        pass
                elif self.DISTRIBUTED or \
                    (self.PARALLEL and i % self.INTER_ITS == 0):
                    try:
                        self.xb_traj = self.USVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        self.xb_traj = shift_trajectory(self.xb_traj, self.nUSV, 1)


            # The outer parallel problems will be solved anew this iteration
            # Update using the previous solution
            if self.PARALLEL and i%self.INTER_ITS == 0 and i > 0:
                self.update_parallel_trajectories()
                self.send_traj_to_USV(self.x_traj)

            # ------- Horizontal Problem --------
            if self.CENTRALISED:
                self.problemCent.solve(self.x, self.xb)
            elif self.DISTRIBUTED:
                # TODO: Make xb_traj naturally an array instead of a matrix
                self.problemUAV.solve(self.x, np.asarray(self.xb_traj))
            elif self.PARALLEL and i % self.INTER_ITS == 0:
                if self.PRED_PARALLEL_TRAJ:
                    x0 = self.x_traj_inner[self.INTER_ITS*self.nUAV\
                        :(self.INTER_ITS+1)*self.nUAV]
                    traj = shift_trajectory(self.xb_traj, self.nUSV, self.INTER_ITS)
                else:
                    x0 = self.x
                    traj = self.xb_traj
                self.problemUAV.solve_in_parallel(x0, traj)

            self.update_hor_trajectories(i)

            if self.PARALLEL:
                self.problemUAVFast.solve(self.x[0:(self.T_inner+1)*self.nUAV],\
                    self.x_traj[0:(self.T_inner+1)*self.nUAV])

            (self.uUAV, self.uUSV) = self.get_horizontal_control()
            # ------- Vertical Problem --------
            if self.dist_traj is not None:
                if not self.PARALLEL:
                    # TODO: Make dist_traj naturally be an array instead of a matrix
                    self.problemVert.solve(self.xv, 0.0, np.asarray(self.dist_traj))
                elif self.PARALLEL and i % self.INTER_ITS == 0:
                    if self.PRED_PARALLEL_TRAJ:
                        xv0 = self.xv_traj[self.INTER_ITS*self.nv:\
                            (self.INTER_ITS+1)*self.nv]
                        dist_traj = shift_trajectory(np.asarray(self.dist_traj),\
                            1, self.INTER_ITS)
                    else:
                        xv0 = self.xv
                        dist_traj = np.asarray(self.dist_traj)
                    # TODO: Make dist_traj nartually an array instead of matrix
                    self.problemVert.solve_in_parallel(xv0, 0.0,\
                        dist_traj)

            self.update_vert_trajectories()

            if self.PARALLEL:
                self.problemVertFast.solve(self.xv[0:(self.T_inner+1)*self.nv],
                    self.xv_traj[0:(self.T_inner+1)*self.nv, 0:1])

            self.wdes = self.get_vertical_control()
            self.update_logs(self.i)

            # ------- Simulate Dynamics / Apply Control --------

            if self.CENTRALISED:
                self.send_control_to_USV(self.uUSV)

            if self.DISTRIBUTED:
                self.send_traj_to_USV(self.x_traj)
            # In parallel case, trajectory is sent at the beggining of the loop

            if not self.USE_HIL:
                # self.x  =  self.A*self.x  +  self.B*self.uUAV
                # self.xv = self.Av*self.xv + self.Bv*self.wdes
                self.x  =  np.dot(self.A,self.x)  +  np.dot(self.B,self.uUAV)
                if self.USE_COMPLETE_HORIZONTAL:
                    self.x += self.problemCent.C_d
                self.xv = np.dot(self.Av,self.xv) + np.dot(self.Bv,self.wdes)
            else:
                self.publish_HIL_control(self.uUAV, self.wdes)
            # ------- Sleep --------
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        # ------------ END OF LOOP ------------
        self.x_log[:, sim_len:sim_len+1] = self.x
        self.xv_log[:, sim_len:sim_len+1] = self.xv
        if self.CENTRALISED:
            self.xb_log[:, sim_len:sim_len+1] = self.xb
        else:
            self.xb_log[:, sim_len:sim_len+1] = self.xb_traj[0:self.nUSV, 0:1]

    def get_horizontal_control(self):
        if self.CENTRALISED:
            return (self.problemCent.u[ 0:self.mUAV, 0:1].value,\
                    self.problemCent.ub[0:self.mUSV, 0:1].value)
        elif self.DISTRIBUTED:
            return (self.problemUAV.u[0:self.mUAV, 0:1].value, None)
        elif self.PARALLEL:
            return (self.problemUAVFast.u[0:self.mUAV, 0:1].value, None)

    def get_vertical_control(self):
        if self.CENTRALISED or self.DISTRIBUTED:
            wdes = self.problemVert.wdes[0:self.mv, 0:1].value
        elif self.PARALLEL:
            wdes = self.problemVertFast.wdes[0:self.mv, 0:1].value

        if np.isnan(wdes).any():
            # If solution of vertical problem failed, make the UAV rise
            wdes = self.params.wmax
        return wdes

    def update_hor_trajectories(self, i):
        if self.CENTRALISED:
            self.x_traj  = self.problemCent.x.value
            self.xb_traj = self.problemCent.xb.value
        elif self.DISTRIBUTED:
            self.x_traj = self.problemUAV.x.value
        elif self.PARALLEL:
            self.x_traj_inner = self.problemUAVFast.x.value
            if self.i%self.INTER_ITS != 0:
                self.x_traj = shift_trajectory(self.x_traj, self.nUAV, 1)
                self.xb_traj = shift_trajectory(self.xb_traj, self.nUSV, 1)

        self.dist_traj = get_dist_traj(self.x_traj, self.xb_traj, self.T, \
            self.nUAV, self.nUSV)
        self.dist_traj_signed = \
            get_dist_traj(self.x_traj, self.xb_traj, self.T, self.nUAV,\
            self.nUSV, True)

    def update_vert_trajectories(self):
        if np.isnan(self.problemVert.xv.value).any():
            # Failed to solve vertical problem, rise up to a safe height
            wdes_traj = np.full((self.T*self.mv, 1), self.params.wmax)
            self.xv_traj = self.problemVert.predict_trajectory(self.xv, wdes_traj)
        else:
            if not self.PARALLEL:
                self.xv_traj = self.problemVert.xv.value
            elif self.PARALLEL and self.i%self.INTER_ITS != 0:
                self.xv_traj = shift_trajectory(self.xv_traj, self.nv, 1)
        if self.PARALLEL:
            self.xv_traj_inner = self.problemVertFast.xv.value

    # Also stores solution duration of parallel problem
    def update_parallel_trajectories(self):
        self.problemUAV.end_process()
        self.problemVert.end_process()
        self.x_traj = self.problemUAV.x.value
        self.xv_traj = self.problemVert.xv.value
        self.hor_solution_durations.append(self.problemUAV.last_solution_duration)
        self.vert_solution_durations.append(self.problemVert.last_solution_duration)

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
        if self.CENTRALISED:
            self.xb_log[:, i:i+1] = self.xb
            self.uUSV_log[:, i:i+1] = self.uUSV
            self.s_UAV_log[:, i:i+1] = self.problemCent.s_UAV.value
            self.s_USV_log[:, i:i+1] = self.problemCent.s_USV.value
            self.hor_solution_durations.append(self.problemCent.last_solution_duration)
        else:
            self.xb_log[:, i:i+1] = self.xb_traj[0:self.nUSV, 0:1]

        if self.DISTRIBUTED:
            self.hor_solution_durations.append(self.problemUAV.last_solution_duration)

        if self.PARALLEL:
            self.UAV_inner_traj_log[:, i:i+1] = self.x_traj_inner
            self.vert_inner_traj_log[:, i:i+1] = self.xv_traj_inner
            self.hor_inner_solution_durations.append(self.problemUAVFast.last_solution_duration)
            self.vert_inner_solution_durations.append(self.problemVertFast.last_solution_duration)
        else:
            self.vert_solution_durations.append(self.problemVert.last_solution_duration)

    def send_control_to_USV(self, uUSV):
        USV_input_msg = AccelStamped()
        USV_input_msg.accel.linear.x = uUSV[0]
        USV_input_msg.accel.linear.y = uUSV[1]
        USV_input_msg.header.stamp = rospy.Time.now()
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            # DEBUG: Adds message droput
            print "DOPPRED"
            pass
        else:
            self.USV_input_pub.publish(USV_input_msg)

    def send_traj_to_USV(self, x_traj):
        traj_msg = mat_to_multiarray_stamped(x_traj, self.T+1, self.nUAV)
        traj_msg.header.stamp = rospy.Time.now()
        if self.ADD_DROPOUT and (self.i >= self.dropout_lower_bound and \
            self.i <= self.dropout_upper_bound):
            # DEBUG: Adds message droput
            pass
        else:
            self.traj_pub.publish(traj_msg)

    def publish_HIL_control(self, uUAV, wdes):
        phi_cmd, theta_cmd = get_cmd_angle(uUAV, wdes, self.xv)
        axes = [phi_cmd, theta_cmd, wdes, 0.0, 0x02]
        UAV_msg = Joy(Header(), axes, [])
        self.UAV_publisher.publish(UAV_msg)

    # ----------------------------------------

    def store_data(self, test_info_str = None):
        experiment_index_pub = self.experiment_index_pub
        CENTRALISED = self.CENTRALISED
        DISTRIBUTED = self.DISTRIBUTED
        PARALLEL = self.PARALLEL
        T = self.T
        SAMPLING_RATE = self.SAMPLING_RATE
        used_solver = self.used_solver

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
        experiment_index_pub.publish(Int8(i))

        info_str = str(datetime.datetime.now()) + '\ntype: '
        if CENTRALISED:
            info_str += 'Centralised\n'
        elif DISTRIBUTED:
            info_str+= 'Distributed\n'
        elif PARALLEL:
            info_str += 'Parallel\n'

        info_str += 'simulation length: ' + str(sim_len) + '\n'
        info_str += 'horizon: ' + str(T) + '\n'
        info_str += 'sampling rate: ' + str(SAMPLING_RATE) + '\n'
        info_str += 'UAV used horizontal solver: ' + used_solver + '\n'
        info_str += 'and vertical solver: ' + self.vert_used_solver + '\n'
        info_str += 'Delay length [iterations]: ' + str(self.delay_len) + '\n'
        info_str += ("HIL setup" if self.USE_HIL else "Local setup") + " was used\n"
        info_str += "USV was at altitude: " + str(self.hb)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/info.txt', [info_str], fmt="%s")
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/x_log.txt', self.x_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/xv_log.txt', self.xv_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_traj_log.txt', self.UAV_traj_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_traj_log.txt', self.vert_traj_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUAV_log.txt', self.uUAV_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/wdes_log.txt', self.wdes_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_iteration_durations.txt', self.iteration_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_time_stamps.txt', self.UAV_times)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_solution_durations.txt', self.vert_solution_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.txt', self.hor_solution_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_vert_log.txt', self.s_vert_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/obj_val_log.txt', self.obj_val_log)
        if self.CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_traj_log.txt', self.USV_traj_log)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_UAV_log.txt', self.s_UAV_log)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/s_USV_log.txt', self.s_USV_log)
        if self.PARALLEL:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_hor_inner_durations.txt', self.hor_inner_solution_durations)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_inner_durations.txt', self.vert_inner_solution_durations)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_inner_traj_log.txt', self.UAV_inner_traj_log)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/vert_inner_traj_log.txt', self.vert_inner_traj_log)
        if test_info_str is not None:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/test_info.txt', [test_info_str], fmt="%s")

        if self.CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/xb_log.txt', self.xb_log)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/uUSV_log.txt', self.uUSV_log)
        if not self.CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV/USV_traj_log.txt', self.USV_traj_log)

        return i

    def plot_results(self, real_time):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        plt.title("UAV Simulation")

        [_, num_USV_trajs] = self.USV_traj_log.shape
        [_, sim_len] = self.UAV_traj_log.shape
        dl = self.params.dl
        ds = self.params.ds
        hs = self.params.hs
        T = self.T
        T_inner = self.T_inner

        forbidden_area_1 = Polygon([ (dl, 0),\
                                     (ds, hs),\
                                     (35, hs),\
                                     (35, 0)], True)
        forbidden_area_2 = Polygon([ (-dl, 0),\
                                     (-ds, hs),\
                                     (-35, hs),\
                                     (-35, 0)], True)
        p2 = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)
        p2.set_color('r')

        if self.PARALLEL:
            # There will be gaps in received trajectory info, fill the gaps out
            ref_vec = np.empty((self.nUSV*(self.T+1), 1))
            ref_vec.fill(np.nan)
            for j in range(sim_len):
                if np.isnan(self.USV_traj_log[:, j]).any():
                    self.USV_traj_log[:, j:j+1] = ref_vec
                else:
                    ref_vec = self.USV_traj_log[:, j:j+1]
                # ref_col = j - j%self.INTER_ITS
                # self.USV_traj_log[:, j] = self.USV_traj_log[:, ref_col]

        if real_time:
            distance = np.sqrt( np.square(self.x_log[0, :] - self.xb_log[0, :])\
                + np.square(self.x_log[1, :] - self.xb_log[1, :]) )
            distance = fill_lost_values(np.reshape(distance, (1, -1)))
            signum = fill_lost_values(np.sign(self.x_log[0:1, :] - self.xb_log[0:1, :]))
            distance = np.dot(np.diag(distance.flatten()), signum.T)
            # ax3.plot(range(sim_len), self.wdes_log.T)
            # ax3.plot(range(sim_len+1), self.xv_log[1, :].T)
            for t in range(sim_len):
                if rospy.is_shutdown():
                    break
                # safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
                # p1 = PatchCollection([safe_circle], alpha=0.1)
                # ax1.add_collection(p1)
                USV_traj = np.reshape(self.USV_traj_log[:,t], \
                    (self.nUSV, T+1), order='F')
                UAV_traj = np.reshape(self.UAV_traj_log[:,t],\
                    (self.nUAV, T+1), order='F')

                vert_traj = \
                    np.reshape(self.vert_traj_log[:,t], (2, T+1), order='F')

                vert_inner_traj = \
                    np.reshape(self.vert_inner_traj_log[:,t], (2, T_inner+1), order='F')

                pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
                    (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )
                sign_traj = np.sign(UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])
                pred_dist = np.dot(np.diag(pred_dist), sign_traj[:,None])

                # used_vert_traj = self.calculated_vert_trajs[:, t:t+1]
                # used_dist_traj = self.calculated_dist_trajs[:, t:t+1]

                # Predicted trajectories
                ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
                ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')

                # Actual trajectories
                ax1.plot(self.x_log[0, 0:t+1], self.x_log[1, 0:t+1], 'bx')
                ax1.plot(self.xb_log[0, 0:t+1], self.xb_log[1, 0:t+1], 'rx')

                # ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t]) # <--- ACCELERATION, AWESOME STUFF!
                ax2.plot(distance[0:t+1], self.xv_log[0, 0:t+1], 'b')
                ax2.plot(pred_dist, vert_traj[0, :], 'g')
                ax2.plot(pred_dist[0:self.T_inner+1], vert_inner_traj[0, :], 'y')
                # ax2.plot(range(T+1), used_vert_traj, 'y')
                # DEBUG block
                # print np.concatenate((pred_dist, used_dist_traj), axis=1)
                # ax2.plot(range(T+1), pred_dist, 'g')
                # ax2.plot(range(T+1), used_dist_traj, 'y')
                # ax2.plot(range(T_inner+1), vert_inner_traj[0, :], 'r')

                # ax2.plot(distance[0:t+1], self.xv_log[0, 0:t+1], 'b')
                # # ax2.plot(pred_dist, vert_traj[0, :], 'g')
                # ax2.plot(pred_dist, used_vert_traj, 'g')
                # ax2.plot(used_dist_traj, used_vert_traj, 'y')
                # ax2.plot(pred_dist[0:T_inner+1], vert_inner_traj[0, :], 'r')

                ax2.add_collection(p2)

                ax1.grid(True)
                ax2.grid(True)
                # ax3.grid(True)
                plt.pause(self.SAMPLING_TIME)

                ax1.cla()
                ax2.cla()

        ax1.plot(self.x_log[0, :], self.x_log[1, :], 'bx')
        ax1.plot(self.xb_log[0, :], self.xb_log[1, :], 'rx')
        # ax2.plot(distance, xv_log[0, :], 'b')
        ax1.grid(True)
        ax2.grid(True)

        # safe_circle = Circle((xb_log[0, sim_len], xb_log[1, sim_len]), ds)
        # p1 = PatchCollection([safe_circle], alpha=0.2)

        # ax1.add_collection(p1)
        ax2.add_collection(p2)

        plt.show()

    # Allows for stopping an object from receiving ROS messages.
    # Useful if a new instance is created, but old object is still kept
    # for other purposes. If this function is not called, the old and new
    # instances will both be subscribed to the same topic. I can't remember
    # right now why that is a problem, but it did cause me issues previously.
    def deinitialise(self):
        if self.CENTRALISED:
            self.USV_state_sub.unregister()
        else:
            self.USV_traj_sub.unregister()
            self.traj_pub.unregister()
        if self.USE_HIL:
            self.imu_sub.unregister()
            self.height_sub.unregister()
            self.vel_sub.unregister()
            self.gps_sub.unregister()
            self.attitude_sub.unregister()

    # ---------- Callbacks -----------

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

    def USV_traj_callback(self, msg):
        self.USVApprox.put_traj( msg )

    def USV_state_callback(self, msg):
        self.USV_state_queue.put(msg)
