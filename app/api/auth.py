from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserCreate, UserLogin, Token
from app.services.auth_service import register_user, authenticate_user
from app.db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

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

