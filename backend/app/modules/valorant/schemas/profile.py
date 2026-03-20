from pydantic import BaseModel

from app.modules.shared import ComparisonMetric, MatchHistoryEntry, ReferenceData


class ValorantOverview(BaseModel):
    handle: str
    region: str
    rank: str
    agents: list[str]
    weapons: list[str]
    core_stats: dict[str, float]
    recent_highlights: list[str]


class ValorantComparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, ComparisonMetric]


class ValorantHistoryEntry(MatchHistoryEntry):
    pass


class ValorantReferenceData(ReferenceData):
    pass
