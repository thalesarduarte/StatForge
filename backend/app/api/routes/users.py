from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import list_response
from app.repositories.user_repository import UserRepository
from app.schemas.api import ListEnvelope
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[UserRead])
def list_users(db: Session = Depends(get_db)) -> dict:
    return list_response(UserRepository(db).list_all())
