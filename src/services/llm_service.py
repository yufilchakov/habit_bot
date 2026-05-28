from abc import ABC, abstractmethod
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from src.config import settings


class LLMService(ABC):
    """Абстрактный базовый класс для всех LLM-сервисов."""
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Генерирует ответ LLM на основе пользовательского запроса."""
        pass

class YandexGPTService(LLMService):
    """Реализация LLM-сервиса через YandexGPT (REST API Yandex Cloud)."""
    def __init__(self):
        """Инициализирует клиент YandexGPT."""
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.headers = {
            "Authorization": f"Api-Key {settings.yandexgpt_api_key}",
            "Content-Type": "application/json"
        }

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Отправляет запрос к YandexGPT и возвращает сгенерированный текст."""
        system = system_prompt or (
            "Ты позитивный тренер по привычкам. Не придумывай факты о выполнении привычек. "
            "Говори коротко, поддерживающе, используй эмодзи, когда уместно."
        )
        body = {
            "modelUri": f"gpt://{settings.yandexgpt_folder_id}/{settings.llm_model}",
            "completionOptions": {
                "temperature": settings.llm_temperature,
                "maxTokens": settings.llm_max_tokens
            },
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ]
        }
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(self.url, headers=self.headers, json=body)
            response.raise_for_status()
            data = response.json()
            return data["result"]["alternatives"][0]["message"]["text"]

class MockLLMService(LLMService):
    """Заглушка для тестов и разработки без реального API."""
    async def generate(self, prompt: str, system_prompt: str = None) -> str:
        """Генерирует фиктивный ответ, не обращаясь к внешнему сервису."""
        return "Отличный прогресс! Ты молодец, что не сдаёшься. Давай продолжать в том же духе! 💪"
