from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class Favorite(Base, TimestampMixin):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    target_type: Mapped[str] = mapped_column(String(50), index=True)
    target_id: Mapped[int] = mapped_column(index=True)
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
