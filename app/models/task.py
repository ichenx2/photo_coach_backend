from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    main_topic = Column(String, nullable=False)
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="tasks")
    subtasks = relationship("SubTask", back_populates="task", cascade="all, delete")

class SubTask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    content = Column(String, nullable=False)
    tag = Column(String, nullable=False)
    suggested_position = Column(String)
    lighting_condition = Column(String)
    shooting_technique = Column(String)
    recommended_time = Column(String)
    is_completed = Column(Boolean, default=False)

    task = relationship("Task", back_populates="subtasks")
    photo = relationship("Photo", back_populates="subtask")
