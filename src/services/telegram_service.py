import httpx
from src.config import settings

async def send_telegram_message(chat_id: int, text: str) -> None:
    """Асинхронно отправляет текстовое сообщение пользователю в Telegram."""
    url = f"https://api.telegram.org/bot{settings.telegram_token}/sendMessage"
    proxies = None
    if hasattr(settings, 'telegram_proxy') and settings.telegram_proxy:
        proxies = settings.telegram_proxy
    async with httpx.AsyncClient(proxy=proxies, timeout=15.0) as client:
        await client.post(url, json={"chat_id": chat_id, "text": text})
