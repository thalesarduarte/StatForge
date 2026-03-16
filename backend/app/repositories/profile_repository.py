from sqlalchemy.orm import Session

from app.models.profile import Profile
from app.repositories.base import BaseRepository


class ProfileRepository(BaseRepository):
    model = Profile

    def __init__(self, db: Session) -> None:
        super().__init__(db)
