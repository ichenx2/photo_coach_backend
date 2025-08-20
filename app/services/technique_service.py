import google.generativeai as genai
import os
import re
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_image_techniques(photo_data: bytes):
    prompt = """
    你是一位專業攝影老師，請觀察這張照片，並依照以下兩個步驟進行分析。

    ---

    第一步：畫面觀察  
    請依下列觀察要點，條列出具體畫面特徵（至少 3 點）：
    請具體描述主體與畫面中心的幾何位置關係，例如「主體距畫面中心約偏右 20%」、「略微偏離中心仍屬中央構圖範圍」。
    - 主體是什麼？（人像、靜物、食物、風景、建築等）
    - 主體位置（中央 / 靠近畫面上下左右三分之一線）
    - 主體大小（主體佔畫面比例）
    - 光線方向（光從哪個方向照射？是否為柔光？是否有陰影？）
    - 拍攝角度（從上往下？平視？仰角？）
    - 是否有特定構圖特徵（例如：左右視覺對稱、有留白、出現引導線等）

    ---

    第二步：技巧推論  
    根據上述觀察，從下列攝影技巧中**選出符合的項目**，請依據觀察結果，**複選所有符合的項目**，不要限制每類僅選一項。
    若畫面特徵與某技巧定義接近，即可合理判斷為使用該技巧（不須絕對符合）。  
    請不要創造新的技巧，僅從提供的清單中選擇。

    ---

    【構圖技巧】
    - 中心構圖：主體位於畫面中央或接近中央，畫面穩定、聚焦
    → 若主體略微偏移但整體重心仍集中，也可視為中心構圖
    - 三分法：主體明顯落在畫面三分之一線附近（非中央區域），畫面左右或上下**視覺重心偏移**  
    → 若主體偏左／偏右／偏上／偏下，且非完全置中，可視為三分法構圖
    - 對稱構圖：畫面左右或上下視覺上大致對稱
    - 留白構圖：主體佔畫面比例較小，背景或周圍空間空曠，形成呼吸感
    → 若主體小但背景複雜，則不建議選留白構圖
    - 框架構圖：主體被前景或環境物包圍，如窗、門、樹枝等
    - 對角線構圖：畫面主線條沿對角線排列
    - 引導線構圖：道路、欄杆、建築等線條指向主體

    【光線運用】
    - 順光：光線從攝影師方向照射主體，主體明亮清晰
    - 逆光：光線從主體背後射來，可能產生剪影或光暈
    - 側光：光線從側邊照射，有立體感與陰影層次
    - 頂光：光線從上方照射，可能產生強烈陰影
    - 背光：背景比主體亮，輪廓明顯
    - 柔光：光線柔和均勻、陰影不明顯（如陰天、窗邊光）

    【拍攝角度】
    - 特寫：主體靠近鏡頭，細節清楚，背景模糊
    - 廣角：視野寬廣，背景資訊豐富
    - 仰角：從下往上拍，主體顯得高大或莊嚴
    - 平視：與主體高度一致，自然、平衡
    - 俯視：從上往下拍，主體顯得渺小或可愛

    ---

    請依照以下 JSON 結構輸出，**不要加上多餘的文字說明**：

    {
        "observation": [
            "主體是...位於...",
            "主體佔畫面約 ...%，背景為...",
            "光線從...，光線...",
            "拍攝視角..."
        ],
        "techniques": {
            "構圖技巧": ["..."],
            "光線運用": ["..."],
            "拍攝角度": ["..."]
        }
    }
    """


    response = None
    try:
        response = model.generate_content(
            [prompt, {"mime_type": "image/jpeg", "data": photo_data}]
        )

        raw_text = response.text.strip()
        cleaned_json = clean_json_response(raw_text)
        return json.loads(cleaned_json)

    except Exception as e:
        return {
            "error": f"LLM 回傳格式錯誤: {str(e)}",
            "raw": response.text if response else None
        }

def clean_json_response(raw_text: str) -> str:
    """清理 LLM 回傳的 JSON（去掉 ```json ... ``` 包裝，並只保留 {} 內的 JSON）"""
    # 先移除 Markdown 標記
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text)
    cleaned = re.sub(r"\s*```$", "", cleaned).strip()

    # 嘗試只抓 JSON 主體（避免 LLM 多講話）
    match = re.search(r"\{[\s\S]*\}", cleaned)
    if match:
        return match.group(0)
    return cleaned
