import json
from urllib.parse import parse_qsl

from aiogram.utils.web_app import check_webapp_signature
from aiogram.types import LabeledPrice
from fastapi import HTTPException

from .bot_base import bot

from app.core.logging import logger

from app.core.config import settings

from app.schemas.telegram import TelegramUser
from app.utils.helper import validate_language


async def check_init_data(init_data: str) -> bool | None:
    """
    Authenticates a user using Telegram Web App initData.
    
    Args:
        init_data (str): The initData string from the Telegram Web App.
    Returns:
        boolean: True information if authentication is successful, False otherwise.
    """

    if not init_data:
        return None
    
    return await check_webapp_signature(
        init_data=init_data,
        token=settings.BOT_TOKEN.get_secret_value()
    )


async def extract_init_data(init_data: str) -> TelegramUser | None:
    """
    Extracts user information from Telegram Web App initData without authentication.
    
    Args:
        init_data (str): The initData string from the Telegram Web App.
    """
    if not init_data:
        return None

    data_dict = dict(parse_qsl(init_data))
    user_data = data_dict.get("user")
    if not user_data:
        return None

    tg_user = json.loads(user_data)

    return TelegramUser(
        user_id=tg_user.get("id"),
        username=tg_user.get("username"),
        lang_code=validate_language(tg_user.get("language_code", "ru")),
        full_name=tg_user.get("first_name") + " " + tg_user.get("last_name", "")
    )


async def authorize_user(init_data: str):
    if not check_init_data(init_data):
        raise HTTPException(status_code=401, detail="Invalid init_data signature!")

    return await extract_init_data(init_data)


async def check_is_bot_admin(channel_id: int) -> bool:
    """
    Check if the bot is an admin in the specified channel.
    
    Args:
        channel_id (int): The Telegram channel ID to check.
    
    Returns:
        bool: True if the bot is an admin, False otherwise.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=bot.id)
        if member.status in ["administrator"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking bot admin status in channel {channel_id}: {e}")
        return False


async def check_bot_subscription(user_id: int, channel_id: int) -> bool:
    """
    Check if the user is subscribed to the bot's channel.
    
    Args:
        user_id (int): The Telegram user ID.
        channel_id (int): The Telegram channel ID to check subscription against.
    
    Returns:
        int: True if the user is subscribed, False otherwise.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking subscription for user {user_id}: {e}")
        return False


async def create_stars_invoice(amount: int, payload: str) -> str:

    """Create telegram stars invoice"""

    return await bot.create_invoice_link(
        title=f"SMM SERVICE",
        description=f"Deposit for {amount} stars",
        payload=payload,
        currency="XTR",
        prices=[
            LabeledPrice(
                label="Deposit",
                amount=amount,
            )
        ]
    )