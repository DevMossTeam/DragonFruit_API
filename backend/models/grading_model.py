from sqlalchemy import Column, Integer, String, Float
from core.database import Base

class GradingRecord(Base):
    __tablename__ = "grading"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    area_cm2 = Column(Float)
    weight_est_g = Column(Float)
    texture_score = Column(Float)
    hue_mean = Column(Float)
    final_grade = Column(String)
