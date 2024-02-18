# minimal example for shadowing 
# message
# Shadows name 'area' from outer scope

import numpy as np

class Trial:

    @staticmethod
    def calculate_area(radius):
        # global area_global
        # print(f"{area_global = }")
        #
        area_global = radius ** 2 * np.pi
        print(f"{area_global = }")
        return area_global




if __name__ == '__main__':
    import femmt as fmt
    import numpy as np
    example_waveform = np.array([[0, 1.34, 3.14, 4.48, 6.28], [-175.69, 103.47, 175.69, -103.47, -175.69]])
    fmt.fft(example_waveform, plot='yes', mode='rad', f0=25000, title='ffT input current', filter_value_factor=0.00001)