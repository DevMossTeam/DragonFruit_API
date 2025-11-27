# backend/main.py
import os
import socket
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from fastapi import APIRouter
from sqlalchemy import text

load_dotenv()

app = FastAPI(title="Dragon Fruit Grading API")

API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("❌ API_KEY is not set in .env file!")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="❌ Invalid or missing API key",
            headers={"WWW-Authenticate": "APIKey"},
        )
    return api_key

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

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        return ip
    except Exception:
        try:
            ip = os.popen("ipconfig getifaddr en0 2>/dev/null").read().strip()
            if ip:
                return ip
            ip = os.popen("ipconfig getifaddr en1 2>/dev/null").read().strip()
            return ip if ip else "127.0.0.1"
        except Exception:
            return "127.0.0.1"

@app.on_event("startup")
async def startup_event():
    port = os.getenv("PORT", "8000")
    local_ip = get_local_ip()
    print(f"\n🌍 Your API is accessible on the local network at:")
    print(f"   http://{local_ip}:{port}")
    print(f"   🔑 Access requires header: X-API-Key: {API_KEY}")
    print(f"   (Local: http://127.0.0.1:{port})\n")

protected_router = APIRouter(dependencies=[Depends(verify_api_key)])

@protected_router.get("/")
async def root():
    return {"message": "Dragon Fruit Grading API is running"}

@protected_router.get("/health")
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

protected_router.include_router(auth_router)
protected_router.include_router(user_router, prefix="/users", tags=["Users"])
protected_router.include_router(grading_router, prefix="/grading", tags=["Grading"])
protected_router.include_router(device_router, prefix="/device", tags=["Device / IoT"])
protected_router.include_router(camera_router, prefix="/camera", tags=["Camera"])

app.include_router(protected_router)