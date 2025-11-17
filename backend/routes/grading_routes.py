from fastapi import APIRouter
from models.schemas import GradingInput, GradingOutput
from services.grading_service import process_image

router = APIRouter(prefix="/grading")

@router.post("/", response_model=GradingOutput)
def grade_fruit(data: GradingInput):
    result = process_image(data.image_base64)
    return GradingOutput(
        final_grade=result.final_grade,
        area_cm2=result.area_cm2,
        weight_est_g=result.weight_est_g,
        texture_score=result.texture_score,
        hue_mean=result.hue_mean,
    )
