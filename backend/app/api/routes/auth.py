from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.api.responses import item_response
from app.schemas.api import ApiEnvelope
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=ApiEnvelope[UserRead], status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)) -> dict:
    service = AuthService(db)
    return item_response(service.register_user(payload), message="user registered")


@router.post("/login", response_model=ApiEnvelope[Token])
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    service = AuthService(db)
    token = service.authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return item_response(token, message="authenticated")


@router.get("/me", response_model=ApiEnvelope[UserRead])
def me(current_user=Depends(get_current_user)) -> dict:
    return item_response(current_user)
