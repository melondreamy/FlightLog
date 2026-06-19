from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlite3 import Connection
from typing import Optional

from app.database import get_connection
from app.schemas import UserCreate, UserResponse, UserMeResponse, Token, LoginRequest
from app.auth_utils import verify_password, get_password_hash, create_access_token, ALGORITHM, SECRET_KEY

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_db():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Connection = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: Connection = Depends(get_db)):
    # Check if user already exists
    existing_user = db.execute(
        "SELECT id FROM users WHERE username = ? OR email = ?", 
        (user_in.username, user_in.email)
    ).fetchone()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Check if this is the first user
    user_count = db.execute("SELECT COUNT(*) as count FROM users").fetchone()["count"]
    is_admin = 1 if user_count == 0 else 0
    
    hashed_password = get_password_hash(user_in.password)
    
    try:
        cursor = db.execute(
            """INSERT INTO users (username, email, hashed_password, is_admin, full_name) 
               VALUES (?, ?, ?, ?, ?)""",
            (user_in.username, user_in.email, hashed_password, is_admin, user_in.full_name)
        )
        user_id = cursor.lastrowid
        
        # Create welcome config
        db.execute(
            "INSERT INTO welcome_config (user_id, show_welcome, setup_complete) VALUES (?, ?, ?)",
            (user_id, 1, 0)
        )
        
        db.commit()
        
        new_user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login(login_data: LoginRequest, db: Connection = Depends(get_db)):
    user = db.execute("SELECT * FROM users WHERE username = ?", (login_data.username,)).fetchone()
    
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserMeResponse)
async def read_users_me(current_user = Depends(get_current_user), db: Connection = Depends(get_db)):
    # Join with welcome_config
    config = db.execute(
        "SELECT show_welcome, setup_complete FROM welcome_config WHERE user_id = ?", 
        (current_user["id"],)
    ).fetchone()
    
    user_data = dict(current_user)
    if config:
        user_data.update(dict(config))
    else:
        user_data["show_welcome"] = True
        user_data["setup_complete"] = False
        
    return user_data
