from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.modules.cs2.schemas.profile import CS2Comparison, CS2HistoryEntry, CS2Overview, CS2ReferenceData, CS2SyncRequest
from app.modules.cs2.services.profile_service import CS2ProfileService
from app.modules.shared import SyncStatus

router = APIRouter()


@router.post("/sync", response_model=ApiEnvelope[SyncStatus])
def sync_cs2_profile(payload: CS2SyncRequest, db: Session = Depends(get_db)) -> dict:
    return item_response(CS2ProfileService(db).sync_profile(payload), message="cs2 profile synced")


@router.get("/overview/{handle}", response_model=ApiEnvelope[CS2Overview])
def get_cs2_profile(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return item_response(CS2ProfileService(db).get_overview(handle, refresh=refresh))


@router.get("/compare/{left_handle}/{right_handle}", response_model=ApiEnvelope[CS2Comparison])
def compare_cs2_players(
    left_handle: str,
    right_handle: str,
    refresh: bool = Query(False),
    db: Session = Depends(get_db),
) -> dict:
    return item_response(CS2ProfileService(db).compare_players(left_handle, right_handle, refresh=refresh))


@router.get("/reference-data", response_model=ApiEnvelope[CS2ReferenceData])
def get_cs2_reference_data(db: Session = Depends(get_db)) -> dict:
    return item_response(CS2ProfileService(db).get_reference_data())


@router.get("/history/{handle}", response_model=ListEnvelope[CS2HistoryEntry])
def get_cs2_history(handle: str, refresh: bool = Query(False), db: Session = Depends(get_db)) -> dict:
    return list_response(CS2ProfileService(db).get_recent_history(handle, refresh=refresh))
