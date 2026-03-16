from sqlalchemy.orm import Session

from app.models.follow import Follow
from app.repositories.base import BaseRepository


class FollowRepository(BaseRepository):
    model = Follow

    def __init__(self, db: Session) -> None:
        super().__init__(db)
