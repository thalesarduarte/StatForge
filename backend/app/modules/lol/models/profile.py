from sqlalchemy import Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class LolProfile(Base, TimestampMixin):
    __tablename__ = "lol_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), unique=True, index=True)
    current_elo: Mapped[str] = mapped_column(String(60))
    primary_role: Mapped[str] = mapped_column(String(40))
    champion_pool: Mapped[list[str]] = mapped_column(JSON, default=list)
    core_stats: Mapped[dict] = mapped_column(JSON, default=dict)
