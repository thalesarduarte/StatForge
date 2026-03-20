from datetime import datetime, timezone

from app.schemas.favorite import FavoriteRead


class FavoriteService:
    def list_favorites(self) -> list[FavoriteRead]:
        return [
            FavoriteRead(
                id=1,
                user_id=1,
                target_type="player",
                target_id=101,
                note="High priority tracked player",
                created_at=datetime.now(timezone.utc),
            ),
            FavoriteRead(
                id=2,
                user_id=1,
                target_type="team",
                target_id=8,
                note="Regional rival team",
                created_at=datetime.now(timezone.utc),
            ),
        ]
