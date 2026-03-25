from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.overwatch.schemas.profile import (
    OverwatchComparison,
    OverwatchHistoryEntry,
    OverwatchOverview,
    OverwatchReferenceData,
    OverwatchSyncRequest,
)
from app.modules.overwatch.services.profile_service import OverwatchProfileService
from app.modules.shared import SyncStatus

router = APIRouter()


@router.post("/sync", response_model=ApiEnvelope[SyncStatus])
def sync_overwatch_profile(payload: OverwatchSyncRequest, db: Session = Depends(get_db)) -> dict:
    return item_response(OverwatchProfileService(db).sync_profile(payload), message="overwatch profile synced")


@router.get("/overview/{handle}", response_model=ApiEnvelope[OverwatchOverview])
def get_overwatch_profile(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return item_response(OverwatchProfileService(db).get_overview(handle, refresh=refresh))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[OverwatchComparison])
def compare_overwatch_players(
    left_handle: str,
    right_handle: str,
    refresh: bool = Query(False),
    db: Session = Depends(get_db),
) -> dict:
    return item_response(OverwatchProfileService(db).compare_players(left_handle, right_handle, refresh=refresh))


@router.get("/reference-data", response_model=ApiEnvelope[OverwatchReferenceData])
def get_overwatch_reference_data(db: Session = Depends(get_db)) -> dict:
    return item_response(OverwatchProfileService(db).get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[OverwatchHistoryEntry])
def get_overwatch_history(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return list_response(OverwatchProfileService(db).get_recent_history(handle, refresh=refresh))
