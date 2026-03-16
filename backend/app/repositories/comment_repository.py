from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.repositories.base import BaseRepository


class CommentRepository(BaseRepository):
    model = Comment

    def __init__(self, db: Session) -> None:
        super().__init__(db)
