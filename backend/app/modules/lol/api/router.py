from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.lol.schemas.profile import (
    LolComparison,
    LolHistoryEntry,
    LolOverview,
    LolReferenceData,
    LolSyncRequest,
)
from app.modules.lol.services.profile_service import LolProfileService
from app.modules.shared import SyncStatus

router = APIRouter()


@router.post("/sync", response_model=ApiEnvelope[SyncStatus])
def sync_lol_profile(payload: LolSyncRequest, db: Session = Depends(get_db)) -> dict:
    return item_response(LolProfileService(db).sync_profile(payload), message="lol profile synced")


@router.get("/overview/{summoner_name}", response_model=ApiEnvelope[LolOverview])
def get_lol_overview(summoner_name: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return item_response(LolProfileService(db).get_overview(summoner_name, refresh=refresh))


@router.get("/compare/{left_name}/{right_name}", response_model=ApiEnvelope[LolComparison])
def compare_lol_players(
    left_name: str,
    right_name: str,
    refresh: bool = Query(False),
    db: Session = Depends(get_db),
) -> dict:
    return item_response(LolProfileService(db).compare_players(left_name, right_name, refresh=refresh))


@router.get("/reference-data", response_model=ApiEnvelope[LolReferenceData])
def get_lol_reference_data(db: Session = Depends(get_db)) -> dict:
    return item_response(LolProfileService(db).get_reference_data())


@router.get("/history/{summoner_name}", response_model=ListEnvelope[LolHistoryEntry])
def get_lol_history(summoner_name: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return list_response(LolProfileService(db).get_recent_history(summoner_name, refresh=refresh))
