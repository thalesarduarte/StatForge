from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentBase(BaseModel):
    author_id: int
    profile_id: int | None = None
    target_type: str
    target_id: int
    content: str


class CommentCreate(CommentBase):
    pass


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
