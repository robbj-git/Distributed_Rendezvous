from math import ceil

USE_ROS = False
CENTRALISED = False
DISTRIBUTED = False
PARALLEL = True
SAMPLING_RATE = 20              # Dynamics change if this changes
SAMPLING_TIME = 1.0/SAMPLING_RATE
ADD_DROPOUT = False

if CENTRALISED + DISTRIBUTED + PARALLEL > 1:
    print "PLEASE ONLY SELECT ONE OUT OF CENTRALISED, DISTRIBUTED, OR PARALLEL"
    exit()

INTER_ITS = 5  # Number of iteration    between each solution of the parallel optimisaion problem

# For testing scripts
# Instructions
NEXT_HORIZON = 0
FOUND_HORIZON = 1

delay_time = 0.75
# delay_len = int(ceil(delay_time/SAMPLING_TIME))
delay_len = 0 #DEBUG

# Horizon
T_short = 45 #25        For Centralised case
T_long = 45     # 45    For Distributed case
T_parallel = 100
sim_len = 500

T = 0
if PARALLEL:
    T = T_parallel      # Can't use CVXGEN, Horizon too long
elif CENTRALISED:
    T = T_short
else:
    T = T_long

# T = 100
