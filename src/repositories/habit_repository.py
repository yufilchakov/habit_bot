from datetime import datetime
from typing import Dict
from src.models.habit import UserHabitHistory, HabitCompletion


class HabitRepository:
    """Хранилище истории привычек в оперативной памяти."""
    def __init__(self, redis_client=None):
        """Инициализирует репозиторий."""
        self._storage: Dict[str, UserHabitHistory] = {}
    
    def get_user_history(self, user_id: str) -> UserHabitHistory:
        """Возвращает историю привычек пользователя."""
        return self._storage.get(user_id, UserHabitHistory())
    
    def save_user_history(self, user_id: str, history: UserHabitHistory) -> None:
        """Сохраняет историю привычек пользователя."""
        self._storage[user_id] = history
    
    def add_habit_completion(self, user_id: str, habit: str, completed: bool) -> None:
        """Добавляет запись о выполнении привычки."""
        history = self.get_user_history(user_id)
        completion = HabitCompletion(habit=habit, completed=completed, timestamp=datetime.now())
        history.last_7_days.append(completion)
        if len(history.last_7_days) > 7:
            history.last_7_days = history.last_7_days[-7:]
        if habit not in history.habits:
            history.habits.append(habit)
        history.last_activity = datetime.now()
        self.save_user_history(user_id, history)
