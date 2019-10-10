from math import ceil
from sys import maxint

USE_HIL = False     # Should the UAV communicate with the HIL setup?
# SET ONE OF THESE TO TRUE
CENTRALISED = False
DISTRIBUTED = True
PARALLEL = False

SAMPLING_RATE = 20              # Dynamics change if this changes
SAMPLING_TIME = 1.0/SAMPLING_RATE
ADD_DROPOUT = False # Should a communication loss between the vehicles be simulated?

PRED_PARALLEL_TRAJ = False

USE_COMPLETE_HORIZONTAL = True

dropout_lower_bound = 80    # Iteration index at which communication loss should start
dropout_upper_bound = 130   # Iteration index at which communication loss should end

if CENTRALISED + DISTRIBUTED + PARALLEL != 1:
    print "PLEASE SELECT EXACTLY ONE OUT OF CENTRALISED, DISTRIBUTED, OR PARALLEL"
    exit()

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"
OSQP = "OSQP"

used_hor_solver = OSQP
used_vert_solver = OSQP

INTER_ITS = 5  # Number of iteration between each solution of the parallel optimisaion problem

# Macros for testing scripts (UAV_TESTER.py and USV_TESTER.py at the time of writing, might have been renamed)
# Instructions
NEXT_HORIZON = 0
FOUND_HORIZON = 1

SHOULD_SHIFT_MESSAGES = False

# Simulated minimum delay between a sent and received message
delay_time = 0.75   # Measured in seconds
# delay_len = int(ceil(delay_time/SAMPLING_TIME))   # Measured in number of iterations
delay_len = -maxint - 1 #DEBUG, set delay to lowest possible value, so that ...
# ...no artificial delay is added even when scripts are running on separate...
# ...machines with non-synchronised clocks

# Number of iterations simulation should last
sim_len = 500
