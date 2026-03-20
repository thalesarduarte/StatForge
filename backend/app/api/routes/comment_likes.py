from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.responses import item_response, list_response
from app.repositories.comment_like_repository import CommentLikeRepository
from app.schemas.api import ApiEnvelope, ListEnvelope
from app.schemas.comment_like import CommentLikeCreate, CommentLikeRead

router = APIRouter()


@router.get("/", response_model=ListEnvelope[CommentLikeRead])
def list_comment_likes(db: Session = Depends(get_db)) -> dict:
    return list_response(CommentLikeRepository(db).list_all())


@router.post("/", response_model=ApiEnvelope[CommentLikeRead], status_code=status.HTTP_201_CREATED)
def create_comment_like(payload: CommentLikeCreate, db: Session = Depends(get_db)) -> dict:
    return item_response(CommentLikeRepository(db).create(payload), message="comment like created")
