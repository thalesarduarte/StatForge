from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.tournament_repository import TournamentRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.tournament import TournamentCreate, TournamentRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[TournamentRead])
def list_tournaments(db: Session = Depends(get_db)) -> dict:
    return list_response(TournamentRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[TournamentRead], status_code=status.HTTP_201_CREATED)
def create_tournament(payload: TournamentCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(TournamentRepository(db).create(payload), message="tournament created")
