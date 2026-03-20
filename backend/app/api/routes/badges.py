from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.badge_repository import BadgeRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.badge import BadgeCreate, BadgeRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[BadgeRead])
def list_badges(db: Session = Depends(get_db)) -> dict:
    return list_response(BadgeRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[BadgeRead], status_code=status.HTTP_201_CREATED)
def create_badge(payload: BadgeCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(BadgeRepository(db).create(payload), message="badge created")
