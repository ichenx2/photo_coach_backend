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

        prompt = """    
        你是攝影教練，請根據以下街拍任務，評估照片是否成功達成任務目標，並提供以下格式的 JSON 評分回應。

        ---
        任務目標：
        拍攝一張帶有濃厚日系氛圍的街道畫面，可取景於巷弄、便利商店、自動販賣機或有電線桿的街角。構圖乾淨、光影自然。

        子任務要求：
        1. 拍攝電線桿與交錯的電線構成的畫面
        2. 捕捉便利商店或自動販賣機所在的街角
        3. 使用對角線或引導線構圖呈現街道延伸感

        請根據整體任務達成度給 1~5 分，並給出詳細評語與具體建議，回傳格式如下：

        {
            "ai_score": "1~5分",
            "highlight": "照片中已成功展現的亮點，鼓勵與強化之處",
            "tip": "針對任務主題的學習建議，可提供構圖、光線、角度等技巧",
            "suggestion": "本張照片尚可改進的地方與建議方向",
            "challenge": "進階挑戰，可作為下次拍攝進一步挑戰目標",
        }

        請以繁體中文回應，並**只回傳 JSON 格式**，不要附加說明或其他文字。
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