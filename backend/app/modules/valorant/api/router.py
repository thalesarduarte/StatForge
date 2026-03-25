from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.valorant.schemas.profile import (
    ValorantComparison,
    ValorantHistoryEntry,
    ValorantOverview,
    ValorantReferenceData,
    ValorantSyncRequest,
)
from app.modules.valorant.services.profile_service import ValorantProfileService
from app.modules.shared import SyncStatus

router = APIRouter()


@router.post("/sync", response_model=ApiEnvelope[SyncStatus])
def sync_valorant_profile(payload: ValorantSyncRequest, db: Session = Depends(get_db)) -> dict:
    return item_response(ValorantProfileService(db).sync_profile(payload), message="valorant profile synced")


@router.get("/overview/{handle}", response_model=ApiEnvelope[ValorantOverview])
def get_valorant_profile(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return item_response(ValorantProfileService(db).get_overview(handle, refresh=refresh))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[ValorantComparison])
def compare_valorant_players(
    left_handle: str,
    right_handle: str,
    refresh: bool = Query(False),
    db: Session = Depends(get_db),
) -> dict:
    return item_response(ValorantProfileService(db).compare_players(left_handle, right_handle, refresh=refresh))


@router.get("/reference-data", response_model=ApiEnvelope[ValorantReferenceData])
def get_valorant_reference_data(db: Session = Depends(get_db)) -> dict:
    return item_response(ValorantProfileService(db).get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[ValorantHistoryEntry])
def get_valorant_history(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return list_response(ValorantProfileService(db).get_recent_history(handle, refresh=refresh))
