import femmt as fmt
import os
import materialdatabase as mdb
# byJan
import numpy as np
import matplotlib.pyplot as plt
import json


def find_common_in_freq_save_amplitude_phase(array_fs_prim, array_amplitude_prim, array_phase_prim,
                                             array_fs_sek1, array_amplitude_sek1, array_phase_sek1,
                                             array_fs_sek2, array_amplitude_sek2, array_phase_sek2):

    # Convert to a list if no list
    list_fs_prim = list(array_fs_prim) if isinstance(array_fs_prim, list) else array_fs_prim.tolist()
    list_fs_sek1 = list(array_fs_sek1) if isinstance(array_fs_sek1, list) else array_fs_sek1.tolist()
    list_fs_sek2 = list(array_fs_sek2) if isinstance(array_fs_sek2, list) else array_fs_sek2.tolist()

    list_amplitude_prim = list(array_amplitude_prim) if isinstance(array_amplitude_prim,
                                                                   list) else array_amplitude_prim.tolist()
    list_amplitude_sek1 = list(array_amplitude_sek1) if isinstance(array_amplitude_sek1,
                                                                   list) else array_amplitude_sek1.tolist()
    list_amplitude_sek2 = list(array_amplitude_sek2) if isinstance(array_amplitude_sek2,
                                                                   list) else array_amplitude_sek2.tolist()

    list_phase_prim = list(array_phase_prim) if isinstance(array_phase_prim, list) else array_phase_prim.tolist()
    list_phase_sek1 = list(array_phase_sek1) if isinstance(array_phase_sek1, list) else array_phase_sek1.tolist()
    list_phase_sek2 = list(array_phase_sek2) if isinstance(array_phase_sek2, list) else array_phase_sek2.tolist()

    common_fs_values = set(list_fs_prim) & set(list_fs_sek1) & set(list_fs_sek2)
    amplitude_list = []
    phase_list = []

    # For each common value in list_fs, find corresponding values in amplitude and phase
    for value in common_fs_values:
        index1 = list_fs_prim.index(value)
        index2 = list_fs_sek1.index(value)
        index3 = list_fs_sek2.index(value)

        # Get corresponding values from amplitude, if index is within bounds
        amplitude_prim_value = list_amplitude_prim[index1] if index1 < len(list_amplitude_prim) else None
        amplitude_sek1_value = list_amplitude_sek1[index2] if index2 < len(list_amplitude_sek1) else None
        amplitude_sek2_value = list_amplitude_sek2[index3] if index3 < len(list_amplitude_sek2) else None

        amplitude_list.append([amplitude_prim_value, amplitude_sek1_value, amplitude_sek2_value])

        # Get corresponding values from phase, if index is within bounds
        phase_prim_value = list_phase_prim[index1] if index1 < len(list_phase_prim) else None
        phase_sek1_value = list_phase_sek1[index2] if index2 < len(list_phase_sek1) else None
        phase_sek2_value = list_phase_sek2[index3] if index3 < len(list_phase_sek2) else None

        phase_list.append([phase_prim_value, phase_sek1_value, phase_sek2_value])

        # common_fs_values = np.array(common_fs_values)

    return list(common_fs_values), amplitude_list, phase_list

