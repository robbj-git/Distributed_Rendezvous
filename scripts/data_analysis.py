import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from Dynamics import dl, ds, hs, nv
import os
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation
import matplotlib.animation

dir_path = '/home/student/robbj_experiment_results/'

# green_like = '#404788'
# orange_like = '#DCE319'
# blue_like = '#55C667'
green_like = '#1b9e77'
orange_like = '#d95f02'
blue_like = '#7570b3'
# light_blue = '#7fcdbb'
light_blue = (0.498, 0.804, 0.733, 0.7)
# red = '#ff0000'
red = (1.0, 0.0, 0.0, 0.7)

def combine_multiple_results(dirs):
    time_list = []
    dist_list = []
    test_means_list = []
    test_hor_means_list = []
    test_vert_means_list = []
    z_traj_inter_list = []
    dist_hor_list = []
    for dir in dirs:
        test_means = np.loadtxt(dir_path + dir + '/MEAN.txt')
        test_medians = np.loadtxt(dir_path + dir + '/MEDIAN.txt')
        test_means_hor = np.loadtxt(dir_path + dir + '/HOR_MEAN.txt')
        test_medians_hor = np.loadtxt(dir_path + dir + '/HOR_MEDIAN.txt')
        test_means_vert = np.loadtxt(dir_path + dir + '/VERT_MEAN.txt')
        test_medians_vert = np.loadtxt(dir_path + dir + '/VERT_MEDIAN.txt')
        UAV_time_stamps = np.loadtxt(dir_path + dir + '/UAV_time_stamps.txt')
        USV_time_stamps = np.loadtxt(dir_path + dir + '/USV_time_stamps.txt')
        t_0 = np.maximum(UAV_time_stamps[0], USV_time_stamps[0])

        #DEBUG, UAV_time_stamps just happened to have last element equal to nan
        UAV_time_stamps[-1] = UAV_time_stamps[-2] + 0.05

        UAV_time_stamps = UAV_time_stamps - t_0
        USV_time_stamps = USV_time_stamps - t_0

        x_log  = np.loadtxt(dir_path + dir + '/x_log.txt')
        xb_log = np.loadtxt(dir_path + dir + '/xb_log.txt')
        xv_log = np.loadtxt(dir_path + dir + '/xv_log.txt')
        x_traj = x_log[0,:]
        y_traj = x_log[1,:]
        z_traj = xv_log[0,:]
        xb_traj = xb_log[0,:]
        yb_traj = xb_log[1,:]
        # distance_hor = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) )
        # distance = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) + np.square(z_traj))

        new_UAV_times = np.arange(0, UAV_time_stamps[-1], 0.05)
        new_USV_times = np.arange(0, USV_time_stamps[-1], 0.05)
        if len(new_UAV_times) > len(new_USV_times):
            common_times = new_USV_times
        else:
            common_times = new_UAV_times

        x_traj_inter = get_interpolated_traj(x_traj, UAV_time_stamps, common_times)
        y_traj_inter = get_interpolated_traj(y_traj, UAV_time_stamps, common_times)
        z_traj_inter = get_interpolated_traj(z_traj, UAV_time_stamps, common_times)
        xb_traj_inter = get_interpolated_traj(xb_traj, USV_time_stamps, common_times)
        yb_traj_inter = get_interpolated_traj(yb_traj, USV_time_stamps, common_times)

        distance_hor = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
            + np.square(y_traj_inter - yb_traj_inter) )
        distance = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
            + np.square(y_traj_inter - yb_traj_inter) + np.square(z_traj_inter) )

        time_list.append(common_times)
        dist_list.append(distance)
        test_means_list.append(test_means)
        test_hor_means_list.append(test_means_hor)
        test_vert_means_list.append(test_means_vert)
        z_traj_inter_list.append(z_traj_inter)
        dist_hor_list.append(distance_hor)

        # Calculate landing time
        land_time = 0
        for i in range(len(z_traj)):
            if z_traj[i] > 0.1:
                land_time = UAV_time_stamps[i]
            else:
                break

        print "Landed at time:", land_time

    colors = [(1.0, 0.0, 0.0, 0.5), (0.0, 0.0, 1.0, 0.5)]
    legends = ['Centralised', 'Distributed']
    xlabel = 'Mean Vertical Problem Solution Time [s]'
    # xlabel = 'Mean Iteration Durations [s]'
    ylabel = 'Number of Trials'
    # plot_all_histograms(test_vert_means_list, [red, light_blue], legends, xlabel, ylabel)
    # plot_all_dists(time_list, dist_list, ['Centralised', 'Distributed', 'Cascading'])
    plot_all_with_constraints(dist_hor_list, z_traj_inter_list,\
        ['Centralised', 'Distributed'], 'horizontal distance [m]', 'height [m]')    #['Centralised', 'Distributed', 'Cascading']
    # save_all_with_constraints(dist_hor_list, z_traj_inter_list,\
    #     ['Centralised', 'Distributed'], 'horizontal distance [m]', 'height [m]')

