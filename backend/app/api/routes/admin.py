from fastapi import APIRouter

from app.api.responses import item_response
from app.schemas.admin import AdminSummary
from app.schemas.api import ApiEnvelope

router = APIRouter()


@router.get("/summary", response_model=ApiEnvelope[AdminSummary])
def admin_summary() -> dict:
    return item_response(
        AdminSummary(
            panels=[
                "users",
                "profiles",
                "comments",
                "comment_likes",
                "favorites",
                "teams",
                "tournaments",
                "activity",
            ],
            total_games=5,
            health="bootstrap-ready",
        )
    )
