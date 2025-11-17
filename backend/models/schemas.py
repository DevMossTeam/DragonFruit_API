from pydantic import BaseModel

class GradingInput(BaseModel):
    image_base64: str

class GradingOutput(BaseModel):
    final_grade: str
    area_cm2: float
    weight_est_g: float
    texture_score: float
    hue_mean: float
