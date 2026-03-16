from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session


class BaseRepository:
    model = None

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Any]:
        return self.db.query(self.model).all()

    def create(self, payload: BaseModel) -> Any:
        instance = self.model(**payload.model_dump())
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance
