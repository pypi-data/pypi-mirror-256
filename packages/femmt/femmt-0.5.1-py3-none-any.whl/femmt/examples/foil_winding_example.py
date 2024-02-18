import femmt as fmt
import os

# Choose wrap para type
wrap_para_type = fmt.WrapParaType.FixedThickness
# wrap_para_type = fmt.WrapParaType.Interpolate

working_directory = os.path.join(os.path.dirname(__file__), "example_results" , "inductor_foil")
if not os.path.exists(working_directory):
    os.mkdir(working_directory)

geo = fmt.MagneticComponent(component_type=fmt.ComponentType.Inductor, working_directory=working_directory, silent=False)

core_db = fmt.core_database()["PQ 40/40"]

core = fmt.Core(core_inner_diameter=core_db["core_inner_diameter"], window_w=core_db["window_w"], window_h=core_db["window_h"],
                mu_r_abs=3100, phi_mu_deg=12,
                sigma=0.6)
geo.set_core(core)

air_gaps = fmt.AirGaps(fmt.AirGapMethod.Center, core)
air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 0.0005)
geo.set_air_gaps(air_gaps)

insulation = fmt.Insulation()
insulation.add_core_insulations(0.001, 0.001, 0.002, 0.001)
insulation.add_winding_insulations([0.0005])
geo.set_insulation(insulation)

winding_window = fmt.WindingWindow(core, insulation)
vww = winding_window.split_window(fmt.WindingWindowSplit.NoSplit)

winding = fmt.Conductor(0, fmt.Conductivity.Copper)
winding.set_rectangular_conductor(thickness=1e-3)

vww.set_winding(winding, 5, fmt.WindingScheme.FoilVertical, wrap_para_type)
geo.set_winding_window(winding_window)

geo.create_model(freq=100000, pre_visualize_geometry=True, save_png=False)

geo.single_simulation(freq=100000, current=[3], show_fem_simulation_results=True)
