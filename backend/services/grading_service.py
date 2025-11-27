# services/grading_service.py
import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np
import cv2
from sqlalchemy.orm import Session

from models.grading_model import GradingResult

# PCV utilities
from services.pcv.preprocess import preprocess_image
from services.pcv.segmentation import segment_image
from services.pcv.feature_extract import extract_features
from services.pcv.normalization import normalize_pct, normalize_fixed

# Fuzzy logic
from services.fuzzy.mamdani import compute_fuzzy_score, grade_from_weight

# MQTT publisher
from services.mqtt_service import mqtt_publish

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Normalisasi nilai aman (internal only)
# -------------------------------------------------------------------
def _safe_normalize(value: float, reference_series, lo: Optional[float] = None, hi: Optional[float] = None) -> float:
    """
    Normalize value to [0,1].
    - If reference_series provided → percentile normalization.
    - Else fallback to fixed-range normalization.
    """
    try:
        if reference_series is not None:
            return normalize_pct(value, reference_series)
    except Exception:
        logger.debug("Percentile normalization failed → fallback.")

    if lo is not None and hi is not None and hi > lo:
        return normalize_fixed(value, lo, hi)

    return 0.0


# -------------------------------------------------------------------
# Payload JSON hasil grading
# -------------------------------------------------------------------
def _build_result_payload(db_record: GradingResult) -> Dict[str, Any]:
    """Create JSON-serializable result payload from DB model."""
    return {
        "id": db_record.id,
        "filename": db_record.filename,
        "length_cm": db_record.length_cm,
        "diameter_cm": db_record.diameter_cm,
        "weight_est_g": db_record.weight_est_g,
        "weight_actual_g": db_record.weight_actual_g,
        "ratio": db_record.ratio,
        "fuzzy_score": float(db_record.fuzzy_score) if db_record.fuzzy_score is not None else None,
        "grade_by_weight": db_record.grade_by_weight,
        "final_grade": db_record.final_grade,
    }

# -------------------------------------------------------------------
# Wrapper untuk kompatibilitas lama
# -------------------------------------------------------------------
def process_grading(
    image_bgr,
    reference_df,
    filename,
    db,
    publish_mqtt=True,
    fuzzy_fallback_on_invalid_weight=True,
    weight_actual_g=None
):
    """
    Wrapper agar kode lama yang memanggil 'process_grading'
    tetap bekerja dengan fungsi baru 'process_image'.
    """
    return process_image(
        image_bgr=image_bgr,
        reference_df=reference_df,
        filename=filename,
        db=db,
        publish_mqtt=publish_mqtt,
        fuzzy_fallback_on_invalid_weight=fuzzy_fallback_on_invalid_weight,
        weight_actual_g=weight_actual_g
    )

# -------------------------------------------------------------------
# PROSES UTAMA: Grading
# -------------------------------------------------------------------
def process_image(
    image_bgr: np.ndarray,
    reference_df,
    filename: str,
    db: Session,
    publish_mqtt: bool = True,
    fuzzy_fallback_on_invalid_weight: bool = True,
    weight_actual_g: Optional[float] = None
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Process a single image: PCV → feature extraction → normalization → fuzzy → grade → DB → MQTT.

    Args:
      - image_bgr: BGR image array
      - reference_df: pandas DataFrame with reference columns for percentile normalization
      - filename: original filename
      - db: SQLAlchemy Session
      - publish_mqtt: whether to publish result to MQTT
      - fuzzy_fallback_on_invalid_weight: if True and no valid weight -> use fuzzy thresholds
      - weight_actual_g: optional weight read from loadcell (grams). If provided, used as primary for grade_by_weight.

    Returns:
      (result_dict, error_message). error_message=None on success.
    """

    # 1. Preprocess to HSV
    hsv = preprocess_image(image_bgr)

    # 2. Segment to obtain fruit mask
    segmented, mask = segment_image(hsv)

    # 3. Extract visual features
    # extract_features returns (length_cm, diameter_cm, weight_est_g, ratio)
    length_cm, diameter_cm, weight_est_g, ratio = extract_features(segmented, mask)

    # 4. Normalization (only for fuzzy computation, not stored)
    length_norm = _safe_normalize(
        length_cm,
        reference_df.get("length_cm") if hasattr(reference_df, "get") else None,
        lo=5.0, hi=18.0
    )
    diameter_norm = _safe_normalize(
        diameter_cm,
        reference_df.get("diameter_cm") if hasattr(reference_df, "get") else None,
        lo=3.0, hi=12.0
    )
    weight_norm = _safe_normalize(
        weight_est_g,
        reference_df.get("weight_est_g") if hasattr(reference_df, "get") else None,
        lo=150.0, hi=650.0
    )

    # ratio reference
    ratio_series = None
    try:
        if hasattr(reference_df, "get") and ("ratio" in reference_df.columns):
            ratio_series = reference_df["ratio"]
        elif hasattr(reference_df, "get") and ("length_cm" in reference_df.columns and "diameter_cm" in reference_df.columns):
            ratio_series = reference_df["length_cm"] / (reference_df["diameter_cm"] + 1e-9)
    except Exception:
        ratio_series = None

    ratio_norm = _safe_normalize(ratio, ratio_series, lo=1.0, hi=1.8)

    # 5. Fuzzy score (computed from normalized inputs)
    try:
        fuzzy_score = compute_fuzzy_score(length_norm, diameter_norm, weight_norm, ratio_norm)
    except Exception:
        logger.exception("Fuzzy computation failed.")
        fuzzy_score = 0.0

    # 6. Determine weight-based grade:
    # Prefer actual weight from sensor if provided; fallback to estimated weight.
    primary_weight_for_grade = None
    if weight_actual_g is not None:
        try:
            primary_weight_for_grade = float(weight_actual_g)
        except Exception:
            primary_weight_for_grade = None

    if primary_weight_for_grade is None:
        primary_weight_for_grade = weight_est_g

    grade_by_weight = grade_from_weight(primary_weight_for_grade)

    # optional fallback: if primary weight invalid use fuzzy_score thresholds
    final_grade = grade_by_weight
    if (primary_weight_for_grade is None or primary_weight_for_grade <= 0) and fuzzy_fallback_on_invalid_weight:
        if fuzzy_score >= 70:
            final_grade = "A"
        elif fuzzy_score >= 45:
            final_grade = "B"
        else:
            final_grade = "C"

    # 7. Persist to DB
    try:
        db_record = GradingResult(
            filename=filename,
            length_cm=length_cm,
            diameter_cm=diameter_cm,
            weight_est_g=weight_est_g,
            weight_actual_g=weight_actual_g,
            ratio=ratio,
            fuzzy_score=float(fuzzy_score),
            grade_by_weight=grade_by_weight,
            final_grade=final_grade
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

    except Exception as e:
        logger.exception("DB write failed.")
        try:
            db.rollback()
        except Exception:
            logger.exception("DB rollback failed.")
        return {}, f"DB error: {e}"

    result_payload = _build_result_payload(db_record)

    # 8. MQTT publish (best effort)
    if publish_mqtt:
        try:
            mqtt_publish("grading/result", result_payload)
        except Exception:
            logger.exception("MQTT publish failed (non-fatal).")

    # 9. Return success
    return result_payload, None