def print_data(dir):
    UAV_iteration_durations = \
        np.loadtxt(dir_path + dir + '/UAV_iteration_durations.txt')
    UAV_horizontal_durations = np.loadtxt(\
        dir_path + dir +'/UAV_horizontal_durations.txt')
    UAV_vertical_durations = np.loadtxt(\
        dir_path + dir +'/vertical_durations.txt')

    test_means = np.loadtxt(dir_path + dir + '/MEAN.txt')
    test_medians = np.loadtxt(dir_path + dir + '/MEDIAN.txt')
    test_means_hor = np.loadtxt(dir_path + dir + '/HOR_MEAN.txt')
    test_medians_hor = np.loadtxt(dir_path + dir + '/HOR_MEDIAN.txt')
    test_means_vert = np.loadtxt(dir_path + dir + '/VERT_MEAN.txt')
    test_medians_vert = np.loadtxt(dir_path + dir + '/VERT_MEDIAN.txt')
    UAV_time_stamps = np.loadtxt(dir_path + dir + '/UAV_time_stamps.txt')
    USV_time_stamps = np.loadtxt(dir_path + dir + '/USV_time_stamps.txt')
    try:
        landing_times = np.loadtxt(dir_path + dir + '/LANDING_TIMES.txt')
        print "min:", landing_times.min(), ', max:', landing_times.max(), ', mean:', np.mean(landing_times)
    except:
        print 'Found no stored landing times'
    t_0 = np.maximum(UAV_time_stamps[0], USV_time_stamps[0])

    #DEBUG, UAV_time_stamps just happened to have last element equal to nan
    UAV_time_stamps[-1] = UAV_time_stamps[-2] + 0.05

    UAV_time_stamps = UAV_time_stamps - t_0
    USV_time_stamps = USV_time_stamps - t_0

    x_log  = np.loadtxt(dir_path + dir + '/x_log.txt')
    xb_log = np.loadtxt(dir_path + dir + '/xb_log.txt')
    xv_log = np.loadtxt(dir_path + dir + '/xv_log.txt')
    x_traj = x_log[0,:]
    y_traj = x_log[1,:]
    z_traj = xv_log[0,:]
    w_traj = xv_log[1, :]
    xb_traj = xb_log[0,:]
    yb_traj = xb_log[1,:]
    # distance_hor = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) )
    # distance = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) + np.square(z_traj))

    new_UAV_times = np.arange(0, UAV_time_stamps[-1], 0.05)
    new_USV_times = np.arange(0, USV_time_stamps[-1], 0.05)
    if len(new_UAV_times) > len(new_USV_times):
        common_times = new_USV_times
    else:
        common_times = new_UAV_times

    # print np.count_nonzero( np.isnan(z_traj))
    # print np.count_nonzero( np.isnan( w_traj))
    # print '##################################'
    x_traj_inter = get_interpolated_traj(x_traj, UAV_time_stamps, common_times)
    y_traj_inter = get_interpolated_traj(y_traj, UAV_time_stamps, common_times)
    z_traj_inter = get_interpolated_traj(z_traj, UAV_time_stamps, common_times)
    w_traj_inter = get_interpolated_traj(w_traj, UAV_time_stamps, common_times)
    xb_traj_inter = get_interpolated_traj(xb_traj, USV_time_stamps, common_times)
    yb_traj_inter = get_interpolated_traj(yb_traj, USV_time_stamps, common_times)
    # print np.count_nonzero( np.isnan(z_traj_inter))
    # print np.count_nonzero( np.isnan( w_traj_inter))
    # print '!!!!!!'

    distance_hor = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
        + np.square(y_traj_inter - yb_traj_inter) )
    distance = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
        + np.square(y_traj_inter - yb_traj_inter) + np.square(z_traj_inter) )

    # Calculate landing time
    land_time = 0
    for i in range(len(z_traj)):
        if z_traj[i] > 0.1:
            land_time = UAV_time_stamps[i]
        else:
            break

    print "Landed at time:", land_time

    # print 'Mean UAV iteration: ' + str(np.mean(UAV_iteration_durations))
    # print 'Median UAV iteration: ' + str(np.median(UAV_iteration_durations))
    # print 'Mean UAV horizontal: ' + str(np.mean(UAV_horizontal_durations))
    # print 'Median UAV horizontal: ' + str(np.median(UAV_horizontal_durations))
    # print 'Mean UAV vertical: ' + str(np.mean(UAV_vertical_durations))
    # print 'Median UAV vertical: ' + str(np.median(UAV_vertical_durations))
    # print '----------------------------------------------'

    xv_log_trimmed = np.reshape( np.array([z_traj_inter, w_traj_inter]), (-1, 1), order='F' )
    constraints_satisfied(common_times, distance_hor, xv_log_trimmed, land_time)

    # plot_3d(x_traj, y_traj, z_traj, xb_traj, yb_traj)
    # save_3d_animation(x_traj, y_traj, z_traj, xb_traj, yb_traj)
    # plot_topview(x_traj, y_traj, xb_traj, yb_traj)
    plot_with_constraints(distance_hor, z_traj_inter, 'horizontal distance [m]', 'height [m]')
    # plot_3d_realtime(x_traj, y_traj, z_traj, xb_traj, yb_traj)
    # plot_histogram(test_means_hor, 'Mean Horizontal Problem Solution Time [s]', 'Number of Trials')   #Mean Vertical Problem Solution Time [s]
    # plot_hor_dist(common_times, distance_hor)
    # plot_dist(common_times, distance)
    # plot_height(UAV_time_stamps - t_0, z_traj)
    return

