from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.repositories.comment_repository import CommentRepository
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter()


@router.get("/", response_model=list[CommentRead])
def list_comments(db: Session = Depends(get_db)) -> list[CommentRead]:
    return CommentRepository(db).list_all()


@router.post("/", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db)) -> CommentRead:
    return CommentRepository(db).create(payload)
