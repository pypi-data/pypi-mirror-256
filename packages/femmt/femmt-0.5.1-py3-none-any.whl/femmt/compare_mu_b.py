import femmt as fmt
import os

working_directory = "/home/nikolasf/Downloads/2022-11-20_simulation_femmt"


# 1. chose simulation type
geo = fmt.MagneticComponent(component_type=fmt.ComponentType.Inductor, working_directory=working_directory, silent=False)

# 2. set core parameters
core = fmt.Core(core_inner_diameter=0.045000000000000005, window_w=0.03222222222222222, window_h=0.01,
                material="N95", temperature=100, frequency=100000, datasource="manufacturer_datasheet")
                # mu_rel=3000, phi_mu_deg=5,
                # sigma=0.16)
geo.set_core(core)

# 3. set air gap parameters
air_gaps = fmt.AirGaps(fmt.AirGapMethod.Percent, core)
air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 0.0004, 33.33)
#air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 0.0002, 66.66)
geo.set_air_gaps(air_gaps)

# 4. set insulations
insulation = fmt.Insulation()
insulation.add_core_insulations(0.001, 0.001, 0.001, 0.001)
insulation.add_winding_insulations([0.0005], 0.0001)
geo.set_insulation(insulation)

# 5. create winding window and virtual winding windows (vww)
winding_window = fmt.WindingWindow(core, insulation)
vww = winding_window.split_window(fmt.WindingWindowSplit.NoSplit)

# 6. create conductor and set parameters: use solid wires
winding = fmt.Conductor(0, fmt.Conductivity.Copper)
#winding.set_solid_round_conductor(conductor_radius=0.0013, conductor_arrangement=fmt.ConductorArrangement.Square)
winding.set_litz_round_conductor(conductor_radius=0.0007, number_strands=200, strand_radius=3.55e-5,
 fill_factor=None, conductor_arrangement=fmt.ConductorArrangement.Square)

# 7. add conductor to vww and add winding window to MagneticComponent
vww.set_winding(winding, 5, None)
geo.set_winding_window(winding_window)

# 8. create the model
geo.create_model(freq=100000, pre_visualize_geometry=False, save_png=False)

# 6.a. start simulation
geo.single_simulation(freq=100000, current=[8], show_fem_simulation_results=True)