import asyncio

from app.repositories.platform_repository import PlatformRepository
from app.repositories.setting_repository import SettingRepository

from app.utils.scheduler.tasks.smm_services import update_service_data

from app.database.base import AsyncSessionLocal


PLATFORM_SEEDS = {
    "telegram": ["telegram", "tg", "телеграм"],
    "youtube": ["youtube", "yt", "ютуб"],
    "discord": ["discord", "дискорд"],
    "twitch": ["twitch", "твич"],
    "instagram": ["instagram", "insta", "ig", "инстаграм"],
    "vk": ["vk", "vkontakte", "вк", "вконтакте"],
    "spotify": ["spotify", "спотифай"],
    "apple music": ["apple music", "itunes", "айпл мьюзик"],
    "soundcloud": ["soundcloud", "саундклауд"],
    "whatsapp": ["whatsapp", "ватсап"],
    "onlyfans": ["onlyfans", "оф"],
    "yappy": ["yappy"],
    "web traffic": ["web", "traffic", "веб трафик", "трафик"],
    "facebook": ["facebook", "fb", "фейсбук"],
    "tiktok": ["tiktok", "tik tok", "тт", "тикток"],
    "twitter": ["twitter", "x", "твиттер"],
    "dzen": ["dzen", "дзен"],
    "map reviews": ["google maps", "карты", "reviews", "отзывы"],
    "reddit": ["reddit"],
    "others": []
}


class PlatformSeeder:
    def __init__(self, platform_repo: PlatformRepository):
        self.platform_repo = platform_repo

    async def seed(self):
        for name, keywords in PLATFORM_SEEDS.items():
            name = name.lower()
            keywords = [kw.lower() for kw in keywords]

            existing = await self.platform_repo.get_platform_by_name(name)
            if existing:
                continue

            await self.platform_repo.create(
                name=name,
                keywords=",".join(keywords)
            )


class SettingsSeeder:
    def __init__(self, setting_repo: SettingRepository):
        self.setting_repo = setting_repo

    async def seed(self):
        existing = await self.setting_repo.get_settings()

        if existing:
            return

        await self.setting_repo.create(
            markup_rate=5,
            ton_rate=1.6
        )


async def start_seed():
    async with AsyncSessionLocal() as session:
        platform_repo = PlatformRepository(session)
        settings_repo = SettingRepository(session)

        settings_seeder = SettingsSeeder(settings_repo)
        platform_seeder = PlatformSeeder(platform_repo)

        await settings_seeder.seed()
        await platform_seeder.seed()
        await update_service_data()


asyncio.run(start_seed())