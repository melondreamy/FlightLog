from fastapi import APIRouter, Depends, HTTPException, status
from sqlite3 import Connection
import json
from typing import List

from app.database import get_connection
from app.routers.auth import get_current_user, get_db
from app.schemas import UserResponse, UserCreate
from app.auth_utils import get_password_hash

router = APIRouter()

async def get_current_admin(current_user = Depends(get_current_user)):
    if not current_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user does not have enough privileges"
        )
    return current_user

# Welcome Config Endpoints
@router.get("/welcome-config")
async def get_welcome_config(db: Connection = Depends(get_db)):
    row = db.execute("SELECT value FROM global_config WHERE key = 'welcome_page'").fetchone()
    if not row:
        return {}
    return json.loads(row["value"])

@router.put("/welcome-config")
async def update_welcome_config(config: dict, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    db.execute("UPDATE global_config SET value = ? WHERE key = 'welcome_page'", (json.dumps(config),))
    db.commit()
    return config

# Admin User Management Endpoints
@router.get("/admin/users", response_model=List[UserResponse])
async def list_users(admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    rows = db.execute("SELECT * FROM users").fetchall()
    return [dict(r) for r in rows]

@router.post("/admin/users", response_model=UserResponse)
async def create_user_admin(user_in: UserCreate, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    hashed_password = get_password_hash(user_in.password)
    try:
        cursor = db.execute(
            "INSERT INTO users (username, email, hashed_password, full_name) VALUES (?, ?, ?, ?)",
            (user_in.username, user_in.email, hashed_password, user_in.full_name)
        )
        user_id = cursor.lastrowid
        db.execute("INSERT INTO welcome_config (user_id) VALUES (?)", (user_id,))
        db.commit()
        new_user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/admin/users/{user_id}/reset-password")
async def reset_password_admin(user_id: int, new_password: str, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    hashed_password = get_password_hash(new_password)
    db.execute("UPDATE users SET hashed_password = ? WHERE id = ?", (hashed_password, user_id))
    db.commit()
    return {"status": "success"}

@router.delete("/admin/users/{user_id}")
async def delete_user_admin(user_id: int, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    if user_id == admin["id"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    return {"status": "success"}
