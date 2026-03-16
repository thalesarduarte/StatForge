from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.follow_repository import FollowRepository
from app.schemas.follow import FollowCreate, FollowRead

router = APIRouter()


@router.get("/", response_model=list[FollowRead])
def list_follows(db: Session = Depends(get_db)) -> list[FollowRead]:
    return FollowRepository(db).list_all()


@router.post("/", response_model=FollowRead, status_code=status.HTTP_201_CREATED)
def create_follow(payload: FollowCreate, db: Session = Depends(get_db)) -> FollowRead:
    return FollowRepository(db).create(payload)
