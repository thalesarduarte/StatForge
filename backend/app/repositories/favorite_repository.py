from sqlalchemy.orm import Session

from app.models.favorite import Favorite
from app.repositories.base import BaseRepository


class FavoriteRepository(BaseRepository):
    model = Favorite

    def __init__(self, db: Session) -> None:
        super().__init__(db)
