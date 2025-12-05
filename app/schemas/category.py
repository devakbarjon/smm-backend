from pydantic import BaseModel, ConfigDict


class CategoryOut(BaseModel):
    id: int = 1
    name: str = "Category name"
    platform_id: int = 1

    model_config = ConfigDict(from_attributes=True)