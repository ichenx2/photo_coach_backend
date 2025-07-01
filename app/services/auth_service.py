# 登入驗證、token 驗證、用戶管理等
from app.db.user_crud import get_user_by_username, create_user, get_user_by_email, get_user_by_id
from app.utils.token_utils import create_access_token, verify_token
from app.db.database import get_db
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from app.schemas.user_schema import UserCreate, UserLogin
from app.models.user import User

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(db, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = create_user(db, user.username, user.email, hashed_password)
    return create_access_token({"sub": new_user.username})

def authenticate_user(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return None
    return create_access_token({"sub": db_user.username})

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)