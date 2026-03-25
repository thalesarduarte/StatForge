from typing import Optional

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class GameProfile(Base, TimestampMixin):
    __tablename__ = "game_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    game_slug: Mapped[str] = mapped_column(String(50), index=True)
    handle: Mapped[str] = mapped_column(String(120), index=True)
    display_name: Mapped[str] = mapped_column(String(120), index=True)
    provider_slug: Mapped[str] = mapped_column(String(50), index=True)
    region: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    external_player_id: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
