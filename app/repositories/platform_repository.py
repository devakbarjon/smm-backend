from .base import BaseRepository

from app.models.platform import Platform


class PlatformRepository(BaseRepository):
    async def create(self, name: str, keywords: str) -> Platform | None:
        platform = Platform(
            name=name,
            keywords=keywords
        )

        return await self.add(platform)
    
    async def get_platform_by_name(self, name: str) -> Platform | None:

        return await self.get_one(Platform, name=name)
    

    async def get_all_platforms(self) -> list[Platform] | None:

        return await self.get_all(Platform)