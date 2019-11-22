from math import ceil
from sys import maxint

# Number of iterations simulation should last
sim_len = 500
# Should the UAV communicate with the HIL setup? Setting this to true makes the
# algorithm publish control inputs to appropriate DJI-topics instead of
# simulating using the linear model of the dynamics
USE_HIL = False
# SET ONE OF THESE TO TRUE
CENTRALISED = False
DISTRIBUTED = False
PARALLEL = True

SAMPLING_RATE = 20              # Dynamics change if this changes
SAMPLING_TIME = 1.0/SAMPLING_RATE
ADD_DROPOUT = False # Should a communication loss between the vehicles be simulated?

PRED_PARALLEL_TRAJ = True
USE_COMPLETE_HORIZONTAL = False
USE_COMPLETE_USV = False
SOLVE_PARALLEL_AT_END = True

SHOULD_SHIFT_MESSAGES = True
dropout_lower_bound = 80    # Iteration index at which communication loss should start
dropout_upper_bound = 130   # Iteration index at which communication loss should end

if CENTRALISED + DISTRIBUTED + PARALLEL != 1:
    print "PLEASE SELECT EXACTLY ONE OUT OF CENTRALISED, DISTRIBUTED, OR PARALLEL"
    exit()

INTER_ITS = 5  # Number of iteration between each solution of the parallel optimisaion problem
ADD_USV_SECOND_OBJECTIVE = True

# Macros for testing scripts UAV_TESTER.py and USV_TESTER.py
NEXT_HORIZON = 0

# Simulated minimum delay between a sent and received message
delay_time = 0.75   # Measured in seconds
# delay_len = int(ceil(delay_time/SAMPLING_TIME))   # Measured in number of iterations
delay_len = -maxint - 1 #DEBUG, set delay to lowest possible value, so that ...
# ...no artificial delay is added even when scripts are running on separate...
# ...machines with non-synchronised clocks

class Settings():
    def __init__(self):
        self.USE_HIL = USE_HIL
        self.CENTRALISED = CENTRALISED
        self.DISTRIBUTED = DISTRIBUTED
        self.PARALLEL = PARALLEL
        self.SAMPLING_RATE = SAMPLING_RATE
        self.SAMPLING_TIME = SAMPLING_TIME
        self.ADD_DROPOUT = ADD_DROPOUT
        self.PRED_PARALLEL_TRAJ = PRED_PARALLEL_TRAJ
        self.SHOULD_SHIFT_MESSAGES = SHOULD_SHIFT_MESSAGES
        self.dropout_lower_bound = dropout_lower_bound
        self.dropout_upper_bound = dropout_upper_bound
        self.INTER_ITS = INTER_ITS
        self.ADD_USV_SECOND_OBJECTIVE = ADD_USV_SECOND_OBJECTIVE
        self.delay_len = delay_len
        self.sim_len = sim_len

settings = Settings()
