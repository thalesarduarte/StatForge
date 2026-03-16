from datetime import datetime

from pydantic import BaseModel, ConfigDict


class FollowBase(BaseModel):
    follower_id: int
    following_id: int


class FollowCreate(FollowBase):
    pass


class FollowRead(FollowBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
