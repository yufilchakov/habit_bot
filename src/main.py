import logging
from fastapi import FastAPI, Request, Response, BackgroundTasks, Depends
from src.config import settings
from src.services.telegram_service import send_telegram_message
from src.handlers.message_handler import MessageHandler
from src.dependencies import get_message_handler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Habit LLM Bot")

@app.post("/webhook")
async def telegram_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    handler: MessageHandler = Depends(get_message_handler),
) -> Response:
    """Принимает вебхук от Telegram, обрабатывает сообщение в фоне."""
    try:
        body = await request.json()
    except Exception as e:
        logger.error(f"Invalid JSON: {e}")
        return Response(status_code=400)

    message = body.get("message")
    if not message:
        return Response(status_code=200)

    chat_id = message["chat"]["id"]
    user_id = str(message["from"]["id"])
    text = message.get("text", "")
    background_tasks.add_task(process_and_reply, handler, chat_id, user_id, text)
    return Response(status_code=200)

async def process_and_reply(handler: MessageHandler, chat_id: int, user_id: str, text: str):
    """Фоновая задача: обработка сообщения и отправка ответа."""
    try:
        reply = await handler.process_command(user_id, text)
        await send_telegram_message(chat_id, reply)
    except Exception as e:
        logger.error(f"Error processing message from {user_id}: {e}")
        await send_telegram_message(chat_id, "⚠️ Произошла ошибка. Попробуй позже.")

@app.get("/health")
async def health() -> dict:
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    logger.info("FastAPI приложение запущено. In-memory репозиторий активен.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("FastAPI приложение завершает работу.")
