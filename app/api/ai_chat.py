from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.ai_schema import AIChatRequest, AIChatResponse
from app.services.ai_service import chat_with_gemini
from app.schemas.ai_schema import AIKeywordRequest, AIKeywordResponse
from app.services.ai_service import generate_keywords_from_subtopics
from app.schemas.ai_schema import AIGeneratedTaskList, AIKeywordRequest
from app.services.ai_service import generate_tasks_from_subtopics

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(req: AIChatRequest):
    try:
        result = await chat_with_gemini(req.prompt)
        return AIChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/keywords", response_model=AIKeywordResponse)
async def generate_keywords(req: AIKeywordRequest):
    try:
        result = await generate_keywords_from_subtopics(req.main_topic, req.sub_topics)
        return AIKeywordResponse(visual_keywords=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks", response_model=AIGeneratedTaskList)
async def generate_tasks(req: AIKeywordRequest):
    try:
       tasks = await generate_tasks_from_subtopics(req.main_topic, req.sub_topics)
       return AIGeneratedTaskList(tasks=tasks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))