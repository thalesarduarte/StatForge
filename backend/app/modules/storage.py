from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import ResourceNotFoundError
from app.repositories.game_match_repository import GameMatchRepository
from app.repositories.game_profile_repository import GameProfileRepository
from app.repositories.game_stat_repository import GameStatRepository


class GameModuleStorage:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.profile_repository = GameProfileRepository(db)
        self.stat_repository = GameStatRepository(db)
        self.match_repository = GameMatchRepository(db)

    def persist_snapshot(
        self,
        *,
        game_slug: str,
        handle: str,
        display_name: str,
        provider_slug: str,
        region: str | None,
        external_player_id: str | None,
        metadata_json: dict,
        stats_scopes: dict[str, dict],
        matches: list[dict],
    ) -> dict:
        profile = self.profile_repository.upsert(
            game_slug=game_slug,
            handle=handle,
            display_name=display_name,
            provider_slug=provider_slug,
            region=region,
            external_player_id=external_player_id,
            metadata_json=metadata_json,
        )
        self.stat_repository.replace_scopes(profile.id, game_slug, stats_scopes)
        self.match_repository.replace_matches(profile.id, game_slug, matches)
        return {
            "profile": profile,
            "synced_at": profile.last_synced_at or datetime.now(timezone.utc),
        }

    def load_snapshot(self, game_slug: str, handle: str) -> dict:
        profile = self.profile_repository.get_by_game_and_handle(game_slug, handle)
        if profile is None:
            raise ResourceNotFoundError(f"No cached data found for {game_slug}:{handle}")

        overview = self.stat_repository.get_scope(profile.id, "overview")
        reference_data = self.stat_repository.get_scope(profile.id, "reference_data")
        history = self.match_repository.list_recent(profile.id)

        return {
            "profile": profile,
            "overview": overview.payload if overview else {},
            "reference_data": reference_data.payload if reference_data else {},
            "history": history,
        }
