import os
import json
import random
from dotenv import load_dotenv
from typing import Optional
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

async def chat_with_gemini(user_input: str, place_type: Optional[str] = None) -> dict:
    try:
        # print(f'[DEBUG] place_type = {place_type!r}')
        
        place_type_instruction_map = {
            "tourist_attraction": "你現在在觀光景點，請從建築、地標、人流、環境氛圍等角度規劃拍攝。",
            "cafe": "你現在在咖啡廳，請著重於光影、咖啡、座位、擺設與空間氛圍的拍攝。",
            "book_store": "你現在在書店，適合拍攝書架細節、閱讀場景與文藝氣息。",
            "art_gallery": "你現在在藝術空間，請著重於展品、裝置藝術與場地氛圍的捕捉。",
            "park": "你現在在公園，建議拍攝自然景觀、人與自然互動、小徑延伸等。",
            "store": "你現在在特色小店，可以拍商品陳列、空間裝飾與店主互動。",
            "restaurant": "你現在在餐廳，請拍餐點擺盤、用餐場景與內部裝潢。",
            "subway_station": "你現在在街景或車站，適合拍攝人流、建築線條與城市節奏。",
        }

        if place_type and place_type in place_type_instruction_map:
            type_instruction = place_type_instruction_map[place_type]
            prompt = f"""
            我希望你針對使用者選擇的主題 "{place_type}" 產生：
            - 子主題（sub_topics）：給我3個與主題相關的拍攝子主題，適合用來當作選項顯示給使用者參考，字數盡量不要超過5個字，簡短明瞭即可，所生成的子主題之間重複性也不要太高，可以參考類型描述：{type_instruction}。

            再來，請根據使用者提供的主題 "{user_input}" 以及{place_type}產生：
            - 主題簡化（main_topic）：請你判斷使用者輸入的文字核心主題為何，這個主題的place_type是{place_type}，並簡化為1個可以用來代表整體拍攝主題的詞（如「日本街景」、「咖啡廳」、「山景露營」等）。

            最後產生回覆說明（reply）：請先給予鼓勵回覆，再用 1–2 句話簡單並簡短說明這個主題的拍攝重點或靈感，例如可以聚焦的元素、構圖方式或氛圍設定，幫助使用者理解怎麼拍會好看。

            請回傳以下 JSON 格式：
            ```json
            {{
            "main_topic": "...",         
            "reply": "...",              
            "sub_topics": ["...", "...", "..."]
            }}
            """
        else:
            prompt = f"""
            我希望你針對使用者提供的主題 "{user_input}" 回傳以下資訊：

            1. 子主題（sub_topics）：給我3個與主題相關的拍攝子主題，適合用來當作選項顯示給使用者參考，字數盡量不要超過5個字，簡短明瞭即可，所生成的子主題之間重複性也不要太高。
            2. 主題簡化（main_topic）：請你判斷使用者輸入的文字核心主題為何，並簡化為1個可以用來代表整體拍攝主題的詞（如「日本街景」、「咖啡廳」、「山景露營」等）。
            3. 回覆說明（reply）：請用 1–2 句話簡單並簡短說明這個主題的拍攝重點或靈感，例如可以聚焦的元素、構圖方式或氛圍設定，幫助使用者理解怎麼拍會好看。

            請回傳以下 JSON 格式，必須包含這三個欄位：
            ```json
            {{
            "main_topic": "...",
            "reply": "...",
            "sub_topics": ["...", "...", "..."]
            }}
            """


        # print(prompt)

        response = model.generate_content(prompt)
        clean_json = extract_json_block(response.text.strip())
        result = json.loads(clean_json)
        # print("JSON 處理後結果：", json.dumps(result, indent=2, ensure_ascii=False)) #debug用

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
            "main_topic": result.get("main_topic", user_input),
            "sub_topics": subs,
            "itinerary": result.get("itinerary", None),
        }

    except Exception as e:
        print(f"Gemini 發生錯誤：{e}")
        return {
            "reply": "抱歉，AI 回覆時發生錯誤。",
            "main_topic": result.get("main_topic", user_input),
            "sub_topics": [],
            "itinerary": None,
        }

