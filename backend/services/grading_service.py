import base64
import numpy as np
import cv2
from core.database import SessionLocal
from models.grading_model import GradingRecord
from services.pcv.preprocess import preprocess
from services.pcv.segmentation import segment
from services.pcv.feature_extract import extract_features
from services.fuzzy.mamdani import fuzzy_grade

def decode_image(b64):
    data = base64.b64decode(b64)
    img_arr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

def process_image(base64_img):
    db = SessionLocal()

    img = decode_image(base64_img)
    hsv = preprocess(img)
    segmented, mask = segment(hsv)
    area, w, h, weight, texture, hue = extract_features(segmented, mask)

    # Normalisasi
    area_norm = min(area / 200, 1.0)
    weight_norm = min(weight / 500, 1.0)
    texture_norm = texture
    hue_norm = hue

    fuzzy_label = fuzzy_grade(area_norm, weight_norm, texture_norm, hue_norm)

    record = GradingRecord(
        filename="stream",
        area_cm2=area,
        weight_est_g=weight,
        texture_score=texture,
        hue_mean=hue,
        final_grade=fuzzy_label
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record
