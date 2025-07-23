from fastapi import FastAPI
from app.api import ping, auth, analyze
from fastapi.staticfiles import StaticFiles
from app.db.database import engine
from app.models.user import Base
from app.api.ai_chat import router as ai_router
from app.api.pexels import router as moodboard_router
from app.api.photo import router as photo_router
import os

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(analyze.router, prefix="/analyze", tags=["Image Analysis"])
app.include_router(ai_router)
app.include_router(moodboard_router)
app.include_router(photo_router, prefix="/api", tags=["Photo"])

app.mount("/static", StaticFiles(directory="static"), name="static")

