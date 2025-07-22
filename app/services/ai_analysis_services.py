# import openai
# import base64
# import os

# openai.api_key = os.getenv("OPENAI_API_KEY") 

# def analyze_image(photo_data):
#     """
#     Analyze the given photo data using AI services.

#     Args:
#         photo_data (bytes): The image data to be analyzed.

#     Returns:
#         dict: Analysis results from AI services.
#     """
#     try:
#         # 將圖片轉為 base64 格式
#         base64_image = base64.b64encode(photo_data).decode("utf-8")
#         image_data = {
#             "type": "image_url",
#             "image_url": {
#                 "url": f"data:image/jpeg;base64,{base64_image}"
#             }
#         }

#         # 傳送請求到 OpenAI GPT-4 Vision 模型
#         response = openai.ChatCompletion.create(
#             model="gpt-4-vision-preview",
#             messages = [
#                 {
#                     "role": "system",
#                     "content": "你是 PhotoCoach 攝影教練，請針對照片從主體、構圖、色調與改善建議四個面向進行分析，請用以下格式回答：\n\n【主體】：\n...\n\n【構圖】：\n...\n\n【色調】：\n...\n\n【改善建議】：\n..."
#                 },
#                 {
#                     "role": "user",
#                     "content": [
#                         {"type": "text", "text": "請幫我分析這張照片"},
#                         image_data
#                     ]
#                 }
#             ],

#             max_tokens=500
#         )
#         return response['choices'][0]['message']['content']
#     except Exception as e:
#         return {"error": str(e)}

# services/image_analysis.py
import os
import re
import json
import google.generativeai as genai


# ✅ 設定 Gemini API 金鑰
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# ✅ 初始化 Gemini 模型（支援圖片）
model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_image(photo_data: bytes) -> dict:
    """
    使用 Gemini Vision 模型分析圖片內容，回傳格式化建議 (JSON 格式)。

    Returns:
        dict: 包含 highlight, composition, color, suggestion 的分析字典
    """
    try:
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": photo_data
            }
        ]

        prompt = """你是 PhotoCoach 攝影教練，請根據接下來的圖片內容進行分析，並請嚴格使用下列 JSON 格式回覆，不要加上任何說明
            {
            "highlight": "拍攝亮點...",
            "challenge": "改進建議...",
            "tip": "學習提示...",
            "suggestion": "建議任務挑戰..."
            }

            請填入每一項的分析內容，並使用繁體中文回答。
            """

        response = model.generate_content([prompt] + image_parts)
        raw_text = response.text.strip()

        cleaned_json = clean_json_response(raw_text)
        return json.loads(cleaned_json)
    
    except Exception as e:
        return {"error": str(e)}

def clean_json_response(raw_text: str) -> str:
    # 去除 ```json 或 ``` 等開頭與結尾標記
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()