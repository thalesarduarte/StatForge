from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import Base
from app.models.mixins import TimestampMixin


class CS2Profile(Base, TimestampMixin):
    __tablename__ = "cs2_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    game_profile_id: Mapped[int] = mapped_column(ForeignKey("game_profiles.id"), unique=True, index=True)
    current_rank: Mapped[str] = mapped_column(String(50))
    kd: Mapped[float] = mapped_column(Float, default=0.0)
    hs_percentage: Mapped[float] = mapped_column(Float, default=0.0)
