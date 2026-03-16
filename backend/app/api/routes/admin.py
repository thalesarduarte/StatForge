from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
def admin_summary() -> dict[str, object]:
    return {
        "panels": ["users", "profiles", "comments", "teams", "tournaments", "badges"],
        "status": "bootstrap-ready",
    }
