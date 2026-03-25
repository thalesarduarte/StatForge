from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.overwatch.integrations.client import OverwatchIntegrationClient
from app.modules.overwatch.models.profile import OverwatchProfile
from app.modules.overwatch.schemas.profile import (
    OverwatchComparison,
    OverwatchHistoryEntry,
    OverwatchOverview,
    OverwatchReferenceData,
    OverwatchSyncRequest,
)
from app.modules.shared import SyncStatus
from app.modules.storage import GameModuleStorage
from app.utils.dicts import get_in


class OverwatchProfileService:
    game_slug = "overwatch"
    provider_slug = "overfast"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client = OverwatchIntegrationClient()
        self.storage = GameModuleStorage(db)

    def sync_profile(self, payload: OverwatchSyncRequest) -> SyncStatus:
        summary = self.client.fetch_summary(payload.handle)
        stats = self.client.fetch_stats_summary(payload.handle)
        reference = self.client.fetch_reference_data()

        role_stats = get_in(stats, ["competitive", "career_stats"], default={}) or {}
        hero_stats = get_in(stats, ["competitive", "heroes"], default={}) or {}
        main_hero = next(iter(hero_stats.keys()), payload.handle.split("-")[0])
        display_name = get_in(summary, ["username"], default=payload.handle)
        region = get_in(summary, ["platform"], default="global")

        overview_payload = {
            "handle": payload.handle,
            "platform": get_in(summary, ["platform"], default="pc"),
            "region": region,
            "rank": self._extract_rank(summary),
            "main_hero": main_hero,
            "role_stats": role_stats,
            "hero_stats": hero_stats,
            "recent_highlights": [
                f"Synced from {self.provider_slug}",
                f"Primary competitive rank: {self._extract_rank(summary)}",
                "Recent match history is limited by provider availability for Overwatch.",
            ],
        }
        reference_payload = self._reference_payload(reference)

        persisted = self.storage.persist_snapshot(
            game_slug=self.game_slug,
            handle=payload.handle,
            display_name=display_name,
            provider_slug=self.provider_slug,
            region=region,
            external_player_id=payload.handle,
            metadata_json={"summary": summary, "stats": stats},
            stats_scopes={
                "overview": overview_payload,
                "reference_data": reference_payload,
            },
            matches=[],
        )

        self._upsert_module_profile(
            game_profile_id=persisted["profile"].id,
            rank=overview_payload["rank"],
            main_hero=main_hero,
            role_stats=role_stats,
            hero_stats=hero_stats,
        )

        return SyncStatus(
            game_slug=self.game_slug,
            handle=payload.handle,
            provider=self.provider_slug,
            synced_at=persisted["synced_at"],
        )

    def get_overview(self, handle: str, refresh: bool = False) -> OverwatchOverview:
        if refresh:
            self.sync_profile(OverwatchSyncRequest(handle=handle))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return OverwatchOverview(**snapshot["overview"])

    def compare_players(self, left_handle: str, right_handle: str, refresh: bool = False) -> OverwatchComparison:
        left = self.get_overview(left_handle, refresh=refresh)
        right = self.get_overview(right_handle, refresh=refresh)
        return OverwatchComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "rank_score": {
                    "left": self._rank_score(left.rank),
                    "right": self._rank_score(right.rank),
                    "better": left_handle if self._rank_score(left.rank) >= self._rank_score(right.rank) else right_handle,
                },
                "hero_pool": {
                    "left": len(left.hero_stats),
                    "right": len(right.hero_stats),
                    "better": left_handle if len(left.hero_stats) >= len(right.hero_stats) else right_handle,
                },
            },
        )

    def get_reference_data(self) -> OverwatchReferenceData:
        reference = self.client.fetch_reference_data()
        return OverwatchReferenceData(**self._reference_payload(reference))

    def get_recent_history(self, handle: str, refresh: bool = False) -> list[OverwatchHistoryEntry]:
        if refresh:
            self.sync_profile(OverwatchSyncRequest(handle=handle))
        return []

    def _extract_rank(self, summary: dict) -> str:
        competitive = get_in(summary, ["competitive"], default={}) or {}
        if isinstance(competitive, dict):
            for platform_data in competitive.values():
                if isinstance(platform_data, dict):
                    for role_data in platform_data.values():
                        rank = get_in(role_data, ["division"], default=None)
                        tier = get_in(role_data, ["tier"], default=None)
                        if rank and tier:
                            return f"{tier} {rank}"
        return "Unranked"

    def _reference_payload(self, reference: dict) -> dict:
        return {
            "maps": [item.get("name", "") for item in reference.get("maps", []) if item.get("name")],
            "roles_or_modes": [
                *[item.get("name", "") for item in reference.get("roles", []) if item.get("name")],
                *[item.get("name", "") for item in reference.get("modes", []) if item.get("name")],
            ],
            "roster_or_characters": [item.get("name", "") for item in reference.get("heroes", []) if item.get("name")],
            "ranks": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"],
        }

    def _upsert_module_profile(
        self,
        *,
        game_profile_id: int,
        rank: str,
        main_hero: str,
        role_stats: dict,
        hero_stats: dict,
    ) -> None:
        record = self.db.query(OverwatchProfile).filter(OverwatchProfile.game_profile_id == game_profile_id).first()
        if record is None:
            record = OverwatchProfile(
                game_profile_id=game_profile_id,
                current_rank=rank,
                main_hero=main_hero,
                role_stats=role_stats,
                hero_stats=hero_stats,
            )
            self.db.add(record)
        else:
            record.current_rank = rank
            record.main_hero = main_hero
            record.role_stats = role_stats
            record.hero_stats = hero_stats
        self.db.commit()

    def _rank_score(self, rank: str) -> int:
        mapping = {
            "Unranked": 0,
            "Bronze": 1,
            "Silver": 2,
            "Gold": 3,
            "Platinum": 4,
            "Diamond": 5,
            "Master": 6,
            "Grandmaster": 7,
        }
        for label, score in mapping.items():
            if rank.startswith(label):
                return score
        return 0
