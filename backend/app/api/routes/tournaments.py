from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.tournament_repository import TournamentRepository
from app.schemas.tournament import TournamentCreate, TournamentRead

router = APIRouter()


@router.get("/", response_model=list[TournamentRead])
def list_tournaments(db: Session = Depends(get_db)) -> list[TournamentRead]:
    return TournamentRepository(db).list_all()


@router.post("/", response_model=TournamentRead, status_code=status.HTTP_201_CREATED)
def create_tournament(payload: TournamentCreate, db: Session = Depends(get_db)) -> TournamentRead:
    return TournamentRepository(db).create(payload)
