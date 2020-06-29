import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits import mplot3d
from IMPORT_UAV import dl, ds, hs, Bv
from helper_classes import DataAnalysisParams
import os
from matplotlib.patches import Polygon, Circle
from matplotlib.collections import PatchCollection
from matplotlib.animation import FuncAnimation
import matplotlib.animation
import getpass

CENTRALISED = 0
DISTRIBUTED = 1
PARALLEL    = 2

USE_TIME_CORRECTION = True

# getpass.getuser()
# print getpass.getuser()

dir_path = '/home/' + getpass.getuser() + '/robbj_experiment_results/'

ACTUAL = 0
UAV = 1
USV = 2
RAW = 3
RAW_UAV = 4

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
nv = Bv.shape[0]

class DataAnalyser():

    def __init__(self, files):
        self.files = files
        self.file_types = self.get_problem_types(files)
        self.p = DataAnalysisParams()
        self.colors = [(0.12, 0.47, 0.71, 0.5), (1.0, 0.50, 0.05, 0.5), (0.17, 0.63, 0.17, 0.5), (0.84, 0.15, 0.16, 0.5), (0.58, 0.40, 0.74, 0.5)]

        # self.x_log  = np.loadtxt(dir_path + dir + '/x_log.txt')
        # self.xb_log = np.loadtxt(dir_path + dir + '/xb_log.txt')
        # self.xv_log = np.loadtxt(dir_path + dir + '/xv_log.txt')
        # self.UAV_traj_log = np.loadtxt(dir_path + dir + '/UAV_traj_log.txt')
        # self.USV_traj_log = np.loadtxt(dir_path + dir + '/USV_traj_log.txt')
        # self.vert_traj_log = np.loadtxt(dir_path + dir + '/vert_traj_log.txt')
        # self.UAV_time_stamps = np.loadtxt(dir_path + dir + '/UAV_time_stamps.txt')
        # self.USV_time_stamps = np.loadtxt(dir_path + dir + '/USV_time_stamps.txt')
        return

    def get_problem_types(self, files):
        file_types = len(files)*[-1]
        for file_index, file in enumerate(files):
            file = open(dir_path + file + '/info.txt')
            lines = file.readlines()
            if lines[1].find('Centralised') > 0:
                file_types[file_index] = CENTRALISED
            elif lines[1].find('Distributed') > 0:
                file_types[file_index] = DISTRIBUTED
            elif lines[1].find('Parallel') > 0:
                file_types[file_index] = PARALLEL
            else:
                raise TypeError('Problem must only be of type Centralised, Distributed, or Parallel')
        return file_types

    def plot_3d(self, real_time = False, perspective = ACTUAL):
        p = self.p
        self.should_close = False
        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes(projection='3d')

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal', 'vertical'], self.p)
            if perspective == ACTUAL:
                x_log  = dtl.x_log
                xb_log = dtl.xb_log
                UAV_traj_log = dtl.UAV_traj_log
                USV_traj_log = dtl.USV_traj_log
            if perspective == UAV:
                x_log  = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
                USV_traj_log = dtl.USV_traj_log_UAV
                xb_log = USV_traj_log[0:dtl.nUSV, :]
            if perspective == USV:
                xb_log = dtl.xb_log
                USV_traj_log = dtl.USV_traj_log
                UAV_traj_log = dtl.UAV_traj_log_USV
                x_log = UAV_traj_log[0:dtl.nUAV, :]
            if perspective == RAW:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                xb_log = dtl.xb_log_raw
                USV_traj_log = dtl.USV_traj_log_raw
            if perspective == RAW_UAV:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                USV_traj_log = dtl.USV_traj_log_UAV_raw
                xb_log = USV_traj_log[0:dtl.nUSV, :]


            if perspective != RAW:
                xv_log = dtl.xv_log
                vert_traj_log = dtl.vert_traj_log
            else:
                xv_log = dtl.xv_log_raw
                vert_traj_log = dtl.vert_traj_log_raw

            # if self.file_types[file_index] == PARALLEL:
            #     UAV_inner_traj_log = np.loadtxt(dir_path + dir + '/UAV_inner_traj_log.txt')
            #     USV_inner_traj_log = np.loadtxt(dir_path + dir + '/USV_inner_traj_log.txt')
            #     vert_inner_traj_log = np.loadtxt(dir_path + dir + '/vert_inner_traj_log.txt')

            time_len = x_log.shape[1]-1
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:

                ax.cla()
                x_pred_traj = UAV_traj_log[0::dtl.nUAV, t]
                y_pred_traj = UAV_traj_log[1::dtl.nUAV, t]
                z_pred_traj = vert_traj_log[0::dtl.nv,  t]
                xb_pred_traj = USV_traj_log[0::dtl.nUSV, t]
                yb_pred_traj = USV_traj_log[1::dtl.nUSV, t]

                if perspective != RAW and self.file_types[file_index] == PARALLEL:
                    x_inner_pred_traj = dtl.UAV_inner_traj_log[0::dtl.nUAV, t]
                    y_inner_pred_traj = dtl.UAV_inner_traj_log[1::dtl.nUAV, t]
                    z_inner_pred_traj = dtl.vert_inner_traj_log[0::dtl.nv,  t]
                    xb_inner_pred_traj = dtl.USV_inner_traj_log[0::dtl.nUSV, t]
                    yb_inner_pred_traj = dtl.USV_inner_traj_log[1::dtl.nUSV, t]
                if perspective == RAW and self.file_types[file_index] == PARALLEL:
                    x_inner_pred_traj = dtl.UAV_inner_traj_log_raw[0::dtl.nUAV, t]
                    y_inner_pred_traj = dtl.UAV_inner_traj_log_raw[1::dtl.nUAV, t]
                    z_inner_pred_traj = dtl.vert_inner_traj_log_raw[0::dtl.nv,  t]
                    xb_inner_pred_traj = dtl.USV_inner_traj_log_raw[0::dtl.nUSV, t]
                    yb_inner_pred_traj = dtl.USV_inner_traj_log_raw[1::dtl.nUSV, t]

                # Actual trajectories
                ax.plot3D(x_log[0, 0:t+1], x_log[1, 0:t+1], xv_log[0, 0:t+1], 'b')
                ax.plot3D(xb_log[0, 0:t+1], xb_log[1, 0:t+1], 0, 'r')
                ax.plot3D(x_log[0, t:t+1], x_log[1, t:t+1], xv_log[0, t:t+1], 'bx')
                ax.plot3D(xb_log[0, t:t+1], xb_log[1, t:t+1], 0, 'rx')
                # Predicted trajectories
                if not np.isnan(z_pred_traj).all():
                    ax.plot3D(x_pred_traj, y_pred_traj, z_pred_traj, 'green', alpha=0.5)
                else:
                    ax.plot3D(x_pred_traj, y_pred_traj,  xv_log[0, t], 'green', alpha=0.5)
                ax.plot3D(xb_pred_traj, yb_pred_traj, 0, 'green', alpha=0.5)

                if self.file_types[file_index] == PARALLEL:
                    ax.plot3D(x_inner_pred_traj, y_inner_pred_traj, z_inner_pred_traj, 'yellow', alpha=0.5)
                    ax.plot3D(xb_inner_pred_traj, yb_inner_pred_traj, 0, 'yellow', alpha=0.5)

                ax.set_zlim(0)
                plt.xlabel('x-position [m]')
                plt.ylabel('y-position [m]')
                ax.set_zlabel('Height [m]')
                plt.legend(['UAV trajectory', 'USV trajectory'])
                try:
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()# raw_input()

    def plot_topview(self, real_time = False, perspective = ACTUAL):
        p = self.p
        self.should_close = False
        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal'], self.p)

            if perspective == ACTUAL:
                x_log  = dtl.x_log
                xb_log = dtl.xb_log
                UAV_traj_log = dtl.UAV_traj_log
                USV_traj_log = dtl.USV_traj_log
            if perspective == UAV:
                x_log  = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
                if self.file_types[file_index] == CENTRALISED:
                    # In centralised case, USV_traj_log is always from UAVs perspective
                    USV_traj_log = dtl.USV_traj_log
                else:
                    USV_traj_log = dtl.USV_traj_log_UAV
                xb_log = USV_traj_log[0:dtl.nUSV, :]
            if perspective == USV:
                xb_log = dtl.xb_log
                USV_traj_log = dtl.USV_traj_log
                UAV_traj_log = dtl.UAV_traj_log_USV
                x_log = UAV_traj_log[0:dtl.nUAV, :]
            if perspective == RAW:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                xb_log = dtl.xb_log_raw
                USV_traj_log = dtl.USV_traj_log_raw

                # DEBUG
                UAV_traj_log_USV = dtl.UAV_traj_log_USV_raw
                USV_traj_log_UAV = dtl.USV_traj_log_UAV_raw

            if perspective == RAW_UAV:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                USV_traj_log = dtl.USV_traj_log_UAV_raw
                xb_log = USV_traj_log[0:dtl.nUSV, :]

            time_len = x_log.shape[1]-1
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            black_star_x = 0
            black_star_y = 0

            for t in time:
                ax.cla()
                # ax.set_xlim([-1,1])
                # ax.set_ylim([-1,1])
                x_pred_traj = UAV_traj_log[0::dtl.nUAV, t]
                y_pred_traj = UAV_traj_log[1::dtl.nUAV, t]
                xb_pred_traj = USV_traj_log[0::dtl.nUSV, t]
                yb_pred_traj = USV_traj_log[1::dtl.nUSV, t]
                # DEBUG
                # x_pred_traj_USV = UAV_traj_log_USV[0::dtl.nUAV, t]
                # y_pred_traj_USV = UAV_traj_log_USV[1::dtl.nUAV, t]
                # xb_pred_traj_UAV = USV_traj_log_UAV[0::dtl.nUAV, t]
                # yb_pred_traj_UAV = USV_traj_log_UAV[1::dtl.nUAV, t]

                if perspective != RAW and self.file_types[file_index] == PARALLEL:
                    x_inner_pred_traj = dtl.UAV_inner_traj_log[0::dtl.nUAV, t]
                    y_inner_pred_traj = dtl.UAV_inner_traj_log[1::dtl.nUAV, t]
                    xb_inner_pred_traj = dtl.USV_inner_traj_log[0::dtl.nUSV, t]
                    yb_inner_pred_traj = dtl.USV_inner_traj_log[1::dtl.nUSV, t]
                if perspective == RAW and self.file_types[file_index] == PARALLEL:
                    x_inner_pred_traj = dtl.UAV_inner_traj_log_raw[0::dtl.nUAV, t]
                    y_inner_pred_traj = dtl.UAV_inner_traj_log_raw[1::dtl.nUAV, t]
                    xb_inner_pred_traj = dtl.USV_inner_traj_log_raw[0::dtl.nUSV, t]
                    yb_inner_pred_traj = dtl.USV_inner_traj_log_raw[1::dtl.nUSV, t]


                # Actual trajectories
                ax.plot(x_log[0, t], x_log[1, t], 'bx')
                ax.plot(xb_log[0, t], xb_log[1, t], 'rx')
                if dtl.nUSV == 6:
                    ax.arrow(xb_log[0, t], xb_log[1,t], np.cos(xb_log[4, t]), np.sin(xb_log[4, t]))
                    speed = np.sqrt(xb_log[2, t]**2 + xb_log[3, t]**2)
                    ax.arrow(xb_log[0, t], xb_log[1,t], xb_log[2, t]/speed, xb_log[3, t]/speed, color='red')
                    ub_log = dtl.ub_log
                    print "Psi_des:", np.rad2deg(ub_log[1,t]), "Psi:", np.rad2deg(xb_log[4, t])
                    # ax.arrow(xb_log[0, t], xb_log[1,t], np.cos(ub_log[1,t]), np.sin(ub_log[1,t]), color='blue')
                # Predicted trajectories
                ax.plot(x_pred_traj, y_pred_traj, 'b.', alpha=0.4)
                ax.plot(xb_pred_traj, yb_pred_traj, 'r.', alpha=0.4)
                # ax.plot(x_pred_traj_USV, y_pred_traj_USV, 'k.', alpha=0.1)  # DEBUG
                # ax.plot(xb_pred_traj_UAV, yb_pred_traj_UAV, 'k.', alpha=0.1)  # DEBUG

                if self.file_types[file_index] == PARALLEL:
                    ax.plot(x_inner_pred_traj, y_inner_pred_traj, 'g*', alpha=0.4)
                    ax.plot(xb_inner_pred_traj, yb_inner_pred_traj, 'y*', alpha=0.4)
                    # DEBUG
                    # if t%5 == 0:
                    #     black_star_x = xb_inner_pred_traj[5]
                    #     black_star_y = yb_inner_pred_traj[5]
                    # ax.plot(black_star_x, black_star_y, 'k*', alpha=1)

                plt.xlabel('x-position [m]')
                plt.ylabel('y-position [m]')
                plt.legend(['UAV trajectory', 'USV trajectory'])
                plt.grid(True)
                # loc = ticker.MultipleLocator(base=0.1)
                # ax.xaxis.set_major_locator(loc)
                # ax.yaxis.set_major_locator(loc)
                # plt.xticks(np.arange(0, 50, 1))
                # plt.yticks(np.arange(0, 50, 1))
                # plt.gca().set_aspect('equal', adjustable='box')
                try:
                    # ax.set_xlim([2, 6])
                    # ax.set_ylim([-6, -2])
                    # ax.set_xlim([0, 12])
                    # ax.set_ylim([-20, 0])
                    plt.pause(0.05)
                    # raw_input()
                except Exception as e:
                    # print e
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()# raw_input()

    def plot_with_vel_constraints(self, real_time = False):
        p = self.p
        upper_vel_constraints = self.get_vel_polygon(p.wmax)
        lower_vel_constraints = self.get_vel_polygon(p.wmin)
        self.should_close = False

        for file_index, dir in enumerate(self.files):
            patch_collection = PatchCollection( [upper_vel_constraints,\
                lower_vel_constraints], alpha=0.5, color='grey')
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['vertical'], self.p)

            if self.file_types[file_index] == PARALLEL:
                T_inner =dtl.vert_inner_traj_log.shape[0]//dtl.nv

            T_outer = dtl.vert_traj_log.shape[0]//dtl.nv
            time_len = dtl.vert_traj_log.shape[1]
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:
                ax.cla()
                upper_vel_constraints_slack = self.get_vel_polygon(p.wmax, -dtl.s_vert_log[t])
                lower_vel_constraints_slack = self.get_vel_polygon(p.wmin, -dtl.s_vert_log[t])
                patch_collection_slack = PatchCollection( \
                    [upper_vel_constraints_slack, lower_vel_constraints_slack],\
                    alpha=0.2, color='grey')
                vel_pred_log = dtl.vert_traj_log[1::dtl.nv, t]
                actual_vel_bound = -p.kl*dtl.xv_log[0, 0:t+1] + p.wmin_land
                pred_vel_bound   = -p.kl*dtl.vert_traj_log[0::dtl.nv, t] + p.wmin_land
                actual_vel_bound_slack = -p.kl*dtl.xv_log[0, 0:t+1] + p.wmin_land - dtl.s_vert_log[0:t+1]
                pred_vel_bound_slack   = -p.kl*dtl.vert_traj_log[0::dtl.nv, t] + p.wmin_land - dtl.s_vert_log[t]
                if np.isnan(vel_pred_log).any():
                    vel_pred_log = np.full((T_outer,), dtl.xv_log[1, t])
                if np.isnan(pred_vel_bound).any():
                    pred_vel_bound = np.full((T_outer,), -p.kl*dtl.xv_log[0, t] + p.wmin_land)
                    # TODO: Add a velocity bound predicted by inner controller in parallel case?

                ax.plot(range(t+1), dtl.xv_log[1, 0:t+1], 'blue')
                ax.plot(range(t+1, t+T_outer+1), vel_pred_log, 'green', alpha=0.5)
                ax.plot(range(t+1), actual_vel_bound, 'red')
                ax.plot(range(t+1, t+T_outer+1), pred_vel_bound, 'orange')
                ax.plot(range(t+1), actual_vel_bound_slack, 'red', alpha=0.5)
                ax.plot(range(t+1, t+T_outer+1), pred_vel_bound_slack, 'orange', alpha=0.5)
                ax.plot(range(t+1), dtl.s_vert_log[0:t+1], 'black')
                if self.file_types[file_index] == PARALLEL:
                    vel_inner_pred_log = dtl.vert_inner_traj_log[1::dtl.nv, t]
                    ax.plot(range(t+1, t+T_inner+1), vel_inner_pred_log, 'yellow', alpha=0.5)

                ax.add_collection(patch_collection)
                ax.add_collection(patch_collection_slack)
                plt.xlabel('time [iterations]')
                plt.ylabel('velocity [m/s]')
                try:
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        # fig = plt.figure()
        # fig.canvas.mpl_connect('close_event', self.handle_close)
        # ax = plt.axes()
        # ax.plot(range(500), obj_val_log, 'red')
        # ax.plot(range(500), 500*s_vert_log, 'green')
        plt.show()

    def plot_hor_velocities(self, real_time = False):
        p = self.p
        upper_vel_constraints_UAV = self.get_vel_polygon(p.vmax)
        lower_vel_constraints_UAV = self.get_vel_polygon(-p.vmax)
        upper_vel_constraints_USV = self.get_vel_polygon(p.vmax_b)
        lower_vel_constraints_USV = self.get_vel_polygon(-p.vmax_b)
        self.should_close = False

        for file_index, dir in enumerate(self.files):
            patch_collection_UAV = PatchCollection( [upper_vel_constraints_UAV,\
                lower_vel_constraints_UAV], alpha=0.5, color='grey')
            patch_collection_USV = PatchCollection( [upper_vel_constraints_USV,\
                lower_vel_constraints_USV], alpha=0.5, color='grey')
            # fig = plt.figure()
            # ax = plt.axes()
            fig, axes = plt.subplots(nrows=1, ncols=2)
            fig.canvas.mpl_connect('close_event', self.handle_close)

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal'], self.p)

            if self.file_types[file_index] == PARALLEL:
                T_inner =dtl.UAV_inner_traj_log.shape[0]//dtl.nUAV

            T_outer = dtl.UAV_traj_log.shape[0]//dtl.nUAV
            time_len = dtl.UAV_traj_log.shape[1]
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:
                axes[0].cla()
                axes[1].cla()
                axes[0].set_title("UAV")
                axes[1].set_title("USV")

                pred_UAV_vel_x_log = dtl.UAV_traj_log[2::dtl.nUAV, t]
                pred_UAV_vel_y_log = dtl.UAV_traj_log[3::dtl.nUAV, t]
                pred_USV_vel_x_log = dtl.USV_traj_log[2::dtl.nUSV, t]
                pred_USV_vel_y_log = dtl.USV_traj_log[3::dtl.nUSV, t]

                axes[0].plot(range(t+1), dtl.x_log[2, 0:t+1], 'blue')
                axes[0].plot(range(t+1, t+T_outer+1), pred_UAV_vel_x_log, 'blue', alpha=0.5)
                axes[0].plot(range(t+1), dtl.x_log[3, 0:t+1], 'red')
                axes[0].plot(range(t+1, t+T_outer+1), pred_UAV_vel_y_log, 'red', alpha=0.5)
                axes[1].plot(range(t+1), dtl.xb_log[2, 0:t+1], 'blue')
                axes[1].plot(range(t+1, t+T_outer+1), pred_USV_vel_x_log, 'blue', alpha=0.5)
                axes[1].plot(range(t+1), dtl.xb_log[3, 0:t+1], 'red')
                axes[1].plot(range(t+1, t+T_outer+1), pred_USV_vel_y_log, 'red', alpha=0.5)

                if self.file_types[file_index] == PARALLEL:
                    pred_UAV_vel_inner_x_log = dtl.UAV_inner_traj_log[2::dtl.nUAV, t]
                    pred_UAV_vel_inner_y_log = dtl.UAV_inner_traj_log[3::dtl.nUAV, t]
                    pred_USV_vel_inner_x_log = dtl.USV_inner_traj_log[2::dtl.nUSV, t]
                    pred_USV_vel_inner_y_log = dtl.USV_inner_traj_log[3::dtl.nUSV, t]
                    axes[0].plot(range(t+1, t+T_inner+1), pred_UAV_vel_inner_x_log, 'green', alpha=0.3)
                    axes[0].plot(range(t+1, t+T_inner+1), pred_UAV_vel_inner_y_log, 'yellow', alpha=0.3)
                    axes[1].plot(range(t+1, t+T_inner+1), pred_USV_vel_inner_x_log, 'green', alpha=0.3)
                    axes[1].plot(range(t+1, t+T_inner+1), pred_USV_vel_inner_y_log, 'yellow', alpha=0.3)

                axes[0].add_collection(patch_collection_UAV)
                axes[1].add_collection(patch_collection_USV)
                # ax.add_collection(patch_collection_slack)
                plt.xlabel('time [iterations]')
                plt.ylabel('velocity [m/s]')
                try:
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()

    def plot_with_constraints(self, real_time = False, perspective = ACTUAL):
        p = self.p
        self.should_close = False

        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal', 'vertical'], self.p)
            # print dtl.x_log_raw[0, 0:3]
            # print dtl.x_log[0, 0:3]
            # return
            forbidden_area_1 = Polygon([ (dl, dtl.hb),\
                                         (ds, dtl.hb+hs),\
                                         (35, dtl.hb+hs),\
                                         (35, dtl.hb)], True)
            forbidden_area_2 = Polygon([ (-dl, dtl.hb),\
                                         (-ds, dtl.hb+hs),\
                                         (-35, dtl.hb+hs),\
                                         (-35, dtl.hb)], True)
            safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.5, color='grey')

            if perspective == ACTUAL:
                xb_log = dtl.xb_log#np.loadtxt(dir_path + dir + '/xb_log.txt')
                USV_traj_log = dtl.USV_traj_log#np.loadtxt(dir_path + dir + '/USV_traj_log.txt')
                x_log = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
            elif perspective == UAV:
                if self.file_types[file_index] == CENTRALISED:
                    USV_traj_log = dtl.USV_traj_log
                else:
                    USV_traj_log = dtl.USV_traj_log_UAV
                xb_log = dtl.xb_log_UAV
                x_log = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
            elif perspective == USV:
                xb_log = dtl.xb_log
                USV_traj_log = dtl.USV_traj_log
                if self.file_types[file_index] == CENTRALISED:
                    x_log = dtl.x_log
                    UAV_traj_log = dtl.UAV_traj_log
                else:
                    x_log = dtl.x_log_USV
                    UAV_traj_log = dtl.UAV_traj_log_USV
            elif perspective == RAW:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                xb_log = dtl.xb_log_raw
                USV_traj_log = dtl.USV_traj_log_raw
            if perspective == RAW_UAV:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                USV_traj_log = dtl.USV_traj_log_UAV_raw
                xb_log = USV_traj_log[0:dtl.nUSV, :]

            if perspective == RAW:
                xv_log = dtl.xv_log_raw
            else:
                xv_log = dtl.xv_log

            time_len = dtl.x_log.shape[1]-1
            dist_log = np.sqrt( np.square(x_log[0, 0:time_len] - xb_log[0, 0:time_len]) + \
                np.square(x_log[1, 0:time_len] - xb_log[1, 0:time_len]) )
            if self.file_types[file_index] == PARALLEL:
                T_inner = dtl.vert_inner_traj_log.shape[0]//dtl.nv

            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:
                ax.cla()
                dist_pred_log = np.sqrt( np.square(UAV_traj_log[0::dtl.nUAV, t] - USV_traj_log[0::dtl.nUSV, t])\
                    + np.square(UAV_traj_log[1::dtl.nUAV, t] - USV_traj_log[1::dtl.nUSV, t]) )
                if perspective != RAW:
                    vert_pred_log = dtl.vert_traj_log[0::dtl.nv, t]
                else:
                    vert_pred_log = dtl.vert_traj_log_raw[0::dtl.nv, t]

                if self.file_types[file_index] == PARALLEL:
                    # IMPORTANT: ACTUAL and UAV doesn't really make sense here, there's no "actual" predicted trajectory
                    # EDIT: Well, couldn't you have a traj predicted by e.g. the UAV be "actual" if you use the USV's prediction of its own position, instead of the UAV's?
                    if perspective == ACTUAL:
                        dist_inner_pred_log = np.sqrt( \
                            np.square(dtl.UAV_inner_traj_log[0::dtl.nUAV, t] - dtl.USV_inner_traj_log[0::dtl.nUSV, t])\
                            + np.square(dtl.UAV_inner_traj_log[1::dtl.nUAV, t] - dtl.USV_inner_traj_log[1::dtl.nUSV, t]) )
                    elif perspective == UAV:
                        dist_inner_pred_log = np.sqrt( \
                            np.square(dtl.UAV_inner_traj_log[0:T_inner*dtl.nUAV:dtl.nUAV, t]\
                            - USV_traj_log[0:T_inner*dtl.nUSV:dtl.nUSV, t])\
                            + np.square(dtl.UAV_inner_traj_log[1:T_inner*dtl.nUAV:dtl.nUAV, t]\
                            - USV_traj_log[1:T_inner*dtl.nUSV:dtl.nUSV, t])\
                        )
                    elif perspective == RAW:
                        dist_inner_pred_log = np.sqrt( \
                            np.square(dtl.UAV_inner_traj_log_raw[0::dtl.nUAV, t] - dtl.USV_inner_traj_log_raw[0::dtl.nUSV, t])\
                            + np.square(dtl.UAV_inner_traj_log_raw[1::dtl.nUAV, t] - dtl.USV_inner_traj_log_raw[1::dtl.nUSV, t]) )

                    if perspective != RAW:
                        vert_inner_pred_log = dtl.vert_inner_traj_log[0::dtl.nv, t]
                    elif perspective == RAW:
                        vert_inner_pred_log = dtl.vert_inner_traj_log_raw[0::dtl.nv, t]

                # TODO: When perspective is ACTUAL, you should use true future trajectory
                # instead of predicted future trajectories, no? Naah, would only work if you did that only
                # for horizontal, and kept predicted for vertical. There seems to be no point to it really
                ax.plot(dist_log[0:t+1], xv_log[0, 0:t+1], 'blue')
                ax.plot(dist_pred_log, vert_pred_log, 'green', alpha=0.5)
                if self.file_types[file_index] == PARALLEL:
                    ax.plot(dist_inner_pred_log, vert_inner_pred_log, 'yellow', alpha=0.5)
                ax.add_collection(safety_patch_collection)
                plt.xlabel('horizontal distance [m]')
                plt.ylabel('height [m]')
                try:
                    # ax.set_xlim([0,5])
                    # ax.set_ylim([0,8])
                    plt.grid(True)
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()

    def compare_topviews(self, real_time = False):
        p = self.p
        self.should_close = False
        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()
            UAV_traj_log_UAV = np.loadtxt(dir_path + dir + '/UAV_traj_log.txt')
            USV_traj_log_USV = np.loadtxt(dir_path + dir + '/USV_traj_log.txt')
            USV_traj_log_UAV = np.loadtxt(dir_path + dir + '/UAV/USV_traj_log.txt')
            UAV_traj_log_USV = np.loadtxt(dir_path + dir + '/USV/UAV_traj_log.txt')
            x_log_UAV  = np.loadtxt(dir_path + dir + '/x_log.txt')
            xb_log_UAV = USV_traj_log_UAV[0:dtl.nUSV, :]
            xb_log_USV = np.loadtxt(dir_path + dir + '/xb_log.txt')
            x_log_USV = UAV_traj_log_USV[0:dtl.nUAV, :]

            if self.file_types[file_index] == PARALLEL:
                UAV_inner_traj_log = np.loadtxt(dir_path + dir + '/UAV_inner_traj_log.txt')
                USV_inner_traj_log = np.loadtxt(dir_path + dir + '/USV_inner_traj_log.txt')

            time_len = x_log_UAV.shape[1]-1
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:
                ax.cla()
                # Actual trajectories
                ax.plot(x_log_UAV[0, 0:t+1], x_log_UAV[1, 0:t+1], 'bx')
                ax.plot(xb_log_UAV[0, 0:t+1], xb_log_UAV[1, 0:t+1], 'gx')
                ax.plot(x_log_USV[0, 0:t+1], x_log_USV[1, 0:t+1], 'yx')
                ax.plot(xb_log_USV[0, 0:t+1], xb_log_USV[1, 0:t+1], 'rx')
                plt.xlabel('x-position [m]')
                plt.ylabel('y-position [m]')
                plt.legend(['UAV trajectory', 'USV trajectory'])
                plt.grid(True)
                try:
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()# raw_input()

    def plot_time_evolution(self, real_time = False):
        p = self.p
        self.should_close = False
        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal', 'vertical'], self.p)

            x_log_raw = dtl.x_log_raw
            UAV_traj_log_raw = dtl.UAV_traj_log_raw
            xb_log_raw = dtl.xb_log_raw
            USV_traj_log_raw = dtl.USV_traj_log_raw
            x_log = dtl.x_log
            UAV_traj_log = dtl.UAV_traj_log
            xb_log = dtl.xb_log
            USV_traj_log = dtl.USV_traj_log

            # UAV_traj_log_UAV = np.loadtxt(dir_path + dir + '/UAV_traj_log.txt')
            # USV_traj_log_USV = np.loadtxt(dir_path + dir + '/USV_traj_log.txt')
            # USV_traj_log_UAV = np.loadtxt(dir_path + dir + '/UAV/USV_traj_log.txt')
            # UAV_traj_log_USV = np.loadtxt(dir_path + dir + '/USV/UAV_traj_log.txt')
            # x_log_UAV  = np.loadtxt(dir_path + dir + '/x_log.txt')
            # xb_log_UAV = USV_traj_log_UAV[0:dtl.nUSV, :]
            # xb_log_USV = np.loadtxt(dir_path + dir + '/xb_log.txt')
            # x_log_USV = UAV_traj_log_USV[0:dtl.nUAV, :]

            T = UAV_traj_log.shape[0]//dtl.nUAV

            time_len = x_log.shape[1]-1
            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            dist_log = np.sqrt( np.square(x_log[0, 0:time_len] - xb_log[0, 0:time_len]) + \
                np.square(x_log[1, 0:time_len] - xb_log[1, 0:time_len]) )

            dist_log_raw = np.sqrt( np.square(x_log_raw[0, 0:time_len] - xb_log_raw[0, 0:time_len]) + \
                np.square(x_log_raw[1, 0:time_len] - xb_log_raw[1, 0:time_len]) )

            for t in time:
                ax.cla()

                dist_pred_log = np.sqrt( np.square(UAV_traj_log[0::dtl.nUAV, t] - USV_traj_log[0::dtl.nUSV, t])\
                    + np.square(UAV_traj_log[1::dtl.nUAV, t] - USV_traj_log[1::dtl.nUSV, t]) )
                dist_pred_log_raw = np.sqrt( np.square(UAV_traj_log_raw[0::dtl.nUAV, t] - USV_traj_log_raw[0::dtl.nUSV, t])\
                    + np.square(UAV_traj_log_raw[1::dtl.nUAV, t] - USV_traj_log_raw[1::dtl.nUSV, t]) )



                ax.plot(range(t+1), dist_log[0:t+1], 'b')
                ax.plot(range(t+1), dist_log_raw[0:t+1], 'r')
                ax.plot(range(t, t+T), dist_pred_log, 'b', alpha=0.4)
                ax.plot(range(t, t+T), dist_pred_log_raw, 'r', alpha=0.4)
                # ax.plot(range(t+1), x_log_UAV[0, 0:t+1], 'blue')
                # ax.plot(range(t+1), x_log_USV[0, 0:t+1], 'red')
                # ax.plot(range(t, t+T), UAV_traj_log_UAV[0::dtl.nUAV, t], 'green', alpha=0.5)
                # ax.plot(range(t, t+T), UAV_traj_log_USV[0::dtl.nUSV, t], 'yellow', alpha=0.5)
                plt.xlabel('time [s]')
                plt.ylabel('value [m]')
                plt.legend(['Real-time', 'Raw'])
                plt.grid(True)
                try:
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()# raw_input()

    def plot_altitude(self, real_time = False, perspective = ACTUAL):
        p = self.p
        self.should_close = False

        for file_index, dir in enumerate(self.files):
            fig = plt.figure()
            fig.canvas.mpl_connect('close_event', self.handle_close)
            ax = plt.axes()

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal', 'vertical'], self.p)

            if perspective == ACTUAL:
                xb_log = dtl.xb_log
                USV_traj_log = dtl.USV_traj_log
                x_log = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
            elif perspective == UAV:
                if self.file_types[file_index] == CENTRALISED:
                    USV_traj_log = dtl.USV_traj_log
                else:
                    USV_traj_log = dtl.USV_traj_log_UAV
                xb_log = dtl.xb_log_UAV
                x_log = dtl.x_log
                UAV_traj_log = dtl.UAV_traj_log
            elif perspective == USV:
                xb_log = dtl.xb_log
                USV_traj_log = dtl.USV_traj_log
                if self.file_types[file_index] == CENTRALISED:
                    x_log = dtl.x_log
                    UAV_traj_log = dtl.UAV_traj_log
                else:
                    x_log = dtl.x_log_USV
                    UAV_traj_log = dtl.UAV_traj_log_USV
            elif perspective == RAW:
                xb_log = dtl.xb_log_raw
                USV_traj_log = dtl.USV_traj_log_raw
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
            if perspective == RAW_UAV:
                x_log = dtl.x_log_raw
                UAV_traj_log = dtl.UAV_traj_log_raw
                USV_traj_log = dtl.USV_traj_log_UAV_raw
                xb_log = USV_traj_log[0:dtl.nUSV, :]

            time_len = x_log.shape[1]-1
            dist_log = np.sqrt( np.square(x_log[0, 0:time_len] - xb_log[0, 0:time_len]) + \
                np.square(x_log[1, 0:time_len] - xb_log[1, 0:time_len]) )
            b_log = (dist_log < ds).astype(int)
            vert_const_log = np.dot(np.diag(b_log), (hs*dl - hs*dist_log)/(dl - ds)) + np.dot(np.diag(1-b_log), np.full((time_len, ), hs))
            vert_const_log = np.maximum(vert_const_log, np.zeros(vert_const_log.shape))
            T = UAV_traj_log.shape[0]//dtl.nUAV
            if self.file_types[file_index] == PARALLEL:
                T_inner = dtl.vert_inner_traj_log.shape[0]//dtl.nv

            if real_time:
                time = range(time_len)
            else:
                time = [time_len-1]

            for t in time:
                ax.cla()
                # dist_pred_log = np.sqrt( np.square(UAV_traj_log[0::dtl.nUAV, t] - USV_traj_log[0::dtl.nUSV, t])\
                #     + np.square(UAV_traj_log[1::dtl.nUAV, t] - USV_traj_log[1::dtl.nUSV, t]) )
                if perspective != RAW:
                    vert_pred_log = dtl.vert_traj_log[0::dtl.nv, t]
                    xv_log = dtl.xv_log
                if perspective == RAW:
                    vert_pred_log = dtl.vert_traj_log_raw[0::dtl.nv, t]
                    xv_log = dtl.xv_log_raw

                ax.plot(range(t+1), xv_log[0, 0:t+1], 'blue')
                ax.plot(range(t+1), vert_const_log[0:t+1], 'r--')
                # ax.plot(range(t, t+T), vert_pred_log, 'green', alpha=0.5)
                # if self.file_types[file_index] == PARALLEL:
                #     vert_inner_pred_log = dtl.vert_inner_traj_log[0::dtl.nv, t]
                #     ax.plot(range(t, t+T_inner), vert_inner_pred_log, 'yellow', alpha=0.5)
                plt.xlabel('iteration')
                plt.ylabel('altitude [m]')
                plt.legend(['UAV altitude', 'Altitude constraint'])
                try:
                    plt.grid(True)
                    plt.pause(0.05)
                except:
                    # Window was probably closed
                    return
                if self.should_close:   # Window was closed
                    return
            fig.show()
        plt.show()

    def plot_time_histogram(self):
        fig = plt.figure()
        ax = plt.axes()
        for file_index, dir in enumerate(self.files):
            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['time'], self.p)

            ax.hist(dtl.hor_mean_UAV, bins=10, color=self.colors[file_index])
            # if file_index == 0:
            # _, bins, _ = ax.hist(dtl.mean_iteration_UAV, bins=10, color=self.colors[file_index])
            # else:
            #     ax.hist(dtl.mean_iteration_UAV, bins=bins)

        plt.xlabel('mean iteration time [s]')
        plt.ylabel('number of occurrences')
        plt.legend(['Cascading Distributed', 'Distributed', 'Centralized'])
        plt.grid(True)
        plt.show()

    def plot_time_curve(self):
        fig = plt.figure()
        ax = plt.axes()
        for file_index, dir in enumerate(self.files):
            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['time'], self.p)

            time_len = dtl.mean_iteration_UAV.shape[0]
            ax.plot(range(time_len),dtl.mean_iteration_UAV, color=self.colors[file_index])

        plt.grid(True)
        plt.show()

    def store_formatted_descent(self, perspective = ACTUAL):
        p = self.p

        num_files = len(self.files)

        for file_index, dir in enumerate(self.files):

            if file_index == 0:
                postfix = 'centralised'
            elif file_index == 1:
                postfix = 'distributed'
            elif file_index == 2:
                postfix = 'cascading'
            else:
                postfix = str(file_index)

            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['horizontal', 'vertical'], self.p)

            if dtl.used_dropout:
                postpostfix = '_dropout'
            else:
                postpostfix = ''

            hs = dtl.hs

            if perspective == ACTUAL:
                xb_log = dtl.xb_log
                x_log = dtl.x_log
            elif perspective == UAV:
                xb_log = dtl.xb_log_UAV
                x_log = dtl.x_log
            elif perspective == USV:
                xb_log = dtl.xb_log
                if self.file_types[file_index] == CENTRALISED:
                    x_log = dtl.x_log
                else:
                    x_log = dtl.x_log_USV
            elif perspective == RAW:
                xb_log = dtl.xb_log_raw
                x_log = dtl.x_log_raw
            elif perspective == RAW_UAV:
                x_log = dtl.x_log_raw
                USV_traj_log = dtl.USV_traj_log_UAV_raw     # WAIT!!!
                xb_log = USV_traj_log[0:dtl.nUSV, :]


            time_len = x_log.shape[1]

            if perspective != RAW:
                height_log = dtl.xv_log[0, :] - dtl.hb
            else:
                height_log = dtl.xv_log_raw[0, :] - dtl.hb
            dx_log = x_log[0, :] - xb_log[0, :]
            dy_log = x_log[1, :] - xb_log[1, :]
            dist_log = np.sqrt( np.square(dx_log) + np.square(dy_log) )
            b_log = (dist_log < ds).astype(int)
            vert_const_log = np.dot(np.diag(b_log), (hs*dl - hs*dist_log)/(dl - ds)) + np.dot(np.diag(1-b_log), np.full((time_len, ), hs))
            vert_const_log = np.maximum(vert_const_log, np.zeros(vert_const_log.shape))

            # Finds landing time
            has_landed = False
            for t_land in range(time_len):
                if not has_landed and height_log[t_land] <= 0:
                    has_landed = True
                if has_landed and height_log[t_land] > 0:
                    break

            # Finds break in communication times
            if dtl.used_dropout:
                t_break_start = -1
                t_break_end = -1
                for t in range(time_len):
                    if dtl.new_time_stamps[t] >= dtl.dropout_start and t_break_start == -1:
                        t_break_start = t
                    if dtl.new_time_stamps[t] >= dtl.dropout_end and t_break_end == -1:
                        t_break_end = t
                        break

            dist_range = np.arange(min(dist_log[0:t_land]), max(dist_log[0:t_land]), step=0.1)
            b_range = (dist_range < ds).astype(int)
            vert_const_range = np.dot(np.diag(b_range), (hs*dl - hs*dist_range)/(dl - ds)) + np.dot(np.diag(1-b_range), np.full((len(dist_range), ), hs))
            vert_const_range = np.maximum(vert_const_range, np.zeros(vert_const_range.shape))

            if not os.path.isdir(dir_path+dir+'/Descent_Formated'):
                os.mkdir(dir_path+dir+'/Descent_Formated')

            new_mat = np.block([[dtl.new_time_stamps[0:t_land]], [height_log[0:t_land]],\
                [vert_const_log[0:t_land]], [dx_log[0:t_land]], [dy_log[0:t_land]], [dist_log[0:t_land]]]).T
            other_mat = np.block([[dist_range], [vert_const_range]]).T
            header = 'time,altitude,vertical constraint,dx,dy,distance'
            other_header = 'distance range,vertical constraint range'
            np.savetxt(dir_path+dir+'/Descent_Formated/' + postfix + postpostfix + '.csv', new_mat, delimiter=',', header=header, comments='')
            np.savetxt(dir_path+dir+'/Descent_Formated/' + postfix + postpostfix + '_ranges.csv', other_mat, delimiter=',', header=other_header, comments='')

            if dtl.used_dropout:
                pre_mat = np.block([
                    [dtl.new_time_stamps[0:t_break_start]],
                    [height_log[0:t_break_start]],
                    [dist_log[0:t_break_start]]
                ]).T
                mat = np.block([
                    [dtl.new_time_stamps[t_break_start:t_break_end]],
                    [height_log[t_break_start:t_break_end]],
                    [dist_log[t_break_start:t_break_end]]
                ]).T
                post_mat = np.block([
                    [dtl.new_time_stamps[t_break_end:t_land]],
                    [height_log[t_break_end:t_land]],
                    [dist_log[t_break_end:t_land]]
                ]).T
                header = 'time,altitude,distance'
                np.savetxt(dir_path+dir+'/Descent_Formated/' + postfix + '_predropout.csv', pre_mat, delimiter=',', header=header, comments='')
                np.savetxt(dir_path+dir+'/Descent_Formated/' + postfix + '_duringdropout.csv', mat, delimiter=',', header=header, comments='')
                np.savetxt(dir_path+dir+'/Descent_Formated/' + postfix + '_postdropout.csv', post_mat, delimiter=',', header=header, comments='')

    def store_formatted_durations(self):

        # Find appropriate bin width
        dataloaders = []
        max_width = 0
        for file_index, dir in enumerate(self.files):
            dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['time'], self.p)
            dataloaders.append(dtl)
            data_width = max(dtl.mean_iteration_UAV) - min(dtl.mean_iteration_UAV)
            max_width = max(data_width, max_width)

        bin_width = max_width*0.1

        for file_index, dir in enumerate(self.files):

            if file_index == 0:
                postfix = 'centralised'
            elif file_index == 1:
                postfix = 'distributed'
            elif file_index == 2:
                postfix = 'cascading'
            else:
                post_fix = str(file_index)

            # dtl = DataLoader(dir_path+dir, self.file_types[file_index], ['time'], self.p)
            dtl = dataloaders[file_index]

            data_width = max(dtl.mean_iteration_UAV) - min(dtl.mean_iteration_UAV)
            num_bins = int(np.ceil(data_width/bin_width))
            (n, bins, _) = plt.hist(dtl.mean_iteration_UAV, bins=num_bins)
            plt.show()
            bin_mids = np.empty((len(bins)-1,))
            for i in range(len(bins)-1):
                bin_mids[i] = (bins[i] + bins[i+1])*0.5

            headers='bins,frequency'
            mat = np.block([[bin_mids], [n]])

            if not os.path.isdir(dir_path+'Formated_Durations'):
                os.mkdir(dir_path+'Formated_Durations')
            np.savetxt(dir_path+'Formated_Durations/time_' + postfix + '.csv', mat.T, delimiter=',', header=headers, comments='')

    def handle_close(self, evt):
        self.should_close = True

    def get_vel_polygon(self, bound, shift=0):
        return Polygon([ (-100,   1000*bound+shift),\
                          (1000,   1000*bound+shift),\
                          (1000,   bound+shift),\
                          (-100,   bound+shift)], True)

