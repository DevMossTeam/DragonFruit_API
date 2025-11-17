# models/schemas.py

from pydantic import BaseModel
from uuid import UUID

class GradingResultCreate(BaseModel):
    filename: str

    area_cm2: float
    width_cm: float
    height_cm: float
    weight_est_g: float
    texture_score: float
    hue_mean: float

    area_norm: float
    weight_norm: float
    texture_norm: float
    hue_norm: float

    fuzzy_score: float
    fuzzy_grade_label: str

    grade_by_weight: str
    final_grade: str


class GradingResultResponse(GradingResultCreate):
    id: UUID   # ← sudah bukan int lagi

    class Config:
        from_attributes = True   # pengganti orm_mode=True di Pydantic v2
