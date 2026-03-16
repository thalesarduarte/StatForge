from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.team_repository import TeamRepository
from app.schemas.team import TeamCreate, TeamRead

router = APIRouter()


@router.get("/", response_model=list[TeamRead])
def list_teams(db: Session = Depends(get_db)) -> list[TeamRead]:
    return TeamRepository(db).list_all()


@router.post("/", response_model=TeamRead, status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)) -> TeamRead:
    return TeamRepository(db).create(payload)
