# controllers/grading_controller.py

from services.pcv.preprocess import preprocess_image
from services.pcv.segmentation import segment_image
from services.pcv.feature_extract import extract_features
from services.pcv.normalization import normalize_features
from services.fuzzy.mamdani import compute_fuzzy_score
from services.grading_service import combine_final_grade
from models.grading_model import GradingResult
from core.database import SessionLocal

def process_and_grade_image(img, filename):
    db = SessionLocal()

    # 1. Preprocess
    hsv = preprocess_image(img)

    # 2. Segmentasi
    segmented, mask = segment_image(hsv)

    # 3. Ekstraksi fitur
    area, width, height, weight, texture, hue = extract_features(segmented, mask)

    # 4. Normalisasi
    area_n, weight_n, texture_n, hue_n = normalize_features(area, weight, texture, hue)

    # 5. Fuzzy
    fuzzy_score, fuzzy_label = compute_fuzzy_score(area_n, weight_n, texture_n, hue_n)

    # 6. Grade berat
    grade_w = "A" if weight >= 350 else "B" if weight >= 250 else "C"

    # 7. Final
    final_grade = combine_final_grade(grade_w, fuzzy_label)

    # 8. Simpan ke database
    record = GradingResult(
        filename=filename,
        area_cm2=area,
        width_cm=width,
        height_cm=height,
        weight_est_g=weight,
        texture_score=texture,
        hue_mean=hue,
        area_norm=area_n,
        weight_norm=weight_n,
        texture_norm=texture_n,
        hue_norm=hue_n,
        fuzzy_score=fuzzy_score,
        fuzzy_grade_label=fuzzy_label,
        grade_by_weight=grade_w,
        final_grade=final_grade
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
