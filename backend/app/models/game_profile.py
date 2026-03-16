from typing import Optional

from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class GameProfile(Base, TimestampMixin):
    __tablename__ = "game_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    game_slug: Mapped[str] = mapped_column(String(50), index=True)
    handle: Mapped[str] = mapped_column(String(120), index=True)
    region: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    external_player_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
