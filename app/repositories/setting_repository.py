from .base import BaseRepository

from app.models.setting import Setting


class SettingRepository(BaseRepository):
    
    async def get_settings(self) -> Setting:

        return await self.get_one(Setting)