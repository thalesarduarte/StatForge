from fastapi import APIRouter

from app.api.responses import list_response
from app.schemas.activity import ActivityEventRead
from app.schemas.api import ListEnvelope
from app.services.activity_service import ActivityService

router = APIRouter()


@router.get("/feed", response_model=ListEnvelope[ActivityEventRead])
def activity_feed() -> dict:
    return list_response(ActivityService().list_feed())
