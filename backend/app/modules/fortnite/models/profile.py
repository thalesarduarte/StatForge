from sqlalchemy import Float, ForeignKey, JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class FortniteProfile(Base, TimestampMixin):
    __tablename__ = "fortnite_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), unique=True, index=True)
    platform: Mapped[str] = mapped_column(String(40))
    victories: Mapped[int] = mapped_column(Integer, default=0)
    kills: Mapped[int] = mapped_column(Integer, default=0)
    kd: Mapped[float] = mapped_column(Float, default=0.0)
    mode_breakdown: Mapped[dict] = mapped_column(JSON, default=dict)
