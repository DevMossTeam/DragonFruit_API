import skfuzzy as fuzz
import numpy as np

x = np.linspace(0, 1, 101)

ukuran_small = fuzz.trimf(x, [0, 0, 0.4])
ukuran_medium = fuzz.trimf(x, [0.3, 0.55, 0.75])
ukuran_large = fuzz.trimf(x, [0.6, 1, 1])
