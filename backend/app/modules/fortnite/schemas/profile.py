from pydantic import BaseModel

from app.modules.shared import ComparisonMetric, MatchHistoryEntry, ReferenceData


class FortniteOverview(BaseModel):
    handle: str
    platform: str
    victories: int
    kills: int
    kd: float
    preferred_modes: list[str]
    recent_highlights: list[str]


class FortniteComparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, ComparisonMetric]


class FortniteHistoryEntry(MatchHistoryEntry):
    pass


class FortniteReferenceData(ReferenceData):
    pass
