from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.favorite_repository import FavoriteRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.favorite import FavoriteCreate, FavoriteRead
from app.services.favorite_service import FavoriteService

router = APIRouter()


@router.get("/", response_model=ListEnvelope[FavoriteRead])
def list_favorites() -> dict:
    return list_response(FavoriteService().list_favorites())


@router.post("/", response_model=ApiEnvelope[FavoriteRead], status_code=status.HTTP_201_CREATED)
def create_favorite(payload: FavoriteCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(FavoriteRepository(db).create(payload), message="favorite created")
