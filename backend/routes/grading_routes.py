# routes/grading_routes.py

from fastapi import APIRouter, UploadFile, File, Depends
import numpy as np
import cv2
import pandas as pd
from sqlalchemy.orm import Session
import os

from core.database import get_db
from services.grading_service import process_image
from models.schemas import GradingResultResponse

router = APIRouter()

# ============================================
# PERBAIKAN PATH CSV (gunakan path absolut)
# ============================================
CSV_PATH = r"/Users/sartriaardianthauno/Desktop/project semster 5/DragonFruit_Grading/dataset/features.csv"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Dataset CSV tidak ditemukan di: {CSV_PATH}")

reference_df = pd.read_csv(CSV_PATH)


@router.post("/grade-image", response_model=GradingResultResponse)
async def grade_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # baca file
    img_bytes = await file.read()
    img_np = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)

    # proses citra + simpan otomatis ke DB
    result = process_image(
        image_np=img_np,
        reference_df=reference_df,
        filename=file.filename,
        db=db
    )

    return result
