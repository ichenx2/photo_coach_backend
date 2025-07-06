import os
import json
from dotenv import load_dotenv
from app.services.moodboard_service import create_moodboard_from_keywords
import google.generativeai as genai
import re


load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure the Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def extract_json_block(text: str) -> str:
    if "```json" in text:
        text = text.split("```json")[-1]
    if "```" in text:
        text = text.split("```")[0]
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else "{}"

async def chat_with_gemini(user_input: str) -> dict:
    try:
        prompt = f"""
        我希望你針對使用者提供的主題 "{user_input}" 回傳兩種資訊：

        1. 子主題（sub_topics）：給我3個與主題相關的拍攝子主題，適合用來當作選項顯示給使用者參考，語氣自然即可。

        2. 關鍵字（visual_keywords）：給我6個具體的視覺描述關鍵字，適合用來從圖庫網站（如 Pexels）搜尋圖片。請回傳精簡、不抽象、不重複的名詞或短語（例如 "sunset beach", "green forest", "wooden chair"）

        請回傳 JSON 格式如下：
        ```json
        {{
        "reply": "...", 
        "sub_topics": ["...", "..."],
        "visual_keywords": ["...", "..."]
        }}
        """
        response = model.generate_content(prompt)
        clean_json = extract_json_block(response.text.strip())
        result = json.loads(clean_json)
        print("JSON 處理後結果：", json.dumps(result, indent=2, ensure_ascii=False)) #debug用

        subs = result.get("sub_topics", [])
        if isinstance(subs, str):
            try:
                subs = json.loads(subs.replace("'", '"'))
            except:
                subs = []
        
        visual_keywords = result.get("visual_keywords", [])
        if isinstance(visual_keywords, str):
            try:
                visual_keywords = json.loads(visual_keywords.replace("'", '"'))
            except:
                visual_keywords = []


        return {
            "reply": result.get("reply", ""),
            "sub_topics": subs,
            "visual_keywords": result.get("visual_keywords", []),
            "itinerary": result.get("itinerary", None),
        }

    except Exception as e:
        print(f"Gemini 發生錯誤：{e}")
        return {
            "reply": "抱歉，AI 回覆時發生錯誤。",
            "sub_topics": [],
            "itinerary": None,
        }
