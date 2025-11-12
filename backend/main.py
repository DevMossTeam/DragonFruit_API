from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlalchemy import text  
from routes.user import router as users_router
from auth.login import router as auth_router 
from auth.api_login import router as api_auth_router  

app = FastAPI()

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

@app.get("/")
async def root():
    return {"message": "Dragon Fruit Api"}

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

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(api_auth_router, prefix="/api/auth", tags=["auth"])


# @app.get("/users")
# async def get_all_users():
#     """Fetch all users from the database"""
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text('SELECT uid, username, email FROM public."user"'))
            
#             users = []
#             for row in result:
#                 users.append({
#                     "uid": row.uid,
#                     "username": row.username,
#                     "email": row.email
#                 })
            
#             return {
#                 "users": users,
#                 "count": len(users)
#             }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500,
#             detail=f"Failed to fetch users: {str(e)}"
#         )