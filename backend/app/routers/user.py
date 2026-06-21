from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
import json
from typing import Any, Dict

from app.database import get_connection
from app.routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/settings", response_model=Dict[str, Any])
async def get_settings(current_user = Depends(get_current_user)):
    """Retrieve the current user's settings."""
    settings_str = current_user["settings"] or "{}"
    try:
        return json.loads(settings_str)
    except json.JSONDecodeError:
        return {}

@router.put("/settings", response_model=Dict[str, Any])
async def update_settings(settings: Dict[str, Any], current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    """Update the current user's settings."""
    settings_json = json.dumps(settings)
    db.execute("UPDATE users SET settings = ? WHERE id = ?", (settings_json, current_user["id"]))
    db.commit()
    return settings
