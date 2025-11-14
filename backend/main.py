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

@app.post("/test-send-grade")
async def test_send_grade():
    import json
    current_grade = mqtt.dragonFruitGrade

    if current_grade is None:
        return {"error": "No grade available. Please send weight data first via MQTT."}

    payload = {"grade": current_grade}
    print(f"📤 Publishing to {mqtt.GRADE_TOPIC}: {json.dumps(payload)}")
    mqtt.client.publish(mqtt.GRADE_TOPIC, json.dumps(payload))
    return {
        "message": f"Current grade '{current_grade}' republished to {mqtt.GRADE_TOPIC}",
        "grade": current_grade
    }

@app.get("/current-grade")
async def current_grade():
    return {"current_grade": mqtt.dragonFruitGrade}

@app.get("/current-weight")
async def current_weight():
    return {"current_weight": mqtt.dragonFruitWeight}

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