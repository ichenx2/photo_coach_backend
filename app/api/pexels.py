from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.moodboard_service import create_moodboard_from_keywords

router = APIRouter(prefix="/moodboard", tags=["Moodboard"])

class KeywordsRequest(BaseModel):
    keywords: list[str]

@router.post("/generate")
async def generate_moodboard_from_keywords_api(req: KeywordsRequest):
    try:
        image_url = create_moodboard_from_keywords(req.keywords)
        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
