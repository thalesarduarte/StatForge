from sqlalchemy.orm import Session

from app.models.team import Team
from app.repositories.base import BaseRepository


class TeamRepository(BaseRepository):
    model = Team

    def __init__(self, db: Session) -> None:
        super().__init__(db)
