# routes/users.py
from fastapi import APIRouter, HTTPException
from models.User import UserCreate, UserUpdate, UserResponse
from controllers.UserController import (
    get_all_users,
    get_user_by_uid,
    create_user,
    update_user,
    delete_user
)

router = APIRouter()

@router.get("/", response_model=dict)
async def read_users():
    return get_all_users()

@router.get("/{uid}", response_model=UserResponse)
async def read_user(uid: str):
    return get_user_by_uid(uid)

@router.post("/", response_model=UserResponse)
async def create_new_user(user: UserCreate):
    return create_user(user.username, user.email, user.password)

@router.put("/{uid}", response_model=UserResponse)
async def update_existing_user(uid: str, user: UserUpdate):
    return update_user(
        uid=uid,
        username=user.username,
        email=user.email,
        password=user.password
    )

@router.delete("/{uid}")
async def delete_existing_user(uid: str):
    return delete_user(uid)