def constraints_satisfied(common_times, distance_hor, xv_log, landing_time):
    T_trimmed = len(common_times)
    height_extractor = np.zeros(( T_trimmed, nv*T_trimmed ))
    for i in range(T_trimmed):
        height_extractor[ i, nv*i ] = 1

    distance_hor = np.reshape(distance_hor, (-1, 1))
    b_vec = distance_hor < ds

    # SAFETY CONSTRAINT
    # dl - ds < 0 --> Automatically satisfied in b == 0
    safe1 = (dl - ds)*np.dot(height_extractor,xv_log) <= np.diag(b_vec)*(hs*dl - hs*distance_hor)
    safe2 = (dl - ds)*np.dot(height_extractor,xv_log) <= np.diag(b_vec)*(hs*dl + hs*distance_hor)   # shouldn't be necessary if distance in positive
    # SAFE HEIGHT CONSTRAINT
    # UAV height usually > 0 --> Automatically satisfied if b == 1
    safe3 = np.dot(height_extractor,xv_log) >= hs*(np.ones((T_trimmed, 1)) - b_vec)

    # np.savetxt('/home/robert/DELTE_ME/safe1.txt', safe1)
    # np.savetxt('/home/robert/DELTE_ME/safe2.txt', safe2)
    # np.savetxt('/home/robert/DELTE_ME/safe3.txt', safe3)
    np.set_printoptions(threshold=sys.maxsize)
    times_constraints_violated = []
    for safe_vec in [safe1, safe2, safe3]:
        if np.count_nonzero(~safe_vec) > 0:
            nonzero_indices = np.nonzero(~safe_vec)[0]
            for i in nonzero_indices:
                if common_times[i] < landing_time:
                    # Only include constraints that were violated BEFORE landing
                    times_constraints_violated.append(common_times[i])

    # print np.count_nonzero(~safe1)
    # print np.count_nonzero(~safe2)
    # print np.count_nonzero(~safe3)
    # print np.nonzero(~safe3)[0]
    print len(times_constraints_violated), 'constraints were violated before landing'

    # # Safety constraints
    # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
    #     <= cp.diag(self.b)*(params.hs*params.dl - params.hs*self.dist)]
    # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
    #     <= cp.diag(self.b)*(params.hs*params.dl + params.hs*self.dist)]
    # # Safe height constraints
    # constraintsVert += [self.height_extractor*self.xv \
    #     >= params.hs*(np.ones(( T+1, 1 )) - self.b)]
    return

