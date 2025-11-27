# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from core.database import engine
from core.mqtt import init_mqtt, publish_grade, mqttGrade, mqttWeight, GRADE_TOPIC
from routes.device_routes import router as device_router

# Request model
from pydantic import BaseModel

class GradeRequest(BaseModel):
    grade: str


app = FastAPI(title="Dragon Fruit Grading API")


# ==========================
# CORS
# ==========================
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================
# MQTT STARTUP
# ==========================
@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing MQTT client...")
    init_mqtt()


# ==========================
# MQTT MANUAL CONTROL API
# ==========================
@app.post("/set-grade")
async def set_grade(req: GradeRequest):
    publish_grade(req.grade)
    return {
        "message": f"Grade set to '{req.grade}'",
        "grade": req.grade
    }


@app.post("/test-send-grade")
async def test_send_grade():
    if mqttGrade is None:
        return {"error": "No grade available. Please use /set-grade first."}

    publish_grade(mqttGrade)
    return {
        "message": f"Current grade '{mqttGrade}' republished to {GRADE_TOPIC}",
        "grade": mqttGrade
    }


@app.get("/current-grade")
async def current_grade():
    return {"current_grade": mqttGrade}


@app.get("/current-weight")
async def current_weight():
    return {"current_weight": mqttWeight}


# ==========================
# ROUTERS
# ==========================
from routes.grading_routes import router as grading_router
from routes.camera_routes import router as camera_router

app.include_router(grading_router, prefix="/grading", tags=["Grading"])
app.include_router(camera_router, prefix="/camera", tags=["Camera"])
app.include_router(device_router, prefix="/device", tags=["Device / IoT"])


# ==========================
# ROOT & HEALTH
# ==========================
@app.get("/")
async def root():
    return {"message": "Dragon Fruit Grading API is running"}


@app.get("/health")
async def health():
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version();")).fetchone()[0]
        return {"status": "ok", "database": f"SQLite {version}"}

    except Exception as e:
        return {"status": "error", "detail": str(e)}
