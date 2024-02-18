import femmt as fmt
import numpy as np
from matplotlib import pyplot as plt
import itertools

core_inner_diameter = 0.01
air_gap_middle_leg_list = [0.0002, 0.0004, 0.0008, 0.0016, 0.0032]
window_w = 0.02
window_h = 0.03
stray_path_air_gap_length = 0.0003
mu_r = 3000
start_index = 1
position_air_gap_percent_list = [10, 20, 30, 79, 98]



def air_gap_generator(total_air_gaps_min_max_list, total_air_gap_hight_min_max_count_list, sweep_distance = 0.01):
    """
    :param sweep_distance: air gap distance to sweep [0... 1],  0.01 = 1 percent.
    """

    air_gaps_list = np.arange(total_air_gaps_min_max_list[0], total_air_gaps_min_max_list[1] + 1)
    air_gap_hight_list = np.linspace(total_air_gap_hight_min_max_count_list[0], total_air_gap_hight_min_max_count_list[1], total_air_gap_hight_min_max_count_list[2])


    for total_air_gaps, total_air_gap_hight in itertools.product(air_gaps_list, air_gap_hight_list):
        air_gap_middle_leg_list_list = []
        if total_air_gaps == 2:
            for air_gap_1_factor in np.arange(sweep_distance, 1 - sweep_distance + sweep_distance, sweep_distance):
                air_gap_1 = air_gap_1_factor * total_air_gap_hight
                air_gap_2 = (1 - air_gap_1_factor) * total_air_gap_hight
                air_gap_middle_leg_list_list.append([air_gap_1, air_gap_2])
                if air_gap_2 < 0.9 * sweep_distance * total_air_gap_hight:
                    print(f"{air_gap_1_factor = }")
                    raise Exception("error in program code implementation")
        elif total_air_gaps > 2:
            raise NotImplementedError("air gaps > 2 are not supported for the reluctance model")
        else:
            raise Exception("total air gaps needs to be 2...5")
    return air_gap_middle_leg_list_list


def generate_meshgrids():
    air_gap_middle_leg_list = [0.0002, 0.0004, 0.0008, 0.0016, 0.0032]
    stray_path_air_gap_length_list = [0.0003, 0.0004, 0.0005]
    mu_r_list = [2900, 3000, 3100]
    window_w_list = [0.02, 0.03, 0.04]
    window_h_list = [0.023, 0.034, 0.056]


    air_gap_middle_leg_mesh, stray_path_air_gap_length_mesh, mu_r_mesh, window_w_mesh, window_h_mesh = np.meshgrid(air_gap_middle_leg_list, stray_path_air_gap_length_list, mu_r_list, window_w_list, window_h_list)

    print(np.shape(air_gap_middle_leg_mesh))


