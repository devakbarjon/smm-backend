from .base import BaseRepository

from app.models.category import Category


class CategoryRepository(BaseRepository):

    async def create(self, name: str, platform_id: int) -> Category | None:
        category = Category(
                name=name,
                platform_id=platform_id
            )
        
        return await self.add(category)
    
    async def get_category_by_name(self, name: str) -> Category | None:

        return await self.get_one(Category, name=name)
    

    async def get_categories_by_platform(self, platform_id: int) -> list[Category] | None:

        return await self.get_all(Category, platform_id=platform_id)
    

    async def get_all_categories(self) -> list[Category] | None:

        return await self.get_all(Category)