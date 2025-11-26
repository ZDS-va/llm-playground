from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    # Qwen (DashScope)
    dashscope_api_key: str
    dashscope_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # DeepSeek / VectorEngine (可选)
    deepseek_api_key: str | None = None
    deepseek_base_url: str | None = None
    vectorengine_api_key: str | None = None
    vectorengine_base_url: str | None = None

    # pydantic v2 配置
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",  # 忽略未声明的环境变量，避免报错
    )


settings = Settings()
