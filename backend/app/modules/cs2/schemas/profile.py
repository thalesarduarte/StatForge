from pydantic import BaseModel

from app.modules.shared import ComparisonMetric, MatchHistoryEntry, ReferenceData


class CS2Overview(BaseModel):
    handle: str
    region: str
    rank: str
    maps: list[str]
    kd: float
    hs_percentage: float
    adr: float
    weapons: list[str]
    recent_highlights: list[str]


class CS2Comparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, ComparisonMetric]


class CS2HistoryEntry(MatchHistoryEntry):
    pass


class CS2ReferenceData(ReferenceData):
    pass
