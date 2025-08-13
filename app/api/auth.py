from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, Token
from app.services.auth_service import register_user, authenticate_user, get_current_user
from app.db.database import get_db
from app.models.user import User
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/register", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    token = register_user(user, db)
    if not token:
        raise HTTPException(status_code=400, detail="Registration failed")
    return token

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(user, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token

