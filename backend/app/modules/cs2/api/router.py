from fastapi import APIRouter

from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.cs2.schemas.profile import CS2Comparison, CS2HistoryEntry, CS2Overview, CS2ReferenceData
from app.modules.cs2.services.profile_service import CS2ProfileService

router = APIRouter()
service = CS2ProfileService()


@router.get("/overview/{handle}", response_model=ApiEnvelope[CS2Overview])
def get_cs2_profile(handle: str) -> dict:
    return item_response(service.get_overview(handle))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[CS2Comparison])
def compare_cs2_players(left_handle: str, right_handle: str) -> dict:
    return item_response(service.compare_players(left_handle, right_handle))


@router.get("/reference-data", response_model=ApiEnvelope[CS2ReferenceData])
def get_cs2_reference_data() -> dict:
    return item_response(service.get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[CS2HistoryEntry])
def get_cs2_history(handle: str) -> dict:
    return list_response(service.get_recent_history(handle))
