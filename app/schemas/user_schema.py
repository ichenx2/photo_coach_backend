# 定義註冊/登入時前端傳來的格式
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class Token(BaseModel):
    access_token: str
    token_type: str