def horizon_vs_performance(dirs):
    fig = plt.figure()
    ax = plt.axes()
    colors = ['blue', 'red']
    legends = ['Centralised', 'Distributed']
    j = -1
    for dir in dirs:
        j += 1
        # Find range of horizons
        min_hor = -1
        max_hor = -1
        i = 0
        while min_hor == -1 or max_hor == -1:
            file_exists = os.path.isfile(dir_path + dir + '/landing_times_' + str(i) + '.txt')
            if file_exists and min_hor == -1:
                min_hor = i
            elif min_hor != -1 and not file_exists:
                max_hor = i-1
            i = i + 1

        all_landing_times = []
        all_mean_horizontal = []
        all_median_horizontal = []
        all_mean_iteration = []
        all_median_iteration = []
        all_mean_vertical = []
        all_median_vertical = []
        plotable_landing_times = []
        plotable_mean_horizontal = []
        plotable_median_horizontal = []
        plotable_mean_iteration = []
        plotable_median_iteration = []
        plotable_mean_vertical = []
        plotable_median_vertical = []

        print "min:", min_hor, 'max:', max_hor
        for hor in range(min_hor, max_hor+1):
            landing_times = np.loadtxt(dir_path + dir + '/landing_times_' + str(hor) + '.txt')
            mean_horizontal = np.loadtxt(dir_path + dir + '/mean_horizontal_' + str(hor) + '.txt')
            median_horizontal = np.loadtxt(dir_path + dir + '/median_horizontal_' + str(hor) + '.txt')
            mean_iteration = np.loadtxt(dir_path + dir + '/mean_iteration_' + str(hor) + '.txt')
            median_iteration = np.loadtxt(dir_path + dir + '/median_iteration_' + str(hor) + '.txt')
            mean_vertical = np.loadtxt(dir_path + dir + '/mean_vertical_' + str(hor) + '.txt')
            median_vertical = np.loadtxt(dir_path + dir + '/median_vertical_' + str(hor) + '.txt')

            # all_landing_times.append(landing_times)
            # all_mean_horizontal.append(mean_horizontal)
            # all_median_horizontal.append(median_horizontal)
            # all_mean_iteration.append(mean_iteration)
            # all_median_iteration.append(median_iteration)
            # all_mean_vertical.append(mean_vertical)
            # all_median_vertical.append(median_vertical)
            plotable_landing_times.append(np.mean(landing_times))
            plotable_mean_horizontal.append(np.mean(mean_horizontal))
            plotable_median_horizontal.append(np.mean(median_horizontal))
            plotable_mean_iteration.append(np.mean(mean_iteration))
            plotable_median_iteration.append(np.mean(median_iteration))
            plotable_mean_vertical.append(np.mean(mean_vertical))
            plotable_median_vertical.append(np.mean(median_vertical))

        ax.plot(range(min_hor, max_hor+1), plotable_mean_iteration, colors[j])
        # ax.plot(range(min_hor, max_hor+1), plotable_mean_horizontal)
        # ax.plot(range(min_hor, max_hor+1), plotable_mean_vertical)
        # plt.legend(['Iteration Time [s]', 'Horizontal Problem Solution Time [s]', 'Vertical Problem Solution Time [s]'])
        plt.grid(True)
        plt.xlabel('Prediction Horizon')
        plt.ylabel('Iteration Duration [s]')
    plt.legend(legends)
    plt.show()

def plot_with_constraints(x_vector, height, xlabel, ylabel):
    forbidden_area_1 = Polygon([ (dl, 0),\
                                 (ds, hs),\
                                 (35, hs),\
                                 (35, 0)], True)
    forbidden_area_2 = Polygon([ (-dl, 0),\
                                 (-ds, hs),\
                                 (-35, hs),\
                                 (-35, 0)], True)
    safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)

    fig = plt.figure()
    ax = plt.axes()
    ax.plot(x_vector, height, 'b')
    ax.add_collection(safety_patch_collection)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def plot_height(time, z_traj):
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(time, z_traj, 'b')
    plt.grid(True)
    plt.show()

def plot_hor_dist(time, distance):
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(time, distance, 'b')
    plt.grid(True)
    plt.show()

