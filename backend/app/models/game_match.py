from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class GameMatch(Base, TimestampMixin):
    __tablename__ = "game_matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), index=True)
    game_slug: Mapped[str] = mapped_column(String(50), index=True)
    external_match_id: Mapped[str] = mapped_column(String(120), index=True)
    played_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
