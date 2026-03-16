from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.repositories.base import BaseRepository


class BadgeRepository(BaseRepository):
    model = Badge

    def __init__(self, db: Session) -> None:
        super().__init__(db)