def plot_dist(time, distance):
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(time, distance, 'b')
    plt.xlabel('time [s]')
    plt.ylabel('distance [m]')
    plt.grid(True)
    plt.show()

def plot_all_dists(time_list, distance_list, legend_list):
    fig = plt.figure()
    ax = plt.axes()
    colors = [blue_like, orange_like, green_like]
    styles = ['-', '--', '-.']
    for i in range(len(time_list)):
        ax.plot(time_list[i], distance_list[i],styles[i])
    plt.xlabel('time [s]')
    plt.ylabel('distance [m]')
    plt.grid(True)
    plt.legend(legend_list)
    ax.set_xlim(left=0, right=100)
    plt.show()

def plot_all_with_constraints(x_vector_list, y_vector_list, legend_list, xlabel, ylabel):
    forbidden_area_1 = Polygon([ (dl, 0),\
                                 (ds, hs),\
                                 (35, hs),\
                                 (35, 0)], True)
    forbidden_area_2 = Polygon([ (-dl, 0),\
                                 (-ds, hs),\
                                 (-35, hs),\
                                 (-35, 0)], True)
    safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4, edgecolors='red', facecolors='red')

    fig = plt.figure()
    ax = plt.axes()
    colors = [blue_like, orange_like, green_like]
    # styles = ['-', '--', '-.']
    styles = ['red', 'blue', 'yellow']
    for i in range(len(y_vector_list)):
        ax.plot(x_vector_list[i], y_vector_list[i], styles[i])
    ax.add_collection(safety_patch_collection)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend(legend_list)
    plt.show()

def save_all_with_constraints(x_vector_list, y_vector_list, legend_list, xlabel, ylabel):
    fig = plt.figure()
    ax = plt.axes()
    forbidden_area_1 = Polygon([ (dl, 0),\
                                 (ds, hs),\
                                 (35, hs),\
                                 (35, 0)], True)
    forbidden_area_2 = Polygon([ (-dl, 0),\
                                 (-ds, hs),\
                                 (-35, hs),\
                                 (-35, 0)], True)
    safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4, edgecolors='red', facecolors='red')

    xcdata, ycdata, xddata, yddata = [], [], [], []
    line1, = plt.plot([], [], 'r')
    line2, = plt.plot([], [], 'b')
    # line3 = plt.plot([], [])
    lines = [line1, line2]
    def init():
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid(True)
        plt.legend(legend_list)
        ax.add_collection(safety_patch_collection)
        ax.set_xlim(left=0, right=35)
        ax.set_ylim(bottom=0, top=12)
        return lines

    def update(i):
        xcdata.append(x_vector_list[0][i])
        ycdata.append(y_vector_list[0][i])
        xddata.append(x_vector_list[1][i])
        yddata.append(y_vector_list[1][i])
        lines[0].set_data(xcdata, ycdata)
        lines[1].set_data(xddata, yddata)
        return lines

    animation = FuncAnimation(fig, update, frames = len(x_vector_list[0]),\
        init_func = init, blit=True)

    Writer = matplotlib.animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    animation.save('my_constraint_anim.mp4', writer=writer)
    print "Should have saved constraint mp4"

def save_3d_animation(x_traj, y_traj, z_traj, xb_traj, yb_traj):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    xdata, ydata, zdata = [x_traj[0]], [y_traj[0]], [z_traj[2]]
    xbdata, ybdata, zbdata = [xb_traj[0]], [yb_traj[0]], [0]
    line1, = ax.plot3D(xdata, ydata, zdata, 'blue')
    line2, = ax.plot3D(xbdata, ybdata, zbdata, 'red')
    lines = [line1, line2]
    def init():
        ax.set_xlim(left=0, right=30)
        ax.set_ylim(bottom=0, top=16)
        ax.set_zlim(0)
        plt.xlabel('x-position [m]')
        plt.ylabel('y-position [m]')
        ax.set_zlabel('Height [m]')
        plt.legend(['Drone trajectory', 'Boat trajectory'])
        return lines

    def update(i):

        xdata.append(x_traj[i])
        ydata.append(y_traj[i])
        zdata.append(z_traj[max(i,2)])
        xbdata.append(xb_traj[i])
        ybdata.append(yb_traj[i])
        zbdata.append(0)
        lines[0].set_data(xdata, ydata)
        lines[0].set_3d_properties(zdata)
        lines[1].set_data(xbdata, ybdata)
        lines[1].set_3d_properties(zbdata)
        return lines

    animation = FuncAnimation(fig, update, frames = len(x_traj),\
        init_func = init, blit=True)

    Writer = matplotlib.animation.writers['ffmpeg']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    animation.save('my_anim.mp4', writer=writer)
    print "Should have saved mp4"

