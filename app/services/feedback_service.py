import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

TEMPLATE = """
請依據收到的攝影分析結果，客觀且專業地產出一段完整的回饋建議，語氣保持專業、溫和但直接，避免過度主觀或空泛的讚美。
內容需依照以下邏輯撰寫成一段話（不要分段）：

1. 根據 observation，精確描述照片的主體、背景、光線方向與品質、拍攝視角。
2. 根據 techniques，指出照片運用了哪些攝影技巧（構圖技巧、光線運用、拍攝角度）。
3. 若有值得稱讚的地方，簡短給予肯定與鼓勵。
4. 若有不足之處，具體指出問題點，避免籠統描述。
5. 提供明確、可執行的改善方法，讓拍攝者下次能嘗試。

請用繁體中文輸出，不要使用條列式或編號，整合成流暢的一段評論。

【分析觀察】
{observation

【攝影技巧】
構圖技巧：{composition}
光線運用：{lighting}
拍攝角度：{angle}
""".strip()


def _safe_join(items):
    if not items:
        return "（未提供）"
    return "；".join([str(x) for x in items if str(x).strip()])


def generate_feedback(data: dict) -> str:
    """
    data 期待的新格式：
    {
        "observation": [...],
        "techniques": {
            "構圖技巧": [...],
            "光線運用": [...],
            "拍攝角度": [...]
        }
    }
    """
    observations = data.get("observation", []) or []
    techniques = data.get("techniques", {}) or {}

    composition = techniques.get("構圖技巧", []) or []
    lighting    = techniques.get("光線運用", []) or []
    angle       = techniques.get("拍攝角度", []) or []

    prompt = TEMPLATE.format(
        observation=_safe_join(observations),
        composition="、".join(composition) if composition else "（未偵測）",
        lighting="、".join(lighting) if lighting else "（未偵測）",
        angle="、".join(angle) if angle else "（未偵測）",
    )


    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return (response.text or "").strip() or "目前無法產出回饋內容，請稍後再試。"
