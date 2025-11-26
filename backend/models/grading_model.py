# models/grading_model.py

from sqlalchemy import Column, String, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base


class GradingResult(Base):
    __tablename__ = "grading_results"

    # Primary key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    # Metadata
    filename = Column(String, nullable=False)

    # PCV features (sesuai extract_features di main.py)
    length_cm = Column(Float)       # max(w_box, h_box) * cm_per_pixel * 0.9
    diameter_cm = Column(Float)     # min(w_box, h_box) * cm_per_pixel * 0.9
    weight_est_g = Column(Float)    # estimasi berat dari citra (gram)
    ratio = Column(Float)           # length_cm / diameter_cm

    # Berat aktual dari sensor (opsional)
    weight_actual_g = Column(Float)

    # Normalized features (percentile or fixed-range normalization)
    length_norm = Column(Float)
    diameter_norm = Column(Float)
    weight_norm = Column(Float)
    ratio_norm = Column(Float)

    # Fuzzy result (score-only)
    fuzzy_score = Column(Float)

    # Weight-based grade (deterministic thresholds)
    grade_by_weight = Column(String)

    # Final decision (weight determines final grade; fuzzy for reporting)
    final_grade = Column(String)