def basic_example_transformer_center_tapped(list_freq: list = None, list_list_amplitude: list = None, list_list_phase: list = None,
                                            list_freg_mag: list = None, list_list_amplitude_mag: list = None, list_list_phase_mag: list = None,
                                            onelab_folder: str = None, show_visual_outputs: bool = True,
                                            is_test: bool = False):
    example_results_folder = os.path.join(os.path.dirname(__file__), "example_results")

    if not os.path.exists(example_results_folder):
        os.mkdir(example_results_folder)

    working_directory = os.path.join(example_results_folder, "jan")
    if not os.path.exists(working_directory):
        os.mkdir(working_directory)

    geo = fmt.MagneticComponent(component_type=fmt.ComponentType.Transformer, working_directory=working_directory,
                                verbosity=fmt.Verbosity.ToConsole, is_gui=is_test)

    # This line is for automated pytest running on GitHub only. Please ignore this line!
    if onelab_folder is not None:
        geo.file_data.onelab_folder_path = onelab_folder

    core_dimensions = fmt.dtos.SingleCoreDimensions(window_h=0.018, window_w=0.01175, core_inner_diameter=0.0205,
                                                    core_h=0.029)

    core = fmt.Core(core_type=fmt.CoreType.Single,
                    core_dimensions=core_dimensions,
                    detailed_core_model=False,
                    material=mdb.Material.N95, temperature=45, frequency=10000, mu_r_abs=3300,
                    # permeability_datasource="manufacturer_datasheet",
                    permeability_datasource=fmt.MaterialDataSource.Measurement,
                    permeability_datatype=fmt.MeasurementDataType.ComplexPermeability,
                    permeability_measurement_setup=mdb.MeasurementSetup.LEA_LK,
                    permittivity_datasource=fmt.MaterialDataSource.Measurement,
                    permittivity_datatype=fmt.MeasurementDataType.ComplexPermittivity,
                    permittivity_measurement_setup=mdb.MeasurementSetup.LEA_LK, mdb_verbosity=fmt.Verbosity.Silent)

    geo.set_core(core)

    air_gaps = fmt.AirGaps(fmt.AirGapMethod.Percent, core)
    air_gaps.add_air_gap(fmt.AirGapLegPosition.CenterLeg, 1.15e-3, 50)
    geo.set_air_gaps(air_gaps)

    # set_center_tapped_windings() automatically places the conductors
    insulation, winding_window = fmt.functions_topologies.set_center_tapped_windings(
        core=core,
        primary_turns=15,
        primary_radius=0.95e-3,
        primary_number_strands=600,
        primary_strand_radius=0.035e-3,
        secondary_parallel_turns=4,
        secondary_thickness_foil=0.5e-3,
        iso_top_core=0.001,
        iso_bot_core=0.001,
        iso_left_core=0.0005,
        iso_right_core=0.0005,
        iso_primary_to_primary=1e-4,
        iso_secondary_to_secondary=1e-4,
        iso_primary_to_secondary=1e-4,
        interleaving_type=fmt.CenterTappedInterleavingType.TypeC,
        interleaving_scheme=fmt.InterleavingSchemesFoilLitz.ter_sec_5_ter_sec_5_ter_sec_5_ter_sec,
        primary_additional_bobbin=0e-3,
        winding_temperature=100,
        center_foil_additional_bobbin=0e-3)

    geo.set_insulation(insulation)
    geo.set_winding_windows([winding_window])

    geo.create_model(freq=44500, pre_visualize_geometry=show_visual_outputs)

    # geo.single_simulation(freq=47000, current=[10.8, 0, 0], phi_deg=[0, 0, 0],
    #                       show_fem_simulation_results=show_visual_outputs)

    # Change the phase value from rad to deg by multiply with 360/2pi
    list_list_phase = [[item * (360/(2*np.pi)) for item in sublist] for sublist in list_list_phase]

    # geo.excitation_sweep(frequency_list=list_freq, current_list_list=list_list_amplitude,
    #                      phi_deg_list_list=list_list_phase,show_last_fem_simulation=show_visual_outputs,
    #                      core_hyst_loss=[0.97])

    geo.excitation_sweep(frequency_list=list_freq, current_list_list=list_list_amplitude,
                         phi_deg_list_list=list_list_phase,show_last_fem_simulation=show_visual_outputs)

if __name__ == "__main__":

    with open(
            '/home/nikolasf/Downloads/FixOPmid1/i_res_Vin420_Vout011_I_out140.json',
            'r') as file:
        json_data_i_res = json.load(file)

    with open(
            '/home/nikolasf/Downloads/FixOPmid1/i_sr1_Vin420_Vout011_I_out140.json',
            'r') as file:
        json_data_i_sr1 = json.load(file)

    with open(
            '/home/nikolasf/Downloads/FixOPmid1/i_sr2_Vin420_Vout011_I_out140.json',
            'r') as file:
        json_data_i_sr2 = json.load(file)

    with open(
            '/home/nikolasf/Downloads/FixOPmid1/i_mag_Vin420_Vout011_I_out140.json',
            'r') as file:
        json_data_i_mag = json.load(file)


    # Now json_data to list
    data_i_res = json_data_i_res['data']
    time_i_res = json_data_i_res['time']

    data_i_sr1 = json_data_i_sr1['data']
    time_i_sr1 = json_data_i_sr1['time']

    data_i_sr2 = json_data_i_sr2['data']
    time_i_sr2 = json_data_i_sr2['time']

    data_i_mag = json_data_i_mag['data']
    time_i_mag = json_data_i_mag['time']

    # FFT
    out_i_prim = fmt.fft(np.array([time_i_res, data_i_res]), plot='yes', mode='time', title='ffT _i_res', filter_value_factor=0.001)
    out_i_sek1 = fmt.fft(np.array([time_i_sr1, data_i_sr1]), plot='yes', mode='time', title='ffT _i_sr1', filter_value_factor=0.02)
    out_i_sek2 = fmt.fft(np.array([time_i_sr2, data_i_sr2]), plot='yes', mode='time', title='ffT _i_sr2', filter_value_factor=0.02)
    out_i_mag = fmt.fft(np.array([time_i_mag, data_i_mag]), plot='yes', mode='time', title='ffT _i_mag', filter_value_factor=0.02)

    # Simulation transformer
    ############################

    # Finding common values in frequency and saving corresponding values from amplitude and phase
    [fs_list, amplitude_list_list, phase_list_list] = find_common_in_freq_save_amplitude_phase(
        out_i_prim[0], out_i_prim[1], out_i_prim[2],
        out_i_sek1[0], out_i_sek1[1], out_i_sek1[2],
        out_i_sek2[0], out_i_sek2[1], out_i_sek2[2])


    # # Build lists for exitation sweep for core loss calculation (Wrong! Use single exitation!)
    # fs_list_mag = [out_i_mag[0][1], out_i_mag[0][2], out_i_mag[0][3], out_i_mag[0][4]]
    # amplitude_list_list_mag = [[out_i_mag[1][1],0,0], [out_i_mag[1][2],0,0], [out_i_mag[1][3],0,0], [out_i_mag[1][4],0,0]]
    # phase_list_list_mag = [[out_i_mag[2][1],0,0], [out_i_mag[2][2],0,0], [out_i_mag[2][3],0,0], [out_i_mag[2][4],0,0]]

    basic_example_transformer_center_tapped(fs_list, amplitude_list_list, phase_list_list, show_visual_outputs=True)