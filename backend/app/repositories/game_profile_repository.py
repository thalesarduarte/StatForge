from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.game_profile import GameProfile


class GameProfileRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_game_and_handle(self, game_slug: str, handle: str) -> GameProfile | None:
        return (
            self.db.query(GameProfile)
            .filter(GameProfile.game_slug == game_slug, GameProfile.handle == handle)
            .first()
        )

    def upsert(
        self,
        *,
        game_slug: str,
        handle: str,
        display_name: str,
        provider_slug: str,
        region: str | None,
        external_player_id: str | None,
        metadata_json: dict,
    ) -> GameProfile:
        instance = self.get_by_game_and_handle(game_slug, handle)
        if instance is None:
            instance = GameProfile(
                game_slug=game_slug,
                handle=handle,
                display_name=display_name,
                provider_slug=provider_slug,
                region=region,
                external_player_id=external_player_id,
                metadata_json=metadata_json,
            )
            self.db.add(instance)
        else:
            instance.display_name = display_name
            instance.provider_slug = provider_slug
            instance.region = region
            instance.external_player_id = external_player_id
            instance.metadata_json = metadata_json

        instance.last_synced_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(instance)
        return instance
