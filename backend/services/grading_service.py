# services/grading_service.py
import logging
from typing import Any, Dict, Optional, Tuple

import numpy as np
import cv2
from sqlalchemy.orm import Session

from models.grading_model import GradingResult

# PCV utilities (single source of truth)
from services.pcv.preprocess import preprocess_image
from services.pcv.segmentation import segment_image
from services.pcv.feature_extract import extract_features
from services.pcv.normalization import normalize_pct, normalize_fixed

# Fuzzy helpers (score-only) and deterministic grade-by-weight
from services.fuzzy.mamdani import compute_fuzzy_score, grade_from_weight

# MQTT publisher (wrapped)
from services.mqtt_service import mqtt_publish

logger = logging.getLogger(__name__)


def _safe_normalize(value: float, reference_series, lo: Optional[float] = None, hi: Optional[float] = None) -> float:
    """
    Normalize value to [0,1].
    - If reference_series provided (pd.Series-like), use percentile normalization.
    - Else if lo and hi provided, use fixed range normalization.
    - Else return 0.0 as fallback.
    """
    try:
        if reference_series is not None:
            return normalize_pct(value, reference_series)
    except Exception:
        logger.debug("Percentile normalization failed, falling back to fixed range if provided.")

    if lo is not None and hi is not None and hi > lo:
        return normalize_fixed(value, lo, hi)

    return 0.0


def _build_result_payload(db_record: GradingResult) -> Dict[str, Any]:
    """Create JSON-serializable result payload from DB model."""
    return {
        "id": db_record.id,
        "filename": db_record.filename,
        "area_cm2": db_record.area_cm2,
        "length_cm": db_record.length_cm,
        "diameter_cm": db_record.diameter_cm,
        "weight_est_g": db_record.weight_est_g,
        "ratio": db_record.ratio,
        "length_norm": db_record.length_norm,
        "diameter_norm": db_record.diameter_norm,
        "weight_norm": db_record.weight_norm,
        "ratio_norm": db_record.ratio_norm,
        "fuzzy_score": float(db_record.fuzzy_score) if db_record.fuzzy_score is not None else None,
        "final_grade": db_record.final_grade,
    }


def process_image(
    image_bgr: np.ndarray,
    reference_df,
    filename: str,
    db: Session,
    publish_mqtt: bool = True,
    fuzzy_fallback_on_invalid_weight: bool = True
) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Process a single image: PCV -> feature extraction -> normalization -> fuzzy score -> grade -> save -> mqtt.

    Args:
      - image_bgr: input image (BGR numpy array)
      - reference_df: pandas DataFrame with reference columns for percentile normalization (batch)
      - filename: original filename (string)
      - db: SQLAlchemy Session (transaction handled here)
      - publish_mqtt: whether to publish result to MQTT
      - fuzzy_fallback_on_invalid_weight: if True and weight<=0, decide grade from fuzzy score

    Returns:
      (result_dict, error_message). error_message is None on success.
    """
    # 1. Preprocess (to HSV)
    hsv = preprocess_image(image_bgr)

    # 2. Segment and get mask
    segmented, mask = segment_image(hsv)

    # 3. Extract features (single source)
    # expected return: (area_cm2, width_cm, height_cm, weight_g, ratio)
    area_cm2, width_cm, height_cm, weight_g, ratio = extract_features(segmented, mask)

    # canonical length/diameter
    length_cm = max(width_cm, height_cm)
    diameter_cm = min(width_cm, height_cm)

    # 4. Normalize inputs (prefer percentile from reference_df; fallback to fixed ranges)
    # Provide sensible fixed ranges if reference_df missing columns
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
        weight_g,
        reference_df.get("weight_est_g") if hasattr(reference_df, "get") else None,
        lo=150.0, hi=650.0
    )
    # ratio reference: either column 'ratio' or compute from reference_df if present
    ratio_series = None
    try:
        if hasattr(reference_df, "get") and ("ratio" in reference_df.columns):
            ratio_series = reference_df["ratio"]
        elif hasattr(reference_df, "get") and ("length_cm" in reference_df.columns and "diameter_cm" in reference_df.columns):
            ratio_series = reference_df["length_cm"] / (reference_df["diameter_cm"] + 1e-9)
    except Exception:
        ratio_series = None

    ratio_norm = _safe_normalize(ratio, ratio_series, lo=1.0, hi=1.8)

    # 5. Compute fuzzy score (score-only). Accepts normalized inputs in [0,1]
    try:
        fuzzy_score = compute_fuzzy_score(length_norm, diameter_norm, weight_norm, ratio_norm)
    except Exception as e:
        logger.exception("Fuzzy computation failed, defaulting fuzzy_score to 0.0")
        fuzzy_score = 0.0

    # 6. Determine final grade (weight primary)
    final_grade = grade_from_weight(weight_g)
    # optional fallback: if weight invalid (<=0) use fuzzy thresholds
    if (weight_g is None or weight_g <= 0) and fuzzy_fallback_on_invalid_weight:
        if fuzzy_score >= 70:
            final_grade = "A"
        elif fuzzy_score >= 45:
            final_grade = "B"
        else:
            final_grade = "C"

    # 7. Persist to DB (transaction safe)
    db_record = None
    try:
        db_record = GradingResult(
            filename=filename,
            area_cm2=area_cm2,
            length_cm=length_cm,
            diameter_cm=diameter_cm,
            weight_est_g=weight_g,
            ratio=ratio,
            length_norm=length_norm,
            diameter_norm=diameter_norm,
            weight_norm=weight_norm,
            ratio_norm=ratio_norm,
            fuzzy_score=float(fuzzy_score),
            final_grade=final_grade
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)
    except Exception as e:
        logger.exception("DB write failed, rolling back")
        try:
            db.rollback()
        except Exception:
            logger.exception("DB rollback also failed")
        return {}, f"DB error: {e}"

    result_payload = _build_result_payload(db_record)

    # 8. Publish to MQTT (best-effort)
    if publish_mqtt:
        try:
            mqtt_publish("grading/result", result_payload)
        except Exception:
            logger.exception("MQTT publish failed (non-fatal)")

    # 9. Return result
    return result_payload, None
