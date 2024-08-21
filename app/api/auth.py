import sys
sys.path.append('./')
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.operations.user_repo import *
from passlib.context import CryptContext
from app.schemas.user_schema import *
import jwt

router = APIRouter(prefix="/auth")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "A_VERY_SECRET_KEY" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register", tags=["auth"])
def register(user_data: UserCreate):

    existing_user = get_user_by_handle(user_data.handle)
    if existing_user:
        raise HTTPException(status_code=400, detail="Handle already registered")
    
    # Now check if email exists
    existing_user = get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered") 

    # Now check if username exists
    existing_user = get_user_by_username(user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    
    hashed_password = pwd_context.hash(user_data.password)
    
    user = create_user(user_data, hashed_password)
    
    return {"message": "User registered successfully", "user": user}

@router.post("/login", tags=["auth"])
def login(user_data: UserLogin):
    user = get_user_by_username(user_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid Username")
    
    if not pwd_context.verify(user_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid password")

    user = {
        "username": user.username,
        "email": user.email,
        "handle": user.handle,
        "vjudge_handle": user.vjudge_handle,
        "is_admin": user.is_admin
    }

    token = jwt.encode(user, SECRET_KEY, algorithm=ALGORITHM)

    return {"message": "Login successful", "user": user, "token": token}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Dependency to decode and verify JWT
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=400, detail="Invalid Token")

# Verify endpoint
@router.get("/verify", tags=["auth"])
def verify_user(current_user: dict = Depends(get_current_user)):
    return {"user": current_user}