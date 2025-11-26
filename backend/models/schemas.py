# models/schemas.py

from pydantic import BaseModel
from uuid import UUID


# ----------------------------
# CREATE (input dari program)
# ----------------------------
class GradingResultCreate(BaseModel):
    filename: str

    # PCV features
    length_cm: float
    diameter_cm: float
    weight_est_g: float
    ratio: float

    # berat aktual (optional)
    weight_actual_g: float | None = None

    # Normalization
    length_norm: float
    diameter_norm: float
    weight_norm: float
    ratio_norm: float

    # Fuzzy result
    fuzzy_score: float

    # Grading
    grade_by_weight: str
    final_grade: str


# ----------------------------
# RESPONSE (kembalian dari DB)
# ----------------------------
class GradingResultResponse(GradingResultCreate):
    id: UUID

    class Config:
        from_attributes = True   # untuk ORM SQLAlchemy
