import femmt as fmt
import numpy as np
from femmt.femmt_reluctance import MagneticCircuit


# Set core-geometry from core database
core_db1 = fmt.core_database()["PQ 40/40"]
core_db2 = fmt.core_database()["PQ 26/25"]

core_width_list = [core_db1["core_inner_diameter"], core_db2["core_inner_diameter"]]
core_window_w_list = [core_db1["window_w"], core_db2["window_w"]]
core_window_h_list = [core_db1["window_h"], core_db2["window_h"]]

# Set air-gap and core parameters
no_of_turns = list(np.linspace(8, 19, 1))                   # Set No. of turns (N)
n_air_gaps = list(np.linspace(1, 2, 1))                     # Set No. of air-gaps (n)
air_gap_length = list(np.linspace(0.0001, 0.0005, 1))       # Set air-gap length in metre (l)
air_gap_position = list(np.linspace(50, 75, 1))             # Set air-gap position in percentage with respect to core window height
mu_rel = [3000]                                             # Set relative permeability in F/m (u)

# Set two types of equally distributed air-gaps (used only for air-gaps more than 1):
# Type 1: Equally distributed air-gaps including corner air-gaps (eg: air-gaps-position = [0, 50, 100] for 3 air-gaps)
# Type 2: Equally distributed air-gaps excluding corner air-gaps (eg: air-gaps-position = [25, 50, 75] for 3 air-gaps)
mult_air_gap_type = [1, 2]

# Call to Reluctance model (Class MagneticCircuit)
mc = MagneticCircuit(core_width_list, core_window_h_list, core_window_w_list, no_of_turns, n_air_gaps, air_gap_length, air_gap_position, mu_rel, mult_air_gap_type)

# Calculate total reluctance and creates data_matrix to access all corresponding parameters and results
mc.core_reluctance()
mc.air_gap_reluctance()

# To access all/any data, use mc.data_matrix[:, parameter_name]. The parameters are arranged as shown below:
# mc.data_matrix = [core_w, window_h, window_w, mu_rel, no_of_turns, n_air_gaps, air_gap_h, air_gap_position,
# mult_air_gap_type, inductance]
print(f"Total Reluctance:{mc.data_matrix[:, 4] ** 2 / mc.data_matrix[:, 9]}")
print(f"Inductance:{mc.data_matrix[:, 9]}")




