from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
import json

from app.database import get_connection
from app.routers.auth import get_current_user, get_db

router = APIRouter()

@router.get("/settings")
async def get_settings(current_user = Depends(get_current_user)):
    settings_str = current_user["settings"] or "{}"
    return json.loads(settings_str)

@router.put("/settings")
async def update_settings(settings: dict, current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    settings_json = json.dumps(settings)
    db.execute("UPDATE users SET settings = ? WHERE id = ?", (settings_json, current_user["id"]))
    db.commit()
    return settings
