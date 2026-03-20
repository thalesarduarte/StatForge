from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentLikeBase(BaseModel):
    comment_id: int
    user_id: int


class CommentLikeCreate(CommentLikeBase):
    pass


class CommentLikeRead(CommentLikeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
