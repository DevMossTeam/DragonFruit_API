from pydantic import BaseModel
from datetime import datetime

class GradingBase(BaseModel):
    image_name: str
    grade: str
    confidence: float

class GradingCreate(GradingBase):
    pass

class GradingOut(GradingBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
