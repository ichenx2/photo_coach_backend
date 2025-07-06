from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.schemas.ai_schema import AIChatRequest, AIChatResponse
from app.services.ai_service import chat_with_gemini

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat", response_model=AIChatResponse)
async def ai_chat(req: AIChatRequest):
    try:
        result = await chat_with_gemini(req.prompt)
        return AIChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