class DataLoader:

    def __init__(self, dir_path, problem_type, data_types, params):
        # self.debug_convert_txt_to_csv(dir_path, problem_type)
        # exit()
        p = params
        UAV_time_stamps = np.loadtxt(dir_path + '/UAV_time_stamps.csv', delimiter=',')
        USV_time_stamps = np.loadtxt(dir_path + '/USV_time_stamps.csv', delimiter=',')
        if USE_TIME_CORRECTION:
            time_list = np.loadtxt(dir_path + '/TEST/time_diff.txt')
            time_diff = time_list[0] + time_list[1]*0.000000001
            UAV_time_stamps = UAV_time_stamps - time_diff
        t_0 = np.minimum(UAV_time_stamps[0], USV_time_stamps[0])
        t_f = np.maximum(UAV_time_stamps[-1], USV_time_stamps[-1]) - t_0
        UAV_time_stamps = UAV_time_stamps - t_0
        USV_time_stamps = USV_time_stamps - t_0
        new_time_stamps = np.arange(0, t_f, 0.05)
        self.new_time_stamps = new_time_stamps
        print "Time span:", len(new_time_stamps), len(UAV_time_stamps), len(USV_time_stamps)    # DEBUG PRINT
        print UAV_time_stamps[-1] - UAV_time_stamps[0]
        print USV_time_stamps[-1] - USV_time_stamps[0]
        (self.dl, self.ds, self.hs) = self.get_safety_region(dir_path)
        (self.used_dropout, self.dropout_lower_bound, self.dropout_upper_bound) = self.get_dropout_bounds(dir_path)
        if self.used_dropout:
            self.dropout_start = min(UAV_time_stamps[self.dropout_lower_bound], USV_time_stamps[self.dropout_lower_bound])
            self.dropout_end = min(UAV_time_stamps[self.dropout_upper_bound], USV_time_stamps[self.dropout_upper_bound])

        for data_type in data_types:
            if data_type == 'horizontal':
                self.UAV_traj_log_raw = np.loadtxt(dir_path + '/UAV_traj_log.csv', delimiter=',')
                self.USV_traj_log_raw = np.loadtxt(dir_path + '/USV_traj_log.csv', delimiter=',')
                self.x_log_raw  = np.loadtxt(dir_path + '/x_log.csv', delimiter=',')
                self.xb_log_raw = np.loadtxt(dir_path + '/xb_log.csv', delimiter=',')
                self.nUAV = self.x_log_raw.shape[0]
                self.nUSV = self.xb_log_raw.shape[0]

                self.UAV_traj_log = self.get_interpolated_traj(self.UAV_traj_log_raw, UAV_time_stamps, new_time_stamps)
                if problem_type == CENTRALISED:
                    self.USV_traj_log = self.get_interpolated_traj(self.USV_traj_log_raw, UAV_time_stamps, new_time_stamps)
                else:
                    self.USV_traj_log = self.get_interpolated_traj(self.USV_traj_log_raw, USV_time_stamps, new_time_stamps)
                if problem_type != CENTRALISED:
                    self.USV_traj_log_UAV_raw = np.loadtxt(dir_path + '/UAV/USV_traj_log.csv', delimiter=',')
                    # if self.nUSV == 6:
                    #     self.USV_traj_log_raw = self.proj_6_to_4(self.USV_traj_log_raw)
                    self.UAV_traj_log_USV_raw = np.loadtxt(dir_path + '/USV/UAV_traj_log.csv', delimiter=',')
                    self.xb_log_UAV_raw = self.USV_traj_log_UAV_raw[0:self.nUSV, :]
                    self.x_log_USV_raw = self.UAV_traj_log_USV_raw[0:self.nUAV, :]
                    self.USV_traj_log_UAV = self.get_interpolated_traj(self.USV_traj_log_UAV_raw, UAV_time_stamps, new_time_stamps)
                    self.UAV_traj_log_USV = self.get_interpolated_traj(self.UAV_traj_log_USV_raw, USV_time_stamps, new_time_stamps)
                    self.xb_log_UAV = self.get_interpolated_traj(self.xb_log_UAV_raw, UAV_time_stamps, new_time_stamps)
                    self.x_log_USV = self.get_interpolated_traj(self.x_log_USV_raw, USV_time_stamps, new_time_stamps)
                else:
                    # In centralised case, the only log of USV trajectories is already from the UAV's perspective
                    self.xb_log_UAV_raw = self.USV_traj_log_raw[0:self.nUSV, :]
                    self.xb_log_UAV = self.get_interpolated_traj(self.xb_log_UAV_raw, UAV_time_stamps, new_time_stamps)
                self.x_log  = self.get_interpolated_traj(self.x_log_raw, UAV_time_stamps, new_time_stamps)
                self.xb_log = self.get_interpolated_traj(self.xb_log_raw, USV_time_stamps, new_time_stamps)
                self.u_log_raw = np.loadtxt(dir_path + '/uUAV_log.csv', delimiter=',')
                self.ub_log_raw = np.loadtxt(dir_path + '/uUSV_log.csv', delimiter=',')
                self.u_log  = self.get_interpolated_traj(self.u_log_raw, UAV_time_stamps, new_time_stamps)
                self.ub_log = self.get_interpolated_traj(self.ub_log_raw, USV_time_stamps, new_time_stamps)

                self.mUAV = self.u_log_raw.shape[0]
                self.mUSV = self.ub_log_raw.shape[0]

                if problem_type == PARALLEL:
                    self.UAV_inner_traj_log_raw = np.loadtxt(dir_path + '/UAV_inner_traj_log.csv', delimiter=',')
                    self.USV_inner_traj_log_raw = np.loadtxt(dir_path + '/USV_inner_traj_log.csv', delimiter=',')

                    self.UAV_inner_traj_log = self.get_interpolated_traj(self.UAV_inner_traj_log_raw, UAV_time_stamps, new_time_stamps)
                    self.USV_inner_traj_log = self.get_interpolated_traj(self.USV_inner_traj_log_raw, USV_time_stamps, new_time_stamps)
            elif data_type == 'vertical':
                self.xv_log_raw = np.loadtxt(dir_path + '/xv_log.csv', delimiter=',')
                self.vert_traj_log_raw = np.loadtxt(dir_path + '/vert_traj_log.csv', delimiter=',')
                self.s_vert_log_raw = np.loadtxt(dir_path + '/s_vert_log.csv', delimiter=',')

                self.xv_log = self.get_interpolated_traj(self.xv_log_raw, UAV_time_stamps, new_time_stamps)
                self.vert_traj_log = self.get_interpolated_traj(self.vert_traj_log_raw, UAV_time_stamps, new_time_stamps)
                self.s_vert_log = self.get_adjusted_array(self.s_vert_log_raw, UAV_time_stamps, new_time_stamps)

                self.nv = self.xv_log_raw.shape[0]

                self.hb = self.get_USV_altitude(dir_path)

                if problem_type == PARALLEL:
                    self.vert_inner_traj_log_raw = np.loadtxt(dir_path + '/vert_inner_traj_log.csv', delimiter=',')

                    self.vert_inner_traj_log = self.get_interpolated_traj(self.vert_inner_traj_log_raw, UAV_time_stamps, new_time_stamps)

            elif data_type == 'time':
                self.mean_iteration_UAV = np.loadtxt(dir_path + '/TEST/MEAN.csv', delimiter=',')
                self.median_iteration = np.loadtxt(dir_path + '/TEST/MEDIAN.csv', delimiter=',')
                self.mean_iteration_USV = np.loadtxt(dir_path + '/TEST/MEAN_USV.csv', delimiter=',')
                self.median_iteration_USV = np.loadtxt(dir_path + '/TEST/MEDIAN_USV.csv', delimiter=',')
                self.hor_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEAN.csv', delimiter=',')
                self.hor_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN.csv', delimiter=',')
                self.vert_mean = np.loadtxt(dir_path + '/TEST/VERT_MEAN.csv', delimiter=',')
                self.vert_median = np.loadtxt(dir_path + '/TEST/VERT_MEDIAN.csv', delimiter=',')
                self.landing_times = np.loadtxt(dir_path + '/TEST/LANDING_TIMES.csv', delimiter=',')
                if problem_type != CENTRALISED:
                    self.hor_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_MEAN_USV.csv', delimiter=',')
                    self.hor_median_USV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN_USV.csv', delimiter=',')
                if problem_type == PARALLEL:
                    self.hor_inner_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN.csv', delimiter=',')
                    self.hor_inner_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN.csv', delimiter=',')
                    self.hor_inner_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN_USV.csv', delimiter=',')
                    self.hor_inner_median_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN_USV.csv', delimiter=',')
                    self.vert_inner_mean = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEAN.csv', delimiter=',')
                    self.vert_inner_median = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEDIAN.csv', delimiter=',')




        # print USV_inner_traj_log[0, t] - xb_log[0, t]
        # TODO: DELETE, ONLY FOR DEBUG!!!
        # fig1 = plt.figure()
        # ax1 = plt.axes()
        # ax1.plot(range(self.vert_traj_log_raw.shape[1]), self.vert_traj_log_raw[0,:], 'rx', alpha=0.5)
        # ax1.plot(range(self.vert_traj_log.shape[1]), self.vert_traj_log[0,:], 'bx', alpha=0.5)
        # # ax1.plot(UAV_time_stamps, self.vert_traj_log_raw[0,:], 'rx', alpha=0.5)
        # # ax1.plot(new_time_stamps, self.vert_traj_log[0,:], 'bx', alpha=0.5)

        # fig2 = plt.figure()
        # ax2 = plt.axes()
        # ax2.plot(USV_time_stamps[:], self.xb_log_raw[0, :-1], 'r')
        # ax2.plot(UAV_time_stamps[:-1], self.USV_inner_traj_log_raw[0, :-1], 'b')
        # fig3 = plt.figure()
        # ax3 = plt.axes()
        # ax3.plot(new_time_stamps, self.xb_log[1, :], '-', color='orange')
        # ax3.plot(new_time_stamps, self.USV_inner_traj_log[1, :], 'g')
        # fig1 = plt.figure()
        # ax1 = plt.axes()
        # # ax1.plot(range(len(new_time_stamps)), new_time_stamps, 'kx')
        # # ax1.plot(range(500), UAV_time_stamps, 'rx')
        # # ax1.plot(range(500), USV_time_stamps, 'b')

        # plt.show()
        return

    def __init__alt(self, dir_path, problem_type, data_types, perspective, raw, params):
        # # self.debug_convert_txt_to_csv(dir_path, problem_type)
        # # exit()
        # p = params
        # for data_type in data_types:
        #
        #     UAV_time_stamps = np.loadtxt(dir_path + '/UAV_time_stamps.csv', delimiter=',')
        #     USV_time_stamps = np.loadtxt(dir_path + '/USV_time_stamps.csv', delimiter=',')
        #     if USE_TIME_CORRECTION:
        #         time_list = np.loadtxt(dir_path + '/TEST/time_diff.txt')
        #         time_diff = time_list[0] + time_list[1]*0.000000001
        #         UAV_time_stamps = UAV_time_stamps - time_diff
        #     t_0 = np.minimum(UAV_time_stamps[0], USV_time_stamps[0])
        #     t_f = np.maximum(UAV_time_stamps[-1], USV_time_stamps[-1]) - t_0
        #     UAV_time_stamps = UAV_time_stamps - t_0
        #     USV_time_stamps = USV_time_stamps - t_0
        #     new_time_stamps = np.arange(0, t_f, 0.05)
        #     self.new_time_stamps = new_time_stamps
        #     print "Time span:", len(new_time_stamps), len(UAV_time_stamps), len(USV_time_stamps)    # DEBUG PRINT
        #     print UAV_time_stamps[-1] - UAV_time_stamps[0]
        #     print USV_time_stamps[-1] - USV_time_stamps[0]
        #
        #     if data_type == 'horizontal':
        #         self.nUAV = self.x_log_raw.shape[0]
        #         self.nUSV = self.xb_log_raw.shape[0]
        #         if perspective == ACTUAL or perspective == UAV:
        #             self.UAV_traj_log = np.loadtxt(dir_path + '/UAV_traj_log.csv', delimiter=',')
        #             self.x_log  = np.loadtxt(dir_path + '/x_log.csv', delimiter=',')
        #         if perspective == ACTUAL or perspective == USV:
        #             self.USV_traj_log = np.loadtxt(dir_path + '/USV_traj_log.csv', delimiter=',')
        #             self.xb_log = np.loadtxt(dir_path + '/xb_log.csv', delimiter=',')
        #             # UPDATED ABOVE HERE, OLD BELOW HERE!!!
        #         self.UAV_traj_log_raw = np.loadtxt(dir_path + '/UAV_traj_log.csv', delimiter=',')
        #         self.USV_traj_log_raw = np.loadtxt(dir_path + '/USV_traj_log.csv', delimiter=',')
        #         self.x_log_raw  = np.loadtxt(dir_path + '/x_log.csv', delimiter=',')
        #         self.xb_log_raw = np.loadtxt(dir_path + '/xb_log.csv', delimiter=',')
        #
        #         self.UAV_traj_log = self.get_interpolated_traj(self.UAV_traj_log_raw, UAV_time_stamps, new_time_stamps)
        #         if problem_type == CENTRALISED:
        #             self.USV_traj_log = self.get_interpolated_traj(self.USV_traj_log_raw, UAV_time_stamps, new_time_stamps)
        #         else:
        #             self.USV_traj_log = self.get_interpolated_traj(self.USV_traj_log_raw, USV_time_stamps, new_time_stamps)
        #         if problem_type != CENTRALISED:
        #             self.USV_traj_log_UAV_raw = np.loadtxt(dir_path + '/UAV/USV_traj_log.csv', delimiter=',')
        #             # if self.nUSV == 6:
        #             #     self.USV_traj_log_raw = self.proj_6_to_4(self.USV_traj_log_raw)
        #             self.UAV_traj_log_USV_raw = np.loadtxt(dir_path + '/USV/UAV_traj_log.csv', delimiter=',')
        #             self.xb_log_UAV_raw = self.USV_traj_log_UAV_raw[0:self.nUSV, :]
        #             self.x_log_USV_raw = self.UAV_traj_log_USV_raw[0:self.nUAV, :]
        #             self.USV_traj_log_UAV = self.get_interpolated_traj(self.USV_traj_log_UAV_raw, UAV_time_stamps, new_time_stamps)
        #             self.UAV_traj_log_USV = self.get_interpolated_traj(self.UAV_traj_log_USV_raw, USV_time_stamps, new_time_stamps)
        #             self.xb_log_UAV = self.get_interpolated_traj(self.xb_log_UAV_raw, UAV_time_stamps, new_time_stamps)
        #             self.x_log_USV = self.get_interpolated_traj(self.x_log_USV_raw, USV_time_stamps, new_time_stamps)
        #         else:
        #             # In centralised case, the only log of USV trajectories is already from the UAV's perspective
        #             self.xb_log_UAV_raw = self.USV_traj_log_raw[0:self.nUSV, :]
        #             self.xb_log_UAV = self.get_interpolated_traj(self.xb_log_UAV_raw, UAV_time_stamps, new_time_stamps)
        #         self.x_log  = self.get_interpolated_traj(self.x_log_raw, UAV_time_stamps, new_time_stamps)
        #         self.xb_log = self.get_interpolated_traj(self.xb_log_raw, USV_time_stamps, new_time_stamps)
        #         self.u_log_raw = np.loadtxt(dir_path + '/uUAV_log.csv', delimiter=',')
        #         self.ub_log_raw = np.loadtxt(dir_path + '/uUSV_log.csv', delimiter=',')
        #         self.u_log  = self.get_interpolated_traj(self.u_log_raw, UAV_time_stamps, new_time_stamps)
        #         self.ub_log = self.get_interpolated_traj(self.ub_log_raw, USV_time_stamps, new_time_stamps)
        #
        #         self.mUAV = self.u_log_raw.shape[0]
        #         self.mUSV = self.ub_log_raw.shape[0]
        #
        #         if problem_type == PARALLEL:
        #             self.UAV_inner_traj_log_raw = np.loadtxt(dir_path + '/UAV_inner_traj_log.csv', delimiter=',')
        #             self.USV_inner_traj_log_raw = np.loadtxt(dir_path + '/USV_inner_traj_log.csv', delimiter=',')
        #
        #             self.UAV_inner_traj_log = self.get_interpolated_traj(self.UAV_inner_traj_log_raw, UAV_time_stamps, new_time_stamps)
        #             self.USV_inner_traj_log = self.get_interpolated_traj(self.USV_inner_traj_log_raw, USV_time_stamps, new_time_stamps)
        #     elif data_type == 'vertical':
        #         self.xv_log_raw = np.loadtxt(dir_path + '/xv_log.csv', delimiter=',')
        #         self.vert_traj_log_raw = np.loadtxt(dir_path + '/vert_traj_log.csv', delimiter=',')
        #         self.s_vert_log_raw = np.loadtxt(dir_path + '/s_vert_log.csv', delimiter=',')
        #
        #         self.xv_log = self.get_interpolated_traj(self.xv_log_raw, UAV_time_stamps, new_time_stamps)
        #         self.vert_traj_log = self.get_interpolated_traj(self.vert_traj_log_raw, UAV_time_stamps, new_time_stamps)
        #         self.s_vert_log = self.get_adjusted_array(self.s_vert_log_raw, UAV_time_stamps, new_time_stamps)
        #
        #         self.nv = self.xv_log_raw.shape[0]
        #
        #         self.hb = self.get_USV_altitude(dir_path)
        #
        #         if problem_type == PARALLEL:
        #             self.vert_inner_traj_log_raw = np.loadtxt(dir_path + '/vert_inner_traj_log.csv', delimiter=',')
        #
        #             self.vert_inner_traj_log = self.get_interpolated_traj(self.vert_inner_traj_log_raw, UAV_time_stamps, new_time_stamps)
        #
        #     elif data_type == 'time':
        #         self.mean_iteration_UAV = np.loadtxt(dir_path + '/TEST/MEAN.csv', delimiter=',')
        #         self.median_iteration = np.loadtxt(dir_path + '/TEST/MEDIAN.csv', delimiter=',')
        #         self.mean_iteration_USV = np.loadtxt(dir_path + '/TEST/MEAN_USV.csv', delimiter=',')
        #         self.median_iteration_USV = np.loadtxt(dir_path + '/TEST/MEDIAN_USV.csv', delimiter=',')
        #         self.hor_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEAN.csv', delimiter=',')
        #         self.hor_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN.csv', delimiter=',')
        #         self.vert_mean = np.loadtxt(dir_path + '/TEST/VERT_MEAN.csv', delimiter=',')
        #         self.vert_median = np.loadtxt(dir_path + '/TEST/VERT_MEDIAN.csv', delimiter=',')
        #         self.landing_times = np.loadtxt(dir_path + '/TEST/LANDING_TIMES.csv', delimiter=',')
        #         if problem_type != CENTRALISED:
        #             self.hor_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_MEAN_USV.csv', delimiter=',')
        #             self.hor_median_USV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN_USV.csv', delimiter=',')
        #         if problem_type == PARALLEL:
        #             self.hor_inner_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN.csv', delimiter=',')
        #             self.hor_inner_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN.csv', delimiter=',')
        #             self.hor_inner_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN_USV.csv', delimiter=',')
        #             self.hor_inner_median_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN_USV.csv', delimiter=',')
        #             self.vert_inner_mean = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEAN.csv', delimiter=',')
        #             self.vert_inner_median = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEDIAN.csv', delimiter=',')
        return

    def get_interpolated_traj(self, traj, old_times, new_times):
        # if new_times[0] < old_times[0] or new_times[0] > old_times[-1]:
        #     raise LookupError('New time stamps are non-overlapping with old time stamps')
        # Assumes interpolation along 0th dimension (x-direction)
        height = traj.shape[0]
        width = new_times.shape[0]
        len_old_traj = old_times.shape[0]   # old_times can have fewer elements
        # than traj because time stamp after end of loop  is never logged,
        # in contrast to e.g. state after end of loop
        new_traj = np.full((height, width), np.nan)
        for row in range(height):
            i_0 = 0
            i_2 = 1
            for i in range(len(new_times)):
                while True:
                    if (old_times[i_2] < new_times[i]) and i_2 < len_old_traj-1:
                        # haven't passed interpolation point yet, move forward
                        i_0 = i_2
                        i_2 = i_2 + 1
                    else:
                        if old_times[i_0] > new_times[i]:
                            # The old traj had no data points around the time new_times[i]
                            # Use oldest value from old traj as the first values of new traj
                            new_traj[row, i] = traj[row, i_0]
                        elif i_2 == len_old_traj:
                            # The old traj had no data points around the time new_times[i]
                            # Use newest value from old traj as the last values of new traj
                            new_traj[row, i] = traj[row, i_2]
                        else:
                            # We have just passed interpolation point
                            x_0 = old_times[i_0]
                            x_2 = old_times[i_2]
                            y_0 = traj[row, i_0]
                            y_2 = traj[row, i_2]
                            x_1 = new_times[i]
                            new_traj[row, i] = y_0 + (x_1 - x_0)*(y_2 - y_0)/(x_2 - x_0)
                        break
        return new_traj

    # Sort of discrete interpolation. Doesn't actually interpolate values
    # just sets missing values equal to the last known value
    def get_adjusted_array(self, traj, old_times, new_times):
        # if new_times[0] < old_times[0] or new_times[0] > old_times[-1]:
        #     raise LookupError('New time stamps are non-overlapping with old time stamps')
        # Assumes interpolation along 0th dimension (x-direction)
        height = new_times.shape[0]
        new_traj = np.full((height, ), np.nan)
        len_old_traj = old_times.shape[0]   # old_times can have fewer elements
        # than traj because time stamp after end of loop  is never logged,
        # in contrast to e.g. state after end of loop
        i_0 = 0
        i_2 = 1
        for i in range(len(new_times)):
            # if  np.isnan(traj[row, i]):
            #     print "WAS NAN"
            while True:

                if (old_times[i_2] < new_times[i]) and i_2 < len_old_traj-1:
                    # haven't passed interpolation point yet, move forward
                    i_0 = i_2
                    i_2 = i_2 + 1
                else:
                    if old_times[i_0] > new_times[i]:
                        # The old traj had no data points around the time new_times[i]
                        # Use oldest value from old traj as the first values of new traj
                        new_traj[i] = traj[i_0]
                    elif i_2 == len_old_traj:
                        # The old traj had no data points around the time new_times[i]
                        # Use newest value from old traj as the last values of new traj
                        new_traj[i] = traj[i_2]
                    else:
                        # We have just passed interpolation point
                        new_traj[i] = traj[i_0]
                    break
        return new_traj

    def get_USV_altitude(self, dir_path):

        file = open(dir_path + '/info.txt')
        lines = file.readlines()
        if lines[7].find('altitude:') > 0:
            substrings = lines[7].split(':')
            return float(substrings[1])
        else:
            print "Couldn't find USV altitude"
            return 0

    def proj_6_to_4(self, mat):
        new_mat = np.full((4*mat.shape[0]//6, mat.shape[1]), np.nan)
        for i in range(mat.shape[0]//6):
            new_mat[4*i:4*(i+1), :] = mat[6*i:6*i+4]
        return new_mat

    def debug_convert_txt_to_csv(self, dir_path, problem_type):
        # READING
        self.mean_iteration_UAV = np.loadtxt(dir_path + '/TEST/MEAN.txt')
        self.median_iteration = np.loadtxt(dir_path + '/TEST/MEDIAN.txt')
        self.mean_iteration_USV = np.loadtxt(dir_path + '/TEST/MEAN_USV.txt')
        self.median_iteration_USV = np.loadtxt(dir_path + '/TEST/MEDIAN_USV.txt')
        self.hor_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEAN.txt')
        self.hor_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN.txt')
        self.vert_mean = np.loadtxt(dir_path + '/TEST/VERT_MEAN.txt')
        self.vert_median = np.loadtxt(dir_path + '/TEST/VERT_MEDIAN.txt')
        self.landing_times = np.loadtxt(dir_path + '/TEST/LANDING_TIMES.txt')
        if problem_type != CENTRALISED:
            self.hor_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_MEAN_USV.txt')
            self.hor_median_USV = np.loadtxt(dir_path + '/TEST/HOR_MEDIAN_USV.txt')
        if problem_type == PARALLEL:
            self.hor_inner_mean_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN.txt')
            self.hor_inner_median_UAV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN.txt')
            self.hor_inner_mean_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEAN_USV.txt')
            self.hor_inner_median_USV = np.loadtxt(dir_path + '/TEST/HOR_INNER_MEDIAN_USV.txt')
            self.vert_inner_mean = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEAN.txt')
            self.vert_inner_median = np.loadtxt(dir_path + '/TEST/VERT_INNER_MEDIAN.txt')

        self.UAV_time_stamps = np.loadtxt(dir_path +'/UAV_time_stamps.txt')
        self.USV_time_stamps = np.loadtxt(dir_path + '/USV_time_stamps.txt')

        if not os.path.isdir(dir_path+'/TEST_CSV'):
            os.mkdir(dir_path+'/TEST_CSV')

        # WRITING
        np.savetxt(dir_path + '/TEST_CSV/MEAN.csv', self.mean_iteration_UAV, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/MEDIAN.csv', self.median_iteration, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/MEAN_USV.csv', self.mean_iteration_USV, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/MEDIAN_USV.csv', self.median_iteration_USV, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/HOR_MEAN.csv', self.hor_mean_UAV, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/HOR_MEDIAN.csv', self.hor_median_UAV, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/VERT_MEAN.csv', self.vert_mean, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/VERT_MEDIAN.csv', self.vert_median, delimiter=',')
        np.savetxt(dir_path + '/TEST_CSV/LANDING_TIMES.csv', self.landing_times, delimiter=',')
        if problem_type != CENTRALISED:
            np.savetxt(dir_path + '/TEST_CSV/HOR_MEAN_USV.csv', self.hor_mean_USV, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/HOR_MEDIAN_USV.csv', self.hor_median_USV, delimiter=',')
        if problem_type == PARALLEL:
            np.savetxt(dir_path + '/TEST_CSV/HOR_INNER_MEAN.csv', self.hor_inner_mean_UAV, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/HOR_INNER_MEDIAN.csv', self.hor_inner_median_UAV, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/HOR_INNER_MEAN_USV.csv', self.hor_inner_mean_USV, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/HOR_INNER_MEDIAN_USV.csv', self.hor_inner_median_USV, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/VERT_INNER_MEAN.csv', self.vert_inner_mean, delimiter=',')
            np.savetxt(dir_path + '/TEST_CSV/VERT_INNER_MEDIAN.csv', self.vert_inner_median, delimiter=',')

        np.savetxt(dir_path + '/UAV_time_stamps.csv', self.UAV_time_stamps, delimiter=',')
        np.savetxt(dir_path + '/USV_time_stamps.csv', self.USV_time_stamps, delimiter=',')

    def get_safety_region(self, dir_path):
        file = open(dir_path + '/info.txt')
        lines = file.readlines()
        if lines[9].find('dl:') == -1:
            add = 1
        else:
            add = 0

        if lines[9+add].find('dl:') > -1:
            substrings = lines[9+add].split(':')
            dl = float(substrings[1])
        else:
            print "Couldn't find dl"

        if lines[10+add].find('ds:') > -1:
            substrings = lines[10+add].split(':')
            dl = float(substrings[1])
        else:
            print "Couldn't find ds"

        if lines[11+add].find('hs:') > -1:
            substrings = lines[11+add].split(':')
            dl = float(substrings[1])
        else:
            print "Couldn't find hs"

        return (dl, ds, hs)

    def get_dropout_bounds(self, dir_path):
        file = open(dir_path + '/info.txt')
        lines = file.readlines()
        if lines[9].find('Dropout bounds:') == 0:
            substrings1 = lines[9].split(':')
            substrings2 = substrings1[1].split('to')
            return (True, int(substrings2[0]), int(substrings2[1]))
        else:
            return (False, -1, -1)

if __name__ == '__main__':
    data_analyser = DataAnalyser(sys.argv[1:])
    # data_analyser.plot_3d(real_time = True, perspective=ACTUAL)
    # data_analyser.plot_3d_super_realtime()
    # data_analyser.plot_topview(real_time = True, perspective = ACTUAL)
    # data_analyser.compare_topviews(real_time = True)
    # data_analyser.plot_time_evolution(real_time = True)
    data_analyser.plot_with_constraints(real_time = True, perspective = ACTUAL)    # data_analyser.plot_altitude(real_time = False, perspective = ACTUAL)
    # data_analyser.plot_with_vel_constraints(real_time = True)
    # data_analyser.plot_obj_val(real_time = True)
    # data_analyser.plot_hor_velocities(real_time = True)
    # data_analyser.plot_time_histogram()
    # data_analyser.plot_time_curve()
    # data_analyser.store_formatted_descent(perspective = ACTUAL) # WARNING: ONLY ACTUAL PERSPECTIVE IS CORRECTLY IMPLEMENTED, TIME STAMPS ARE NOT CORRECT FOR OTHER PERSPECTIVES
    # data_analyser.store_formatted_durations()

    # use_dir = False
    # use_horizon_vs_performance = False
    # if len(sys.argv) == 2:
    #     # directory specified
    #     dir = sys.argv[1]
    #     use_dir = True
    # elif len(sys.argv) > 2:
    #     # start and end index specified
    #     # start = int(sys.argv[1])
    #     # end = int(sys.argv[2])
    #     if not use_horizon_vs_performance:
    #         combine_multiple_results(sys.argv[1:3])
    #         exit()
    #     else:
    #         dirs = sys.argv[1:4]
    # else:
    #     print "ERROR: Please select directory"
    #     exit()
    #
    # if use_horizon_vs_performance:
    #     if len(sys.argv) > 2:
    #         horizon_vs_performance(dirs)
    #     else:
    #         horizon_vs_performance([dir])
    # elif use_dir:
    #     print_data(dir)
    # else:
    #     for i in range(int(start), int(end)+1):
    #         print_data('Experiment_' + str(i))

# def combine_multiple_results(dirs):
#     time_list = []
#     dist_list = []
#     test_means_list = []
#     test_hor_means_list = []
#     test_vert_means_list = []
#     z_traj_inter_list = []
#     dist_hor_list = []
#     for dir in dirs:
#         test_means = np.loadtxt(dir_path + dir + '/MEAN.txt')
#         test_medians = np.loadtxt(dir_path + dir + '/MEDIAN.txt')
#         test_means_hor = np.loadtxt(dir_path + dir + '/HOR_MEAN.txt')
#         test_medians_hor = np.loadtxt(dir_path + dir + '/HOR_MEDIAN.txt')
#         test_means_vert = np.loadtxt(dir_path + dir + '/VERT_MEAN.txt')
#         test_medians_vert = np.loadtxt(dir_path + dir + '/VERT_MEDIAN.txt')
#         UAV_time_stamps = np.loadtxt(dir_path + dir + '/UAV_time_stamps.txt')
#         USV_time_stamps = np.loadtxt(dir_path + dir + '/USV_time_stamps.txt')
#         t_0 = np.maximum(UAV_time_stamps[0], USV_time_stamps[0])
#
#         #DEBUG, UAV_time_stamps just happened to have last element equal to nan
#         UAV_time_stamps[-1] = UAV_time_stamps[-2] + 0.05
#
#         UAV_time_stamps = UAV_time_stamps - t_0
#         USV_time_stamps = USV_time_stamps - t_0
#
#         x_log  = np.loadtxt(dir_path + dir + '/x_log.txt')
#         xb_log = np.loadtxt(dir_path + dir + '/xb_log.txt')
#         xv_log = np.loadtxt(dir_path + dir + '/xv_log.txt')
#         x_traj = x_log[0,:]
#         y_traj = x_log[1,:]
#         z_traj = xv_log[0,:]
#         xb_traj = xb_log[0,:]
#         yb_traj = xb_log[1,:]
#         # distance_hor = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) )
#         # distance = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) + np.square(z_traj))
#
#         new_UAV_times = np.arange(0, UAV_time_stamps[-1], 0.05)
#         new_USV_times = np.arange(0, USV_time_stamps[-1], 0.05)
#         if len(new_UAV_times) > len(new_USV_times):
#             common_times = new_USV_times
#         else:
#             common_times = new_UAV_times
#
#         x_traj_inter = get_interpolated_traj(x_traj, UAV_time_stamps, common_times)
#         y_traj_inter = get_interpolated_traj(y_traj, UAV_time_stamps, common_times)
#         z_traj_inter = get_interpolated_traj(z_traj, UAV_time_stamps, common_times)
#         xb_traj_inter = get_interpolated_traj(xb_traj, USV_time_stamps, common_times)
#         yb_traj_inter = get_interpolated_traj(yb_traj, USV_time_stamps, common_times)
#
#         distance_hor = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
#             + np.square(y_traj_inter - yb_traj_inter) )
#         distance = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
#             + np.square(y_traj_inter - yb_traj_inter) + np.square(z_traj_inter) )
#
#         time_list.append(common_times)
#         dist_list.append(distance)
#         test_means_list.append(test_means)
#         test_hor_means_list.append(test_means_hor)
#         test_vert_means_list.append(test_means_vert)
#         z_traj_inter_list.append(z_traj_inter)
#         dist_hor_list.append(distance_hor)
#
#         # Calculate landing time
#         land_time = 0
#         for i in range(len(z_traj)):
#             if z_traj[i] > 0.1:
#                 land_time = UAV_time_stamps[i]
#             else:
#                 break
#
#         print "Landed at time:", land_time
#
#     colors = [(1.0, 0.0, 0.0, 0.5), (0.0, 0.0, 1.0, 0.5)]
#     legends = ['Centralised', 'Distributed']
#     xlabel = 'Mean Vertical Problem Solution Time [s]'
#     # xlabel = 'Mean Iteration Durations [s]'
#     ylabel = 'Number of Trials'
#     # plot_all_histograms(test_vert_means_list, [red, light_blue], legends, xlabel, ylabel)
#     # plot_all_dists(time_list, dist_list, ['Centralised', 'Distributed', 'Cascading'])
#     plot_all_with_constraints(dist_hor_list, z_traj_inter_list,\
#         ['Centralised', 'Distributed'], 'horizontal distance [m]', 'height [m]')    #['Centralised', 'Distributed', 'Cascading']
#     # save_all_with_constraints(dist_hor_list, z_traj_inter_list,\
#     #     ['Centralised', 'Distributed'], 'horizontal distance [m]', 'height [m]')
#
# def print_data(dir):
#     UAV_iteration_durations = \
#         np.loadtxt(dir_path + dir + '/UAV_iteration_durations.txt')
#
#     # Figure out problem type based on which files exist
#     is_centralised = False
#     is_distributed = False
#     is_parallel = False
#     try:
#         np.loadtxt(dir_path + dir +'/UAV_horizontal_durations.txt')
#     except:
#         print "Failed getting UAV solution durations, assuming that problem type is PARALLEL"
#         is_parallel = True
#     try:
#         np.loadtxt(dir_path + dir +'/USV_iteration_durations.txt')
#     except:
#         print "Failed loading USV iteration durations, assuming that problem type is CENTRALISED"
#         is_centralised = True
#     is_distributed = not is_centralised and not is_parallel
#
#
#     test_means = np.loadtxt(dir_path + dir + '/MEAN.txt')
#     test_medians = np.loadtxt(dir_path + dir + '/MEDIAN.txt')
#     test_means_hor = np.loadtxt(dir_path + dir + '/HOR_MEAN.txt')
#     test_medians_hor = np.loadtxt(dir_path + dir + '/HOR_MEDIAN.txt')
#     test_means_vert = np.loadtxt(dir_path + dir + '/VERT_MEAN.txt')
#     test_medians_vert = np.loadtxt(dir_path + dir + '/VERT_MEDIAN.txt')
#     UAV_time_stamps = np.loadtxt(dir_path + dir + '/UAV_time_stamps.txt')
#     USV_time_stamps = np.loadtxt(dir_path + dir + '/USV_time_stamps.txt')
#     # mean_UAV_iteration_duration = np.mean(np.loadtxt(dir_path + dir + 'UAV_iteration_durations.txt'))
#     # mean_hor_solution_duration = np.mean(np.loadtxt(dir_path + dir + 'UAV_horizontal_durations.txt'))
#     # mean_vert_solution_duration = np.mean(np.loadtxt(dir_path + dir + 'vert_solution_durations.txt'))
#     # mean_USV_iteration_duration = np.mean(np.loadtxt(dir_path + dir + 'USV_iteration_durations.txt'))
#     # mean_USV_solution_duration = np.mean(np.loadtxt(dir_path + dir + 'USV_iteration_durations.txt'))
#     # if is_parallel:
#     #     mean_inner_hor_solution_duration
#     #     mean_inner_vert_solution_duration
#     #     mean_inner_USV_solution_duration
#     try:
#         landing_times = np.loadtxt(dir_path + dir + '/LANDING_TIMES.txt')
#         print "min:", landing_times.min(), ', max:', landing_times.max(), ', mean:', np.mean(landing_times)
#     except:
#         print 'Found no stored landing times'
#     t_0 = np.maximum(UAV_time_stamps[0], USV_time_stamps[0])
#
#     # EDIT: CAN PROBABLY BE DELETED, SHOULDN'T OCCUR ANYMORE
#     # #DEBUG, UAV_time_stamps just happened to have last element equal to nan
#     # UAV_time_stamps[-1] = UAV_time_stamps[-2] + 0.05
#
#     UAV_time_stamps = UAV_time_stamps - t_0
#     USV_time_stamps = USV_time_stamps - t_0
#
#     x_log  = np.loadtxt(dir_path + dir + '/x_log.txt')
#     xb_log = np.loadtxt(dir_path + dir + '/xb_log.txt')
#     xv_log = np.loadtxt(dir_path + dir + '/xv_log.txt')
#     UAV_traj_log = np.loadtxt(dir_path + dir + '/UAV_traj_log.txt')
#     USV_traj_log = np.loadtxt(dir_path + dir + '/USV_traj_log.txt')
#     vert_traj_log = np.loadtxt(dir_path + dir + '/vert_traj_log.txt')
#     # TODO: Rename these? Slightly confusing names
#     x_traj = x_log[0,:]
#     y_traj = x_log[1,:]
#     z_traj = xv_log[0,:]
#     w_traj = xv_log[1, :]
#     xb_traj = xb_log[0,:]
#     yb_traj = xb_log[1,:]
#     # distance_hor = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) )
#     # distance = np.sqrt( np.square(x_traj-xb_traj) + np.square(y_traj-yb_traj) + np.square(z_traj))
#
#     new_UAV_times = np.arange(0, UAV_time_stamps[-1], 0.05)
#     new_USV_times = np.arange(0, USV_time_stamps[-1], 0.05)
#     if len(new_UAV_times) > len(new_USV_times):
#         common_times = new_USV_times
#     else:
#         common_times = new_UAV_times
#
#     # print np.count_nonzero( np.isnan(z_traj))
#     # print np.count_nonzero( np.isnan( w_traj))
#     # print '##################################'
#     x_traj_inter = get_interpolated_traj(x_traj, UAV_time_stamps, common_times)
#     y_traj_inter = get_interpolated_traj(y_traj, UAV_time_stamps, common_times)
#     z_traj_inter = get_interpolated_traj(z_traj, UAV_time_stamps, common_times)
#     w_traj_inter = get_interpolated_traj(w_traj, UAV_time_stamps, common_times)
#     xb_traj_inter = get_interpolated_traj(xb_traj, USV_time_stamps, common_times)
#     yb_traj_inter = get_interpolated_traj(yb_traj, USV_time_stamps, common_times)
#     # print np.count_nonzero( np.isnan(z_traj_inter))
#     # print np.count_nonzero( np.isnan( w_traj_inter))
#     # print '!!!!!!'
#
#     distance_hor = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
#         + np.square(y_traj_inter - yb_traj_inter) )
#     distance = np.sqrt( np.square(x_traj_inter - xb_traj_inter) \
#         + np.square(y_traj_inter - yb_traj_inter) + np.square(z_traj_inter) )
#
#     # Calculate landing time
#     land_time = 0
#     for i in range(len(z_traj)):
#         if z_traj[i] > 0.1:
#             land_time = UAV_time_stamps[i]
#         else:
#             break
#
#     print "Landed at time:", land_time
#
#     # print 'Mean UAV iteration: ' + str(np.mean(UAV_iteration_durations))
#     # print 'Median UAV iteration: ' + str(np.median(UAV_iteration_durations))
#     # print 'Mean UAV horizontal: ' + str(np.mean(UAV_horizontal_durations))
#     # print 'Median UAV horizontal: ' + str(np.median(UAV_horizontal_durations))
#     # print 'Mean UAV vertical: ' + str(np.mean(UAV_vertical_durations))
#     # print 'Median UAV vertical: ' + str(np.median(UAV_vertical_durations))
#     # print '----------------------------------------------'
#
#     xv_log_trimmed = np.reshape( np.array([z_traj_inter, w_traj_inter]), (-1, 1), order='F' )
#     constraints_satisfied(common_times, distance_hor, xv_log_trimmed, land_time)
#
#     # plot_3d(x_traj, y_traj, z_traj, xb_traj, yb_traj)
#     # save_3d_animation(x_traj, y_traj, z_traj, xb_traj, yb_traj)
#     # plot_topview(x_traj, y_traj, xb_traj, yb_traj)
#     # plot_with_constraints(distance_hor, z_traj_inter, 'horizontal distance [m]', 'height [m]')
#     plot_3d_realtime(x_traj, y_traj, z_traj, xb_traj, yb_traj,\
#         UAV_traj_log, USV_traj_log, vert_traj_log)
#     # plot_histogram(test_means_hor, 'Mean Horizontal Problem Solution Time [s]', 'Number of Trials')   #Mean Vertical Problem Solution Time [s]
#     # plot_hor_dist(common_times, distance_hor)
#     # plot_dist(common_times, distance)
#     # plot_height(UAV_time_stamps - t_0, z_traj)
#     return
#
# def constraints_satisfied(common_times, distance_hor, xv_log, landing_time):
#     T_trimmed = len(common_times)
#     height_extractor = np.zeros(( T_trimmed, nv*T_trimmed ))
#     for i in range(T_trimmed):
#         height_extractor[ i, nv*i ] = 1
#
#     distance_hor = np.reshape(distance_hor, (-1, 1))
#     b_vec = distance_hor < ds
#
#     # SAFETY CONSTRAINT
#     # dl - ds < 0 --> Automatically satisfied in b == 0
#     safe1 = (dl - ds)*np.dot(height_extractor,xv_log) <= np.diag(b_vec)*(hs*dl - hs*distance_hor)
#     safe2 = (dl - ds)*np.dot(height_extractor,xv_log) <= np.diag(b_vec)*(hs*dl + hs*distance_hor)   # shouldn't be necessary if distance in positive
#     # SAFE HEIGHT CONSTRAINT
#     # UAV height usually > 0 --> Automatically satisfied if b == 1
#     safe3 = np.dot(height_extractor,xv_log) >= hs*(np.ones((T_trimmed, 1)) - b_vec)
#
#     # np.savetxt('/home/robert/DELTE_ME/safe1.txt', safe1)
#     # np.savetxt('/home/robert/DELTE_ME/safe2.txt', safe2)
#     # np.savetxt('/home/robert/DELTE_ME/safe3.txt', safe3)
#     np.set_printoptions(threshold=sys.maxsize)
#     times_constraints_violated = []
#     for safe_vec in [safe1, safe2, safe3]:
#         if np.count_nonzero(~safe_vec) > 0:
#             nonzero_indices = np.nonzero(~safe_vec)[0]
#             for i in nonzero_indices:
#                 if common_times[i] < landing_time:
#                     # Only include constraints that were violated BEFORE landing
#                     times_constraints_violated.append(common_times[i])
#
#     # print np.count_nonzero(~safe1)
#     # print np.count_nonzero(~safe2)
#     # print np.count_nonzero(~safe3)
#     # print np.nonzero(~safe3)[0]
#     print len(times_constraints_violated), 'constraints were violated before landing'
#
#     # # Safety constraints
#     # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
#     #     <= cp.diag(self.b)*(params.hs*params.dl - params.hs*self.dist)]
#     # constraintsVert += [(params.dl-params.ds)*self.height_extractor*self.xv\
#     #     <= cp.diag(self.b)*(params.hs*params.dl + params.hs*self.dist)]
#     # # Safe height constraints
#     # constraintsVert += [self.height_extractor*self.xv \
#     #     >= params.hs*(np.ones(( T+1, 1 )) - self.b)]
#     return
#
# def horizon_vs_performance(dirs):
#     fig = plt.figure()
#     ax = plt.axes()
#     colors = ['blue', 'red']
#     legends = ['Centralised', 'Distributed']
#     j = -1
#     for dir in dirs:
#         j += 1
#         # Find range of horizons
#         min_hor = -1
#         max_hor = -1
#         i = 0
#         while min_hor == -1 or max_hor == -1:
#             file_exists = os.path.isfile(dir_path + dir + '/landing_times_' + str(i) + '.txt')
#             if file_exists and min_hor == -1:
#                 min_hor = i
#             elif min_hor != -1 and not file_exists:
#                 max_hor = i-1
#             i = i + 1
#
#         all_landing_times = []
#         all_mean_horizontal = []
#         all_median_horizontal = []
#         all_mean_iteration = []
#         all_median_iteration = []
#         all_mean_vertical = []
#         all_median_vertical = []
#         plotable_landing_times = []
#         plotable_mean_horizontal = []
#         plotable_median_horizontal = []
#         plotable_mean_iteration = []
#         plotable_median_iteration = []
#         plotable_mean_vertical = []
#         plotable_median_vertical = []
#
#         print "min:", min_hor, 'max:', max_hor
#         for hor in range(min_hor, max_hor+1):
#             landing_times = np.loadtxt(dir_path + dir + '/landing_times_' + str(hor) + '.txt')
#             mean_horizontal = np.loadtxt(dir_path + dir + '/mean_horizontal_' + str(hor) + '.txt')
#             median_horizontal = np.loadtxt(dir_path + dir + '/median_horizontal_' + str(hor) + '.txt')
#             mean_iteration = np.loadtxt(dir_path + dir + '/mean_iteration_' + str(hor) + '.txt')
#             median_iteration = np.loadtxt(dir_path + dir + '/median_iteration_' + str(hor) + '.txt')
#             mean_vertical = np.loadtxt(dir_path + dir + '/mean_vertical_' + str(hor) + '.txt')
#             median_vertical = np.loadtxt(dir_path + dir + '/median_vertical_' + str(hor) + '.txt')
#
#             # all_landing_times.append(landing_times)
#             # all_mean_horizontal.append(mean_horizontal)
#             # all_median_horizontal.append(median_horizontal)
#             # all_mean_iteration.append(mean_iteration)
#             # all_median_iteration.append(median_iteration)
#             # all_mean_vertical.append(mean_vertical)
#             # all_median_vertical.append(median_vertical)
#             plotable_landing_times.append(np.mean(landing_times))
#             plotable_mean_horizontal.append(np.mean(mean_horizontal))
#             plotable_median_horizontal.append(np.mean(median_horizontal))
#             plotable_mean_iteration.append(np.mean(mean_iteration))
#             plotable_median_iteration.append(np.mean(median_iteration))
#             plotable_mean_vertical.append(np.mean(mean_vertical))
#             plotable_median_vertical.append(np.mean(median_vertical))
#
#         ax.plot(range(min_hor, max_hor+1), plotable_mean_iteration, colors[j])
#         # ax.plot(range(min_hor, max_hor+1), plotable_mean_horizontal)
#         # ax.plot(range(min_hor, max_hor+1), plotable_mean_vertical)
#         # plt.legend(['Iteration Time [s]', 'Horizontal Problem Solution Time [s]', 'Vertical Problem Solution Time [s]'])
#         plt.grid(True)
#         plt.xlabel('Prediction Horizon')
#         plt.ylabel('Iteration Duration [s]')
#     plt.legend(legends)
#     plt.show()
#
# def plot_with_constraints(x_vector, height, xlabel, ylabel):
#     forbidden_area_1 = Polygon([ (dl, 0),\
#                                  (ds, hs),\
#                                  (35, hs),\
#                                  (35, 0)], True)
#     forbidden_area_2 = Polygon([ (-dl, 0),\
#                                  (-ds, hs),\
#                                  (-35, hs),\
#                                  (-35, 0)], True)
#     safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4)
#
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(x_vector, height, 'b')
#     ax.add_collection(safety_patch_collection)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.grid(True)
#     plt.show()
#
# def plot_height(time, z_traj):
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(time, z_traj, 'b')
#     plt.grid(True)
#     plt.show()
#
# def plot_hor_dist(time, distance):
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(time, distance, 'b')
#     plt.grid(True)
#     plt.show()
#
# def plot_dist(time, distance):
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(time, distance, 'b')
#     plt.xlabel('time [s]')
#     plt.ylabel('distance [m]')
#     plt.grid(True)
#     plt.show()
#
# def plot_all_dists(time_list, distance_list, legend_list):
#     fig = plt.figure()
#     ax = plt.axes()
#     colors = [blue_like, orange_like, green_like]
#     styles = ['-', '--', '-.']
#     for i in range(len(time_list)):
#         ax.plot(time_list[i], distance_list[i],styles[i])
#     plt.xlabel('time [s]')
#     plt.ylabel('distance [m]')
#     plt.grid(True)
#     plt.legend(legend_list)
#     ax.set_xlim(left=0, right=100)
#     plt.show()
#
# def plot_all_with_constraints(x_vector_list, y_vector_list, legend_list, xlabel, ylabel):
#     forbidden_area_1 = Polygon([ (dl, 0),\
#                                  (ds, hs),\
#                                  (35, hs),\
#                                  (35, 0)], True)
#     forbidden_area_2 = Polygon([ (-dl, 0),\
#                                  (-ds, hs),\
#                                  (-35, hs),\
#                                  (-35, 0)], True)
#     safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4, edgecolors='red', facecolors='red')
#
#     fig = plt.figure()
#     ax = plt.axes()
#     colors = [blue_like, orange_like, green_like]
#     # styles = ['-', '--', '-.']
#     styles = ['red', 'blue', 'yellow']
#     for i in range(len(y_vector_list)):
#         ax.plot(x_vector_list[i], y_vector_list[i], styles[i])
#     ax.add_collection(safety_patch_collection)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.grid(True)
#     plt.legend(legend_list)
#     plt.show()
#
# def save_all_with_constraints(x_vector_list, y_vector_list, legend_list, xlabel, ylabel):
#     fig = plt.figure()
#     ax = plt.axes()
#     forbidden_area_1 = Polygon([ (dl, 0),\
#                                  (ds, hs),\
#                                  (35, hs),\
#                                  (35, 0)], True)
#     forbidden_area_2 = Polygon([ (-dl, 0),\
#                                  (-ds, hs),\
#                                  (-35, hs),\
#                                  (-35, 0)], True)
#     safety_patch_collection = PatchCollection([forbidden_area_1, forbidden_area_2], alpha=0.4, edgecolors='red', facecolors='red')
#
#     xcdata, ycdata, xddata, yddata = [], [], [], []
#     line1, = plt.plot([], [], 'r')
#     line2, = plt.plot([], [], 'b')
#     # line3 = plt.plot([], [])
#     lines = [line1, line2]
#     def init():
#         plt.xlabel(xlabel)
#         plt.ylabel(ylabel)
#         plt.grid(True)
#         plt.legend(legend_list)
#         ax.add_collection(safety_patch_collection)
#         ax.set_xlim(left=0, right=35)
#         ax.set_ylim(bottom=0, top=12)
#         return lines
#
#     def update(i):
#         xcdata.append(x_vector_list[0][i])
#         ycdata.append(y_vector_list[0][i])
#         xddata.append(x_vector_list[1][i])
#         yddata.append(y_vector_list[1][i])
#         lines[0].set_data(xcdata, ycdata)
#         lines[1].set_data(xddata, yddata)
#         return lines
#
#     animation = FuncAnimation(fig, update, frames = len(x_vector_list[0]),\
#         init_func = init, blit=True)
#
#     Writer = matplotlib.animation.writers['ffmpeg']
#     writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     animation.save('my_constraint_anim.mp4', writer=writer)
#     print "Should have saved constraint mp4"
#
# def save_3d_animation(x_traj, y_traj, z_traj, xb_traj, yb_traj):
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     xdata, ydata, zdata = [x_traj[0]], [y_traj[0]], [z_traj[2]]
#     xbdata, ybdata, zbdata = [xb_traj[0]], [yb_traj[0]], [0]
#     line1, = ax.plot3D(xdata, ydata, zdata, 'blue')
#     line2, = ax.plot3D(xbdata, ybdata, zbdata, 'red')
#     lines = [line1, line2]
#     def init():
#         ax.set_xlim(left=0, right=30)
#         ax.set_ylim(bottom=0, top=16)
#         ax.set_zlim(0)
#         plt.xlabel('x-position [m]')
#         plt.ylabel('y-position [m]')
#         ax.set_zlabel('Height [m]')
#         plt.legend(['Drone trajectory', 'Boat trajectory'])
#         return lines
#
#     def update(i):
#
#         xdata.append(x_traj[i])
#         ydata.append(y_traj[i])
#         zdata.append(z_traj[max(i,2)])
#         xbdata.append(xb_traj[i])
#         ybdata.append(yb_traj[i])
#         zbdata.append(0)
#         lines[0].set_data(xdata, ydata)
#         lines[0].set_3d_properties(zdata)
#         lines[1].set_data(xbdata, ybdata)
#         lines[1].set_3d_properties(zbdata)
#         return lines
#
#     animation = FuncAnimation(fig, update, frames = len(x_traj),\
#         init_func = init, blit=True)
#
#     Writer = matplotlib.animation.writers['ffmpeg']
#     writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
#     animation.save('my_anim.mp4', writer=writer)
#     print "Should have saved mp4"
#
# def plot_3d(x_traj, y_traj, z_traj, xb_traj, yb_traj):
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#     plt.grid(False)
#     ax.plot3D(x_traj[3:], y_traj[3:], z_traj[3:], 'blue')
#     ax.plot3D(xb_traj, yb_traj, 0, '#FF5555')
#     ax.set_zlim(0)
#     ax.set_yticklabels([])
#     ax.set_xticklabels([])
#     ax.set_zticklabels([])
#     # plt.axis('off')
#     # plt.xlabel('x-position [m]')
#     # plt.ylabel('y-position [m]')
#     # ax.set_zlabel('Height [m]')
#     # plt.legend(['UAV trajectory', 'USV trajectory'])
#     # # plt.legend(['Drone trajectory', 'Boat trajectory'])
#     plt.show()
#
# def plot_3d_realtime(x_traj, y_traj, z_traj, xb_traj, yb_traj,\
#     UAV_traj_log, USV_traj_log, vert_traj_log):
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
#
#     time = range(len(x_traj))
#     for t in time:
#         x_pred_traj = UAV_traj_log[0::nUAV, t:t+1]
#         y_pred_traj = UAV_traj_log[1::nUAV, t:t+1]
#         z_pred_traj = vert_traj_log[0::nv,  t:t+1]
#         xb_pred_traj = UAV_traj_log[0::nUSV, t:t+1]
#         yb_pred_traj = UAV_traj_log[1::nUSV, t:t+1]
#         # Actual trajectories
#         ax.plot3D(x_traj[0:t+1], y_traj[0:t+1], z_traj[0:t+1], 'blue')
#         ax.plot3D(xb_traj[0:t+1], yb_traj[0:t+1], 0, 'red')
#         # Predicted trajectories
#         ax.plot3D(x_pred_traj[0:t+1], y_pred_traj[0:t+1], z_pred_traj[0:t+1], 'green')
#         ax.plot3D(xb_pred_traj[0:t+1], yb_pred_traj[0:t+1], 0, 'green')
#         ax.set_zlim(0)
#         plt.xlabel('x-position [m]')
#         plt.ylabel('y-position [m]')
#         ax.set_zlabel('Height [m]')
#         plt.legend(['UAV trajectory', 'USV trajectory'])
#         plt.pause(0.05)
#         ax.cla()
#
# def plot_topview(x_traj, y_traj, xb_traj, yb_traj):
#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(x_traj, y_traj, 'blue')
#     ax.plot(xb_traj, yb_traj, 'red')
#     plt.xlabel('x-position [m]')
#     plt.ylabel('y-position [m]')
#     plt.legend(['UAV trajectory', 'USV trajectory'])
#     plt.show()
#
# def plot_histogram(vector, xlabel, ylabel, bins=10):
#     plt.hist(vector, bins=bins)
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.grid(True)
#     plt.show()
#
# def plot_all_histograms(vectors, colors, legend_list, xlabel, ylabel, bins=10):
#     for (vector, color) in zip(vectors, colors):
#         plt.hist(vector, bins=bins, color=color)
#     # plt.hist(vector1, bins=bins, color=(1.0, 0.0, 0.0, 0.5))
#     # plt.hist(vector2, bins=bins, color=(0.0, 0.0, 1.0, 0.5))
#     plt.xlabel(xlabel)
#     plt.ylabel(ylabel)
#     plt.grid(True)
#     plt.legend(legend_list)
#     plt.show()
#
# def get_interpolated_traj(traj, old_times, new_times):
#     new_traj = np.empty(new_times.shape)
#     new_traj.fill(np.nan)
#     i_0 = 0
#     i_2 = 1
#     for i in range(len(new_times)):
#         while True:
#             if (old_times[i_2] < new_times[i]):
#                 # haven't passed interpolation point yet, move forward
#                 i_0 = i_2
#                 i_2 = i_2 + 1
#             else:
#                 # We have passed interpolation point
#                 x_0 = old_times[i_0]
#                 x_2 = old_times[i_2]
#                 y_0 = traj[i_0]
#                 y_2 = traj[i_2]
#                 x_1 = new_times[i]
#                 new_traj[i] = y_0 + (x_1 - x_0)*(y_2 - y_0)/(x_2 - x_0)
#                 break
#     return new_traj
#
# def remove_negative_elements(vector):
#     i = 0
#     while vector[i] < 0 and i < len(vector):
#         i += 1
#
#     return vector[i:]
