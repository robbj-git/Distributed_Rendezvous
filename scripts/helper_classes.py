from rendezvous_problem.msg import Float32MultiArrayStamped
from helper_functions import shift_trajectory, get_traj_dir, get_cos_angle_between
from IMPORT_ME import SAMPLING_TIME, USE_COMPLETE_HORIZONTAL
from matrices_and_parameters import n_UAV, n_USV, nv, wmax, wmin, wmin_land, kl, vmax, vmax_b
import numpy as np
import Queue
import rospy
import time # for DEBUG, remove later
import copy

class Parameters():

    def __init__(self, amin, amax, amin_b, amax_b, hs, ds, dl, \
        wmin, wmax, wmin_land, kl, vmax, vmax_b, vmin_b, ang_max = 0):
        self.amin = amin
        self.amax = amax
        self.amin_b = amin_b
        self.amax_b = amax_b
        self.hs = hs
        self.ds = ds
        self.dl = dl
        self.wmin = wmin
        self.wmax = wmax
        self.wmin_land = wmin_land
        self.kl = kl
        self.v_max = vmax
        self.v_max_b = vmax_b
        self.v_min_b = vmin_b
        self.ang_max = ang_max

    def __str__(self):
        string = ''
        string += "amin: " + str(self.amin) + ";"
        string += "amax: "+ str(self.amax) + ";"
        string += "amin_b: "+ str(self.amin_b) + ";"
        string += "amax_b: "+ str(self.amax_b) + ";"
        string += "hs: "+ str(self.hs) + ";"
        string += "ds: "+ str(self.ds) + ";"
        string += "dl: "+ str(self.dl) + ";"
        string += "wmin: "+ str(self.wmin) + ";"
        string += "wmax: "+ str(self.wmax) + ";"
        string += "wmin_land: "+ str(self.wmin_land) + ";"
        string += "kl: "+ str(self.kl) + ";"
        string += "v_max: "+ str(self.v_max) + ";"
        return string

class StampedMsgQueue():

    def __init__(self, delay_time):
        self.delay_duration = rospy.Duration.from_sec(delay_time)
        # self.traj_msg = Float32MultiArrayStamped()
        # self.traj_msg.array.data = None
        self.msg = None
        self.queue = Queue.Queue()

    def get(self):
        queue_copy = copy.copy(self.queue.queue)
        new_msg = None
        most_recent_message_found = False

        while not most_recent_message_found:
            try:
                msg_candidate = queue_copy.popleft()
                if rospy.Time.now() - msg_candidate.header.stamp > self.delay_duration:
                    # Pop the same msg from the original queue
                    new_msg = self.queue.get_nowait()
                    # print "Got thing with delay", (rospy.Time.now() - msg_candidate.header.stamp).to_sec()
                else:
                    # print "Too recent", (rospy.Time.now() - msg_candidate.header.stamp).to_sec()
                    most_recent_message_found = True
            except IndexError:
                # print 'was empty'
                most_recent_message_found = True

        if new_msg is None:
            # If self.delay_time > 0, the queue isn't necessary empty. This
            # just means that no element in the queue was sufficiently old for
            # simulating the desired delay
            raise IndexError('Queue was empty')
        else:
            self.msg = new_msg
            return self.msg

    def put(self, msg):
        if self.queue.full():
            print "Duuuude, queue was totally full, despite having infinite length...?"
            try:
                self.queue.get_nowait()
            except Queue.Empty:
                pass
        self.queue.put_nowait(msg)

    def set_delay_time(self, new_delay_time):
        self.delay_duration = rospy.Duration.from_sec(new_delay_time)

class StampedTrajQueue():

    def __init__(self, delay_time, should_shift = False):
        self.delay_duration = rospy.Duration.from_sec(delay_time)
        # self.traj_msg = Float32MultiArrayStamped()
        # self.traj_msg.array.data = None
        self.traj_msg = None
        self.traj_queue = Queue.Queue()
        self.should_shift = should_shift

    def get_traj(self):
        queue_copy = copy.copy(self.traj_queue.queue)
        new_traj_msg = None
        most_recent_message_found = False

        while not most_recent_message_found:
            try:
                msg_candidate = queue_copy.popleft()
                if rospy.Time.now() - msg_candidate.header.stamp > self.delay_duration:
                    # Pop the same msg from the original queue
                    new_traj_msg = self.traj_queue.get_nowait()
                    # print "Got the thing"
                else:
                    # print "Too recent", (rospy.Time.now() - msg_candidate.header.stamp).to_sec()
                    most_recent_message_found = True
            except IndexError:
                # print 'was empty'
                most_recent_message_found = True

        if new_traj_msg is None:
            # If self.delay_time > 0, the queue isn't necessary empty. This
            # just means that no element in the queue was sufficiently old for
            # simulating the desired delay
            raise IndexError('Queue was empty')
        else:
            self.traj_msg = new_traj_msg
            return_array = np.reshape(self.traj_msg.array.data, (-1, 1))
            if self.should_shift:
                d = int(np.floor((rospy.Time.now() - msg_candidate.header.stamp).to_sec()/SAMPLING_TIME))
                print "shifted", d
                return shift_trajectory(return_array, 4, d)   # TODO: Somehow get hold of variable nUAV so that you don't have to hard-code 4
            else:
                return return_array

    def put_traj(self, traj_msg):
        if self.traj_queue.full():
            print "Duuuude, queue was totally full, despite having infinite length...?"
            # Attempt to remove element from queue
            try:
                self.traj_queue.get_nowait()
            except Queue.Empty:
                pass
        self.traj_queue.put_nowait(traj_msg)
        # print rospy.get_time(), traj_msg.header.stamp.secs + traj_msg.header.stamp.nsecs/1000000000.0

    def set_delay_time(self, new_delay_time):
        self.delay_duration = rospy.Duration.from_sec(new_delay_time)

