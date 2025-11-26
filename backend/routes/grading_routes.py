# routes/grading_routes.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
import numpy as np
import cv2
import pandas as pd
from sqlalchemy.orm import Session
import os
import logging

from core.database import get_db
from services.grading_service import process_image
from models.schemas import GradingResultResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# ============================================================
# PATH CSV HARUS SAMA DENGAN DATASET FINAL
# ============================================================
CSV_PATH = r"E:\DragonEye\dataset\graded_features.csv"

# Load CSV saat startup modul
reference_df = None
try:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Dataset CSV tidak ditemukan di: {CSV_PATH}")

    reference_df = pd.read_csv(CSV_PATH)

    # Hilangkan spasi di nama kolom jika ada
    reference_df.columns = reference_df.columns.str.strip()

    logger.info(f"Reference CSV loaded successfully: {CSV_PATH} ({len(reference_df)} rows)")

except Exception as e:
    logger.exception("Gagal memuat reference CSV saat startup.")
    reference_df = None


# =====================================================================
# ENDPOINT: /grade-image
# =====================================================================
@router.post("/grade-image", response_model=GradingResultResponse)
async def grade_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Menerima upload gambar, menjalankan proses grading (PCV + normalisasi +
    fuzzy + DB insert + MQTT publish), dan mengembalikan hasil grading.
    """

    # 1. Cek reference CSV
    if reference_df is None:
        logger.error("Reference dataset tidak tersedia.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Reference dataset not loaded on server. Contact admin."
        )

    # 2. Decode gambar
    try:
        img_bytes = await file.read()

        if not img_bytes:
            raise ValueError("File upload kosong.")

        img_arr = np.frombuffer(img_bytes, np.uint8)
        img_np = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)

        if img_np is None:
            raise ValueError("File bukan gambar valid atau format tidak didukung.")

    except ValueError as ve:
        logger.warning(f"Upload error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception:
        logger.exception("Error saat membaca file upload.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to read uploaded image."
        )

    # 3. Proses grading
    try:
        result, err_msg = process_image(
            image_bgr=img_np,
            reference_df=reference_df,
            filename=file.filename,
            db=db,
            publish_mqtt=True,                 # MQTT aktif
            fuzzy_fallback_on_invalid_weight=True
        )
    except Exception:
        logger.exception("Error tak terduga saat proses grading.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal processing error."
        )

    # 4. Jika ada error di processing
    if err_msg:
        logger.error(f"Processing failed: {err_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=err_msg
        )

    # 5. Return result (divalidasi oleh Pydantic)
    return result
