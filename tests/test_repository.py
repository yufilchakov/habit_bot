from src.models.habit import UserHabitHistory

def test_get_empty_history(habit_repo):
    """Проверяет, что для несуществующего пользователя возвращается пустая история."""
    history = habit_repo.get_user_history("nonexistent")
    assert history.habits == []
    assert len(history.last_7_days) == 0

def test_add_completion(habit_repo):
    """Проверяет добавление выполнения привычки: обновляются habits и last_7_days."""
    habit_repo.add_habit_completion("user1", "бегать", True)
    history = habit_repo.get_user_history("user1")
    assert "бегать" in history.habits
    assert len(history.last_7_days) == 1
    assert history.last_7_days[0].completed is True

def test_trim_to_7_days(habit_repo):
    """Проверяет, что список last_7_days не превышает 7 записей (обрезается до 7)."""
    for i in range(10):
        habit_repo.add_habit_completion("user2", f"habit{i}", True)
    history = habit_repo.get_user_history("user2")
    assert len(history.last_7_days) == 7
