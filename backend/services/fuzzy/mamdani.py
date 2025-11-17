import pandas as pd

def fuzzy_grade(area_norm, weight_norm, texture_norm, hue_norm):
    # panggil kode fuzzy kamu di sini 
    # atau import langsung controller fuzzy dari file grading
    from fuzzy_grading import compute_single_fuzzy  # kamu buat fungsi ini
    return compute_single_fuzzy(area_norm, weight_norm, texture_norm, hue_norm)
