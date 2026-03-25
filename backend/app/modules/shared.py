from datetime import datetime

from pydantic import BaseModel


class MatchHistoryEntry(BaseModel):
    match_id: str
    result: str
    mode: str
    map_name: str
    played_at: datetime
    stats: dict[str, float | int | str]


class ComparisonMetric(BaseModel):
    left: float | int
    right: float | int
    better: str


class ReferenceData(BaseModel):
    maps: list[str]
    roles_or_modes: list[str]
    roster_or_characters: list[str]
    ranks: list[str]


class SyncStatus(BaseModel):
    game_slug: str
    handle: str
    provider: str
    synced_at: datetime


class SearchResult(BaseModel):
    handle: str
    display_name: str
    platform_or_region: str | None = None
    external_player_id: str | None = None
