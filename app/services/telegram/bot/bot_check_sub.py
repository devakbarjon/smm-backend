from app.logging_config import logger
from .bot_base import bot


async def check_is_bot_admin(channel_link: int) -> bool:    
    """
    Check if the bot is an admin in the specified channel.
    
    Args:
        channel_id (int): The Telegram channel ID to check.
    
    Returns:
        bool: True if the bot is an admin, False otherwise.
    """
    try:
        member = await bot.get_chat_member(chat_id=channel_link, user_id=bot.id)
        if member.status in ["administrator"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Error checking bot admin status in channel {channel_link}: {e}")
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