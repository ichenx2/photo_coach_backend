from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user: UserCreate):
    token = register_user(user)
    if not token:
        raise HTTPException(status_code=400, detail="Registration failed")
    return token

@router.post("/login", response_model=Token)
def login(user: UserLogin):
    token = authenticate_user(user)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

