#%%

import matplotlib.pyplot as plt
import numpy as np
import math
import time

#%%# Set the label to display a negative sign, the coordinate axis can display Chinese
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

#%%
# Measured data; time is time, rain is rainfall intensity, qoc is runoff
ori_time = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00']
ori_rain = [5, 5, 5, 5, 5, 5, 5, 5, 5, 3, 2, 1, 0]
ori_qoc = [0.477, 0.563, 0.744, 1.18, 1.966, 3.315, 4.269, 5.271, 5.859, 4.943, 4.365, 3.97, 3.758]

#%% tank fcn 1
def cre_single_tank(in_rain, d_factor, r_factor, thres, h_intial=None):
    """
         :param h_intial: initial water storage capacity of single-hole water tank, default is 10
         :param h_initial: the initial storage of a single tank, the default is 10
         :param in_rain: measured rainfall data
         :param d_factor: coefficient of infiltration of single-side water tank
         :param r_factor: outflow coefficient of single-side water tank
         :param thres: hole height of single side hole water tank
         :return: out_down is the time change of infiltration volume; out_right is the time change of outflow volume
    """
    if h_intial is None:
        h_intial = 0
    out_down = []
    out_right = []
    z_end = []
    # Calculate the initial z_end
    temp = in_rain[0] + h_intial
    out_down.append(temp * d_factor)
    if temp <= thres:
        out_right.append(0)
    else:
        out_right.append((temp - thres) * r_factor)
    z_end.append(temp - out_down[0] - out_right[0])
    # Calculate z_end at other moments
    for i in range(1, len(in_rain)):
        z_start = in_rain[i] + z_end[i-1]
        down = z_start * d_factor
        if z_start <= thres:
            right = 0
        else:
            right = (z_start - thres) * r_factor
        z_end.append(z_start - down - right)
        out_down.append(down)
        out_right.append(right)
    out_down = np.array([round(i, 3) for i in out_down])
    out_right = np.array([round(i, 3) for i in out_right])
    return out_down, out_right

#%% tank fcn 2
def cre_double_tank(in_rain,  d_factor, r1_factor, r2_factor, thres_1, thres_2, h_intial=None):
    """
         :param h_initial: the initial storage capacity of the two-hole water tank, the default is 10
         :param in_rain: measured rainfall data
         :param d_factor: infiltration coefficient of the double-sided water tank
         :param r1_factor: Outflow coefficient of the lower hole of the double-sided water tank
         :param r2_factor: Outflow coefficient of the upper hole of the double-sided water tank
         :param thres_1: hole height of the lower hole of the double side water tank
         :param thres_2: the hole height of the hole on the double side water tank
         :return: out_down is the time change of infiltration volume; out_right is the time change of outflow volume
    """
    out_down = []
    out_right = []
    z_end = []
    if h_intial is None:
        h_intial = 0
    # Calculate the initial z_end
    temp = in_rain[0] + h_intial
    if temp <= thres_1:
        right_1 = 0
    else:
        right_1 = (temp - thres_1) * r1_factor
    if temp <= thres_2:
        right_2 = 0
    else:
        right_2 = (temp - thres_2) * r2_factor
    out_down.append(temp * d_factor)
    out_right.append(right_1 + right_2)
    z_end.append(temp - out_down[0] - out_right[0])
    # Calculate z_end at other moments
    for i in range(1, len(in_rain)):
        z_start = in_rain[i] + z_end[i - 1]
        down = z_start * d_factor
        if z_start <= thres_1:
            right_1 = 0
        else:
            right_1 = (z_start - thres_1) * r1_factor
        if z_start <= thres_2:
            right_2 = 0
        else:
            right_2 = (z_start - thres_2) * r2_factor
        z_end.append(z_start - down - right_1 - right_2)
        out_down.append(down)
        out_right.append(right_1 + right_2)
    out_down = np.array([round(i, 3) for i in out_down])
    out_right = np.array([round(i, 3) for i in out_right])
    return out_down, out_right


def cal_correlation(real_data, sim_data):
    x_bar = np.mean(real_data)
    y_bar = np.mean(sim_data)
    ssr = 0
    var_x = 0
    var_y = 0
    for i in range(len(real_data)):
        diff_xx_bar = real_data[i] - x_bar
        diff_yy_bar = sim_data[i] - y_bar
        ssr += (diff_xx_bar * diff_yy_bar)
        var_x += diff_xx_bar ** 2
        var_y += diff_yy_bar ** 2
    sst = math.sqrt(var_x * var_y)
    return round(ssr/sst, 4)


