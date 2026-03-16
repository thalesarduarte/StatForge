from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TournamentBase(BaseModel):
    name: str
    game_slug: str
    starts_at: datetime
    status: str = "scheduled"
    description: str | None = None


class TournamentCreate(TournamentBase):
    pass


class TournamentRead(TournamentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
