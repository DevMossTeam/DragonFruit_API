# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from core.database import engine
from core.mqtt import init_mqtt

# Routers
from routes.grading_routes import router as grading_router
from routes.device_routes import router as device_router
from routes.camera_routes import router as camera_router

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
# MQTT STARTUP & Routes
# ==========================
@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing MQTT client...")
    init_mqtt()


@app.post("/set-grade")
async def set_grade(req: GradeRequest):
    mqtt.publish_grade(req.grade)
    return {"message": f"Grade set to '{req.grade}'", "grade": req.grade}

@app.post("/test-send-grade")
async def test_send_grade():
    current_grade = mqtt.mqttGrade
    if current_grade is None:
        return {"error": "No grade available. Please use /set-grade first."}
    mqtt.publish_grade(current_grade)
    return {
        "message": f"Current grade '{current_grade}' republished to {mqtt.GRADE_TOPIC}",
        "grade": current_grade
    }

@app.get("/current-grade")
async def current_grade():
    return {"current_grade": mqtt.mqttGrade}

@app.get("/current-weight")
async def current_weight():
    return {"current_weight": mqtt.mqttWeight}

# ==========================
# ROUTERS
# ==========================
app.include_router(grading_router, prefix="/grading", tags=["Grading"])
app.include_router(device_router, prefix="/device", tags=["Device / IoT"])
app.include_router(camera_router, prefix="/camera", tags=["Camera"])


# ==========================
# ROOT ENDPOINT
# ==========================
@app.get("/")
async def root():
    return {"message": "Dragon Fruit Grading API is running"}


# ==========================
# HEALTH CHECK (SQLAlchemy 2.0 FIX)
# ==========================
@app.get("/health")
async def health():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT sqlite_version();"))
            version = result.fetchone()[0]

        return {
            "status": "ok",
            "database": f"SQLite {version}"
        }

    except Exception as e:
        return {"status": "error", "detail": str(e)}
