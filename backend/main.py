# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from core.database import engine
from core.mqtt import init_mqtt, publish_grade, get_mqtt_grade, get_mqtt_weight, GRADE_TOPIC

# Auth & User
from auth.session import get_session
from controllers.UserController import get_user_by_uid

# Routers
from routes.grading_routes import router as grading_router
from routes.device_routes import router as device_router
from auth.api_login import router as api_auth_router
from routes.metrics_routes import router as metrics_router

# Request model
from pydantic import BaseModel
from controllers.GradingresultController import router as gradingresult_router 

class GradeRequest(BaseModel):
    grade: str


app = FastAPI(title="Dragon Fruit Grading API")
app.include_router(gradingresult_router, prefix="/api/gradingresult", tags=["Grading Results"])
app.include_router(metrics_router, prefix="/api", tags=["Metrics"])
# ==========================
# CORS - MUST BE FIRST!
# ==========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
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

# @app.post("/test-send-grade")
# async def test_send_grade():
#     if mqttGrade is None:
#         return {"error": "No grade available. Please use /set-grade first."}
#     publish_grade(mqttGrade)
#     return {
#         "message": f"Current grade '{mqttGrade}' republished to {GRADE_TOPIC}",
#         "grade": mqttGrade
    # }

@app.get("/current-weight")
async def current_weight():
    return {"current_weight": get_mqtt_weight()}
 
@app.post("/test-send-grade")
async def test_send_grade():
    current_grade = get_mqtt_grade()
    if current_grade is None:
        return {"error": "No grade available. Please use /set-grade first."}
    publish_grade(current_grade)
    return {
        "message": f"Current grade '{current_grade}' republished to {GRADE_TOPIC}",
        "grade": current_grade
    }

@app.get("/current-grade")
async def current_grade():
    return {"current_grade": get_mqtt_grade()}


# ==========================
# ROUTERS
# ==========================
from routes.grading_routes import router as grading_router
from routes.camera_routes import router as camera_router
from routes.user import router as user_router

app.include_router(grading_router, prefix="/grading", tags=["Grading"])
app.include_router(camera_router, prefix="/camera", tags=["Camera"])
app.include_router(device_router, prefix="/device", tags=["Device / IoT"])
app.include_router(api_auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(user_router, prefix="/users", tags=["Users"])

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


@app.get("/debug/db-status")
async def debug_db_status():
    """Debug endpoint to check database and grading_results table status"""
    try:
        with engine.connect() as conn:
            # Check if table exists
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'grading_results'
                )
            """)).fetchone()
            
            table_exists = result[0] if result else False
            
            if table_exists:
                # Count records
                count_result = conn.execute(text("SELECT COUNT(*) FROM grading_results")).fetchone()
                record_count = count_result[0] if count_result else 0
                
                return {
                    "status": "ok",
                    "table_exists": True,
                    "table_name": "grading_results",
                    "record_count": record_count,
                    "message": f"Table exists with {record_count} records"
                }
            else:
                return {
                    "status": "warning",
                    "table_exists": False,
                    "table_name": "grading_results",
                    "message": "Table does not exist. Run migrations or create it."
                }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "message": "Failed to check database status"
        }
    
# ==========================
# DATABASE MIGRATIONS
# ==========================
@app.post("/debug/create-tables")
async def create_tables():
    """Create all database tables from models"""
    try:
        from core.database import Base
        Base.metadata.create_all(bind=engine)
        return {
            "status": "ok",
            "message": "All tables created successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e),
            "message": "Failed to create tables"
        }

# ==========================
# DEBUG: List all routes (optional, remove in production)
# ==========================
@app.get("/debug/routes")
def debug_routes():
    routes = [r.path for r in app.routes if hasattr(r, 'path')]
    return {"routes": sorted(routes)}