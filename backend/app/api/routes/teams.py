from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.team_repository import TeamRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.team import TeamCreate, TeamRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[TeamRead])
def list_teams(db: Session = Depends(get_db)) -> dict:
    return list_response(TeamRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[TeamRead], status_code=status.HTTP_201_CREATED)
def create_team(payload: TeamCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(TeamRepository(db).create(payload), message="team created")
