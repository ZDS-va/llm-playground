from pydantic_settings import BaseSettings
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    dashscope_api_key: str
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    class Config:
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"

settings = Settings()
