import os
import femmt as fmt


def load_from_file(onelab_folder: str = None, show_visual_outputs: bool = True, is_test: bool = False):

    example_results_folder = os.path.join(os.path.dirname(__file__), "example_results")
    if not os.path.exists(example_results_folder):
        os.mkdir(example_results_folder)

    working_directory = os.path.join(example_results_folder, "from-file")
    if not os.path.exists(working_directory):
        os.mkdir(working_directory)

    #file = os.path.join(os.path.dirname(__file__), "example_log.json")
    #file = os.path.join('/home/nikolasf/Dokumente/01_git/30_Python/FEMMT/femmt/examples/example_results/transformer/results', 'log_electro_magnetic.json')
    file = os.path.join('/home/nikolasf/Dokumente/01_git/30_Python/FEMMT/femmt/examples/example_results/stacked-center-tapped-transformer/results','log_electro_magnetic.json')


    geo = fmt.MagneticComponent.decode_settings_from_log(file, working_directory)

    geo.create_model(freq=200000, pre_visualize_geometry=show_visual_outputs, save_png=False)

    geo.single_simulation(freq=200000, current=[2, 2],  phi_deg=[0, 180], show_fem_simulation_results=show_visual_outputs)

if __name__ == "__main__":
    load_from_file(show_visual_outputs=False)