from .bot_base import bot

from app.core.config import settings
from app.core.logging import logger


async def notify(chat_id: int, text: str) -> None:
    """Send telegram notification to user"""

    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as ex:
        logger.error("Failed to send telegram notification", exc_info=ex)


async def notify_admin(message: str) -> None:
    try:
        await bot.send_message(
            chat_id=settings.LOGS_CHAT_ID,
            message=message
        )
    except Exception as ex:
        logger.error(f"Failed to notify admin: {ex}", exc_info=ex)