import os
from dotenv import load_dotenv
import google.generativeai as genai

from sqlalchemy.orm import Session
from app.db.feedback_crud import create_feedback
from app.models.feedback import Feedback
from app.schemas.feedback_schema import FeedbackCreate
from app.services.ai_analysis_service import analyze_image

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
{observation}

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
    根據 observation + techniques 產出 Gemini 攝影建議回饋
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


def analyze_and_store_feedback(photo_id: str, photo_data: bytes, db: Session, user_id: int) -> Feedback:
    """
    分析照片並儲存回饋
    :param photo_id: Unique identifier for the photo
    :param photo_data: Binary data of the photo
    :param db: Database session
    :param user_id: 使用者 ID
    :return: Feedback 資料（已儲存）
    """
    
    analysis_result = analyze_image(photo_data)

    if 'error' in analysis_result:
        raise ValueError(f"Image analysis failed: {analysis_result['error']}")

    feedback_data = FeedbackCreate(
        user_id=user_id,
        photo_id=photo_id,
        content_analysis={
            "ai_score": analysis_result.get('ai_score', '0.0'),
            "highlight": analysis_result.get("highlight", "無"),
            "tip": analysis_result.get("tip", "無"),
            "suggestion": analysis_result.get("suggestion", "無"),
            "challenge": analysis_result.get("challenge", "無"),
            "completed_subtasks": analysis_result.get("completed_subtasks", [])
        },
    )

    # Step 3: Store feedback in the database
    feedback = create_feedback(db, feedback_data)

    return feedback