def plot_3d(x_traj, y_traj, z_traj, xb_traj, yb_traj):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    plt.grid(False)
    ax.plot3D(x_traj[3:], y_traj[3:], z_traj[3:], 'blue')
    ax.plot3D(xb_traj, yb_traj, 0, '#FF5555')
    ax.set_zlim(0)
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_zticklabels([])
    # plt.axis('off')
    # plt.xlabel('x-position [m]')
    # plt.ylabel('y-position [m]')
    # ax.set_zlabel('Height [m]')
    # plt.legend(['UAV trajectory', 'USV trajectory'])
    # # plt.legend(['Drone trajectory', 'Boat trajectory'])
    plt.show()

def plot_3d_realtime(x_traj, y_traj, z_traj, xb_traj, yb_traj):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    time = range(len(x_traj))
    for t in time:
        ax.plot3D(x_traj[0:t+1], y_traj[0:t+1], z_traj[0:t+1], 'blue')
        ax.plot3D(xb_traj[0:t+1], yb_traj[0:t+1], 0, 'red')
        ax.set_zlim(0)
        plt.xlabel('x-position [m]')
        plt.ylabel('y-position [m]')
        ax.set_zlabel('Height [m]')
        plt.legend(['UAV trajectory', 'USV trajectory'])
        plt.pause(0.05)
        ax.cla()

def plot_topview(x_traj, y_traj, xb_traj, yb_traj):
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(x_traj, y_traj, 'blue')
    ax.plot(xb_traj, yb_traj, 'red')
    plt.xlabel('x-position [m]')
    plt.ylabel('y-position [m]')
    plt.legend(['UAV trajectory', 'USV trajectory'])
    plt.show()

def plot_histogram(vector, xlabel, ylabel, bins=10):
    plt.hist(vector, bins=bins)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.show()

def plot_all_histograms(vectors, colors, legend_list, xlabel, ylabel, bins=10):
    for (vector, color) in zip(vectors, colors):
        plt.hist(vector, bins=bins, color=color)
    # plt.hist(vector1, bins=bins, color=(1.0, 0.0, 0.0, 0.5))
    # plt.hist(vector2, bins=bins, color=(0.0, 0.0, 1.0, 0.5))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.legend(legend_list)
    plt.show()

def get_interpolated_traj(traj, old_times, new_times):
    new_traj = np.empty(new_times.shape)
    new_traj.fill(np.nan)
    i_0 = 0
    i_2 = 1
    for i in range(len(new_times)):
        while True:
            if (old_times[i_2] < new_times[i]):
                # haven't passed interpolation point yet, move forward
                i_0 = i_2
                i_2 = i_2 + 1
            else:
                # We have passed interpolation point
                x_0 = old_times[i_0]
                x_2 = old_times[i_2]
                y_0 = traj[i_0]
                y_2 = traj[i_2]
                x_1 = new_times[i]
                new_traj[i] = y_0 + (x_1 - x_0)*(y_2 - y_0)/(x_2 - x_0)
                break
    return new_traj

def remove_negative_elements(vector):
    i = 0
    while vector[i] < 0 and i < len(vector):
        i += 1

    return vector[i:]

if __name__ == '__main__':
    use_dir = False
    use_horizon_vs_performance = False
    if len(sys.argv) == 2:
        # directory specified
        dir = sys.argv[1]
        use_dir = True
    elif len(sys.argv) > 2:
        # start and end index specified
        # start = int(sys.argv[1])
        # end = int(sys.argv[2])
        if not use_horizon_vs_performance:
            combine_multiple_results(sys.argv[1:3])
            exit()
        else:
            dirs = sys.argv[1:4]
    else:
        print "ERROR: Please select directory"
        exit()

    if use_horizon_vs_performance:
        if len(sys.argv) > 2:
            horizon_vs_performance(dirs)
        else:
            horizon_vs_performance([dir])
    elif use_dir:
        print_data(dir)
    else:
        for i in range(int(start), int(end)+1):
            print_data('Experiment_' + str(i))