async def generate_keywords_from_subtopics(main_topic: str, sub_topics: list[str]) -> list[str]:
    try:
        prompt = f"""
        請根據使用者想拍攝的主題「{main_topic}」，以及以下子主題：
        {sub_topics}

        請你延伸出約 6 個具體、精準、可視化的關鍵字，適合用來在圖庫網站（如 Pexels）搜尋圖片，用於製作多元風格的 moodboard（以sub_topics)為主。

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

async def generate_tasks_from_subtopics(main_topic: str, sub_topics: list[str]) -> list[dict]:

    try:
        prompt = f"""
        請根據使用者想拍攝的主題「{main_topic}」，以及以下延伸子主題：
        {sub_topics}

        請為每個子主題產出一個具體的拍攝任務建議，並為該任務指派一個最合適的主題分類。請遵守以下要求：

        【拍攝任務內容】
        - 每個子主題產出一句清楚具體的拍攝建議，形式為「可執行的拍攝指令」，如：「從低角度拍攝海浪撞擊岩石，強調動態感」。
        - 每句建議應具體描述畫面內容、拍攝角度、構圖方式、主體動作或氛圍等。
        - 避免冗長敘述或寫成散文風格，也不要只給出關鍵詞，盡量保持在一句話的長度。

        【分類標籤指派】
        請從以下分類中**擇一最適合的標籤**，作為該任務的主題類別，並根據每類的重點進行判斷：

        1. **人像**：拍攝人或人物互動（如寫真、情緒捕捉、生活情境），重視表情、眼神與人物姿態。
        2. **食物**：聚焦於餐點擺盤與色彩、細節呈現，常見於咖啡廳、餐廳、美食相關主題。
        3. **街拍**：在城市街道中捕捉日常場景、人群、交通或建物組合，強調瞬間與節奏感。
        4. **風景**：拍攝自然景觀或城市風景（如山、海、夕陽、街道遠景），重視構圖層次與光線時間變化。
        5. **靜物**：靜止物品特寫（如書籍、飾品、商品），強調物件擺放、光影與質感。
        6. **建築**：明確以建物為主體，強調透視、線條、對稱與外觀造型。
        7. **動物**：捕捉寵物或野生動物，重點為動態、神情或互動。
        8. **旅拍**：整合風景、人像或街拍，呈現旅行情境與完整故事性，帶有記錄旅程氛圍。

        【欄位補充說明】
        請在每個任務中加入以下 4 個拍攝建議欄位（每個欄位的內容含標點符號字數不超過13字）：

        - "suggested_position"：建議站位（如站在巷口、低角度仰拍）
        - "lighting_condition"：建議光線條件（如黃昏順光、陰天柔光）
        - "shooting_technique"：推薦拍攝手法（如引導線構圖、淺景深）
        - "recommended_time"：適合拍攝時段（如清晨、人潮多時）

        請確保這四個欄位皆存在。

        【回傳格式】
        請**只**回傳一段符合以下格式的 JSON，不要加入自然語言說明或 Markdown 語法：

        ```json
        {{
        "tasks": [
            {{
            "main_topic": "...",
            "tasks": [
                {{
                "tag": "食物",
                "content": "從俯角拍攝一杯拉花咖啡，突顯拉花圖案與桌面質感",
                "suggested_position": "站在桌子正上方往下拍攝",
                "lighting_condition": "柔和室內自然光",
                "shooting_technique": "使用大光圈營造淺景深，突出拉花細節",
                "recommended_time": "白天有自然光時"
                }},
                {{
                "tag": "建築",
                "content": "站在對街拍攝咖啡廳的整體外觀與店招，呈現空間風格",
                "suggested_position": "對街正面站位，微仰角",
                "lighting_condition": "順光或陰天皆可",
                "shooting_technique": "使用對稱構圖，保留建築完整形狀",
                "recommended_time": "上午或黃昏光線柔和時"
                }}
            ]
            }},
            {{
            "main_topic": "...",
            "tasks": [
                {{
                "tag": "...",
                "content": "...",
                "suggested_position": "...",
                "lighting_condition": "...",
                "shooting_technique": "...",
                "recommended_time": "..."
                }},
                {{
                "tag": "...",
                "content": "...",
                "suggested_position": "...",
                "lighting_condition": "...",
                "shooting_technique": "...",
                "recommended_time": "..."
                }}
            ]
            }}
        ]
        }}
        """


        response = model.generate_content(prompt)
        clean_json = extract_json_block(response.text.strip())
        result = json.loads(clean_json)
        
        flat_tasks = []
        first_topic = result.get("tasks", [])[0] if result.get("tasks") else {}

        topic_name = first_topic.get("main_topic", main_topic)  
        for task in first_topic.get("tasks", []):
            flat_tasks.append({
                "sub_topic": topic_name,
                "tag": task.get("tag", ""),
                "task": task.get("content", ""),
                "suggested_position": task.get("suggested_position", ""),
                "lighting_condition": task.get("lighting_condition", ""),
                "shooting_technique": task.get("shooting_technique", ""),
                "recommended_time": task.get("recommended_time", ""),
            })

        return flat_tasks


    except Exception as e:
        print(f"generate_tasks_from_subtopics 發生錯誤：{e}")
        return []
