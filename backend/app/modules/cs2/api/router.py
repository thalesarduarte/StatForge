from fastapi import APIRouter

from app.modules.cs2.schemas.profile import CS2Comparison, CS2PlayerProfile

router = APIRouter()


@router.get("/profiles/{handle}", response_model=CS2PlayerProfile)
def get_cs2_profile(handle: str) -> CS2PlayerProfile:
    return CS2PlayerProfile(
        handle=handle,
        region="sa",
        rank="level 10",
        maps=["Mirage", "Inferno"],
        kd=1.18,
        hs_percentage=46.2,
    )


@router.get("/compare/{left_handle}/{right_handle}", response_model=CS2Comparison)
def compare_cs2_players(left_handle: str, right_handle: str) -> CS2Comparison:
    return CS2Comparison(
        left_handle=left_handle,
        right_handle=right_handle,
        metrics={"kd": {"left": 1.22, "right": 1.10}, "hs_percentage": {"left": 48.0, "right": 42.5}},
    )