class ReluctanceIntegratedTransformer:
    def __init__(self, air_gap_top_min_max_count_list, air_gap_bot_min_max_count_list, air_gap_bot_position_min_max_count_list,
                 stray_path_air_gap_min_max_count_list, tablet_hight_min_max_count_list, mu_r_min_max_count_list, window_h_min_max_count_list, window_w_min_max_count_list,
                 core_inner_diameter_min_max_count_list, n_p_top_min_max_list, n_p_bot_min_max_list, n_s_top_min_max_list, n_s_bot_min_max_list):
        self.generate_meshgrids(air_gap_top_min_max_count_list, air_gap_bot_min_max_count_list, air_gap_bot_position_min_max_count_list,
                       stray_path_air_gap_min_max_count_list, tablet_hight_min_max_count_list, n_p_top_min_max_list, n_p_bot_min_max_list, n_s_top_min_max_list, n_s_bot_min_max_list)
        self.sweep_global_alorithm(window_h_min_max_count_list, window_w_min_max_count_list, mu_r_min_max_count_list,
                              core_inner_diameter_min_max_count_list)

    def generate_meshgrids(self, air_gap_top_min_max_count_list, air_gap_bot_min_max_count_list, air_gap_bot_position_min_max_count_list,
        stray_path_air_gap_min_max_count_list, tablet_hight_min_max_count_list, n_p_top_min_max_list, n_p_bot_min_max_list, n_s_top_min_max_list, n_s_bot_min_max_list):
        # matrix parameters: core geometry
        self.air_gap_top_list = np.linspace(air_gap_top_min_max_count_list[0], air_gap_top_min_max_count_list[1], air_gap_top_min_max_count_list[2])
        self.air_gap_bot_list = np.linspace(air_gap_bot_min_max_count_list[0], air_gap_bot_min_max_count_list[1], air_gap_top_min_max_count_list[2])
        self.air_gap_bot_position = np.linspace(air_gap_bot_position_min_max_count_list[0], air_gap_bot_position_min_max_count_list[1], air_gap_bot_position_min_max_count_list[2])
        self.stray_path_air_gap_list = np.linspace(stray_path_air_gap_min_max_count_list[0], stray_path_air_gap_min_max_count_list[1], stray_path_air_gap_min_max_count_list[2])
        self.tablet_hight_list = np.linspace(tablet_hight_min_max_count_list[0], tablet_hight_min_max_count_list[1], tablet_hight_min_max_count_list[2])

        # matrix parameters: windings
        self.n_p_top_list = np.arange(n_p_top_min_max_list[0], n_p_top_min_max_list[1] + 1)
        self.n_p_bot_list = np.arange(n_p_bot_min_max_list[0], n_p_bot_min_max_list[1] + 1)
        self.n_s_top_list = np.arange(n_s_top_min_max_list[0], n_s_top_min_max_list[1] + 1)
        self.n_s_bot_list = np.arange(n_s_bot_min_max_list[0], n_s_bot_min_max_list[1] + 1)

        print(f"8 Dimensions")
        combinations = len(self.air_gap_top_list) * len(self.air_gap_bot_list) * len(self.air_gap_bot_position) *  \
            len(self.stray_path_air_gap_list) * \
            len(self.n_p_top_list) * len(self.n_p_bot_list) * len(self.n_s_top_list) * len(self.n_s_bot_list)
        print(f"{combinations = }")
        byte = 8 # byte per numpy float64 = 64 bit = 8 byte
        storage_gb = combinations * 8 / ( 1e9)
        print(f"storage_gb per matrix: {storage_gb} GB")

        # set up meshgrid matrix
        self.m_air_gap_top, self.m_air_gap_bot, self.m_air_gap_bot_position, self.m_stray_path_air_gap, self.m_tablet_hight, self.m_n_p_top, self.m_n_p_bot, self.m_n_s_top, self.m_n_s_bot = np.meshgrid(self.air_gap_top_list, self.air_gap_bot_list, self.air_gap_bot_position, self.stray_path_air_gap_list, self.tablet_hight_list, self.n_p_top_list, self.n_p_bot_list, self.n_s_top_list, self.n_s_bot_list, sparse=True)

    @staticmethod
    def mf_r_core_round(core_inner_diameter, core_round_hight, mu_r):
        """
        Calculates the core reluctance for a round structure

        :param core_round_hight: hight of the round core part section
        :param core_inner_diameter: core inner diameter
        :param mu_r: relative permeability (mu_r) of the core material from datasheet
        """
        return core_round_hight / (fmt.mu0 * mu_r * (core_inner_diameter / 2) ** 2 * np.pi)


    def sweep_global_alorithm(self, window_h_min_max_count_list, window_w_min_max_count_list, mu_r_min_max_count_list, core_inner_diameter_min_max_count_list):
        # global sweep parameters
        self.window_h_list = np.linspace(window_h_min_max_count_list[0], window_h_min_max_count_list[1],
                                         window_h_min_max_count_list[2])
        self.window_w_list = np.linspace(window_w_min_max_count_list[0], window_w_min_max_count_list[1],
                                         window_w_min_max_count_list[2])
        self.mu_r_list = np.linspace(mu_r_min_max_count_list[0], mu_r_min_max_count_list[1], mu_r_min_max_count_list[2])
        self.core_inner_diameter_list = np.linspace(core_inner_diameter_min_max_count_list[0], core_inner_diameter_min_max_count_list[1], core_inner_diameter_min_max_count_list[2])
