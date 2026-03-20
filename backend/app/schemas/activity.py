from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityEventRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor_id: int | None = None
    verb: str
    entity_type: str
    entity_id: int | None = None
    summary: str
    created_at: datetime
