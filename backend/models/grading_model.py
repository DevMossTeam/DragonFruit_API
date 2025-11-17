# models/grading_model.py

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base

class GradingResult(Base):
    __tablename__ = "grading_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    filename = Column(String, nullable=False)

    # fitur PCV
    area_cm2 = Column(Float)
    width_cm = Column(Float)
    height_cm = Column(Float)
    weight_est_g = Column(Float)
    texture_score = Column(Float)
    hue_mean = Column(Float)

    # normalisasi
    area_norm = Column(Float)
    weight_norm = Column(Float)
    texture_norm = Column(Float)
    hue_norm = Column(Float)

    # fuzzy
    fuzzy_score = Column(Float)
    fuzzy_grade_label = Column(String)

    # berat
    grade_by_weight = Column(String)

    # final gabungan
    final_grade = Column(String)
