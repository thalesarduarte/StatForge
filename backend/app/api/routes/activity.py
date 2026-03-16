from fastapi import APIRouter

router = APIRouter()


@router.get("/feed")
def activity_feed() -> list[dict[str, str]]:
    return [{"type": "system", "message": "Activity feed bootstrap ready"}]
