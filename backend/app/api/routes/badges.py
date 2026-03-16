from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.badge_repository import BadgeRepository
from app.schemas.badge import BadgeCreate, BadgeRead

router = APIRouter()


@router.get("/", response_model=list[BadgeRead])
def list_badges(db: Session = Depends(get_db)) -> list[BadgeRead]:
    return BadgeRepository(db).list_all()


@router.post("/", response_model=BadgeRead, status_code=status.HTTP_201_CREATED)
def create_badge(payload: BadgeCreate, db: Session = Depends(get_db)) -> BadgeRead:
    return BadgeRepository(db).create(payload)
