from sqlalchemy.orm import Session

from app.models.comment_like import CommentLike
from app.repositories.base import BaseRepository


class CommentLikeRepository(BaseRepository):
    model = CommentLike

    def __init__(self, db: Session) -> None:
        super().__init__(db)
