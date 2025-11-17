import numpy as np
import skfuzzy as fuzz

def get_memberships():
    ukuran = np.linspace(0, 1, 101)
    berat = np.linspace(0, 1, 101)
    tekstur = np.linspace(0, 1, 101)
    warna = np.linspace(0, 1, 101)
    kondisi = np.linspace(0, 100, 101)

    return ukuran, berat, tekstur, warna, kondisi
