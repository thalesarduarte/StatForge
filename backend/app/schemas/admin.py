from pydantic import BaseModel


class AdminSummary(BaseModel):
    panels: list[str]
    total_games: int
    health: str
