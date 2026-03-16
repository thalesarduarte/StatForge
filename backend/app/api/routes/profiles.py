from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreate, ProfileRead

router = APIRouter()


@router.get("/", response_model=list[ProfileRead])
def list_profiles(db: Session = Depends(get_db)) -> list[ProfileRead]:
    return ProfileRepository(db).list_all()


@router.post("/", response_model=ProfileRead)
def create_profile(payload: ProfileCreate, db: Session = Depends(get_db)) -> ProfileRead:
    return ProfileRepository(db).create(payload)
