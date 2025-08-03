import os
from fastapi import FastAPI
from app.api import ping, auth, analyze
from fastapi.staticfiles import StaticFiles
from app.db.database import engine
from app.models.user import Base
from app.api.ai_chat import router as ai_router
from app.api.pexels import router as moodboard_router
from app.api import nearby
from app.api.photo import router as photo_router
import os

app = FastAPI()
Base.metadata.create_all(bind=engine)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/analyze", tags=["Image Analysis"])
app.include_router(photo_router, prefix="/api", tags=["Photo"])
app.include_router(ai_router)
app.include_router(moodboard_router)
app.include_router(nearby.router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")