#matrix_output = np.array(list(itertools.product(self.mu_r_list, self.window_w_list, self.window_h_list, self.core_inner_diameter_list))):        matrix_output = np.array(list(itertools.product(self.mu_r_list, self.window_w_list, self.window_h_list, self.core_inner_diameter_list))):
        for mu_r, window_w, window_h, core_inner_diameter in itertools.product(self.mu_r_list, self.window_w_list, self.window_h_list, self.core_inner_diameter_list):
            # calculate r_top, r_bot, r_stray
            start_index = 0
            #r_top, r_bot, r_stray = self.r_top_bot_stray(matrix_output)  # irgendwas kreuz vier matirx
            #, r_bot, r_stray = self.r_top_bot_stray(core_inner_diameter, window_w, window_h, mu_r) # irgendwas kreuz vier matirx
            print("1")
            #abhängig von den Suchraum-samples
            #shape(r_top) = (3,4,5,2,3,4,5,6,7)
            # shape(r_bot) = (3,4,5,2,3,4,5,6,7)
            # shape(r_stray) = (3,4,5,2,3,4,5,6,7)
            # shapes immer gleich!


            # generate reluctance matrix

            #r_top[1,1,1,1,1,1,1,1,1,1] +r_bot[1,1,1,1,1,1,1,1,1,1] + stray []
            #-> IMMER shape(2,2)

            # L_trafo_reluctance = [ [] , []]
            # -> shape(2,2)

            # L_trafo [1,1,1,1,1,1,1,1,1,1] = [[],[]]
            #

            # generate widing matrix
            # N

            # calculate inductance matrix
            # -> ls und lh extrahieren

            # verify for valid designs in range of goal parameters
            # wenn ls und lh innerhalb von [] []
            # numpy fancy indexing
            # dann speichere design.




    def r_top_bot_stray(self, core_inner_diameter, window_w, window_h, mu_r):
        """
        Steps:
         - calculate m_r_top
            -> r_core
            -> m_r_top_air_gap
         - calculate r_bot
            -> r_bot_core
            -> r_bot_air_gap
         - calculate r_stray
            -> m_r_stray_core
            -> m_r_stray_air_gap
        """

        def calculate_r_core(core_inner_diameter, core_round_hight, mu_r, window_w):
            # calculate middle leg reluctance
            r_core_round_inner = fmt.r_core_round(core_inner_diameter, core_round_hight, mu_r)

            # calculate top-core-part reluctance
            # ToDo: radiant calculation core hight is very simplified using core_inner_diameter/2
            r_core_radiant = fmt.r_core_top_bot_radiant(core_inner_diameter, window_w, mu_r,
                                                            core_inner_diameter / 2)
            # calculate outer leg reluctance
            r_core_round_outer = r_core_round_inner

            # return total top core reluctance
            r_core = r_core_round_inner + r_core_radiant + r_core_round_outer
            r_core[r_core < 0] = np.nan
            return r_core

        def calculate_r_air_gap(core_inner_diameter, core_round_hight):
            # this is for the first air gap, what is definetly a round_inf air gap
            r_air_gap = fmt.r_air_gap_round_inf(self.m_air_gap_top, core_inner_diameter, core_round_hight)
            return r_air_gap


        #m_middle_leg_bot_hight = np.full_like(self.m_n_p_bot, np.nan)

        # calculate core hights
        m_middle_leg_bot_hight = window_h * 0.01 * self.m_air_gap_bot_position - self.m_air_gap_bot / 2
        m_middle_leg_top_hight = window_h  - m_middle_leg_bot_hight - self.m_tablet_hight - self.m_air_gap_bot - self.m_air_gap_top
        m_middle_leg_top_hight[m_middle_leg_top_hight < 0] = np.nan

        # m_r_top
        m_r_top_core = calculate_r_core(core_inner_diameter, m_middle_leg_top_hight, mu_r, window_w) # spalte übergeben output_matrix[:,spalte]
        m_r_top_air_gap = calculate_r_air_gap(core_inner_diameter, m_middle_leg_top_hight)
        m_r_top = m_r_top_core + m_r_top_air_gap

        # r_bot
        m_r_bot_core = calculate_r_core(core_inner_diameter, m_middle_leg_bot_hight, mu_r, window_w)
        m_r_bot_air_gap = calculate_r_air_gap(core_inner_diameter, m_middle_leg_bot_hight)
        m_r_bot = m_r_bot_core + m_r_bot_air_gap

        # calculate r_stray
        m_r_stray_air_gap = fmt.r_air_gap_tablet_cyl(self.m_tablet_hight, self.m_stray_path_air_gap,
                                               core_inner_diameter / 2 + window_w)
        m_r_stray_core = fmt.r_core_tablet(self.m_tablet_hight, core_inner_diameter / 2 + window_w - self.m_stray_path_air_gap, mu_r,
                                     core_inner_diameter)
        m_r_stray = m_r_stray_air_gap + m_r_stray_core

        return m_r_top, m_r_bot, m_r_stray


if __name__ == "__main__":

    ReluctanceIntegratedTransformer(air_gap_top_min_max_count_list = [0.0005, 0.001, 3],
                            air_gap_bot_min_max_count_list = [0.0005, 0.001, 3],
                            air_gap_bot_position_min_max_count_list = [0.1, 0.4, 5],
                            stray_path_air_gap_min_max_count_list = [0.0005, 0.001, 3],
                            tablet_hight_min_max_count_list = [0.005, 0.015, 10],
                            mu_r_min_max_count_list = [2900, 3100, 3],
                            window_h_min_max_count_list = [0.01, 0.04, 10],
                            window_w_min_max_count_list = [0.01, 0.04, 10],
                            core_inner_diameter_min_max_count_list = [0.01, 0.05, 10],
                                    n_p_top_min_max_list = [10,20],
                                    n_p_bot_min_max_list = [10,20],
                                    n_s_top_min_max_list = [10,20],
                                    n_s_bot_min_max_list = [10,20])