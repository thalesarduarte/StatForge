from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BadgeBase(BaseModel):
    name: str
    slug: str
    description: str | None = None


class BadgeCreate(BadgeBase):
    pass


class BadgeRead(BadgeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
