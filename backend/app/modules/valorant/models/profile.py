from sqlalchemy import ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class ValorantProfile(Base, TimestampMixin):
    __tablename__ = "valorant_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), unique=True, index=True)
    current_rank: Mapped[str] = mapped_column(String(50))
    favorite_agents: Mapped[list[str]] = mapped_column(JSON, default=list)
    core_stats: Mapped[dict] = mapped_column(JSON, default=dict)
    weapon_stats: Mapped[dict] = mapped_column(JSON, default=dict)
