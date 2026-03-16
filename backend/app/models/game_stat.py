from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class GameStat(Base, TimestampMixin):
    __tablename__ = "game_stats"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), index=True)
    game_slug: Mapped[str] = mapped_column(String(50), index=True)
    stat_scope: Mapped[str] = mapped_column(String(50), index=True)
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
