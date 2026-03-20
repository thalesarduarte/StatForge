from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.comment_repository import CommentRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[CommentRead])
def list_comments(db: Session = Depends(get_db)) -> dict:
    return list_response(CommentRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[CommentRead], status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(CommentRepository(db).create(payload), message="comment created")