def cal_dy(real_data, sim_data):
    num_data = len(real_data)
    aver_real = sum(real_data) / num_data
    t_1 = 0
    t_2 = 0
    for i in range(num_data):
        t_1 += (real_data[i] - sim_data[i]) ** 2
        t_2 += (real_data[i] - aver_real) ** 2
    r = 1 - (t_1 / t_2)
    return round(r, 2)


def do_simulation(switchs=None):
    # F_n: time series of the infiltration volume of the n-th tank
    # R_n: Time series of the outflow of the n-th tank
    if switchs is None:
        switchs = [1, 0]

    # Build a water tank model
    F_1, R_1 = cre_double_tank(ori_rain, d_factors[0], r_factors[0], r_factors[1], hole_heights[0], hole_heights[1], h_start[0])
    F_2, R_2 = cre_single_tank(F_1, d_factors[1], r_factors[2], hole_heights[2], h_start[1])
    F_3, R_3 = cre_single_tank(F_2, d_factors[2], r_factors[3], hole_heights[3], h_start[2])
    F_4, R_4 = cre_single_tank(F_3, d_factors[3], r_factors[4], hole_heights[4], h_start[3])

    # cal_qoc: simulation results to get qoc time series
    cal_qoc = R_1 + R_2 + R_3 + R_4
    cal_qoc = [round(qoc, 3) for qoc in cal_qoc]

    # Use R-square and certainty coefficient dy to measure the quality of the simulation
    r_square.append(cal_correlation(ori_qoc, cal_qoc))
    dy.append(cal_dy(ori_qoc, cal_qoc))

    # To draw
    figure_show_switch = switchs[0]
    types = ['kx-', 'ks-']
    each_layer_switch = 1
    if figure_show_switch:
        plt.plot(ori_qoc, types[0], linewidth=1, label='Measured', markeredgecolor='blue')
        plt.plot(cal_qoc, types[1], linewidth=1, label='simulation')
        if each_layer_switch:
            plt.plot(R_1, 'r', linewidth=1, label='L1')
            plt.plot(R_2, 'g', linewidth=1, label='L2')
            plt.plot(R_3, 'b', linewidth=1, label='L3')
            plt.plot(R_4, 'y', linewidth=1, label='L4')
        plt.legend()
        plt.show()

    # Generate simulation logs
    save_log_switch = switchs[1]
    time_run = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    log_name = 'log.txt'
    if save_log_switch:
        with open(log_name, 'a+') as f_obj:
            f_obj.writelines('{0}\n'.format("=" * 30))
            # current time
            f_obj.writelines(time_run + '\n')
            f_obj.writelines("\nInput parameters:\n")
            f_obj.writelines("d_factors = {0}\n".format(d_factors))
            f_obj.writelines("r_factors = {0}\n".format(r_factors))
            f_obj.writelines("hole_heights = {0}\n".format(hole_heights))
            f_obj.writelines("\nSimulated result:\n")
            f_obj.writelines("cal_qoc = {0}\n".format(list(cal_qoc)))
            f_obj.writelines("R_square:{0}\n".format(r_square[-1]))
            f_obj.writelines("dy:{0}\n".format(dy[-1]))
            f_obj.writelines("=" * 30)

    # Output the fitting result
    print("r_square: {0}".format(r_square[-1]))
    print("dy: {0}".format(dy[-1]))
    return max(dy)


"""
 All parameters related to the four-layer water tank model are as follows
                                 Pore ​​height Infiltration coefficient Outflow coefficient Initial water storage
 The first layer hole_h[0]/hole_h[1] d_f[0] r_f[0]/r_f[1] h_start[0]
 Second layer hole_h[2] d_f[1] r_f[2] h_start[1]
 The third layer hole_h[3] d_f[2] r_f[3] h_start[2]  
 The fourth layer hole_h[4] d_f[3] r_f[4] h_start[3]
"""
# The default value
d_factors = [0.2, 0.1, 0.05, 0]
r_factors = [0.2, 0.1, 0.05, 0.03, 0.01]
hole_heights = [40, 25, 10, 15, 15]
h_start = [0, 0, 0, 0]
r_square = []
dy = []

# First layer parameters
hole_heights[0] = 45
hole_heights[1] = 15
r_factors[0] = 0.3
r_factors[1] = 0.06
d_factors[0] = 0.2

# Second layer parameters
hole_heights[2] = 10
r_factors[2] = 0.06
d_factors[1] = 0.1

# Layer 3 parameters
hole_heights[3] = 0
r_factors[3] = 0.03
d_factors[2] = 0.03

# Layer 4 parameters
hole_heights[4] = 0
r_factors[4] = 0.005
d_factors[3] = 0

# For simulation, two 1s respectively control drawing and log
do_simulation([1, 1])
# %%
