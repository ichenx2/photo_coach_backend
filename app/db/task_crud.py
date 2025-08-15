from sqlalchemy.orm import Session
from app.models.task import Task, SubTask
from app.schemas.task_schema import TaskCreate, TaskUpdate
from datetime import date

def create_task_with_subtasks(db: Session, user_id: int, task_data: TaskCreate) -> Task:
    task = Task(
        user_id=user_id,
        main_topic=task_data.main_topic,
        image_url=task_data.image_url,
    )
    db.add(task)
    db.flush()

    for subtask_data in task_data.subtasks:
        subtask = SubTask(
            task_id=task.id,
            content=subtask_data.content,
            tag=subtask_data.tag,
            suggested_position=subtask_data.suggested_position,
            lighting_condition=subtask_data.lighting_condition,
            shooting_technique=subtask_data.shooting_technique,
            recommended_time=subtask_data.recommended_time
        )
        db.add(subtask)

    db.commit()
    db.refresh(task)
    return task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(Task).filter(Task.user_id == user_id).order_by(Task.created_at.desc()).all()

from datetime import datetime, time

def get_tasks_by_user_and_date(db: Session, user_id: int, assigned_date: date):
    start_datetime = datetime.combine(assigned_date, time.min)  # 當天 00:00:00
    end_datetime = datetime.combine(assigned_date, time.max)    # 當天 23:59:59.999999

    return db.query(Task).filter(
        Task.user_id == user_id,
        Task.created_at >= start_datetime,
        Task.created_at <= end_datetime
    ).all()


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()

def mark_subtask_complete(db: Session, subtask_id: int):
    subtask = db.query(SubTask).filter(SubTask.id == subtask_id).first()
    if subtask:
        subtask.is_completed = True
        db.commit()
        return subtask
    return None

def update_task(db: Session, task_id: int, task_data: TaskUpdate, user_id: int) -> Task:
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
    if not task:
        return None

    task.title = task_data.title
    task.description = task_data.description
    task.date_assigned = task_data.date_assigned
    db.commit()
    db.refresh(task)
    return task
