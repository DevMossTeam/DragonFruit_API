# models/schemas.py

from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Optional


# ----------------------------
# CREATE (input dari program)
# ----------------------------
class GradingResultCreate(BaseModel):
    filename: str

    # PCV features
    length_cm: Optional[float] = None
    diameter_cm: Optional[float] = None
    weight_est_g: Optional[float] = None
    ratio: Optional[float] = None

    # berat aktual (optional)
    weight_actual_g: Optional[float] = None

    # Fuzzy result
    fuzzy_score: Optional[float] = None

    # Grading
    grade_by_weight: Optional[str] = None
    final_grade: Optional[str] = None
    tanggal: datetime 


# ----------------------------
# RESPONSE (kembalian dari DB)
# ----------------------------
class GradingResultResponse(GradingResultCreate):
    id: UUID

    class Config:
        orm_mode = True
