from src.services.llm_service import LLMService
from src.repositories.habit_repository import HabitRepository

class MessageHandler:
    """Центральный класс бизнес-логики бота."""
    def __init__(self, llm_service: LLMService, habit_repo: HabitRepository):
        """Инициализирует обработчик."""
        self.llm = llm_service
        self.repo = habit_repo

    async def process_command(self, user_id: str, text: str) -> str:
        """Основной метод маршрутизации команд."""
        text_lower = text.lower().strip()

        if text_lower == "/start":
            return self._cmd_start()
        elif text_lower.startswith("+ "):
            habit = text_lower[2:].strip()
            return await self._cmd_complete_habit(user_id, habit)
        elif text_lower in ["совет", "мотивация", "support", "мотивація"]:
            return await self._cmd_advice(user_id)
        else:
            # Если нет привычек – предложить добавить
            history = self.repo.get_user_history(user_id)
            if not history.habits and not text_lower.startswith("+"):
                return self._cmd_no_habits()
            return await self._cmd_question(user_id, text)

    def _cmd_start(self) -> str:
        """Возвращает приветственное сообщение с описанием команд бота."""
        return (
            "👋 Привет! Я LLM-тренер для твоих привычек.\n\n"
            "➕ Добавь привычку: просто напиши её название (например, «бегать»)\n"
            "✅ Отметь выполнение: + бегать\n"
            "🎯 Получи совет: напиши «совет»\n"
            "❓ Задай вопрос: просто напиши его – я отвечу как тренер."
        )

    def _cmd_no_habits(self) -> str:
        """Возвращает сообщение, предлагающее создать первую привычку."""
        return "У тебя пока нет привычек. Напиши название привычки, чтобы добавить её (например, «медитация»)."

    async def _cmd_complete_habit(self, user_id: str, habit: str) -> str:
        """Обрабатывает команду отметки выполнения привычки."""
        if not habit:
            return "Укажи привычку после '+', например: '+ бегать'"
        self.repo.add_habit_completion(user_id, habit, True)
        return f"✅ Отлично! Выполнил(а) '{habit}'. Так держать!"

    async def _cmd_advice(self, user_id: str) -> str:
        """Генерирует персонализированный совет на основе последних 7 дней выполнения привычек."""
        history = self.repo.get_user_history(user_id)
        if not history.habits:
            return self._cmd_no_habits()

        last_7 = [f"{c.habit} – {'✅' if c.completed else '❌'}" for c in history.last_7_days]
        context = f"Привычки: {', '.join(history.habits)}. Последние 7 дней: {'; '.join(last_7) if last_7 else 'пока нет записей'}."
        prompt = (
            f"Пользователь с историей: {context}. "
            "Дай короткий (1-2 предложения), тёплый, персонализированный совет, как не бросать привычки. "
            "Обратись к пользователю на 'ты', используй эмодзи."
        )
        return await self.llm.generate(prompt)

    async def _cmd_question(self, user_id: str, question: str) -> str:
        """Отвечает на произвольный вопрос пользователя в роли тренера."""
        history = self.repo.get_user_history(user_id)
        habits_str = ", ".join(history.habits) if history.habits else "пока нет добавленных привычек"
        prompt = (
            f"Пользователь спросил: {question}\n"
            f"Его привычки: {habits_str}.\n"
            "Ответь как поддерживающий тренер по привычкам (коротко, 1-2 предложения, дружелюбно)."
        )
        return await self.llm.generate(prompt)