class DataAnalysisParams():

    def __init__(self):
        # TODO: Avoid hard-coding here
        if not USE_COMPLETE_HORIZONTAL:
            self.nUAV = n_UAV
        else:
            self.nUAV = 8
        self.nUSV = n_USV
        self.nv = nv
        self.T = np.nan
        self.wmax = wmax
        self.wmin = wmin
        self.wmin_land = wmin_land
        self.kl = kl
        self.vmax = vmax
        self.vmax_b = vmax_b

# class StateApproximator():
#
#     def __init__(self, n, T, delay_len, anti_switch=True):
#         self.ignore_changes = False
#         self.its_since_started_ignoring = 0
#         self.num_rapid_changes = 0
#         self.its_since_rapid_change = 0
#         # self.traj_msg = np.full( (n*(T+1), 1), np.nan )
#         self.traj_msg = Float32MultiArrayStamped()
#         # self.traj_msg.array.data = [np.nan]*n*(T+1)
#         self.traj_msg.array.data = None     #TEST
#         self.traj_queue = Queue.Queue(delay_len+1)
#         self.n = n
#         self.T = T
#         self.delay_len = delay_len
#         self.anti_switch = anti_switch
#
#     def get_traj(self):
#         is_empty = False
#         try:
#             traj_msg_new = self.traj_queue.get_nowait()
#         except Queue.Empty:
#             is_empty = True
#
#         if is_empty:
#             # No new trajectory received, return shifted old trajectory
#             if self.traj_msg.array.data is not None:
#                 self.traj_msg = \
#                     shift_traj_msg(self.traj_msg, self.n, SAMPLING_TIME)
#                 # print "Shifted traj"
#                 return np.reshape(self.traj_msg.array.data, (-1, 1))
#             else:
#                 return None
#
#         quit_early = False
#         #np.isnan(self.traj_msg.array.data).any() or not self.anti_switch:
#         if self.traj_msg.array.data is None or not self.anti_switch:    #TEST
#             # self.traj_msg never before set, or anti-switch is turned off
#             quit_early = True
#         else:
#             old_dir = get_traj_dir(\
#                 np.reshape(self.traj_msg.array.data, (-1,1)), self.n)
#             new_dir = get_traj_dir(\
#                 np.reshape(traj_msg_new.array.data, (-1,1)), self.n)
#             cos_angle = get_cos_angle_between(old_dir, new_dir)
#             # direction of previously used trajectory was 0
#             if np.isnan(cos_angle):
#                 quit_early = True
#
#         # Special case
#         if quit_early:
#             self.ignore_changes = False
#             self.its_since_started_ignoring = 0
#             self.num_rapid_changes = 0
#             self.its_since_rapid_change = 0
#             self.traj_msg = \
#                 shift_traj_msg(traj_msg_new, self.n, SAMPLING_TIME)
#                 # shift_trajectory(traj_new, self.n, self.delay_len)
#             return np.reshape(self.traj_msg.array.data, (-1, 1))
#
#         if cos_angle < 0:
#             self.num_rapid_changes += 1
#             self.its_since_rapid_change = 0
#
#         if self.ignore_changes:
#             self.its_since_started_ignoring += 1
#             if self.its_since_started_ignoring > self.delay_len + 1:
#                 self.ignore_changes = False
#                 self.its_since_started_ignoring = 0
#                 self.num_rapid_changes = 0
#                 self.its_since_rapid_change = 0
#         else:
#             if self.num_rapid_changes >= 2:
#                 self.ignore_changes = True
#
#         if self.ignore_changes and cos_angle < 0:
#             # Use old trajectory
#             self.traj_msg = shift_traj_msg(self.traj_msg, self.n, 1)
#             return np.reshape(self.traj_msg.array.data, (-1, 1))
#         else:
#             # Use new trajectory
#             self.traj_msg = \
#                 shift_traj_msg(traj_msg_new, self.n, SAMPLING_TIME)
#                 # shift_trajectory(traj_new, self.n, self.delay_len)
#             return np.reshape(self.traj_msg.array.data, (-1, 1))
#
#     def put_traj(self, traj_msg):
#         if self.traj_queue.full():
#             try:
#                 self.traj_queue.get_nowait()
#             except Queue.Empty:
#                 pass
#         self.traj_queue.put_nowait(traj_msg)
#
#     # def peek(self):
#     #     print "size before:", self.traj_queue.qsize()
#     #     queue_iterable = copy.copy(self.traj_queue.queue)
#     #     print queue_iterable.pop()
#     #     print "progress!"
#     #     print "size after:", self.traj_queue.qsize()
