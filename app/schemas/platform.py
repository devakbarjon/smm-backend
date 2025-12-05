from pydantic import BaseModel, ConfigDict


class PlatformOut(BaseModel):
    id: int = 1
    name: str = "youtube"

    model_config = ConfigDict(from_attributes=True)