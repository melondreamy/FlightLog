from fastapi import APIRouter, Depends, HTTPException, status
from sqlite3 import Connection
import json
from typing import List

from app.database import get_connection
from app.routers.auth import get_current_user, get_db
from app.schemas import UserResponse, UserCreate, WelcomeConfig, PasswordReset
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
@router.get("/welcome-config", response_model=WelcomeConfig)
async def get_welcome_config(db: Connection = Depends(get_db)):
    """Retrieve global welcome page configuration."""
    row = db.execute("SELECT value FROM global_config WHERE key = 'welcome_page'").fetchone()
    if not row:
        return WelcomeConfig(
            title="Welcome to SkyLog",
            description="Your personal, self-hosted flight logbook.",
            features=["Secure", "Private", "Customizable"]
        )
    return json.loads(row["value"])

@router.put("/welcome-config", response_model=WelcomeConfig)
async def update_welcome_config(config: WelcomeConfig, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    """Update global welcome page configuration (Admin only)."""
    db.execute("UPDATE global_config SET value = ? WHERE key = 'welcome_page'", (config.model_dump_json(),))
    db.commit()
    return config

# Admin User Management Endpoints
@router.get("/admin/users", response_model=List[UserResponse])
async def list_users(admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    """List all users (Admin only)."""
    rows = db.execute("SELECT * FROM users").fetchall()
    return [dict(r) for r in rows]

@router.post("/admin/users", response_model=UserResponse)
async def create_user_admin(user_in: UserCreate, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    """Create a new user directly (Admin only)."""
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
async def reset_password_admin(user_id: int, reset: PasswordReset, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    """Force a password reset for a user (Admin only)."""
    hashed_password = get_password_hash(reset.new_password)
    cursor = db.execute("UPDATE users SET hashed_password = ? WHERE id = ?", (hashed_password, user_id))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}

@router.delete("/admin/users/{user_id}")
async def delete_user_admin(user_id: int, admin = Depends(get_current_admin), db: Connection = Depends(get_db)):
    """Delete a user (Admin only)."""
    if user_id == admin["id"]:
        raise HTTPException(status_code=400, detail="Cannot delete yourself")
    cursor = db.execute("DELETE FROM users WHERE id = ?", (user_id,))
    db.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "success"}
