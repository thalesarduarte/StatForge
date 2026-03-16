from pydantic import BaseModel


class CS2PlayerProfile(BaseModel):
    handle: str
    region: str
    rank: str
    maps: list[str]
    kd: float
    hs_percentage: float


class CS2Comparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, dict[str, float]]
