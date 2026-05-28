FROM python:3.12-slim

WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости (без dev-группы, так как для продакшена)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --only main

# Копируем исходный код
COPY src ./src
COPY main.py ./

# Открываем порт, который слушает uvicorn
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]