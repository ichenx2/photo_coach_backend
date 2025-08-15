# 負責連線資料庫
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator

DATABASE_URL = "sqlite:///./photocoach.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 啟用 SQLite 外鍵，確保刪照片會連動刪關聯與回饋
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close() 
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
