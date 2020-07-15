from rendezvous_problem.msg import Float32MultiArrayStamped
from helper_functions import shift_trajectory, get_traj_dir, get_cos_angle_between
from IMPORT_MAIN import SAMPLING_TIME
from IMPORT_UAV import Bv, wmax, wmin, wmin_land, kl
# from IMPORT_UAV import n_UAV, nv, wmax, wmin, wmin_land, kl
import numpy as np
import Queue
import rospy
import copy

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
            # if self.should_shift:
            #     d = int(np.floor((rospy.Time.now() - msg_candidate.header.stamp).to_sec()/SAMPLING_TIME))
            #     print "shifted", d
            #     return shift_trajectory(return_array, 4, d)   # TODO: Somehow get hold of variable nUAV so that you don't have to hard-code 4
            # else:
                # return return_array
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
