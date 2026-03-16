from pydantic import BaseModel


class ValorantPlayerProfile(BaseModel):
    handle: str
    region: str
    rank: str
    agents: list[str]
    maps: list[str]
    core_stats: dict[str, float]


class ValorantComparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, dict[str, float]]
