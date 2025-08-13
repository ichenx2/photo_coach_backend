from fastapi import FastAPI
from app.api import ping, auth
import app.db.feedback_table
from app.db.database import engine, Base, SessionLocal
#from app.models.user import Base
from app.api.ai_chat import router as ai_router
from app.api.pexels import router as moodboard_router
from app.api.feedback import router as feedback_router
from app.api.photo_feedback import router as photos_router

from dotenv import load_dotenv
load_dotenv()   

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(ai_router)
app.include_router(moodboard_router)
app.include_router(feedback_router, prefix="/api")
app.include_router(photos_router, prefix="/api")