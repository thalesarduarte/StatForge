from pydantic import BaseModel

from app.modules.shared import ComparisonMetric, MatchHistoryEntry, ReferenceData


class OverwatchOverview(BaseModel):
    handle: str
    platform: str
    region: str
    rank: str
    main_hero: str
    role_stats: dict[str, dict[str, float | int]]
    hero_stats: dict[str, dict[str, float | int]]
    recent_highlights: list[str]


class OverwatchComparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, ComparisonMetric]


class OverwatchHistoryEntry(MatchHistoryEntry):
    pass


class OverwatchReferenceData(ReferenceData):
    pass
