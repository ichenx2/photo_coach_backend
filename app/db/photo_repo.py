from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.feedback_table import Photo, PhotoAnalysis
import json

def create_photo(db: Session, image_url: str, thumbnail_url: Optional[str], captured_at: Optional[datetime]) -> str:
    p = Photo(image_url=image_url, thumbnail_url=thumbnail_url, captured_at=captured_at)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p.id

def upsert_analysis(db: Session, photo_id: str, observation: List[str], techniques: Dict[str, List[str]]) -> None:
    # 清理字串
    obs = [str(x).strip() for x in observation if str(x).strip()]
    # 確保三個分類 key 存在（可留空陣列）
    tech = {
        "構圖技巧": [str(x).strip() for x in techniques.get("構圖技巧", []) if str(x).strip()],
        "光線運用": [str(x).strip() for x in techniques.get("光線運用", []) if str(x).strip()],
        "拍攝角度": [str(x).strip() for x in techniques.get("拍攝角度", []) if str(x).strip()],
    }

    now = datetime.utcnow()
    rec = db.get(PhotoAnalysis, photo_id)
    if rec is None:
        rec = PhotoAnalysis(
            photo_id=photo_id,
            observation_json=json.dumps(obs, ensure_ascii=False),
            techniques_json=json.dumps(tech, ensure_ascii=False),
            updated_at=now,
        )
        db.add(rec)
    else:
        rec.observation_json = json.dumps(obs, ensure_ascii=False)
        rec.techniques_json = json.dumps(tech, ensure_ascii=False)
        rec.updated_at = now
    db.commit()

def _dt_or_none(dt: Optional[datetime]) -> Optional[str]:
    return dt.isoformat() + "Z" if dt else None

def get_photo_detail(db: Session, photo_id: str) -> Optional[Dict[str, Any]]:
    p = db.get(Photo, photo_id)
    if not p:
        return None
    analysis = None
    if p.analysis:
        analysis = {
            "observation": json.loads(p.analysis.observation_json),
            "techniques": json.loads(p.analysis.techniques_json),
            "updated_at": _dt_or_none(p.analysis.updated_at),
        }
    return {
        "id": p.id,
        "image_url": p.image_url,
        "thumbnail_url": p.thumbnail_url,
        "captured_at": _dt_or_none(p.captured_at),
        "created_at": _dt_or_none(p.created_at),
        "analysis": analysis,
    }

def list_photos(db: Session, limit: int, offset: int) -> Dict[str, Any]:
    q = db.query(Photo).order_by(Photo.created_at.desc()).limit(limit).offset(offset)
    items = []
    for p in q.all():
        items.append(get_photo_detail(db, p.id))
    return {"items": items, "count": len(items)}

def delete_photo(db: Session, photo_id: str) -> bool:
    p = db.get(Photo, photo_id)
    if not p:
        return False
    db.delete(p)  # 觸發 CASCADE：photo_analysis 一併刪
    db.commit()
    return True
