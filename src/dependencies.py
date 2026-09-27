from functools import lru_cache
from fastapi import Depends
from src.services.llm_service import YandexGPTService, LLMService
from src.repositories.habit_repository import HabitRepository
from src.handlers.message_handler import MessageHandler


@lru_cache()
def get_habit_repository() -> HabitRepository:
    """Возвращает экземпляр репозитория привычек (синглтон)."""
    return HabitRepository()


@lru_cache()
def get_llm_service() -> LLMService:
    """Возвращает экземпляр LLM-сервиса (синглтон)."""
    return YandexGPTService()


@lru_cache()
def get_message_handler(
    llm_service: LLMService = Depends(get_llm_service),
    habit_repo: HabitRepository = Depends(get_habit_repository),
) -> MessageHandler:
    """Возвращает экземпляр обработчика команд."""
    return MessageHandler(llm_service, habit_repo)
