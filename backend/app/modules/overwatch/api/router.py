from fastapi import APIRouter

from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.overwatch.schemas.profile import (
    OverwatchComparison,
    OverwatchHistoryEntry,
    OverwatchOverview,
    OverwatchReferenceData,
)
from app.modules.overwatch.services.profile_service import OverwatchProfileService

router = APIRouter()
service = OverwatchProfileService()


@router.get("/overview/{handle}", response_model=ApiEnvelope[OverwatchOverview])
def get_overwatch_profile(handle: str) -> dict:
    return item_response(service.get_overview(handle))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[OverwatchComparison])
def compare_overwatch_players(left_handle: str, right_handle: str) -> dict:
    return item_response(service.compare_players(left_handle, right_handle))


@router.get("/reference-data", response_model=ApiEnvelope[OverwatchReferenceData])
def get_overwatch_reference_data() -> dict:
    return item_response(service.get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[OverwatchHistoryEntry])
def get_overwatch_history(handle: str) -> dict:
    return list_response(service.get_recent_history(handle))
