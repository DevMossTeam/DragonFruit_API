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

# ============================================
# CONFIG: path ke CSV reference (sesuaikan)
# ============================================
CSV_PATH = r"E:\DragonEye\dataset\features.csv"

# Coba load CSV sekali saat module import (startup)
reference_df = None
try:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(f"Dataset CSV tidak ditemukan di: {CSV_PATH}")
    reference_df = pd.read_csv(CSV_PATH)
    # strip column names spasi jika ada
    reference_df.columns = reference_df.columns.str.strip()
    logger.info(f"Reference CSV loaded: {CSV_PATH} ({len(reference_df)} rows)")
except Exception as e:
    # keep reference_df as None and raise on use
    logger.exception("Gagal memuat reference CSV pada startup.")
    reference_df = None


@router.post("/grade-image", response_model=GradingResultResponse)
async def grade_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint untuk menerima upload gambar, melakukan grading (PCV + fuzzy)
    dan menyimpan hasilnya ke database.
    """

    # 1) Validasi reference dataframe ada
    if reference_df is None:
        logger.error("Reference CSV belum tersedia. Tidak dapat memproses grading.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Reference dataset not available on server. Contact admin.")

    # 2) Baca file upload sebagai image numpy (BGR)
    try:
        img_bytes = await file.read()
        if not img_bytes:
            raise ValueError("Uploaded file is empty.")
        img_arr = np.frombuffer(img_bytes, np.uint8)
        img_np = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
        if img_np is None:
            raise ValueError("File bukan gambar yang valid atau format tidak didukung.")
    except ValueError as ve:
        logger.warning("Invalid upload: %s", ve)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        logger.exception("Error saat membaca file upload.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Failed to read uploaded image.")

    # 3) Proses citra (synchronous). process_image => (result_dict, err_msg)
    try:
        result, err = process_image(
            image_bgr=img_np,
            reference_df=reference_df,
            filename=file.filename,
            db=db,
            publish_mqtt=True,
            fuzzy_fallback_on_invalid_weight=True
        )
    except Exception as e:
        logger.exception("Unexpected error during grading process.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Internal processing error.")

    # 4) Check result / error
    if err:
        logger.error("Processing failed: %s", err)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err)

    # 5) Return hasil (Pydantic model akan memvalidasi structure)
    return result
