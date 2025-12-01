from pydantic import BaseModel


class TMAInitData(BaseModel):
    init_data: str


class TelegramUser(BaseModel):
    user_id: int
    username: str | None = None
    lang_code: str = "ru"
    full_name: str | None = None