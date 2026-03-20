from fastapi import APIRouter

from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.lol.schemas.profile import (
    LolComparison,
    LolHistoryEntry,
    LolOverview,
    LolReferenceData,
)
from app.modules.lol.services.profile_service import LolProfileService

router = APIRouter()
service = LolProfileService()


@router.get("/overview/{summoner_name}", response_model=ApiEnvelope[LolOverview])
def get_lol_overview(summoner_name: str) -> dict:
    return item_response(service.get_overview(summoner_name))


@router.get("/compare/{left_name}/{right_name}", response_model=ApiEnvelope[LolComparison])
def compare_lol_players(left_name: str, right_name: str) -> dict:
    return item_response(service.compare_players(left_name, right_name))


@router.get("/reference-data", response_model=ApiEnvelope[LolReferenceData])
def get_lol_reference_data() -> dict:
    return item_response(service.get_reference_data())


@router.get("/history/{summoner_name}", response_model=ListEnvelope[LolHistoryEntry])
def get_lol_history(summoner_name: str) -> dict:
    return list_response(service.get_recent_history(summoner_name))
