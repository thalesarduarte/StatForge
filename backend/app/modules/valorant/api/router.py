from fastapi import APIRouter

from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.valorant.schemas.profile import (
    ValorantComparison,
    ValorantHistoryEntry,
    ValorantOverview,
    ValorantReferenceData,
)
from app.modules.valorant.services.profile_service import ValorantProfileService

router = APIRouter()
service = ValorantProfileService()


@router.get("/overview/{handle}", response_model=ApiEnvelope[ValorantOverview])
def get_valorant_profile(handle: str) -> dict:
    return item_response(service.get_overview(handle))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[ValorantComparison])
def compare_valorant_players(left_handle: str, right_handle: str) -> dict:
    return item_response(service.compare_players(left_handle, right_handle))


@router.get("/reference-data", response_model=ApiEnvelope[ValorantReferenceData])
def get_valorant_reference_data() -> dict:
    return item_response(service.get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[ValorantHistoryEntry])
def get_valorant_history(handle: str) -> dict:
    return list_response(service.get_recent_history(handle))
