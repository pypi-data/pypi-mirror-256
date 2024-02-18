# minimal example for shadowing
def component_study():
    hyst_frequency = 1

    def split_hysteresis_loss_excitation_center_tapped():
        print(hyst_frequency)

    split_hysteresis_loss_excitation_center_tapped()


component_study()
x = 1