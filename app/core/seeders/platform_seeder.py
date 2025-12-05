from app.repositories.platform_repository import PlatformRepository

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


async def seed_platforms():
    async with AsyncSessionLocal() as session:
        platform_repo = PlatformRepository(session)
        seeder = PlatformSeeder(platform_repo)
        await seeder.seed()