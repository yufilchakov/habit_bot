from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class HabitCompletion(BaseModel):
    """Модель одного выполнения привычки."""
    habit: str
    completed: bool
    timestamp: datetime


class UserHabitHistory(BaseModel):
    """ История привычек пользователя."""
    habits: List[str] = []
    last_7_days: List[HabitCompletion] = []
    last_activity: Optional[datetime] = None
