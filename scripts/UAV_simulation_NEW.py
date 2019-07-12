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
from helper_classes import StateApproximator, StampedTrajQueue, StampedMsgQueue
from helper_functions import get_dist_traj, mat_to_multiarray_stamped, shift_trajectory, lat_long_to_pos, fill_lost_values
from math import atan, asin, acos
# from new_callbacks import *
from rendezvous_problem.msg import Float32MultiArrayStamped, StateStamped
from geometry_msgs.msg import AccelStamped
from std_msgs.msg import Int8
from Dynamics import get_cmd_angle
from IMPORT_ME import ADD_DROPOUT

class UAV_simulator():

    def __init__(self, problem_params):
        self.T = problem_params.T
        self.T_inner = problem_params.T_inner
        A = problem_params.A
        self.A = A
        B = problem_params.B
        self.B = B
        Ab = problem_params.Ab
        Bb = problem_params.Bb
        Q = problem_params.Q
        P = problem_params.P
        R = problem_params.R
        Av = problem_params.Av
        self.Av = Av
        Bv = problem_params.Bv
        self.Bv = Bv
        Qv = problem_params.Qv
        Pv = problem_params.Pv
        Rv = problem_params.Rv
        self.used_solver = problem_params.used_solver
        params = problem_params.params
        self.delay_len = problem_params.delay_len
        [nUAV, mUAV] = B.shape
        [nUSV, mUSV] = Bb.shape
        [nv, mv] = Bv.shape
        [self.nUAV, self.mUAV, self.nUSV, self.mUSV, self.nv, self.mv] = \
            [nUAV, mUAV, nUSV, mUSV, nv, mv]
        self.KUAV = problem_params.KUAV
        self.KVert = problem_params.KVert
        self.lookahead = problem_params.lookahead
        self.params = problem_params.params
        self.CENTRALISED = problem_params.CENTRALISED
        self.DISTRIBUTED = problem_params.DISTRIBUTED
        self.PARALLEL = problem_params.PARALLEL
        self.SAMPLING_RATE = problem_params.SAMPLING_RATE
        self.SAMPLING_TIME = problem_params.SAMPLING_TIME
        self.USE_ROS = problem_params.USE_ROS
        self.INTER_ITS = problem_params.INTER_ITS
        self.long_ref = None
        self.lat_ref = None

        self.problemCent = CentralisedProblem(self.T, A, B, Ab, Bb, Q, P, R,\
            self.used_solver, params)
        self.problemUAV = UAVProblem(self.T, A,  B,  Q, P, R, nUSV,\
            self.used_solver, params)
        self.problemVert = VerticalProblem(self.T, Av, Bv, Qv, Pv, Rv,\
            'CVXPY', params)

        self.problemUAVFast = FastUAVProblem(self.T_inner, A, B, Q, P, R, params)
        self.problemVertFast = FastVerticalProblem(self.T_inner, Av, Bv, Qv, Pv, Rv, 'OSQP', params)

        # These must be initialised here since they appear in callbacks
        self.USV_trajectories = np.empty((nUSV*(self.T+1), 1))
        self.xb_log = np.empty((nUSV, 1))
        # self.xb_m = np.nan
        self.xb_m = None
        self.i = 0
        self.USVApprox = StampedTrajQueue(0.0)
        self.USV_state_queue = StampedMsgQueue(0.0)
        # self.USVApprox = StateApproximator(nUSV, self.T, self.delay_len, anti_switch=False)
        self.x_m = np.empty((nUAV, 1))
        self.x_m.fill(np.nan)
        self.xv_m = np.empty((nv, 1))
        self.xv_m.fill(np.nan)

        # --------------------------- ROS SETUP ----------------------------------
        # rospy.init_node('UAV_main')
        self.rate = rospy.Rate(self.SAMPLING_RATE)
        self.USV_input_pub = rospy.Publisher('USV_input', AccelStamped, queue_size = 10)
        self.experiment_index_pub = rospy.Publisher('experiment_index', Int8, queue_size=1, latch=True)
        if self.CENTRALISED:
            self.USV_state_sub = rospy.Subscriber(\
                'USV_state', StateStamped, self.USV_state_callback)
        elif self.DISTRIBUTED:
            self.USV_traj_sub = rospy.Subscriber(\
                'USV_traj', Float32MultiArrayStamped, self.USV_traj_callback)
            self.traj_pub = rospy.Publisher('UAV_traj', Float32MultiArrayStamped, queue_size = 10)
        if self.USE_ROS:
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

    def simulate_problem(self, sim_len, x_val, xv_val):
        CENTRALISED = self.CENTRALISED
        DISTRIBUTED = self.DISTRIBUTED
        PARALLEL = self.PARALLEL
        SAMPLING_RATE = self.SAMPLING_RATE
        USE_ROS = self.USE_ROS
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        nv = self.nv
        mv = self.mv
        T = self.T
        problemCent = self.problemCent
        problemUAV = self.problemUAV
        problemVert = self.problemVert
        USV_input_pub = self.USV_input_pub
        A = self.A
        B = self.B
        Av = self.Av
        Bv = self.Bv
        lookahead = self.lookahead
        amin = self.params.amin
        amax = self.params.amax
        amin_b = self.params.amin_b
        amax_b = self.params.amax_b
        self.i = 0

        self.x_m = x_val
        self.xv_m = xv_val
        x_log  = np.empty((nUAV, sim_len+1))
        x_log.fill(np.nan)
        xv_log = np.empty((nv, sim_len+1))
        xv_log.fill(np.nan)
        self.xb_log = np.empty((nUSV, sim_len+1))
        self.xb_log.fill(np.nan)
        uUAV_log = np.empty((mUAV, sim_len))
        uUAV_log.fill(np.nan)
        UAV_trajectories = np.empty((nUAV*(T+1), sim_len))
        UAV_trajectories.fill(np.nan)
        self.USV_trajectories = np.empty((nUSV*(T+1), sim_len))
        self.USV_trajectories.fill(np.nan)
        # xb_traj = np.empty((nUSV*(T+1), 1))
        # xb_traj.fill(np.nan)
        xb_traj = None  #TEST
        vert_trajectories = np.empty((2*(T+1), sim_len))
        vert_trajectories.fill(np.nan)
        vert_inner_trajectories = np.empty((2*(self.T_inner+1), sim_len))
        vert_inner_trajectories.fill(np.nan)
        wdes_log = np.empty((mv, sim_len))
        wdes_log.fill(np.nan)
        last_used_dist_traj = np.full((T+1, 1), np.nan)
        last_used_vert_traj = np.full((T+1, 1), np.nan)
        calculated_dist_trajs = np.full((T+1, sim_len), np.nan)
        calculated_vert_trajs = np.full((T+1, sim_len), np.nan)
        # Times for all the data in all of the logs. Matches iteration to data-piece
        UAV_times = np.empty((1, sim_len+1))
        UAV_times.fill(np.nan)
        if CENTRALISED:
            # self.xb_m = np.nan
            self.xb_m = None
            self.USV_state_queue = StampedMsgQueue(0.0)
        else:   # DISTRIBUTED
            # self.USVApprox = StateApproximator(nUSV, self.T,  self.delay_len)
            self.USVApprox = StampedTrajQueue(0.0)

        if CENTRALISED and PARALLEL:
            print '######################################################'
            print 'Parallel solving is not supported for centralised case'
            print '######################################################'
            return

        # iteration_durations = [None]*sim_len
        iteration_durations = []
        dist_solution_durations = []
        cent_solution_durations = []
        vert_solution_durations = []   # TODO: DO WE KNOW THAT WE ALWAYS SOLVE THE PROBLEM? NOT IN PARALLEL CASE?

        # while CENTRALISED and np.isnan(self.xb_m).any():
        while CENTRALISED and self.xb_m is None:
            # Centralised case: Wait for the first message from USV to arrive
            self.xb_m = self.USV_state_queue.get()
            if rospy.is_shutdown():
                break
            self.rate.sleep()
        t_since_update = 0
        loop_iter_time_sum = 0
        start = time.time()
        # -------------------- MAIN LOOP ---------------------
        for i in range(sim_len):
            # print i
            self.i = i
            if rospy.is_shutdown():
                break

            # Weird indexing to preserve dimensions
            x_log[:, i:i+1]  = self.x_m
            xv_log[:, i:i+1] = self.xv_m

            # # DEBUG
            # if DISTRIBUTED:
            #     if i == 40 and DISTRIBUTED:
            #         self.USVApprox.set_delay_time(1.0)
            #         # print "NOOOOOOOOOOOOOW!!!!!!!!"
            #     if i == 300 and DISTRIBUTED:
            #         self.USVApprox.set_delay_time(0.0)
            # # END DEBUG

            if CENTRALISED:
                # # DEBUG
                # if i == 40:
                #     self.USV_state_queue.set_delay_time(1.0)
                # if i == 300 and CENTRALISED:
                #     self.USV_state_queue.set_delay_time(0.0)
                # # END DEBUG
                # # We shouldn't have to worry about this returning nan since above
                # # we've waited until a message from USV actually arrives
                xb_m_msg = self.USV_state_queue.get()
                self.xb_m = np.array([[xb_m_msg.pose.position.x], [xb_m_msg.pose.position.y],\
                    [xb_m_msg.twist.linear.x], [xb_m_msg.twist.linear.y]])
            # ------------------- SOLVE OPTIMISATION PROBLEMS --------------------
            if i==0 or not PARALLEL:
                if CENTRALISED:
                    start_cent = time.time()
                    problemCent.solve(self.x_m, self.xb_m)
                    end_cent = time.time()
                    cent_solution_durations.append(end_cent - start_cent)
                    x_traj = problemCent.x.value
                    xb_traj = problemCent.xb.value
                    uUAV = problemCent.u[  0:mUAV, 0:1].value
                    uUSV = problemCent.ub[ 0:mUSV, 0:1].value
                    dist_traj = get_dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
                    # self.USV_trajectories[:, i:i+1] = xb_traj
                elif DISTRIBUTED:
                    try:
                        xb_traj = self.USVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        xb_traj = shift_trajectory(xb_traj, nUSV, 1)

                    if xb_traj is None:#np.isnan(xb_traj).any():    #TEST
                        # We don't know where USV is, apply no control input
                        uUAV = np.matrix([[0], [0]])
                        x_traj = np.asarray(\
                            problemUAV.predict_trajectory( self.x_m, np.zeros((mUAV*T,1)) ))
                        # # dist_traj = np.empty((nUAV*(T+1), 1))
                        # dist_traj.fill(np.nan)
                        dist_traj = None    #TEST
                        # Needed for parallel
                        problemUAV.x.value = x_traj
                        problemUAV.u.value = np.zeros((mUAV*T, 1))
                    else:
                        start_dist = time.time()
                        problemUAV.solve(self.x_m, np.asarray(xb_traj))  # TODO: Make naturally array, not matrix
                        duration = time.time() - start_dist
                        dist_solution_durations.append(duration)
                        x_traj = problemUAV.x.value
                        dist_traj = get_dist_traj(x_traj, \
                            np.reshape(self.USVApprox.traj_msg.array.data, (-1,1)),\
                            T, nUAV, nUSV)
                        dist_traj_signed = get_dist_traj(x_traj, \
                            np.reshape(self.USVApprox.traj_msg.array.data, (-1,1)),\
                            T, nUAV, nUSV, True)

                    uUAV = problemUAV.u[ 0:mUAV, 0:1].value

            elif i%self.INTER_ITS == 0 and PARALLEL:
                # if CENTRALISED:
                #     problemCent.solve_threaded(self.x_m, self.xb_m)
                # el
                if DISTRIBUTED:
                    try:
                        xb_traj = self.USVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajecctory if no new trajectory is available
                        # TODO: WHY ONLY SHIFTED ONE STEP, IF THIS IS ONLY DONE EVERY INTER_ITS ITERATION?
                        # SHOULDN'T IT BE SHIFTED INTER_ITS STEPS INSTEAD???
                        xb_traj = shift_trajectory(xb_traj, nUSV, 1)

                    if xb_traj is None: #np.isnan(xb_traj).any():       #TEST
                        # We don't know where USV is, apply no control input
                        uUAV = np.matrix([[0], [0]])
                        x_traj = np.asarray(\
                            problemUAV.predict_trajectory( self.x_m, np.zeros((mUAV*T,1)) ))
                        dist_traj = np.empty((nUAV*(T+1), 1))
                        dist_traj.fill(np.nan)
                        # Needed for parallel
                        problemUAV.x.value = x_traj
                        problemUAV.u.value = np.zeros((mUAV*T, 1))
                        # For parallel: t_since_update increases with each iteration
                        # If it's not reset to 0 here, it can grow arbitrarily large
                        # without the problem ever being solved (happens if UAV never
                        # receives information about the USV). The intermediate
                        # controller further on will fail to work if it thinks that the
                        # knows x_traj is too outdated. Therefore, by setting
                        # t_since_update to 0, we're telling it that this x_traj is
                        # actually up to date
                        problemUAV.t_since_update = 0
                        t_since_update = problemUAV.t_since_update
                    else:
                        problemUAV.solve_threaded(self.x_m, xb_traj)

            # ------------------------------------------------------------------
            # ----- SET CONTROL INPUTS AND DISTANCE TRAJECTEORY (PARALLEL) -----
            # if CENTRALISED and PARALLEL:
            #     # TODO: Add shifting and such to xb_traj?
            #     # self.USV_trajectories[:, i:i+1] = xb_traj
            #     if problemCent.t_since_update == 0:
            #         uUAV = problemCent.u[ 0:mUAV, 0:1].value
            #         uUSV = problemCent.ub[0:mUSV, 0:1].value
            #         x_traj = problemCent.x.value
            #         xb_traj = problemCent.xb.value
            #         dist_traj = get_dist_traj(x_traj, xb_traj, T, nUAV, nUSV)
            #     else:
            #         dist_traj = shift_trajectory(dist_traj, 1, 1)
            #         # Using linear feedback intermediate controller
            #         uUAV = self.KUAV*(self.x_m  -  x_traj[(t_since_update+lookahead)*nUAV:\
            #             (t_since_update+1+lookahead)*nUAV])
            #         uUSV = self.KUSV*(self.xb_m - xb_traj[(t_since_update+lookahead)*nUSV\
            #         :(t_since_update+1+lookahead)*nUSV])
            #         uUAV = -np.clip(uUAV, amin,   amax)
            #         uUSV = -np.clip(uUSV, amin_b, amax_b)
            #
            #     problemCent.t_since_update += 1
            #     t_since_update = problemCent.t_since_update
            # el

            if DISTRIBUTED and PARALLEL:
                if problemUAV.t_since_update == 0:
                    # uUAV = problemUAV.u[ 0:mUAV, 0:1].value
                    x_traj = problemUAV.x.value
                    # = shift_trajectory(problemUAV.x.value, nUAV, problemUAV.t_since_prev_update)
                    if x_traj is None:                      # DEBUG
                        print "X TRAJ WAS NONE HERE!"       # DEBUG
                        print "U:", uUAV

                    # Seems like CVXPy problem .solve() can sometimes return None
                    if self.USVApprox.traj_msg is not None and x_traj is not None:
                        dist_traj = get_dist_traj(x_traj, \
                            np.reshape(self.USVApprox.traj_msg.array.data, (-1,1)),\
                            T, nUAV, nUSV)
                        dist_traj_signed = get_dist_traj(x_traj, \
                            np.reshape(self.USVApprox.traj_msg.array.data, (-1,1)),\
                            T, nUAV, nUSV, True)
                    else:
                        dist_traj = None
                    if not np.isnan(problemUAV.last_solution_duration):
                        dist_solution_durations.append(problemUAV.last_solution_duration)
                else:
                    if dist_traj is not None:
                        dist_traj = shift_trajectory(dist_traj, 1, 1)
                        dist_traj_signed = shift_trajectory(dist_traj_signed, 1, 1)
                    # Shifts x_traj, so it becomes the most accurate prediction possible
                    x_traj = shift_trajectory(x_traj, nUAV, 1)
                    # xb_traj = shift_trajectory(xb_traj, nUSV, 1)
                # TODO: Add lookahead back, or remove it completely?
                # uUAV = self.KUAV*(self.x_m  -  x_traj[(t_since_update)*nUAV:\
                #     (t_since_update+1)*nUAV])
                # uUAV = -np.clip(uUAV, amin,   amax)
                self.problemUAVFast.solve(self.x_m[0:(self.T_inner+1)*nUAV], x_traj[0:(self.T_inner+1)*nUAV])
                uUAV = self.problemUAVFast.u[ 0:mUAV, 0:1].value
                problemUAV.t_since_update += 1
                t_since_update = problemUAV.t_since_update

            UAV_trajectories[:, i:i+1] = x_traj # TODO: Should I update this by shifting or something, in parallel case?

            # ----------------------- VERTICAL PROBLEM ---------------------------
            # --------- solve problem -----------
            if dist_traj is None:
                # We don't know where the USV is right now
                wdes_current = 0
            elif not PARALLEL or i==0:
                vert_start = time.time()
                problemVert.solve(self.xv_m, 0.0, np.asarray(dist_traj))  # TODO: Make dist naturally array, not matrix
                vert_end = time.time()
                vert_solution_durations.append(vert_end - vert_start)
                # wdes_current = problemVert.wdes[0:mv, 0:1].value
                # vert_trajectories[:, i:i+1] = problemVert.xv.value
            elif PARALLEL and i%self.INTER_ITS == 0:
                problemVert.solve_threaded(self.xv_m, 0.0, np.asarray(dist_traj))
                #DEBUG
                last_used_dist_traj = dist_traj_signed

            # ------------ Pick wdes -------------
            #if np.isnan(dist_traj).any():
            if dist_traj is None:
                # We don't know where USV is (I think that's the reason at least)
                if i == 0:
                    vert_trajectories[:, i:i+1] = problemVert.\
                        predict_trajectory(self.xv_m, np.zeros((mv*T, 1)))
                else:
                    vert_trajectories[:, i:i+1] =\
                        shift_trajectory(vert_trajectories[:, i-1:i], nv, 1)
            elif not PARALLEL:
                wdes_current = problemVert.wdes[0:mv, 0:1].value
                vert_trajectories[:, i:i+1] = problemVert.xv.value
            else: # PARALLEL
                if problemVert.t_since_update == 0:
                    last_used_vert_traj = problemVert.xv[::2].value
                    # Shift trajectory to account for time passed since calculations started
                    vert_trajectories[:, i:i+1] = problemVert.xv.value
                    # = shift_trajectory(problemVert.xv.value, nv, problemVert.t_since_prev_update)
                    # TODO: I think the line above here can crash if the vertical
                    # problem solution at i==0 fails, which happens occasionally.
                    # This problem can be solved by setting problemVert.xv
                    # to a predicted trajectory using problemVert.predict_trajectory
                    # before the simulation begins
                else:
                    vert_trajectories[:, i:i+1] =\
                        shift_trajectory(vert_trajectories[:, i-1:i], nv, 1)
                T_inner = self.T_inner

                if np.isnan(vert_trajectories[0:(T_inner+1)*nv, i:i+1]).any():
                    # Filling wdes_current with NaN symbolises that there was
                    # a failure with calculating it. This failure is adressed
                    # later
                    wdes_current = np.nan
                else:
                    self.problemVertFast.solve(self.xv_m[0:(self.T_inner+1)*nv],\
                        vert_trajectories[0:(T_inner+1)*nv, i:i+1])
                    wdes_current = self.problemVertFast.wdes[0:mv, 0:1].value
                    vert_inner_trajectories[:, i:i+1] = self.problemVertFast.xv.value
                    # wdes_current = -self.KVert*(self.xv_m - \
                    #     vert_trajectories[nv:2*nv, i:i+1])
                    # wdes_current = np.clip(wdes_current,\
                    #     self.params.wmin, self.params.wmax)

            if DISTRIBUTED and PARALLEL:
                problemVert.t_since_update += 1

            calculated_dist_trajs[:, i:i+1] = last_used_dist_traj
            calculated_vert_trajs[:, i:i+1] = last_used_vert_traj

            # # OOOOOOOOOOLLLLLLLLLLLDDDDDDDDDDDDD TODO: FINISH ALL THIS!!!
            # if not np.isnan(dist_traj).any():
            #     # NOT PARALLEL, OR PARALLEL AND i==0
            #     vert_start = time.time()
            #     problemVert.solve(self.xv_m, 0.0, np.asarray(dist_traj))  # TODO: Make dist naturally array, not matrix
            #     vert_end = time.time()
            #     vert_solution_durations.append(vert_end - vert_start)
            #     wdes_current = problemVert.wdes[0:mv, 0:1].value
            #     vert_trajectories[:, i:i+1] = problemVert.xv.value
            #     # TODO: Should anything else be done if the position of the USV is unknown?
            # else:
            #     # WHETER PARALLEL OR NOT, AS LONG AS DIST TRAJ IS NAN
            #     wdes_current = 0
            #
            #     if i == 0:
            #         vert_trajectories[:, i:i+1] = problemVert.\
            #             predict_trajectory(self.xv_m, np.zeros((nv*T, 1)))
            #         # vert_trajectories[:, i:i+1] = np.kron( np.ones((T+1,1)), self.xv_m )
            #     else:
            #         vert_trajectories[:, i:i+1] =\
            #             shift_trajectory(vert_trajectories[:, i-1:i], 2, 1)

            wdes_log[:, i:i+1] = wdes_current
            uUAV_log[:, i:i+1] = uUAV;

            UAV_times[:, i:i+1] = rospy.get_time()

            # ----------- SIMULATE DYNAMICS / PUBLISH CONTROL INPUTS -------------
            self.USV_trajectories[:, i:i+1] = xb_traj
            if xb_traj is not None:
                self.xb_log[:, i:i+1] = xb_traj[0:nUSV, 0:1]
            else:
                # We don't know where USV is, leave default value (nan)
                pass

            if wdes_current is None:
                wdes_current = 0
                print('Wdes was None, iteration:', i)
                # wdes_current = self.params.wmax
            elif np.isnan(wdes_current).any():
                wdes_current = self.params.wmax
                print('Wdes was nan, iteration:', i)

            if CENTRALISED:
                USV_input_msg = AccelStamped()
                USV_input_msg.accel.linear.x = uUSV[0]
                USV_input_msg.accel.linear.y = uUSV[1]
                USV_input_msg.header.stamp = rospy.Time.now()
                if not ADD_DROPOUT or not (i >= 80 and i <= 130): #DEBUG
                    USV_input_pub.publish(USV_input_msg)
                # xb_m = Ab*xb_m + Bb*uUSV  # REMOVE, publish message for USV node instead
            if not USE_ROS:
                self.x_m  =  A*self.x_m  +  B*uUAV
                self.xv_m = Av*self.xv_m + Bv*wdes_current
            if USE_ROS:
                phi_cmd, theta_cmd = get_cmd_angle(uUAV, wdes_current, self.xv_m)
                axes = [phi_cmd, theta_cmd, wdes_current, 0.0, 0x02]
                UAV_msg = Joy(Header(), axes, [])
                self.UAV_publisher.publish(UAV_msg)


            if DISTRIBUTED and (not PARALLEL or t_since_update == 1):
                # t_since_update == 1 means that we just solved the problem
                # usually we check t_since_update == 0, but this block comes
                # just after incrementing t_since_update
                traj_msg = mat_to_multiarray_stamped(x_traj, T+1, nUAV)
                traj_msg.header.stamp = rospy.Time.now()
                if not ADD_DROPOUT or not (i >= 80 and i <= 130):
                    # print time.time()
                    self.traj_pub.publish(traj_msg)  # TODO: CHANGE THIS. JUST DON'T USE A QUEUE



            # ---------------------------- SLEEP ---------------------------------
            end = time.time()
            # print(end - start)
            # loop_iter_time_sum += end-start
            iteration_durations.append(end-start)
            self.rate.sleep()
            # if USE_ROS:
            #     rate.sleep()
            # else:
            #     try:
            #         time.sleep(SAMPLING_TIME - end + start)
            #     except:
            #         pass
            start = time.time()

        try:
            print "MAXIMUM SUCCESSFULL ITERS:", max(problemVert.num_iters_log)
        except:
            print "problemVert.num_iters_log seems empty"

        x_log[:, -nUAV:sim_len+1]  = self.x_m
        xv_log[:, -2:sim_len+1] = self.xv_m
        self.x_log = x_log
        self.xv_log = xv_log
        self.UAV_trajectories = UAV_trajectories
        self.vert_trajectories = vert_trajectories
        self.vert_inner_trajectories = vert_inner_trajectories
        self.calculated_dist_trajs = calculated_dist_trajs
        self.calculated_vert_trajs = calculated_vert_trajs
        self.uUAV_log = uUAV_log
        self.iteration_durations = iteration_durations
        self.vert_solution_durations = vert_solution_durations
        self.UAV_times = UAV_times
        if CENTRALISED:
            self.cent_solution_durations = cent_solution_durations
            self.hor_solution_durations = cent_solution_durations
        else:
            self.dist_solution_durations = dist_solution_durations
            self.hor_solution_durations = dist_solution_durations

    def new_simulate_problem(self, sim_len, x_val, xv_val):
        initialize_logs()   # Allocate memory for all logs, fill with nan etc

        x_log[:, 0:1] = self.x_m
        xv_log[:, 0:1] = self.xv_m

        # If centralised, get initial USV state estimate
        xb_m_msg = None
        while self.CENTRALISED and xb_m_msg is None:
            xb_m_msg = self.USV_state_queue.get()
            if rospy.is_shutdown():
                return
            self.rate.sleep()
        self.xb_m = np.array(\
            [[xb_m_msg.pose.position.x], [xb_m_msg.pose.position.y],\
            [xb_m_msg.twist.linear.x], [xb_m_msg.twist.linear.y]])

        # If distributed or parallel, get initial USV trajectory estimation
        while not self.CENTRALISED and xb_traj is None:
            try:
                xb_traj = self.USVApprox.get_traj()
            except IndexError:
                # This happens if the queue is empty
                xb_traj = None
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
                    # TODO: Shouldn't USV_state_queue use the same approach as
                    # USVApprox? It is currently not clear what the call returns
                    # if there are no elements in the queue
                    xb_m_msg = self.USV_state_queue.get()
                    self.xb_m = np.array(\
                        [[xb_m_msg.pose.position.x], [xb_m_msg.pose.position.y],\
                        [xb_m_msg.twist.linear.x], [xb_m_msg.twist.linear.y]])
                elif self.DISTRIBUTED or \
                    (self.PARALLEL and i % self.INTER_ITS == 0):
                    try:
                        xb_traj = self.USVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        xb_traj = shift_trajectory(xb_traj, nUSV, 1)

            # ------- Horizontal Problem --------
            if self.CENTRALISED:
                solve_centralised_problem()
            elif self.DISTRIBUTED or (self.PARALLEL and i == 0):
                solve_distributed_problem()
            elif self.PARALLEL and i % self.INTER_ITS == 0:
                solve_parallel_problem()
            else:
                print "Please select a problem type: centralised, distributed, or parallel"
                return

            if self.PARALLEL:
                solve_inner_problem()

            uUAV = get_horizontal_control()

            # ------- Vertical Problem --------
            if self.dist_traj is not None:
                if not self.PARALLEL or i == 0:
                    solve_vertical_problem()
                elif self.PARALLEL and i % self.INTER_ITS == 0:
                    solve_vertical_problem_threaded()

            if self.PARALLEL:
                solve_inner_vertical_problem()
                # TODO: Add corresponding statement for horizontal problem
                # Only update t_since_last_update if the vertical problem wasn't
                # solved inbetween the call to solve_inner_vertical_problem
                # and this statement
                if self.problemVert.last_solution_is_used:
                    self.problemVert.t_since_last_update += 1

            wdes_current = get_vertical_control()

            # ------- Update Logs --------
            update_logs()

            # ------- Simulate Dynamics / Apply Control --------
            if self.CENTRALISED:
                send_state_to_USV()

            if self.DISTRIBUTED or \
                (self.PARALLEL and self.problemUAV.t_since_last_update == 0):
                send_traj_to_USV()

            if not USE_ROS:
                self.x_m  =  self.A*self.x_m  +  self.B*uUAV
                self.xv_m = self.Av*self.xv_m + self.Bv*wdes_current
                # TODO: Where is xb_m updated? In a callback? It should be
                # either right here or in a callback
            else:
                publish_HIL_control()

            # ------- Sleep --------
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        # ------------ END OF LOOP ------------
        # TODO: Make sure that you don't need to update logs here

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
        dir_path = '/home/student/robbj_experiment_results/'
        while dir_already_exists:
            i += 1
            dir_already_exists = os.path.isdir(dir_path + 'Experiment_' + str(i))

        os.mkdir(dir_path + 'Experiment_' + str(i))
        experiment_index_pub.publish(Int8(i))

        info_str = str(datetime.datetime.now()) + '\ntype: '
        if CENTRALISED:
            info_str += 'Centralised\n'
        else:
            info_str+= 'Distributed\n'
        info_str += 'parallel: '
        if PARALLEL:
            info_str += 'True\n'
        else:
            info_str += 'False\n'
        info_str += 'simulation length: ' + str(sim_len) + '\n'
        info_str += 'horizon: ' + str(T) + '\n'
        info_str += 'sampling rate: ' + str(SAMPLING_RATE) + '\n'
        info_str += 'UAV used solver: ' + used_solver
        # TODO: Add simulated delay info???
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/info.txt', [info_str], fmt="%s")
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/x_log.txt', self.x_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/xv_log.txt', self.xv_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_trajectories.txt', self.UAV_trajectories)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUAV_log.txt', self.uUAV_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_iteration_durations.txt', self.iteration_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/vertical_durations.txt', self.vert_solution_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_time_stamps.txt', self.UAV_times)
        if CENTRALISED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_trajectories.txt', self.USV_trajectories)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.txt', self.cent_solution_durations)
        else:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/UAV_horizontal_durations.txt', self.dist_solution_durations)
        if test_info_str is not None:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/test_info.txt', [test_info_str], fmt="%s")

        return i

    def plot_results(self, real_time):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        plt.title("UAV Simulation")

        [_, num_USV_trajs] = self.USV_trajectories.shape
        [_, sim_len] = self.UAV_trajectories.shape
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
                if np.isnan(self.USV_trajectories[:, j]).any():
                    self.USV_trajectories[:, j:j+1] = ref_vec
                else:
                    ref_vec = self.USV_trajectories[:, j:j+1]
                # ref_col = j - j%self.INTER_ITS
                # self.USV_trajectories[:, j] = self.USV_trajectories[:, ref_col]

        if real_time:
            distance = np.sqrt( np.square(self.x_log[0, :] - self.xb_log[0, :])\
                + np.square(self.x_log[1, :] - self.xb_log[1, :]) )
            distance = fill_lost_values(np.reshape(distance, (1, -1)))
            signum = fill_lost_values(np.sign(self.x_log[0:1, :] - self.xb_log[0:1, :]))
            distance = np.dot(np.diag(distance.flatten()), signum.T)
            for t in range(sim_len):
                if rospy.is_shutdown():
                    break
                # safe_circle = Circle((xb_log[0, t], xb_log[1, t]), ds)
                # p1 = PatchCollection([safe_circle], alpha=0.1)
                # ax1.add_collection(p1)
                USV_traj = np.reshape(self.USV_trajectories[:,t], \
                    (self.nUSV, T+1), order='F')
                UAV_traj = np.reshape(self.UAV_trajectories[:,t],\
                    (self.nUAV, T+1), order='F')

                vert_traj = \
                    np.reshape(self.vert_trajectories[:,t], (2, T+1), order='F')

                vert_inner_traj = \
                    np.reshape(self.vert_inner_trajectories[:,t], (2, T_inner+1), order='F')

                pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
                    (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )
                sign_traj = np.sign(UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])
                pred_dist = np.dot(np.diag(pred_dist), sign_traj[:,None])

                used_vert_traj = self.calculated_vert_trajs[:, t:t+1]
                used_dist_traj = self.calculated_dist_trajs[:, t:t+1]

                # Predicted trajectories
                ax1.plot(UAV_traj[0, 0:T+1], UAV_traj[1, 0:T+1], 'g')
                ax1.plot(USV_traj[0, 0:T+1], USV_traj[1, 0:T+1], 'y')
                # Actual trajectories
                ax1.plot(self.x_log[0, 0:t+1], self.x_log[1, 0:t+1], 'bx')
                ax1.plot(self.xb_log[0, 0:t+1], self.xb_log[1, 0:t+1], 'rx')

                # ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t]) # <--- ACCELERATION, AWESOME STUFF!
                ax2.plot(range(t+1), self.xv_log[0, 0:t+1], 'b')
                # ax2.plot(range(T+1), vert_traj[0, :], 'g')
                # ax2.plot(range(T+1), used_vert_traj, 'y')
                print np.concatenate((pred_dist, used_dist_traj), axis=1)
                ax2.plot(range(T+1), pred_dist, 'g')
                ax2.plot(range(T+1), used_dist_traj, 'y')
                ax2.plot(range(T_inner+1), vert_inner_traj[0, :], 'r')
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

    def deinitialise(self):
        if self.CENTRALISED:
            self.USV_state_sub.unregister()
        elif self.DISTRIBUTED:
            self.USV_traj_sub.unregister()
            self.traj_pub.unregister()
        if self.USE_ROS:
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
        # global xv_m
        self.xv_m[0] = msg.data

    def velocity_callback(self, msg):
        # global xv_m, x_m
        self.x_m[2]  = msg.vector.x
        self.x_m[3]  = msg.vector.y
        self.xv_m[1] = msg.vector.z

    def pos_callback(self, msg):
        # global x_m, long_ref, lat_ref
        R = 6378138.12

        if self.long_ref is None:
            self.long_ref = msg.longitude
        if self.lat_ref is None:
            self.lat_ref = msg.latitude

        phi_gps = msg.latitude
        phi_ref = self.lat_ref
        lambda_gps = msg.longitude
        lambda_ref = self.long_ref

        self.x_m[0:2] = lat_long_to_pos(phi_gps, lambda_gps, phi_ref, lambda_ref, R);

    def attitude_callback(self, msg):
        # global phi, theta
        qw = msg.quaternion.w
        qx = msg.quaternion.x
        qy = msg.quaternion.y
        qz = msg.quaternion.z
        self.phi = atan( 2*(qw*qx + qy*qz)/(1 - 2*(qx*qx + qy*qy)) )
        self.theta = asin(2*(qw*qy-qz*qx))

    def USV_traj_callback(self, msg):
        # xbhat_m_traj = np.empty((self.nUSV, self.T+1))
        # stride = msg.array.layout.dim[1].stride
        # for t in range(self.T+1):
        #     for i in range(self.nUSV):
        #         temp = msg.array.data[stride*t + i]
        #         xbhat_m_traj[i][t] = temp

        # temp = np.reshape(xbhat_m_traj, (-1, 1), order='F')

        # TODO: In parallel case, this will only fill every tenth element. I think?
        # Or how does the callback actually work?
        # self.USV_trajectories[:, self.i:self.i+1] = temp
        # self.xb_log[:, self.i:self.i+1] = temp[0:self.nUSV, 0:1]
        # num_times_to_add = 1
        # if self.PARALLEL:
        #     num_times_to_add = self.INTER_ITS
        # for i in range(num_times_to_add):
        #     self.USV_trajectories = temp if (self.USV_trajectories is None) else \
        #         np.concatenate((self.USV_trajectories, temp), axis=1)
        #     self.xb_log = temp[0:self.nUSV, 0:1] if (self.xb_log is None) else \
        #         np.concatenate((self.xb_log, temp[0:self.nUSV, 0:1]), axis=1)
        self.USVApprox.put_traj( msg )

    def USV_state_callback(self, msg):
        # TODO: Implement delay here as well?
        self.USV_state_queue.put(msg)
        # print time.time()
        # self.xb_m = np.array([[msg.pose.position.x], [msg.pose.position.y],\
        #     [msg.twist.linear.x], [msg.twist.linear.y]])

        # self.xb_log[:, self.i:self.i+1] = self.xb_m
        # if self.xb_log is None:
        #     self.xb_log = self.xb_m
        # else:
        #     # This guarantees that we don't add multiple trajectories per
        #     # iteration by accident
        #     [_, len] = self.xb_log.shape
        #     if self.i + 1 > len:
        #         # We are at a new iteration, append trajectory
        #         # At iteration 0, length is made equal to 1, therefore self.i+1
        #         self.xb_log = np.concatenate((self.xb_log, self.xb_m), axis=1)
        #     else:
        #         # We are still on the same iteration as previously, overwrite
        #         # last added trajectory
        #         self.xb_log[:, self.i:self.i+1] = self.xb_m

        # self.xb_log = self.xb_m if (self.xb_log is None) else \
        #     np.concatenate((self.xb_log, self.xb_m), axis=1)
