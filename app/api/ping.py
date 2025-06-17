# 測試用（檢查server是否正常運作)

from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong!"}
