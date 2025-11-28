import json
from urllib.parse import parse_qsl

from aiogram.utils.web_app import check_webapp_signature

from app.db.functions.users import get_user_by_id, save_user
from app.core.config import settings
from app.db.base import get_db


async def authenticate_user(init_data: str, start_param: str = "") -> dict:
    """
    Authenticates a user using Telegram Web App initData.
    
    Args:
        init_data (str): The initData string from the Telegram Web App.
        start_param (str | int | None): Optional start parameter from the bot.
    
    Returns:
        dict: User information if authentication is successful, None otherwise.
    """
    # Validate the initData
    if not init_data:
        return {"success": False, "message": "initData is empty!"}
    
    def validate_init_data(init_data: str) -> bool:
        status = check_webapp_signature(settings.bot_token, init_data)
        return status

    if not validate_init_data(init_data):
        return {"success": False, "message": "Invalid initData!"}

    # Parse the initData
    data_dict = dict(parse_qsl(init_data))
    
    # Check if auth_date is recent (within 24 hours)
    # auth_date = int(data_dict.get("auth_date", 0))
    # if datetime.now() - datetime.fromtimestamp(auth_date) > timedelta(hours=24):
    #     return {"success": False, "message": "auth_date is too old!"}
    
    user_data = data_dict.get("user")
    if not user_data:
        return {"success": False, "message": "No user data found!"}

    tg_user = json.loads(user_data)
    user_id = tg_user.get("id")
    username = tg_user.get("username")
    lang_code = tg_user.get("language_code", "ru")
    full_name = tg_user.get("first_name", "")
    if tg_user.get("last_name"):
        full_name += f" {tg_user.get('last_name')}"

    # Authenticate the user (or create a new account)
    async for session in get_db():
        user = await get_user_by_id(
            session=session,
            user_id=user_id
        )

        if not user:
            user = await save_user(
                session=session,
                user_id=user_id,
                lang=lang_code,
                username=username,
                ref=start_param,
                full_name=full_name
            )

        return {
            "success": True,
            "user": user
            }