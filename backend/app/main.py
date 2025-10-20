from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from app.routes import grading, iot

app = FastAPI(title="DragonEye API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ubah ke domain frontend di produksi
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(grading.router, prefix="/api/grading", tags=["Grading"])
app.include_router(iot.router, prefix="/api/iot", tags=["IoT"])

@app.get("/")
def read_root():
    return {"message": "Welcome to DragonEye API"}
