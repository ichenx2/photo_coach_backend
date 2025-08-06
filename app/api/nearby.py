from fastapi import APIRouter, Query
from app.services.nearby_places import get_recommended_spots

router = APIRouter()

@router.get("/recommend_spots")
async def recommend_spots(
    lat: float = Query(...),
    lng: float = Query(...),
    place_type: str = Query("tourist_attraction")  # 預設為景點
):
    spots = get_recommended_spots(lat, lng, place_type)
    return {"spots": spots}
