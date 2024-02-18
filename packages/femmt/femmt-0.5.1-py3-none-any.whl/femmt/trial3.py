import numpy as np


list1 = np.linspace(1, 5, 10)
list2 = np.linspace(100, 200, 3)

m_1, m_2 = np.meshgrid(list1, list2, sparse=False)

out = m_1 * m_2

print(f"{out = }")