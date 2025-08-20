import os
from fastapi import FastAPI
from app.api import ping, auth, analyze
from app.api import task
from fastapi.staticfiles import StaticFiles
from app.db.database import engine
from app.models.user import Base
# 導入所有模型以確保它們被註冊到 SQLAlchemy
from app.models import User, Task, SubTask, Photo
from app.api.ai_chat import router as ai_router
from app.api.pexels import router as moodboard_router
from app.api import nearby
from app.api.photo import router as photo_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 往上一層到專案根目錄
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/analyze", tags=["Image Analysis"])
app.include_router(task.router, prefix="/tasks", tags=["Tasks"])
app.include_router(photo_router, prefix="/photo", tags=["Photo"])
app.include_router(ai_router)
app.include_router(moodboard_router)
app.include_router(nearby.router)
app.mount("/uploads", StaticFiles(directory=os.path.join(STATIC_DIR, "uploads")), name="uploads")




