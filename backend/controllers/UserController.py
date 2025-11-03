# controllers/UserController.py
from fastapi import HTTPException
from sqlalchemy import text
from database import engine
import uuid
import bcrypt

def get_all_users():
    try:
        with engine.connect() as conn:
            result = conn.execute(text('SELECT uid, username, email FROM public."user"'))
            users = [
                {"uid": row.uid, "username": row.username, "email": row.email}
                for row in result
            ]
        return {"users": users, "count": len(users)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")
    

def get_user_by_uid(uid: str):
    try:
        with engine.connect() as conn:
            result = conn.execute(
                text('SELECT uid, username, email FROM public."user" WHERE uid = :uid'),
                {"uid": uid}
            )
            row = result.fetchone()
            if row:
                return {"uid": row.uid, "username": row.username, "email": row.email}
            else:
                raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")
    
def create_user(username: str, email: str, password: str):
    try:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_uid = str(uuid.uuid4())
        with engine.begin() as conn:
            conn.execute(
                text('INSERT INTO public."user" (uid, username, email, password) VALUES (:uid, :username, :email, :password)'),
                {"uid": new_uid, "username": username, "email": email, "password": password}
            )
        return {"uid": new_uid, "username": username, "email": email}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

def delete_user(uid: str):
    try:
        with engine.begin() as conn: 
            result = conn.execute(
                text('DELETE FROM public."user" WHERE uid = :uid'),
                {"uid": uid}
            )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
    
def update_user(uid: str, username: str = None, email: str = None, password: str = None):
    try:
        update_fields = []
        params = {"uid": uid}
        if username is not None:
            update_fields.append("username = :username")
            params["username"] = username
        if email is not None:
            update_fields.append("email = :email")
            params["email"] = email
        if password is not None:
            update_fields.append("password = :password")
            params["password"] = password
        
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        query = f'UPDATE public."user" SET {", ".join(update_fields)} WHERE uid = :uid'
        with engine.begin() as conn:  # 👈 CHANGED
            result = conn.execute(text(query), params)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found")
        
        return get_user_by_uid(uid)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")