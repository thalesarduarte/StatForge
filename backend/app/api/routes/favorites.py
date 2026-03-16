from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def list_favorites() -> list[dict[str, str]]:
    return [{"scope": "player", "status": "core-ready"}]
