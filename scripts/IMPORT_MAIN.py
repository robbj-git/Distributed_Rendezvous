from math import ceil
from sys import maxint

# Number of iterations simulation should last
sim_len = 500

# Set to True if the UAV hardware is used, e.g. in a HIL setup of field test.
# If this is False, the dynamics of the UAV are simulated using the same linear
# model that is used in the MPC formulation. If it is set to True, the algorhtm
# subscribes to the ROS topics 'dji12/dji_sdk/imu',
# 'dji12/dji_sdk/height_above_takeoff', 'dji12/dji_sdk/velocity',
# 'dji12/dji_sdk/gps_position', and 'dji12/dji_sdk/attitude'.
# The algorithm also publishes to 'dji12/dji_sdk/attitude'.
# This list of topic was last updates as of 29/06-2020, check
# UAV_simulator.__init__ in UAV_simulation.py for guaranteed accurate list of
# topics
USE_HIL = False

# SET ONE OF THESE TO TRUE. See original paper, references in readme.md, for
# differences between the different algorithms
CENTRALISED = True
DISTRIBUTED = False
PARALLEL = False

# DO NOT CHANGE FROM 20. IMPORT_UAV AND IMPORT_USV USE DISCRETISED DYNAMICS THAT
# CHANGE IF SAMPLING RATE IS CHANGED
SAMPLING_RATE = 20
SAMPLING_TIME = 1.0/SAMPLING_RATE
# Only relevant if PARALLEL == True. Specifies the number of iterations between
# each solution of the outer optimisaion problem
INTER_ITS = 5

# Should be set to True by default, only change if you are sure about what you
# are doing. Having this as true shifts all trajectories received by the other
# vehicle by one time step. Assuming that the vehicles' iterations are
# synchronised, this is necessary for accurately predicting the trajectory
# of the other vehicle
SHOULD_SHIFT_MESSAGES = True

# Should a communication loss between the vehicles be simulated? If True,
# then between the iterations specified below, no messages will be sent between
# the vehicles. Should be False by default.
ADD_DROPOUT = False
# Iteration index at which communication loss should start
dropout_lower_bound = 80
# Iteration index at which communication loss should end
dropout_upper_bound = 130

# TODO: ADD TO CLASS!!!
g = 9.8 # Used value for gravitational acceleration

# This variable was used to simulate delay in the tranmission of messages.
# The functionality is deprecated and I cannot guarantee that it works correctly
# anymore, so delay_len should be set to a sufficiently low value so that no
# artificial delay is introduces. Currently set to the lowest posible int value.
# The functionality was deprecated because it relied on the UAV and USV to have
# perfectly synchronised clocks to work, which became a significant burden.
#delay_time = 0.75   # Measured in seconds
# delay_len = int(ceil(delay_time/SAMPLING_TIME))
delay_len = -maxint - 1 # Measured in number of iterations

# Macros for testing scripts UAV_TESTER.py and USV_TESTER.py
NEXT_HORIZON = 0

if CENTRALISED + DISTRIBUTED + PARALLEL != 1:
    print "PLEASE SELECT EXACTLY ONE OUT OF CENTRALISED, DISTRIBUTED, OR PARALLEL"
    exit()

class Settings():
    def __init__(self):
        self.sim_len = sim_len
        self.USE_HIL = USE_HIL
        self.CENTRALISED = CENTRALISED
        self.DISTRIBUTED = DISTRIBUTED
        self.PARALLEL = PARALLEL
        self.SAMPLING_RATE = SAMPLING_RATE
        self.SAMPLING_TIME = SAMPLING_TIME
        self.INTER_ITS = INTER_ITS
        self.ADD_DROPOUT = ADD_DROPOUT
        self.SHOULD_SHIFT_MESSAGES = SHOULD_SHIFT_MESSAGES
        self.dropout_lower_bound = dropout_lower_bound
        self.dropout_upper_bound = dropout_upper_bound
        self.g = g
        self.delay_len = delay_len

settings = Settings()
