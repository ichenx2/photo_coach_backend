import google.generativeai as genai
import os
import re
import json

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

def analyze_image_techniques(photo_data: bytes):
    prompt = """
    你是一位專業攝影老師，請觀察這張照片並判斷它使用了哪些攝影技巧。
    請從以下技巧中選擇，並以 JSON 格式輸出結果，**不要自行創造新技巧**。

    ### 構圖技巧
    - 三分法：主體位於畫面三分之一的位置，營造平衡感
    - 對角線構圖：將畫面對角分割出兩份，對角線不用一定要在中間，有偏移也可以
    - 對稱構圖：畫面呈現左右或上下對稱，帶來和諧感
    - 中心構圖：主體置於畫面正中，帶來穩定、直接的視覺效果
    - 框架構圖：利用前景或環境元素把主體框起來
    - 留白構圖：保留大片空白，突出主體並創造呼吸感
    - 引導線構圖：用引導線條引導視覺焦點

    ### 光線運用
    - 順光：光線從攝影師方向照射主體，主體明亮、細節清晰
    - 逆光：光線從主體背後射來，可能形成剪影或光暈
    - 側光：光線從側面照射，增加立體感與陰影效果
    - 頂光：光線從上方直射，容易出現強烈陰影
    - 背光：背景光比主體亮，使主體輪廓突顯
    - 柔光：光線柔和、陰影不明顯，例如陰天或柔光罩效果

    ### 拍攝角度
    - 特寫：靠近主體拍攝，細節占滿畫面
    - 廣角：視野寬廣，背景資訊豐富
    - 仰角：從下往上拍，主體顯得高大或具壓迫感
    - 平視：與主體同高度拍攝，給人自然感
    - 俯視：從上往下拍，主體顯得渺小或可愛

    請使用以下 JSON 格式輸出（可多選，但請精確）：
    {
    "構圖技巧": ["...", "..."],
    "光線運用": ["...", "..."],
    "拍攝角度": ["..."]
    }

    請分析這張照片。
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
