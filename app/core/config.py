# 設定檔（環境變數、API 金鑰、模式切換等）

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    gemini_api_key: str
    gemini_model: str = "gemini-pro"
    request_timeout: float = 14.0
    google_application_credentials: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()