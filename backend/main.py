# backend/main.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from pydantic import BaseModel
import re

from core.database import engine
import core.mqtt as mqtt

# Import session logic directly (since you want everything in main.py)
from auth.session import get_session
from controllers.UserController import get_user_by_uid

# Routers
from routes.grading_routes import router as grading_router
from routes.device_routes import router as device_router
from routes.camera_routes import router as camera_router

from routes.user import router as user_router
from routes.auth import router as auth_router

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
# STARTUP: SHOW LOCAL IP ADDRESS
# ==========================
def get_local_ip():
    """Get the local IP address used for Wi-Fi (en0) on macOS."""
    try:
        # Create a dummy connection to get the outbound interface IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        return ip
    except Exception:
        # Fallback: try to get en0 IP explicitly (macOS Wi-Fi)
        try:
            ip = os.popen("ipconfig getifaddr en0 2>/dev/null").read().strip()
            if ip:
                return ip
            # Try en1 (in case of USB/Ethernet or older Macs)
            ip = os.popen("ipconfig getifaddr en1 2>/dev/null").read().strip()
            return ip if ip else "127.0.0.1"
        except Exception:
            return "127.0.0.1"

# ==========================
# MQTT STARTUP
# ==========================
@app.on_event("startup")
async def startup_event():
    print("🚀 Initializing MQTT client...")
    mqtt.init_mqtt()

# ==========================
# MQTT Routes
# ==========================
class GradeRequest(BaseModel):
    grade: str

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
# ROUTERS (no changes needed!)
# ==========================
app.include_router(auth_router)
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(grading_router, prefix="/grading", tags=["Grading"])
app.include_router(device_router, prefix="/device", tags=["Device / IoT"])
app.include_router(camera_router, prefix="/camera", tags=["Camera"])

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
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
        pg_version = version.split(" ")[1]
        return {
            "status": "ok",
            "database": f"PostgreSQL {pg_version}"
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}