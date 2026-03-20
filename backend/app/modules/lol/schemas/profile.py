from pydantic import BaseModel

from app.modules.shared import ComparisonMetric, MatchHistoryEntry, ReferenceData


class LolOverview(BaseModel):
    summoner_name: str
    server: str
    elo: str
    primary_role: str
    preferred_champions: list[str]
    core_stats: dict[str, float]
    recent_highlights: list[str]


class LolComparison(BaseModel):
    left_name: str
    right_name: str
    metrics: dict[str, ComparisonMetric]


class LolHistoryEntry(MatchHistoryEntry):
    pass


class LolReferenceData(ReferenceData):
    pass
