import pytest
from fakeredis import FakeRedis
from src.services.llm_service import MockLLMService
from src.repositories.habit_repository import HabitRepository
from src.handlers.message_handler import MessageHandler


@pytest.fixture
def fake_redis():
    """Возвращает in-memory эмулятор Redis для тестов (библиотека fakeredis)."""
    return FakeRedis()


@pytest.fixture
def habit_repo(fake_redis):
    """Создаёт репозиторий привычек, использующий FakeRedis вместо реального."""
    return HabitRepository(fake_redis)


@pytest.fixture
def llm_service():
    """Возвращает заглушку LLM (MockLLMService), не требующую реального API."""
    return MockLLMService()


@pytest.fixture
def message_handler(llm_service, habit_repo):
    """Создаёт обработчик сообщений с подставными зависимостями для тестов."""
    return MessageHandler(llm_service, habit_repo)
