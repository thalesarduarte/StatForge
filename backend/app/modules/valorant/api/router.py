from fastapi import APIRouter

from app.modules.valorant.schemas.profile import ValorantComparison, ValorantPlayerProfile

router = APIRouter()


@router.get("/profiles/{handle}", response_model=ValorantPlayerProfile)
def get_valorant_profile(handle: str) -> ValorantPlayerProfile:
    return ValorantPlayerProfile(
        handle=handle,
        region="na",
        rank="ascendant",
        agents=["Jett", "Sova", "Omen"],
        maps=["Ascent", "Bind"],
        core_stats={"kd": 1.21, "acs": 243.4, "headshot_percentage": 27.8},
    )


@router.get("/compare/{left_handle}/{right_handle}", response_model=ValorantComparison)
def compare_valorant_players(left_handle: str, right_handle: str) -> ValorantComparison:
    return ValorantComparison(
        left_handle=left_handle,
        right_handle=right_handle,
        metrics={"acs": {"left": 251.1, "right": 232.7}, "kd": {"left": 1.14, "right": 1.09}},
    )
