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
        我希望你針對使用者提供的主題 "{user_input}" 回傳以下資訊：

        1. 子主題（sub_topics）：給我3個與主題相關的拍攝子主題，適合用來當作選項顯示給使用者參考，字數盡量不要超過5個字，簡短明瞭即可，所生成的子主題之間重複性也不要太高。
        
        請回傳 JSON 格式如下：
        ```json
        {{
        "reply": "...", 
        "sub_topics": ["...", "..."],
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
            "itinerary": result.get("itinerary", None),
        }

    except Exception as e:
        print(f"Gemini 發生錯誤：{e}")
        return {
            "reply": "抱歉，AI 回覆時發生錯誤。",
            "sub_topics": [],
            "itinerary": None,
        }

async def generate_keywords_from_subtopics(sub_topics: list[str]) -> list[str]:
    try:
        prompt = f"""
        根據以下拍攝子主題：{sub_topics}

        請你延伸出約 6 個具體、精準、可視化的關鍵字，適合用來在圖庫網站（如 Pexels）搜尋圖片，用於製作多元風格的 moodboard。

        請注意：
        - 回傳的名詞或短語必須清晰可視化，適合搜尋實體圖片（例如 "sunset beach", "vintage cafe", "wooden table"）
        - 關鍵字之間不得重複，請避免語意或外觀類似的詞彙（如 "green forest" vs "tropical jungle"）
        - 請涵蓋不同風格、色調、或背景，以提高視覺多樣性
        - 不要回傳抽象詞（如 happiness, creativity）或動詞
        
        請回傳以下格式：
        ```json
        {{
          "visual_keywords": ["...", "...", "..."]
        }}
        """
        response = model.generate_content(prompt)
        clean_json = extract_json_block(response.text.strip())
        result = json.loads(clean_json)

        keywords = result.get("visual_keywords", [])
        if isinstance(keywords, str):
            try:
                keywords = json.loads(keywords.replace("'", '"'))
            except:
                keywords = []

        return keywords

    except Exception as e:
        print(f"generate_keywords_from_subtopics 發生錯誤：{e}")
        return []

