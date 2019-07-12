import numpy as np

def shift_trajectory(traj, n, d):
    # n: State Size
    # d: Number of time steps of shift
    traj = np.roll(traj, -n*d, 0)
    print(traj)
    [len, _] = traj.shape
    if (d > 0):
        for i in range(n):
            # Fill the i:th state components of all future states with the i:th
            # component of the previously (before the shift) last state.
            traj[-n*d+i:len:n, :].fill(traj[-n*(d+1)+i, 0])
    return traj

def get_traj_dir(traj, n):
    return traj[0:2, 0:1] - traj[-n:-n+2, 0:1]

traj = np.nan
get_traj_dir(traj, 2)
