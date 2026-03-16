from pydantic import BaseModel


class OverwatchPlayerProfile(BaseModel):
    handle: str
    platform: str
    region: str
    rank: str
    main_hero: str
    role_stats: dict[str, dict[str, float | int]]
    heroes: list[str]
    maps: list[str]
    modes: list[str]


class OverwatchComparison(BaseModel):
    left_handle: str
    right_handle: str
    metrics: dict[str, dict[str, float]]
