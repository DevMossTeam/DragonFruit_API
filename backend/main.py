from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from database import engine

# Routers
from routes.user import router as users_router
from auth.login import router as auth_router
from auth.api_login import router as api_auth_router

# MQTT
import mqtt

app = FastAPI()

# CORS
origins = [
    "http://localhost:8080",
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup: initialize MQTT
@app.on_event("startup")
async def startup_event():
    print("🚀 Starting MQTT client...")
    mqtt.init_mqtt()

from pydantic import BaseModel

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

# Health & root
@app.get("/")
async def root():
    return {"message": "Dragon Fruit API"}

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "version": version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")

# Routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_auth_router, prefix="/api/auth", tags=["auth"])