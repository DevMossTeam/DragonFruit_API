from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from PIL import Image
import io, random, os

router = APIRouter()

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze", response_model=schemas.GradingOut)
async def analyze_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(image_path, "wb") as f:
        f.write(contents)

    # Simulasi AI
    Image.open(io.BytesIO(contents))
    grade = random.choice(["A", "B", "C", "BS"])
    confidence = round(random.uniform(0.8, 0.99), 2)

    result = models.GradingResult(
        image_name=file.filename,
        grade=grade,
        confidence=confidence,
    )
    db.add(result)
    db.commit()
    db.refresh(result)

    return result

@router.get("/history", response_model=list[schemas.GradingOut])
def get_history(db: Session = Depends(get_db)):
    return db.query(models.GradingResult).order_by(models.GradingResult.timestamp.desc()).all()
