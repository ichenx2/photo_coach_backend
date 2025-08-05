# 取得拍照建議、回饋紀錄儲存等
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) #測試用

TEMPLATE = """
請模仿以下的評論風格，針對一張攝影作品產出完整的回饋建議。語氣請保持:絕對的客觀、專業、有趣，可以帶一點小諷刺，內容結構如下：
注意，務必要遵守，語句要自然順暢，回答請簡短且明瞭

1. 依照所收到的分析結果，敘述該照片有甚麼
2. 若是有值得稱讚的點，可以給予認可和鼓勵
3. 若是畫面中有待改進的部分，則具體說明有那裡可以改進，不用客氣，直接說出不好的點有助於成長
4. 提供實用的改進方法（明確且可執行）

請使用繁體中文回答。

【拍攝亮點】
{highlight}

【可改進之處】
{challenge}

【學習提示】
{tip}

【建議任務挑戰】
{suggestion}
"""


def generate_feedback(data: dict) -> str:
    prompt = TEMPLATE.format(
        highlight=data["highlight"],
        challenge=data["challenge"],
        tip=data["tip"],
        suggestion=data["suggestion"]
    ).strip()

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text.strip()
