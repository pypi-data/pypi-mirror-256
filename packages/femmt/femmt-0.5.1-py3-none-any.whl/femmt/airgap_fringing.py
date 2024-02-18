import numpy as np

mu0 = 4*np.pi*1e-7


def r_basic_round_inf(air_gap_radius, air_gap_basic_hight, core_hight):
    conductance_basic = mu0 * (air_gap_radius * 2 / 2 / air_gap_basic_hight + 2 / np.pi * (1 + np.log(np.pi * core_hight / 4 / air_gap_basic_hight)))

    return 1 / conductance_basic

def sigma_round(r_equivalent, air_gap_radius, air_gap_total_hight):
    return r_equivalent * mu0 * air_gap_radius / air_gap_total_hight

def r_air_gap_round_round(air_gap_total_hight, core_inner_diameter, core_hight_upper, core_hight_lower):
    air_gap_radius = core_inner_diameter / 2

    air_gap_basic_hight = air_gap_total_hight / 2
    r_basic_upper = r_basic_round_inf(air_gap_radius, air_gap_basic_hight, core_hight_upper)
    r_basic_lower = r_basic_round_inf(air_gap_radius, air_gap_basic_hight, core_hight_lower)
    print(f"{r_basic_upper = }")

    r_equivalent_round_round = r_basic_upper + r_basic_lower

    sigma = sigma_round(r_equivalent_round_round, air_gap_radius, air_gap_total_hight)
    print(f"{sigma = }")

    r_air_gap_ideal = air_gap_total_hight / mu0 / np.pi / (air_gap_radius ** 2)
    print(f"{r_air_gap_ideal = }")
    r_air_gap = sigma ** 2 * r_air_gap_ideal

    return r_air_gap

def r_air_gap_round_inf(air_gap_total_hight, core_inner_diameter, core_hight):
    air_gap_radius = core_inner_diameter / 2
    r_basic = r_basic_round_inf(air_gap_radius, air_gap_total_hight, core_hight)

    r_equivalent_round_inf = r_basic
    sigma = sigma_round(r_equivalent_round_inf, air_gap_radius, air_gap_total_hight)

    r_air_gap_ideal = air_gap_total_hight / mu0 / np.pi / (air_gap_radius ** 2)
    r_air_gap = sigma ** 2 * r_air_gap_ideal

    return r_air_gap



if __name__ == '__main__':
    core_inner_diameter = 0.045
    single_air_gap_total_hight = 0.0002
    core_hight = 0.01
    air_gap_count = 2


    single_r_gap = r_air_gap_round_round(single_air_gap_total_hight, core_inner_diameter, core_hight, core_hight)
    print(f"{single_r_gap = }")

    r_gap_total = single_r_gap * air_gap_count
    current = 8
    turns = 5
    l_eff_core = 2 * (0.032 + 0.01)
    mu_r_core = 3000

    r_core = l_eff_core / (mu0 * mu_r_core * ((core_inner_diameter / 2) ** 2) * np.pi)

    r_total = r_core + r_gap_total

    flux = current * turns / r_total

    flux_density = flux / (np.pi * (core_inner_diameter / 2) ** 2)

    print(f"{r_core = }")
    print(f"{r_total = }")
    print(f"{flux = }")
    print(f"{flux_density = }")

    #
    # inductance = 0.000298
    #
    #
    # b = inductance * current / turns / ((core_inner_diameter / 2) ** 2 * np.pi)
    # print(f"{b = }")

    r_gap_round_inf = r_air_gap_round_inf(single_air_gap_total_hight, core_inner_diameter, core_hight)
    print(r_gap_round_inf)