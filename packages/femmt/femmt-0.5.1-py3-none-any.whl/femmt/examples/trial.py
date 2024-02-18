import numpy as np


def calculate_area(radius):
    area = radius ** 2 * np.pi
    return area


def app():
    area = calculate_area(1)
    print(f"{area = }")


app()
