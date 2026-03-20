from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.follow_repository import FollowRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.follow import FollowCreate, FollowRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[FollowRead])
def list_follows(db: Session = Depends(get_db)) -> dict:
    return list_response(FollowRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[FollowRead], status_code=status.HTTP_201_CREATED)
def create_follow(payload: FollowCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(FollowRepository(db).create(payload), message="follow created")
