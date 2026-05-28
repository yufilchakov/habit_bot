from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    """Настройки приложения, загружаемые из переменных окружения."""
    telegram_token: str = Field(alias="TELEGRAM_TOKEN")
    yandexgpt_folder_id: str = Field(alias="YANDEXGPT_FOLDER_ID")
    yandexgpt_api_key: str = Field(alias="YANDEXGPT_API_KEY")
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")
    llm_model: str = Field(default="yandexgpt-lite", alias="LLM_MODEL")
    llm_temperature: float = Field(default=0.7, alias="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=200, alias="LLM_MAX_TOKENS")

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings = Settings()
