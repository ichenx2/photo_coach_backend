from sqlalchemy.orm import Session
from app.models.technique import Technique
from app.db.database import SessionLocal

technique_data = [
    {"name": "中心構圖", "category": "構圖技巧", "description": "主體位於畫面中央或接近中央，畫面穩定、聚焦"},
    {"name": "三分法", "category": "構圖技巧", "description": "主體落在畫面三分之一線附近，畫面更有動感"},
    {"name": "對稱構圖", "category": "構圖技巧", "description": "畫面左右或上下對稱"},
    {"name": "留白構圖", "category": "構圖技巧", "description": "主體比例小，背景空曠，形成呼吸感"},
    {"name": "框架構圖", "category": "構圖技巧", "description": "主體被環境或前景物包圍，如窗、門"},
    {"name": "對角線構圖", "category": "構圖技巧", "description": "主線條沿對角線排列，增強動感"},
    {"name": "引導線構圖", "category": "構圖技巧", "description": "線條引導視線聚焦主體"},

    {"name": "順光", "category": "光線運用", "description": "光從攝影師方向射來，主體明亮清晰"},
    {"name": "逆光", "category": "光線運用", "description": "光從主體背後射來，可能產生剪影或光暈"},
    {"name": "側光", "category": "光線運用", "description": "從側邊照射，強調立體感"},
    {"name": "頂光", "category": "光線運用", "description": "光從上方照射，產生陰影"},
    {"name": "背光", "category": "光線運用", "description": "背景比主體亮，主體輪廓明顯"},
    {"name": "柔光", "category": "光線運用", "description": "光線柔和均勻，陰影不明顯"},

    {"name": "特寫", "category": "拍攝角度", "description": "主體靠近鏡頭，細節清楚"},
    {"name": "廣角", "category": "拍攝角度", "description": "視野寬廣，背景豐富"},
    {"name": "仰角", "category": "拍攝角度", "description": "從下往上拍，主體顯得高大"},
    {"name": "平視", "category": "拍攝角度", "description": "與主體高度一致，自然平衡"},
    {"name": "俯視", "category": "拍攝角度", "description": "從上往下拍，主體顯得渺小或可愛"},
]

def seed_techniques():
    db: Session = SessionLocal()

    for data in technique_data:
        existing = db.query(Technique).filter_by(name=data["name"]).first()
        if not existing:
            technique = Technique(**data)
            db.add(technique)

    db.commit()
    db.close()

if __name__ == "__main__":
    seed_techniques()
    print("✅ 技巧資料匯入完成")
