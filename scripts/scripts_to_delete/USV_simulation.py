#!/usr/bin/env python
import rospy
import numpy as np
from helper_classes import StampedTrajQueue, StampedMsgQueue
from helper_functions import mat_to_multiarray_stamped, shift_trajectory
from problemClasses import USVProblem, FastUSVProblem
from rendezvous_problem.msg import Float32MultiArrayStamped, StateStamped
from geometry_msgs.msg import AccelStamped
from std_msgs.msg import Int8
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
import time
from IMPORT_ME import ADD_DROPOUT

class USV_simulator():

    def __init__(self, problem_params):
        self.experiment_index = -1
        self.T = problem_params.T
        self.T_inner = problem_params.T_inner
        B = problem_params.B
        self.Ab = problem_params.Ab
        self.Bb = problem_params.Bb
        Q = problem_params.Q
        P = problem_params.P
        R = problem_params.R
        self.lookahead = problem_params.lookahead
        self.used_solver = problem_params.used_solver
        self.params = problem_params.params
        self.delay_len = problem_params.delay_len
        [self.nUAV, self.mUAV] = B.shape
        [self.nUSV, self.mUSV] = self.Bb.shape
        # [nv, mv] = Bv.shape
        # [self.nUAV, self.mUAV, self.nUSV, self.mUSV, self.nv, self.mv] = \
        #     [nUAV, mUAV, nUSV, mUSV, nv, mv]
        # [self.nUSV, self.mUSV, self.nUAV, self.mUAV] = \
        #     [nUSV, mUSV, nUAV, mUAV]
        self.CENTRALISED = problem_params.CENTRALISED
        self.DISTRIBUTED = problem_params.DISTRIBUTED
        self.PARALLEL = problem_params.PARALLEL
        self.SAMPLING_RATE = problem_params.SAMPLING_RATE
        self.SAMPLING_TIME = problem_params.SAMPLING_TIME
        self.USE_ROS = problem_params.USE_ROS
        self.INTER_ITS = problem_params.INTER_ITS
        self.KUSV = problem_params.KUSV
        SAMPLING_RATE = self.SAMPLING_RATE
        USE_ROS = self.USE_ROS

        self.problemUSV = USVProblem(self.T, self.Ab, self.Bb,  Q, P, R,\
            self.nUAV, self.used_solver, self.params)

        self.problemUSVFast = FastUSVProblem(self.T_inner, self.Ab, self.Bb, Q, P, R,\
            self.params)

        # These must be initialised here since they appear in callbacks
        self.UAV_trajectories = np.empty((self.nUAV*(self.T+1), 1))
        self.x_log = np.empty((self.nUAV, 1))
        # self.UAVApprox = StateApproximator(self.nUAV, self.T, self.delay_len, anti_switch=False)
        self.UAVApprox = StampedTrajQueue(0.0)
        self.input_queue = StampedMsgQueue(0.0)
        self.i = 0
        self.USV_stopped_at_iter = -1   # This one breaks even though it shouldn't, so I added it here to be safe

        # --------------------------- ROS SETUP ----------------------------------
        # rospy.init_node('USV_main')
        rospy.Subscriber('experiment_index', Int8, self.experiment_index_callback)
        if self.DISTRIBUTED:
            self.traj_pub = rospy.Publisher('USV_traj', Float32MultiArrayStamped, queue_size = 10)
            self.UAV_traj_sub = rospy.Subscriber(\
                'UAV_traj', Float32MultiArrayStamped, self.UAV_traj_callback)
        elif self.CENTRALISED:
            self.state_pub = rospy.Publisher('USV_state', StateStamped, queue_size = 10)
            self.USV_input_sub = rospy.Subscriber(\
                'USV_input', AccelStamped, self.USV_input_callback)
        self.rate = rospy.Rate(SAMPLING_RATE)

    def simulate_problem(self, sim_len, xb_val):
        xb_m = xb_val
        CENTRALISED = self.CENTRALISED
        DISTRIBUTED = self.DISTRIBUTED
        PARALLEL = self.PARALLEL
        SAMPLING_RATE = self.SAMPLING_RATE
        USE_ROS = self.USE_ROS
        nUAV = self.nUAV
        mUAV = self.mUAV
        nUSV = self.nUSV
        mUSV = self.mUSV
        T = self.T
        Ab = self.Ab
        Bb = self.Bb
        KUSV = self.KUSV
        lookahead = self.lookahead
        amin_b = self.params.amin_b
        amax_b = self.params.amax_b
        self.i = 0

        xb_log  = np.empty((nUSV, sim_len+1))
        xb_log.fill(np.nan)
        uUSV_log = np.empty((mUSV, sim_len))
        uUSV_log.fill(np.nan)
        self.USV_trajectories = np.empty((nUSV*(T+1), sim_len))
        self.USV_trajectories.fill(np.nan)
        USV_times = np.empty((1, sim_len))
        USV_times.fill(np.nan)
        self.UAV_trajectories = np.empty((nUAV*(T+1), sim_len)) # Only for debug
        self.UAV_trajectories.fill(np.nan)
        # x_traj = np.empty((nUAV*(T+1), 1))
        # x_traj.fill(np.nan)
        x_traj = None   #TEST
        self.x_log = np.empty((nUAV, sim_len))                  # Only for debug
        self.x_log.fill(np.nan)
        self.uUSV = np.zeros((mUSV, 1))
        # self.UAVApprox = StateApproximator(self.nUAV, self.T, self.delay_len)
        self.UAVApprox = StampedTrajQueue(0.0)
        self.input_queue = StampedMsgQueue(0.0)
        iteration_durations = []
        dist_solution_durations = []
        self.USV_stopped_at_iter = -1
        t_since_update = 0
        dist = np.inf   # Stores horizontal distance from UAV
        USV_should_stop = False

        if CENTRALISED and PARALLEL:
            print '######################################################'
            print 'Parallel solving is not supported for centralised case'
            print '######################################################'
            return

        start = time.time()
        for i in range(sim_len):        # TODO: Change to keep on going sort of for ever?
            # print i
            self.i = i
            if rospy.is_shutdown():
                break

            # Weird indexing to preserves dimensions
            xb_log[:, i:i+1]  = xb_m

            # # DEBUG
            # if i == 40 and DISTRIBUTED:
            #     self.UAVApprox.set_delay_time(1.0)
            #     # print "NOOOOOOOOOOOOOW!!!!!!!!"
            # if i == 300 and DISTRIBUTED:
            #     self.UAVApprox.set_delay_time(0.0)
            # # END DEBUG
            # # DEBUG
            # if i == 40 and CENTRALISED:
            #     self.input_queue.set_delay_time(1.0)
            #     # print "NOOOOOOOOOOOOOW!!!!!!!!"
            # if i == 300 and CENTRALISED:
            #     self.input_queue.set_delay_time(0.0)
            # # END DEBUG
            # ------------------- SOLVE OPTIMISATION PROBLEMS --------------------
            if i==0 or not PARALLEL:
                if DISTRIBUTED:
                    try:
                        x_traj = self.UAVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        x_traj = shift_trajectory(x_traj, nUAV, 1)

                    # self.UAV_trajectories[:, self.i:self.i+1] = x_traj
                    if x_traj is None: #np.isnan(x_traj).any():     #TEST
                        # We don't know where UAV is, apply no control input
                        self.uUSV = np.matrix([[0], [0]])
                        xb_traj = np.asarray(\
                            self.problemUSV.predict_trajectory( xb_m, np.zeros((mUSV*T, 1)) ))
                        # Needed for parallel
                        self.problemUSV.xb.value = xb_traj
                        self.problemUSV.ub.value = np.zeros((mUSV*T, 1))
                        # For parallel case: Since problemUSV wasn't actually solved,
                        # we need to have non-zero t_since_update so that rest of
                        # program doesn't think the problem was just solved and will
                        # therefore try to access solution variables
                        self.problemUSV.t_since_update = 0
                        t_since_update = self.problemUSV.t_since_update
                    else:
                        start_dist = time.time()
                        self.problemUSV.solve(xb_m, x_traj, USV_should_stop)
                        duration = time.time() - start_dist
                        dist_solution_durations.append(duration)
                        xb_traj = self.problemUSV.xb.value

                        self.uUSV = self.problemUSV.ub[ 0:mUSV, 0:1].value
                        # THE CODE IN ELSE IS UNREACHABLE, I'M NOT SURE WHAT I WAS THINKING!!!
                        # NO SUPRISE PARALLEL COMPLETELY SUCKED!!!!!
                        # if not PARALLEL or t_since_update == 0:
                        #     self.uUSV = self.problemUSV.ub[ 0:mUSV, 0:1].value
                        # else:
                        #     # Using linear feedback intermediate controller
                        #     self.uUSV = KUSV*(xb_m  -  self.problemUSV.\
                        #         x[t_since_update*nUSV:(t_since_update+1)*nUSV].value)
                        #     self.uUSV = -np.clip(self.uUSV, amin_b, amax_b)
                elif CENTRALISED:
                    # In centralised case, we don't solve anything
                    pass
            elif i%self.INTER_ITS == 0 and PARALLEL:
                if DISTRIBUTED:
                    try:
                        x_traj = self.UAVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        x_traj = shift_trajectory(x_traj, nUAV, 1)
                    # self.UAV_trajectories[:, self.i:self.i+1] = x_traj
                    if x_traj is None:      #np.isnan(x_traj).any():    #TEST
                        # We don't know where UAV is, apply no control input
                        self.uUSV = np.matrix([[0], [0]])
                        xb_traj = np.asarray(\
                            self.problemUSV.predict_trajectory( xb_m, np.zeros((mUSV*T,1)) ))
                        # Needed for parallel
                        self.problemUSV.xb.value = xb_traj
                        self.problemUSV.ub.value = np.zeros((mUSV*T, 1))
                        # In general, t_since_update increases with each iteration
                        # If it's not reset to 1 here, it can grow arbitrarily large
                        # without the problem ever being solved (happens if USV never
                        # receives information about the UAV). The intermediate
                        # controller further on will fail to work if it thinks that the
                        # knows xb_traj is too outdated. Therefore, by setting
                        # t_since_update to 1, we're telling it that this xb_traj is
                        # actually up to date
                        self.problemUSV.t_since_update = 0
                        t_since_update = self.problemUSV.t_since_update
                    else:
                        self.problemUSV.solve_threaded(xb_m, x_traj, USV_should_stop)
                elif CENTRALISED:
                    # In centralised case, we don't solve anything
                    pass

            # -------- SET uUSV FOR DISTRIBUTED CASE ---------------
            if DISTRIBUTED and PARALLEL:
                if self.problemUSV.t_since_update == 0:
                    # self.uUSV = self.problemUSV.ub[ 0:mUSV, 0:1].value
                    xb_traj = shift_trajectory(self.problemUSV.xb.value, nUSV,\
                        self.problemUSV.t_since_prev_update)
                else:
                    # Shifts x_traj, so it becomes the most accurate prediction possible
                    xb_traj = shift_trajectory(xb_traj, nUSV, 1)
                # self.uUSV = KUSV*(xb_m  -  xb_traj[(t_since_update+lookahead)*nUSV:\
                #     (t_since_update+1+lookahead)*nUSV])
                # self.uUSV = -np.clip(self.uUSV, amin_b, amax_b)
                self.problemUSVFast.solve(xb_m[0:(self.T_inner+1)*nUSV], xb_traj[0:(self.T_inner+1)*nUSV])
                self.uUSV = self.problemUSVFast.ub[ 0:mUSV, 0:1].value

                self.problemUSV.t_since_update += 1
                t_since_update = self.problemUSV.t_since_update
            elif CENTRALISED:
                uUSV_msg = self.input_queue.get()
                if uUSV_msg is None:
                    self.uUSV = np.zeros((mUSV, 1))
                else:
                    self.uUSV = np.array([[uUSV_msg.accel.linear.x],[uUSV_msg.accel.linear.y]])

            # ----------------- SIMULATE DYNAMICS -------------------
            self.UAV_trajectories[:, i:i+1] = x_traj
            if x_traj is not None:
                self.x_log[:, self.i:self.i+1] = x_traj[0:nUAV, 0:1]
            else:
                pass
                # We don't know where UAV is, leave default value (nan)

            # # if DISTRIBUTED and not np.isnan(x_traj).any() and not USV_should_stop:
            # if DISTRIBUTED and x_traj is not None and not USV_should_stop:
            #     dist = np.sqrt( np.square(xb_m[0,0] - x_traj[0,0])\
            #         + np.square(xb_m[1,0] - x_traj[1,0]) )
            #     USV_should_stop = False if dist > self.params.ds else True
            #     if USV_should_stop:
            #         USV_stopped_at_iter = self.i

            if DISTRIBUTED:
                # We only have access to predicted trajectory in distributed case.
                # In centralised case, it is UAV_main that calculates it
                self.USV_trajectories[:, i:i+1] = xb_traj
            uUSV_log[:, i:i+1] = self.uUSV;
            USV_times[:, i:i+1] = rospy.get_time()

            # print xb_m
            # print self.uUSV
            # print '------'
            xb_m = Ab*xb_m + Bb*self.uUSV

            if CENTRALISED and (not PARALLEL or t_since_update == 1):
                # t_since_update == 1 means that we just solved the problem
                # usually we check t_since_update == 0, but this block comes
                # just after incrementing t_since_update
                state_msg = StateStamped()
                state_msg.pose.position.x = xb_m[0]
                state_msg.pose.position.y = xb_m[1]
                state_msg.twist.linear.x = xb_m[2]
                state_msg.twist.linear.y = xb_m[3]
                state_msg.header.stamp = rospy.Time.now()
                if not ADD_DROPOUT or not (i >= 80 and i <= 130): #DEBUG
                    self.state_pub.publish(state_msg)
            elif DISTRIBUTED and (not PARALLEL or t_since_update == 1):
                # t_since_update == 1 means that we just solved the problem
                # usually we check t_since_update == 0, but this block comes
                # just after incrementing t_since_update
                traj_msg = mat_to_multiarray_stamped(xb_traj, T+1, nUSV)
                traj_msg.header.stamp = rospy.Time.now()
                if not ADD_DROPOUT or not (i >= 80 and i <= 130): #DEBUG
                    self.traj_pub.publish(traj_msg)  # TODO: CHANGE THIS. JUST DON'T USE A QUEUE

            # ---------------------------- SLEEP ---------------------------------
            end = time.time()
            iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        xb_log[:, -nUSV:sim_len+1]  = xb_m
        self.xb_log = xb_log
        self.uUSV_log = uUSV_log
        self.iteration_durations = iteration_durations
        self.dist_solution_durations = dist_solution_durations
        self.USV_times = USV_times

    def store_data(self):
        while self.experiment_index < 0:
            if rospy.is_shutdown():
                break

        i = self.experiment_index
        dir_path = '/home/student/robbj_experiment_results/'
        info_str = 'USV used solver: ' + self.used_solver + '\n'
        try:
            info_str += 'USV stopped at iteration: ' + str(self.USV_stopped_at_iter)
        except Exception as e:
            print e
            print 'For some reason it still says that USV_stopped_at_iter is undefined...'

        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_info.txt', [info_str], fmt="%s")
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/xb_log.txt', self.xb_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/uUSV_log.txt', self.uUSV_log)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_iteration_durations.txt', self.iteration_durations)
        np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_time_stamps.txt', self.USV_times)
        if self.DISTRIBUTED:
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_trajectories.txt', self.USV_trajectories)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_horizontal_durations.txt', self.dist_solution_durations)

    def plot_results(self, real_time):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        plt.title("USV Simulation")

        [_, sim_len] = self.USV_trajectories.shape
        dl = self.params.dl
        ds = self.params.ds
        hs = self.params.hs

        forbidden_area_1 = Polygon([ (dl, 0),\
                                     (ds, hs),\
                                     (10, hs),\
                                     (10, 0)], True)
        forbidden_area_2 = Polygon([ (-dl, 0),\
                                     (-ds, hs),\
                                     (-10, hs),\
                                     (-10, 0)], True)
        p2 = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)

        if self.PARALLEL:
            # TODO: This shouldn't be necessary anymore!
            # There will be gaps in received trajectory info, fill the gaps out
            ref_vec = np.empty((self.nUSV*(self.T+1), 1))
            ref_vec.fill(np.nan)
            for j in range(sim_len):
                if np.isnan(self.UAV_trajectories[:, j]).any():
                    self.UAV_trajectories[:, j:j+1] = ref_vec
                else:
                    ref_vec = self.UAV_trajectories[:, j:j+1]
                # ref_col = j - j%self.INTER_ITS
                # self.UAV_trajectories[:, j] = self.UAV_trajectories[:, ref_col]

        if real_time:
            if self.UAV_trajectories is None:
                num_UAV_trajs = 0
            else:
                [_, num_UAV_trajs] = self.UAV_trajectories.shape
            for t in range(sim_len):
                if rospy.is_shutdown():
                    break
                safe_circle = Circle((self.xb_log[0, t], self.xb_log[1, t]), ds)
                p1 = PatchCollection([safe_circle], alpha=0.1)
                ax1.add_collection(p1)
                if num_UAV_trajs > t:
                    UAV_traj = np.reshape(self.UAV_trajectories[:,t],\
                        (self.nUAV, self.T+1), order='F')
                    # print UAV_traj[0, 0:self.T+1]
                    ax1.plot(UAV_traj[0, 0:self.T+1], UAV_traj[1, 0:self.T+1], 'g')
                if self.DISTRIBUTED:
                    # We only have access to trajectory in distributed case
                    USV_traj = np.reshape(self.USV_trajectories[:,t],\
                        (self.nUSV, self.T+1), order='F')
                    ax1.plot(USV_traj[0, 0:self.T+1],\
                        USV_traj[1, 0:self.T+1], 'y')
                    ax1.plot(self.x_log[0, 0:t+1], self.x_log[1, 0:t+1], 'bx')

                # pred_dist = np.sqrt( (UAV_traj[0, 0:T+1]-USV_traj[0, 0:T+1])**2 + \
                #     (UAV_traj[1, 0:T+1]-USV_traj[1, 0:T+1])**2 )

                ax1.plot(self.xb_log[0, 0:t+1], self.xb_log[1, 0:t+1], 'rx')
                # ax1.arrow(x_log[0,t], x_log[1,t], uUAV_log[0,t], uUAV_log[1,t]) # <--- ACCELERATION, AWESOME STUFF!
                # ax2.plot(distance[0:t+1], xv_log[0, 0:t+1], 'b')
                # ax2.plot(range(t+1), xv_log[0, 0:t+1], 'b')
                # ax2.plot(pred_dist, vert_traj[0, 0:T+1], 'y')
                # ax2.plot(range(t+1, t+1 + T+1), vert_traj[0, 0:T+1], 'y')
                # ax2.add_collection(p2)

                # ax3.plot([SAMPLING_TIME*i for i in range(t+1)], distance[0:t+1], 'k')

                #print "UAV speed:", np.sqrt(x_log[2,t]**2 + x_log[3,t]**2)
                #print "UAV speeds:", x_log[2,t], " , ", x_log[3,t]

                ax1.grid(True)
                # ax2.grid(True)
                # ax3.grid(True)
                plt.pause(0.01)

                ax1.cla()
                # ax2.cla()

        if self.DISTRIBUTED:
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
        if self.DISTRIBUTED:
            self.UAV_traj_sub.unregister()
        elif self.CENTRALISED:
            self.USV_input_sub.unregister()

    # -------------- CALLBACKS ---------------

    def UAV_traj_callback(self, msg):
        # global UAVApprox, UAV_trajectories, x_log
        nUAV = self.nUAV
        T = self.T
        xhat_m_traj = np.empty((nUAV, T+1))
        stride = msg.array.layout.dim[1].stride
        for t in range(T+1):
            for i in range(nUAV):
                xhat_m_traj[i][t] = msg.array.data[stride*t + i]

        temp = np.reshape(xhat_m_traj, (-1, 1), order='F')

        # self.UAV_trajectories[:, self.i:self.i+1] =  temp
        # self.x_log[:, self.i:self.i+1] = temp[0:nUAV, 0:1]
        # num_times_to_add = 1
        # if self.PARALLEL:
        #     num_times_to_add = self.INTER_ITS
        # for i in range(num_times_to_add):
        #     self.UAV_trajectories = temp if (self.UAV_trajectories is None) else\
        #         np.concatenate((self.UAV_trajectories, temp), axis=1)
        #     self.x_log = temp[0:nUAV, 0:1] if (self.x_log is None) else\
        #         np.concatenate((self.x_log, temp[0:nUAV, 0:1]), axis=1)

        self.UAVApprox.put_traj(msg)

    def USV_input_callback(self, msg):
        self.input_queue.put(msg)
        # print time.time()
        # self.uUSV = np.array([[msg.accel.linear.x],[msg.accel.linear.y]])

    def experiment_index_callback(self, msg):
        self.experiment_index = msg.data
