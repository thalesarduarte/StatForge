from fastapi import APIRouter

from app.modules.overwatch.schemas.profile import OverwatchComparison, OverwatchPlayerProfile

router = APIRouter()


@router.get("/profiles/{handle}", response_model=OverwatchPlayerProfile)
def get_overwatch_profile(handle: str) -> OverwatchPlayerProfile:
    return OverwatchPlayerProfile(
        handle=handle,
        platform="pc",
        region="global",
        rank="diamond",
        main_hero="Tracer",
        role_stats={"tank": {"wins": 12}, "damage": {"wins": 28}, "support": {"wins": 16}},
        heroes=["Tracer", "Ana", "Winston"],
        maps=["King's Row", "Route 66"],
        modes=["Competitive", "Quick Play"],
    )


@router.get("/compare/{left_handle}/{right_handle}", response_model=OverwatchComparison)
def compare_overwatch_players(left_handle: str, right_handle: str) -> OverwatchComparison:
    return OverwatchComparison(
        left_handle=left_handle,
        right_handle=right_handle,
        metrics={"win_rate": {"left": 55.4, "right": 52.8}, "eliminations": {"left": 18.2, "right": 16.7}},
    )
