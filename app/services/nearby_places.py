import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# 預設建議語模板
def generate_recommendation(name: str) -> str:
    return f"推薦拍攝 {name} 的特色風景"

def get_recommended_spots(lat: float, lng: float, place_type: str = "tourist_attraction", radius=1000) -> list:
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "language": "zh-TW",
        "key": GOOGLE_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data.get("status") != "OK":
            print(f"Google API Error: {data.get('status')} - {data.get('error_message')}")
            return []

        results = []
        for place in data.get("results", [])[:10]:  # 限制最多回傳10筆
            results.append({
                "name": place.get("name"),
                "type": place_type,
                "location": place.get("vicinity", "未知地點"),
                "photo_reference": place.get("photos", [{}])[0].get("photo_reference", ""),
                "recommendation": generate_recommendation(place.get("name"))
            })
        return results

    except Exception as e:
        print(f"Error fetching places: {e}")
        return []
