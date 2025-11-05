# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import engine
from sqlalchemy import text  
from routes.user import router as users_router

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


# Root endpoint
@app.get("/")
async def root():
    return {"message": "Dragon Fruit Api"}

@app.get("/health")
async def health_check():
    """Test database connection endpoint"""
    try:
        with engine.connect() as conn:
            # Use text() for raw SQL in newer SQLAlchemy versions
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "version": version
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )
    
app.include_router(users_router, prefix="/users", tags=["users"])

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