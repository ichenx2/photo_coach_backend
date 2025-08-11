from fastapi import FastAPI
from app.api import ping, auth
from app.db.database import engine
from app.models.user import Base
from app.api.ai_chat import router as ai_router
from app.api.pexels import router as moodboard_router
from app.api.learning_record import router as learning_record_router

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(ai_router)
app.include_router(moodboard_router)
app.include_router(learning_record_router, prefix="/learning_records", tags=["LearningRecords"])

