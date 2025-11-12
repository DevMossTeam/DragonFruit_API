# auth/api_login.py

from fastapi import APIRouter, HTTPException, Request, Response, status
from pydantic import BaseModel
from controllers.UserController import get_user_by_username_or_email  # ← NEW FUNCTION NAME
from auth.security import verify_password
from auth.session import create_session

print("🔥 API Login Router Loaded!")

router = APIRouter(tags=["auth"])

class LoginRequest(BaseModel):
    username_or_email: str  # Accepts either username or email
    password: str           # Required

class UserResponse(BaseModel):
    uid: str
    username: str
    email: str

@router.post("/login")
async def api_login(
    response: Response,
    request: LoginRequest
):
    user = get_user_by_username_or_email(request.username_or_email)
    if not user or not verify_password(request.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    session_id = create_session(user["uid"])
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=3600
    )
    
    return {
        "message": "Logged in successfully",
        "user": UserResponse(
            uid=user["uid"],
            username=user["username"],
            email=user["email"]
        )
    }

@router.post("/logout")
async def api_logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if session_id:
        from auth.session import delete_session
        delete_session(session_id)
    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}