from math import ceil

USE_HIL = False     # Should the UAV communicate with the HIL setup?
CENTRALISED = True
DISTRIBUTED = False
PARALLEL = False
SAMPLING_RATE = 20              # Dynamics change if this changes
SAMPLING_TIME = 1.0/SAMPLING_RATE
ADD_DROPOUT = False # Should a communication loss between the vehicles be simulated?

dropout_lower_bound = 80    # Iteration index at which communication loss should start
dropout_upper_bound = 130   # Iteration index at which communication loss should end

if CENTRALISED + DISTRIBUTED + PARALLEL > 1:
    print "PLEASE ONLY SELECT ONE OUT OF CENTRALISED, DISTRIBUTED, OR PARALLEL"
    exit()

CVXGEN = "CVXGEN"
CVXPy = "CVXPy"
OSQP = "OSQP"

used_hor_solver = CVXPy
used_vert_solver = CVXPy

INTER_ITS = 5  # Number of iteration between each solution of the parallel optimisaion problem

# Macros for testing scripts (UAV_TESTER.py and USV_TESTER.py at the time of writing, might have been renamed)
# Instructions
NEXT_HORIZON = 0
FOUND_HORIZON = 1

# Simulated minimum delay between a sent and received message
delay_time = 0.75   # Measured in seconds
# delay_len = int(ceil(delay_time/SAMPLING_TIME))   # Measured in number of iterations
delay_len = 0 #DEBUG

# Number of iterations simulation should last
sim_len = 500
