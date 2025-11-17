# services/grading_service.py

import numpy as np
import cv2
from sqlalchemy.orm import Session

from models.grading_model import GradingResult
from .pcv.preprocess import preprocess_image
from .pcv.segmentation import segment_image
from .pcv.feature_extract import extract_features
from .pcv.normalization import normalize_pct
from .fuzzy.mamdani import get_fuzzy_sim


# grade by weight
def grade_by_weight(weight_g):
    if weight_g >= 350:
        return "A"
    elif weight_g >= 250:
        return "B"
    return "C"


def fuzzy_grade_label(score):
    if score >= 65:
        return "good"
    elif score >= 40:
        return "defect"
    return "rotten"


def process_image(image_np, reference_df, filename: str, db: Session):
    """
    image_np: numpy array BGR
    reference_df: dataset features.csv untuk normalisasi percentile
    db: database session
    """

    # 1. Preprocess → HSV
    hsv = preprocess_image(image_np)

    # 2. Segmentasi
    segmented, mask = segment_image(hsv)

    # 3. Ekstraksi fitur
    area, w, h, weight, tex_score, hue_mean = extract_features(segmented, mask)

    # 4. Normalisasi percentile
    area_norm = normalize_pct(area, reference_df["area_cm2"])
    weight_norm = normalize_pct(weight, reference_df["weight_est_g"])
    tex_norm = normalize_pct(tex_score, reference_df["texture_score"])
    hue_norm = normalize_pct(hue_mean, reference_df["hue_mean"])

    # 5. Fuzzy
    sim = get_fuzzy_sim()
    sim.input["ukuran"] = area_norm
    sim.input["berat"] = weight_norm
    sim.input["tekstur"] = tex_norm
    sim.input["warna"] = hue_norm
    sim.compute()

    fuzzy_score = float(sim.output["kondisi"])
    fuzzy_label = fuzzy_grade_label(fuzzy_score)

    # 6. Weight grade
    weight_label = grade_by_weight(weight)

    # 7. Final grade gabungan
    final_grade = f"{weight_label} {fuzzy_label}"

    # 8. Simpan ke database
    db_record = GradingResult(
        filename=filename,

        area_cm2=area,
        width_cm=w,
        height_cm=h,
        weight_est_g=weight,
        texture_score=tex_score,
        hue_mean=hue_mean,

        area_norm=area_norm,
        weight_norm=weight_norm,
        texture_norm=tex_norm,
        hue_norm=hue_norm,

        fuzzy_score=fuzzy_score,
        fuzzy_grade_label=fuzzy_label,

        grade_by_weight=weight_label,
        final_grade=final_grade
    )

    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # 9. Return ke API
    return {
        "id": db_record.id,
        "filename": filename,

        "area_cm2": area,
        "width_cm": w,
        "height_cm": h,
        "weight_est_g": weight,
        "texture_score": tex_score,
        "hue_mean": hue_mean,

        "area_norm": area_norm,
        "weight_norm": weight_norm,
        "texture_norm": tex_norm,
        "hue_norm": hue_norm,

        "fuzzy_score": fuzzy_score,
        "fuzzy_grade_label": fuzzy_label,

        "grade_by_weight": weight_label,
        "final_grade": final_grade
    }
