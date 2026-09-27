import pytest


@pytest.mark.asyncio
async def test_start_command(message_handler):
    """Проверяет, что команда /start возвращает приветствие с упоминанием LLM-тренера."""
    reply = await message_handler.process_command("user123", "/start")
    assert "LLM-тренер" in reply


@pytest.mark.asyncio
async def test_complete_habit(message_handler):
    """Проверяет отметку выполнения привычки: ответ содержит ✅ и привычка сохраняется в репозитории."""
    reply = await message_handler.process_command("user123", "+ бегать")
    assert "✅" in reply
    history = message_handler.repo.get_user_history("user123")
    assert "бегать" in history.habits


@pytest.mark.asyncio
async def test_advice_without_habits(message_handler):
    """Проверяет, что при запросе совета без привычек бот предлагает их добавить."""
    reply = await message_handler.process_command("new_user", "совет")
    assert "нет привычек" in reply


@pytest.mark.asyncio
async def test_advice_with_habits(message_handler):
    """Проверяет генерацию совета при наличии привычек: ожидается фиксированный ответ от MockLLM."""
    await message_handler.process_command("user_advice", "+ бегать")
    reply = await message_handler.process_command("user_advice", "совет")
    assert "Отличный прогресс" in reply


@pytest.mark.asyncio
async def test_question(message_handler):
    """Проверяет ответ на вопрос: сначала добавляется привычка, затем бот отвечает (через MockLLM)."""
    await message_handler.process_command("user_q", "+ бегать")
    reply = await message_handler.process_command("user_q", "как не лениться?")
    assert "Отличный прогресс" in reply or "молодец" in reply or "тренер" in reply
