from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class OverwatchProfile(Base, TimestampMixin):
    __tablename__ = "overwatch_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), unique=True, index=True)
    current_rank: Mapped[str] = mapped_column(String(50))
    main_hero: Mapped[str] = mapped_column(String(80))
    role_stats: Mapped[dict] = mapped_column(JSON, default=dict)
