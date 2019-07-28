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
        self.UAV_traj_log = np.empty((self.nUAV*(self.T+1), 1))
        self.x_log = np.empty((self.nUAV, 1))
        # self.UAVApprox = StateApproximator(self.nUAV, self.T, self.delay_len, anti_switch=False)
        self.UAVApprox = StampedTrajQueue(0.0)
        self.input_queue = StampedMsgQueue(0.0)
        self.i = 0
        self.USV_stopped_at_iter = -1   # This one breaks even though it shouldn't, so I added it here to be safe

        # --------------------------- ROS SETUP ----------------------------------
        # rospy.init_node('USV_main')
        rospy.Subscriber('experiment_index', Int8, self.experiment_index_callback)
        if not self.CENTRALISED:
            self.traj_pub = rospy.Publisher('USV_traj', Float32MultiArrayStamped, queue_size = 10)
            self.UAV_traj_sub = rospy.Subscriber(\
                'UAV_traj', Float32MultiArrayStamped, self.UAV_traj_callback)
        elif self.CENTRALISED:
            self.state_pub = rospy.Publisher('USV_state', StateStamped, queue_size = 10)
            self.USV_input_sub = rospy.Subscriber(\
                'USV_input', AccelStamped, self.USV_input_callback)
        self.rate = rospy.Rate(SAMPLING_RATE)

    # TODO: Add storing of distance in non-centralised cases. Needed for USV_should_stop
    def simulate_problem(self, sim_len, xb_val):
        self.reset(sim_len, xb_val)

        self.xb = xb_val

        # TODO: If both UAV and USV wait for estimate without publishing,
        # won't they lock and never progress?????
        # If distributed or parallel, get initial UAV trajectory estimation
        if not self.CENTRALISED:
            while self.x_traj is None:
                # TODO: Sometimes self.xb_traj seems to be something other than an array, fix that
                self.send_traj_to_UAV(np.asarray(self.xb_traj))
                try:
                    self.x_traj = self.UAVApprox.get_traj()
                except IndexError:
                    # This happens if the queue is empty
                    self.x_traj = None
                if rospy.is_shutdown():
                    return
                self.rate.sleep()

        # If centralised, get first control input
        if self.CENTRALISED:
            uUSV_msg = None
            while uUSV_msg is None:
                self.send_state_to_UAV(self.xb)
                try:
                    uUSV_msg = self.input_queue.get()
                except IndexError:
                    pass
                if rospy.is_shutdown():
                    return
                self.rate.sleep()
            self.uUSV = np.array([[uUSV_msg.accel.linear.x],\
                [uUSV_msg.accel.linear.y]])

        start = time.time()
        for i in range(sim_len):
            self.i = i
            if rospy.is_shutdown():
                return

            # Receive data from UAV
            if not i == 0:
                if self.CENTRALISED:
                    try:
                        uUSV_msg = self.input_queue.get()
                        self.uUSV = np.array([[uUSV_msg.accel.linear.x],\
                            [uUSV_msg.accel.linear.y]])
                    except IndexError:
                        self.uUSV = np.zeros((self.mUSV, 1))
                elif self.DISTRIBUTED or \
                    (self.PARALLEL and i % self.INTER_ITS == 0):
                    try:
                        self.x_traj = self.UAVApprox.get_traj()
                    except IndexError:
                        # Use shifted old trajectory if no new trajectory is available
                        self.x_traj = shift_trajectory(self.x_traj, self.nUAV, 1)

            # ------- Solving Problem --------
            if self.DISTRIBUTED or (self.PARALLEL and i == 0):
                self.solve_distributed_problem(self.xb, self.x_traj)
            elif self.PARALLEL and i % self.INTER_ITS == 0:
                self.problemUSV.solve_threaded(self.xb, self.x_traj)

            if not self.CENTRALISED:
                # Update values in xb_traj and x_traj
                self.update_trajectories()

            if self.PARALLEL:
                self.solve_inner_problem(self.xb, self.xb_traj)

            (self.uUSV) = self.get_control()

            self.update_logs(self.i)

            # ------- Simulate Dynamics / Apply Control --------
            if self.CENTRALISED:
                self.send_state_to_UAV(self.xb)
            if self.DISTRIBUTED or \
                (self.PARALLEL and self.problemUSV.t_since_update == 0):
                self.send_traj_to_UAV(self.xb_traj)

            if self.PARALLEL and self.problemUSV.last_solution_is_used:
                self.problemUSV.t_since_update += 1

            self.xb = self.Ab*self.xb + self.Bb*self.uUSV

            # ------- Sleep --------
            end = time.time()
            self.iteration_durations.append(end-start)
            self.rate.sleep()
            start = time.time()

        # ------------ END OF LOOP ------------
        self.xb_log[:, sim_len:sim_len+1] = self.xb
        if not self.CENTRALISED:
            self.x_log = self.x_traj[0:self.nUAV, 0:1]   # TODO: Put an if-statement around allocaiton of memory for this

    def reset(self, sim_len, xb_0):
        self.xb_log = np.full((self.nUSV, sim_len+1), np.nan)
        self.uUSV_log = np.full((self.mUSV, sim_len), np.nan)

        if not self.CENTRALISED:
            self.USV_traj_log = np.full((self.nUSV*(self.T+1), sim_len), np.nan)
            self.x_log = np.full((self.nUAV, sim_len+1), np.nan)
            self.UAV_traj_log = np.full( (self.nUAV*(self.T+1), sim_len),\
                np.nan )
        if self.PARALLEL:
            self.USV_inner_traj_log = np.full((self.nUSV*(self.T_inner+1),\
                sim_len), np.nan )

        self.USV_times = np.full((1, sim_len+1), np.nan)
        self.iteration_durations = []
        if not self.CENTRALISED:
            self.hor_solution_durations = []
        if self.DISTRIBUTED:
            self.hor_inner_solution_durations = []

        # Initial predicted trajectory assumes no control signal applied
        self.xb_traj = self.problemUSV.predict_trajectory(xb_0, \
            np.zeros( (self.mUSV*self.T, 1) ))
        self.x_traj = None  # Always contains most up-to-date UAV predicted traj
        # Always contains most up-to-date current distance between vehicles
        self.dist = None

        self.USV_should_stop = False
        self.UAVApprox = StampedTrajQueue(0.0)
        self.input_queue = StampedMsgQueue(0.0)

    def solve_distributed_problem(self, xb, x_traj):
        T = self.T
        nUAV = self.nUAV
        nUSV = self.nUSV
        # TODO: Add code handlign USV_should_stop earlier
        start_time = time.time()
        self.problemUSV.solve(xb, x_traj, self.USV_should_stop)
        end_time = time.time()
        self.hor_solution_durations.append(end_time - start_time)

    def solve_inner_problem(self, xb, xb_traj):
        # TODO: Move out of function? It's just one line of code?
        # TODO: Actually, you have to add storing of times for this
        self.problemUSVFast.solve(xb[0:(self.T_inner+1)*self.nUSV],\
            xb_traj[0:(self.T_inner+1)*self.nUAV])

    def get_control(self):
        if self.CENTRALISED:
            # Input was set in beggining of the main loop already
            return self.uUSV
        elif self.DISTRIBUTED:
            return self.problemUSV.ub[0:self.mUSV, 0:1].value
        elif self.PARALLEL:
            return self.problemUSVFast.ub[0:self.mUSV, 0:1].value

    def update_trajectories(self):
        if self.CENTRALISED:
            # There are no trajectories to update
            pass
        elif self.DISTRIBUTED:
            self.xb_traj = self.problemUSV.xb.value
        elif self.PARALLEL:
            if self.problemUSV.t_since_update == 0:
                self.xb_traj = self.problemUSV.xb.value
                # TODO: Add this variable to USV problemClass
                self.problemUSV.last_solution_is_used = True
            else:
                self.xb_traj = shift_trajectory(self.xb_traj, self.nUSV, 1)

    def update_logs(self, i):
        self.xb_log[:, i:i+1] = self.xb
        self.uUSV_log[:, i:i+1] = self.uUSV
        self.USV_times[:, i:i+1] = rospy.get_time()

        if not self.CENTRALISED:
            self.USV_traj_log[:, i:i+1] = self.xb_traj
            self.UAV_traj_log[:, i:i+1] = self.x_traj

        if self.PARALLEL:
            self.USV_inner_traj_log[:, i:i+1] = self.problemUSVFast.xb.value

    def send_traj_to_UAV(self, xb_traj):
        traj_msg = mat_to_multiarray_stamped(xb_traj, self.T+1, self.nUSV)
        traj_msg.header.stamp = rospy.Time.now()
        if ADD_DROPOUT and (self.i >= 80 and self.i <= 130):
            #DEBUG Adds message dropout
            pass
        else:
            self.traj_pub.publish(traj_msg)

    def send_state_to_UAV(self, xb):
        if ADD_DROPOUT and (self.i >= 80 and self.i <= 130):
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

    # ------------------------------------------

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
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_traj_log.txt', self.USV_traj_log)
            np.savetxt(dir_path + 'Experiment_'+str(i)+'/USV_horizontal_durations.txt', self.hor_solution_durations)

    def plot_results(self, real_time):
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)
        plt.title("USV Simulation")

        [_, sim_len] = self.USV_traj_log.shape
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
                if np.isnan(self.UAV_traj_log[:, j]).any():
                    self.UAV_traj_log[:, j:j+1] = ref_vec
                else:
                    ref_vec = self.UAV_traj_log[:, j:j+1]
                # ref_col = j - j%self.INTER_ITS
                # self.UAV_traj_log[:, j] = self.UAV_traj_log[:, ref_col]

        if real_time:
            if self.UAV_traj_log is None:
                num_UAV_trajs = 0
            else:
                [_, num_UAV_trajs] = self.UAV_traj_log.shape
            for t in range(sim_len):
                if rospy.is_shutdown():
                    break
                safe_circle = Circle((self.xb_log[0, t], self.xb_log[1, t]), ds)
                p1 = PatchCollection([safe_circle], alpha=0.1)
                ax1.add_collection(p1)
                if num_UAV_trajs > t:
                    UAV_traj = np.reshape(self.UAV_traj_log[:,t],\
                        (self.nUAV, self.T+1), order='F')
                    # print UAV_traj[0, 0:self.T+1]
                    ax1.plot(UAV_traj[0, 0:self.T+1], UAV_traj[1, 0:self.T+1], 'g')
                if self.DISTRIBUTED:
                    # We only have access to trajectory in distributed case
                    USV_traj = np.reshape(self.USV_traj_log[:,t],\
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

    # Allows for stopping an object from receiving ROS messages.
    # Useful if a new instance is created, but old object is still kept
    # for other purposes. If this function is not called, the old and new
    # instances will both be subscribed to the same topic. I can't remember
    # right now why that is a problem, but it did cause me issues previously.
    def deinitialise(self):
        if self.DISTRIBUTED:
            self.UAV_traj_sub.unregister()
        elif self.CENTRALISED:
            self.USV_input_sub.unregister()

    # -------------- CALLBACKS ---------------

    # Receives planned trajectory of the UAV
    def UAV_traj_callback(self, msg):
        # global UAVApprox, UAV_traj_log, x_log
        nUAV = self.nUAV
        T = self.T
        xhat_m_traj = np.empty((nUAV, T+1))
        stride = msg.array.layout.dim[1].stride
        for t in range(T+1):
            for i in range(nUAV):
                xhat_m_traj[i][t] = msg.array.data[stride*t + i]

        temp = np.reshape(xhat_m_traj, (-1, 1), order='F')

        # self.UAV_traj_log[:, self.i:self.i+1] =  temp
        # self.x_log[:, self.i:self.i+1] = temp[0:nUAV, 0:1]
        # num_times_to_add = 1
        # if self.PARALLEL:
        #     num_times_to_add = self.INTER_ITS
        # for i in range(num_times_to_add):
        #     self.UAV_traj_log = temp if (self.UAV_traj_log is None) else\
        #         np.concatenate((self.UAV_traj_log, temp), axis=1)
        #     self.x_log = temp[0:nUAV, 0:1] if (self.x_log is None) else\
        #         np.concatenate((self.x_log, temp[0:nUAV, 0:1]), axis=1)

        self.UAVApprox.put_traj(msg)

    # Used in centralised case. Received control input that should be applied
    def USV_input_callback(self, msg):
        self.input_queue.put(msg)
        # print time.time()
        # self.uUSV = np.array([[msg.accel.linear.x],[msg.accel.linear.y]])

    # Used for the function store_data(), to store data into the same folder
    # as the UAV_simulation_NEW.py
    def experiment_index_callback(self, msg):
        self.experiment_index = msg.data
