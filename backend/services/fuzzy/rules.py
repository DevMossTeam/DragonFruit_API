import numpy as np            # <-- WAJIB DITAMBAHKAN
import skfuzzy as fuzz
from skfuzzy import control as ctrl

def build_fuzzy_controller():
    ukuran = ctrl.Antecedent(np.linspace(0, 1, 101), 'ukuran')
    berat = ctrl.Antecedent(np.linspace(0, 1, 101), 'berat')
    tekstur = ctrl.Antecedent(np.linspace(0, 1, 101), 'tekstur')
    warna = ctrl.Antecedent(np.linspace(0, 1, 101), 'warna')
    kondisi = ctrl.Consequent(np.linspace(0, 100, 101), 'kondisi')

    # --- Definisi fuzzy set ---
    ukuran['kecil'] = fuzz.trimf(ukuran.universe, [0.0, 0.0, 0.4])
    ukuran['sedang'] = fuzz.trimf(ukuran.universe, [0.3, 0.55, 0.75])
    ukuran['besar'] = fuzz.trimf(ukuran.universe, [0.6, 1.0, 1.0])

    berat['rendah'] = fuzz.trimf(berat.universe, [0.0, 0.0, 0.4])
    berat['sedang'] = fuzz.trimf(berat.universe, [0.3, 0.55, 0.75])
    berat['tinggi'] = fuzz.trimf(berat.universe, [0.6, 1.0, 1.0])

    tekstur['kasar'] = fuzz.trimf(tekstur.universe, [0.0, 0.0, 0.3])
    tekstur['normal'] = fuzz.trimf(tekstur.universe, [0.2, 0.45, 0.7])
    tekstur['halus'] = fuzz.trimf(tekstur.universe, [0.4, 0.7, 1.0])

    warna['gelap'] = fuzz.trimf(warna.universe, [0.0, 0.0, 0.4])
    warna['normal'] = fuzz.trimf(warna.universe, [0.3, 0.55, 0.8])
    warna['cerah'] = fuzz.trimf(warna.universe, [0.65, 1.0, 1.0])

    kondisi['rotten'] = fuzz.trimf(kondisi.universe, [0, 0, 40])
    kondisi['defect'] = fuzz.trimf(kondisi.universe, [35, 55, 75])
    kondisi['good'] = fuzz.trimf(kondisi.universe, [65, 100, 100])

    # --- Rules ---
    rules = [
        ctrl.Rule(ukuran['besar'] & berat['tinggi'], kondisi['good']),
        ctrl.Rule(berat['tinggi'] & tekstur['halus'], kondisi['good']),
        ctrl.Rule(ukuran['sedang'] & berat['sedang'] & tekstur['halus'], kondisi['good']),
        ctrl.Rule(ukuran['sedang'] & berat['sedang'], kondisi['defect']),
        ctrl.Rule(tekstur['kasar'] | berat['rendah'], kondisi['rotten']),
        ctrl.Rule(warna['cerah'] & tekstur['halus'], kondisi['good']),
        ctrl.Rule(warna['normal'] & tekstur['halus'], kondisi['good']),
        ctrl.Rule(warna['normal'] & tekstur['normal'], kondisi['defect']),
        ctrl.Rule(warna['gelap'] & tekstur['kasar'], kondisi['rotten']),
    ]

    return ctrl.ControlSystem(rules)
