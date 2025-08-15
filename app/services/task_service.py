from app.services.ai_service import generate_tasks_from_subtopics
from app.schemas.task_schema import TaskCreate, SubTaskCreate
from app.db.task_crud import create_task_with_subtasks
from sqlalchemy.orm import Session

async def generate_and_store_task(user_id: int, main_topic: str, sub_topics: list[str], db: Session):
    # 透過 Gemini 產生拍攝任務建議
    subtasks_data = await generate_tasks_from_subtopics(main_topic, sub_topics)

    # 整理成 TaskCreate schema 結構
    task_create = TaskCreate(
        main_topic=main_topic,
        image_url="", 
        subtasks=[
            SubTaskCreate(
                content=subtask['content'],
                tag=subtask['tag'],
                suggested_position=subtask['suggested_position'],
                lighting_condition=subtask['lighting_condition'],
                shooting_technique=subtask['shooting_technique'],
                recommended_time=subtask['recommended_time']
            ) for subtask in subtasks_data
        ]
    )

    task = create_task_with_subtasks(db, user_id, task_create)

    return task
