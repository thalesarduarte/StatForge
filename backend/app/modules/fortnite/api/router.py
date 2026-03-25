from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.fortnite.schemas.profile import (
    FortniteComparison,
    FortniteHistoryEntry,
    FortniteOverview,
    FortniteReferenceData,
    FortniteSyncRequest,
)
from app.modules.fortnite.services.profile_service import FortniteProfileService
from app.modules.shared import SyncStatus

router = APIRouter()


@router.post("/sync", response_model=ApiEnvelope[SyncStatus])
def sync_fortnite_profile(payload: FortniteSyncRequest, db: Session = Depends(get_db)) -> dict:
    return item_response(FortniteProfileService(db).sync_profile(payload), message="fortnite profile synced")


@router.get("/overview/{handle}", response_model=ApiEnvelope[FortniteOverview])
def get_fortnite_overview(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return item_response(FortniteProfileService(db).get_overview(handle, refresh=refresh))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[FortniteComparison])
def compare_fortnite_players(
    left_handle: str,
    right_handle: str,
    refresh: bool = Query(False),
    db: Session = Depends(get_db),
) -> dict:
    return item_response(FortniteProfileService(db).compare_players(left_handle, right_handle, refresh=refresh))


@router.get("/reference-data", response_model=ApiEnvelope[FortniteReferenceData])
def get_fortnite_reference_data(db: Session = Depends(get_db)) -> dict:
    return item_response(FortniteProfileService(db).get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[FortniteHistoryEntry])
def get_fortnite_history(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return list_response(FortniteProfileService(db).get_recent_history(handle, refresh=refresh))
