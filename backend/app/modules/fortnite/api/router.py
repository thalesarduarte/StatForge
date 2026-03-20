from fastapi import APIRouter

from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.fortnite.schemas.profile import (
    FortniteComparison,
    FortniteHistoryEntry,
    FortniteOverview,
    FortniteReferenceData,
)
from app.modules.fortnite.services.profile_service import FortniteProfileService

router = APIRouter()
service = FortniteProfileService()


@router.get("/overview/{handle}", response_model=ApiEnvelope[FortniteOverview])
def get_fortnite_overview(handle: str) -> dict:
    return item_response(service.get_overview(handle))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[FortniteComparison])
def compare_fortnite_players(left_handle: str, right_handle: str) -> dict:
    return item_response(service.compare_players(left_handle, right_handle))


@router.get("/reference-data", response_model=ApiEnvelope[FortniteReferenceData])
def get_fortnite_reference_data() -> dict:
    return item_response(service.get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[FortniteHistoryEntry])
def get_fortnite_history(handle: str) -> dict:
    return list_response(service.get_recent_history(handle))
