.PHONY: install dev test lint format docker-up docker-down

install:
	poetry install

dev:
	poetry run uvicorn src.main:app --reload --port 8000

test:
	poetry run pytest -v

test-cov:
	poetry run pytest --cov=src --cov-report=html

lint:
	poetry run ruff check src tests
	poetry run mypy src

format:
	poetry run black src tests

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

setup: install docker-up
	@echo "✅ Проект готов. Скопируй .env.example в .env и заполни настройки. Запусти make dev"