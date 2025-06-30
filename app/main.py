from fastapi import FastAPI
from app.api import ping, auth
from app.db.database import engine
from app.models.user import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])


