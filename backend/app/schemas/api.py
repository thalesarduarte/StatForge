from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ApiEnvelope(BaseModel, Generic[T]):
    success: bool = True
    message: str = "ok"
    data: T


class ListEnvelope(BaseModel, Generic[T]):
    success: bool = True
    message: str = "ok"
    items: list[T] = Field(default_factory=list)
    total: int = 0
