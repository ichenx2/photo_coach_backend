from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import date
from app.db.database import get_db
from app.models.user import User
from app.services.auth_service import get_current_user
from app.services.task_service import generate_and_store_task
from app.schemas.task_schema import TaskResponse, TaskUpdate
from app.db import task_crud
from app.schemas.ai_schema import AIKeywordRequest

router = APIRouter()

# 取得任務（全部或指定日期）
@router.get("", response_model=List[TaskResponse])
def get_tasks(
    date_param: Optional[str] = Query(None, alias="date", description="Date in YYYY-MM-DD format"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get tasks for current user, optionally filtered by date.
    
    Query parameter:
    - date: Optional date in YYYY-MM-DD format (e.g., ?date=2025-08-12)
    """
    try:
        if date_param:
            # Parse the date string to date object
            parsed_date = date.fromisoformat(date_param)
            tasks = task_crud.get_tasks_by_user_and_date(db, current_user.id, parsed_date)
        else:
            tasks = task_crud.get_tasks_by_user(db, current_user.id)
        
        return tasks
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 新增任務
@router.post("", response_model=TaskResponse)
async def generate_tasks(
    req: AIKeywordRequest, 
    current_user: User = Depends(get_current_user), 
    db: Session = Depends(get_db)):
    try:
       tasks = await generate_and_store_task(current_user.id, req.main_topic, req.sub_topics, db)
       return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 刪除任務
@router.delete("/{task_id}", response_model=dict)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = task_crud.delete_task(db, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"msg": "Task deleted successfully"}

# 更新任務
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    updated = task_crud.update_task(db, task_id, task_data, current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found or not authorized")
    return updated
