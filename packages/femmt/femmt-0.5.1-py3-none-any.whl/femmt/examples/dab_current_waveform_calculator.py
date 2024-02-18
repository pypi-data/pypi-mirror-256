
import numpy as np
from matplotlib import pyplot as plt

def phi_rad_from_input_parameters(lambda_fl: float, transfer_ratio: np.array, v1: float, v2: float, power_max: float) -> np.array:
    """
    Calculate phase shift difference from input to output bridge
    :param lambda_fl: lambda in ln-mesh
    :type lambda_fl: np.array
    :param transfer_ratio: n in ln-mesh
    :type transfer_ratio: np.array
    :param v1: input voltage
    :type v1: float
    :param v2: output voltage   git dif
    :type v2: float
    :param power_max: power
    :type power_max: float
    :return: phi (phase shift difference from input to output bridge)
    :rtype: np.array
    """
    phi_rad = 1 - (8 * lambda_fl * power_max) / (transfer_ratio * v1 * v2)
    phi_rad = np.pi / 2 * (1 - np.sqrt(phi_rad))

    return phi_rad


def input_current(lambda_fl, transfer_ratio, phi_rad, v1, v2):
    """
    Function to calculate the inductor currents il0, il1, il2 and il3
    :param lambda_fl: mesh lambda in f*L
    :param transfer_ratio: mesh n
    :param phi_rad: mesh phi in rad
    :param v1: voltage v1 in V
    :param v2: voltage v2 in V
    :return: currents il0, il1, il2, il3
    """
    # generate matrix
    ib_il0 = np.full_like(lambda_fl, np.nan)
    ib_il1 = np.full_like(lambda_fl, np.nan)
    ib_il2 = np.full_like(lambda_fl, np.nan)
    ib_il3 = np.full_like(lambda_fl, np.nan)

    # calculate the other data points
    ib_il0 = (np.pi * (transfer_ratio * v2 - v1) - 2 * phi_rad * transfer_ratio * v2) / (4 * np.pi * lambda_fl)
    ib_il1 = ib_il0 + (v1 + transfer_ratio * v2) * phi_rad / (2 * np.pi * lambda_fl)
    ib_il2 = ib_il1 + (v1 - transfer_ratio * v2) * (np.pi - phi_rad) / (2 * np.pi * lambda_fl)
    ib_il3 = ib_il2 + (-v1 - transfer_ratio * v2) * phi_rad / (2 * np.pi * lambda_fl)

    return ib_il0, ib_il1, ib_il2, ib_il3

def f_mln_ib_ilm(phi_rad, lambda_fl, transfer_ratio, v2, ratio_lm_ls=10.0):
    """
    Calculates the primary side L_main current
    :param phi_rad: Phase angle in rad, for display only
    :param lambda_fl: lambda = switching frequency * L_stray
    :param transfer_ratio: transfer ratio n
    :param v2: output voltage
    :param ratio_lm_ls: ratio = lm/ls
    :return: ib_ilm_peak, ib_ilm_rms
    """
    ib_ilm_peak = np.full_like(lambda_fl, np.nan)
    ib_ilm_rms = np.full_like(lambda_fl, np.nan)

    # complete mesh with phi
    ib_ilm_peak = v2 * transfer_ratio / (ratio_lm_ls * lambda_fl * 4)

    x = [0, np.pi]
    y = [-ib_ilm_peak, ib_ilm_peak]
    value = np.interp(np.pi - phi_rad, x,y)

    ib_ilm_vec = [-value, -ib_ilm_peak, value, ib_ilm_peak, -value]

    return ib_ilm_vec


if __name__ == '__main__':

    frequency = 200000
    l_s = 85e-6
    l_h = 600e-6
    transfer_ratio = 2.9
    v1 = 700
    v2 = 295
    power_max = 2000

    # pre calculations
    lambda_fl = frequency * l_s
    ratio_lm_ls = l_h / l_s
    # calculations
    phi_rad = phi_rad_from_input_parameters(lambda_fl, transfer_ratio, v1, v2, power_max)
    i1_0, i1_1, i1_2, i1_3 = input_current(lambda_fl, transfer_ratio, phi_rad, v1, v2)

    phi_rad_vec = [0, phi_rad, np.pi, np.pi + phi_rad, 2*np.pi]
    i_1_vec = [i1_0, i1_1, i1_2, i1_3, i1_0]

    i_l_m_vec = f_mln_ib_ilm(phi_rad, lambda_fl, transfer_ratio, v2, ratio_lm_ls=ratio_lm_ls)
    i_2_t_vec = np.array([i_l_m_vec[count] - i_1_vec[count] for count, value in enumerate(i_1_vec)])
    i_2_vec = i_2_t_vec * transfer_ratio

    time_vec = np.array(phi_rad_vec) / (2 * np.pi * frequency)

    # negative sign to output current due to counting arrow system
    print('################################')
    i_1 = [list(time_vec), i_1_vec]
    print(f"{i_1 = }")
    i_2 = [list(time_vec), list(np.array(i_2_vec))]
    print(f"{i_2 = }")
    print('################################')


    plt.plot(time_vec, i_1_vec, label="i_1")
    plt.plot(time_vec, i_l_m_vec, label='i_l_m')
    plt.plot(time_vec, i_2_t_vec, label='i_2,t')
    plt.plot(time_vec, i_2_vec, label='i_2', linestyle="--")
    plt.grid()
    plt.legend()
    plt.show()
