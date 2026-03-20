from datetime import datetime, timezone

from app.schemas.activity import ActivityEventRead


class ActivityService:
    def list_feed(self) -> list[ActivityEventRead]:
        return [
            ActivityEventRead(
                id=1,
                actor_id=12,
                verb="updated_profile",
                entity_type="game_profile",
                entity_id=44,
                summary="Player stats synchronized for the latest ranked session.",
                created_at=datetime.now(timezone.utc),
            ),
            ActivityEventRead(
                id=2,
                actor_id=3,
                verb="joined_team",
                entity_type="team",
                entity_id=9,
                summary="New roster activity detected in the competitive hub.",
                created_at=datetime.now(timezone.utc),
            ),
        ]
