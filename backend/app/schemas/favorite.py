from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FavoriteBase(BaseModel):
    user_id: int
    target_type: str
    target_id: int
    note: str | None = None


class FavoriteCreate(FavoriteBase):
    pass


class FavoriteRead(FavoriteBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
