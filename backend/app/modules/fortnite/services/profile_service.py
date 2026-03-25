from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.fortnite.integrations.client import FortniteIntegrationClient
from app.modules.fortnite.models.profile import FortniteProfile
from app.modules.fortnite.schemas.profile import (
    FortniteComparison,
    FortniteHistoryEntry,
    FortniteOverview,
    FortniteReferenceData,
    FortniteSyncRequest,
)
from app.modules.shared import SyncStatus
from app.modules.storage import GameModuleStorage
from app.utils.dicts import get_in


class FortniteProfileService:
    game_slug = "fortnite"
    provider_slug = "fortnite-api"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client = FortniteIntegrationClient()
        self.storage = GameModuleStorage(db)

    def sync_profile(self, payload: FortniteSyncRequest) -> SyncStatus:
        stats = self.client.fetch_stats(payload.name, payload.account_type)
        playlists = self.client.fetch_reference_data()

        data = stats.get("data", {})
        all_stats = get_in(data, ["stats", "all", "overall"], default={}) or {}
        handle = payload.name
        overview_payload = {
            "handle": handle,
            "platform": data.get("account", {}).get("type", payload.account_type),
            "victories": int(all_stats.get("wins", 0) or 0),
            "kills": int(all_stats.get("kills", 0) or 0),
            "kd": float(all_stats.get("kd", 0) or 0),
            "preferred_modes": [playlist.get("name", "") for playlist in playlists.get("data", [])[:5] if playlist.get("name")],
            "recent_highlights": [
                "Tracked from Fortnite-API",
                f"Lifetime wins: {all_stats.get('wins', 0)}",
                f"Lifetime KD: {all_stats.get('kd', 0)}",
            ],
        }
        reference_payload = {
            "maps": ["Battle Royale Island"],
            "roles_or_modes": [playlist.get("name", "") for playlist in playlists.get("data", [])[:10] if playlist.get("name")],
            "roster_or_characters": ["Assault Rifle", "Pump Shotgun", "SMG", "Sniper"],
            "ranks": ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Elite", "Champion", "Unreal"],
        }
        persisted = self.storage.persist_snapshot(
            game_slug=self.game_slug,
            handle=handle,
            display_name=handle,
            provider_slug=self.provider_slug,
            region=None,
            external_player_id=get_in(data, ["account", "id"], default=None),
            metadata_json={"stats": stats, "playlists": playlists},
            stats_scopes={"overview": overview_payload, "reference_data": reference_payload},
            matches=[],
        )
        self._upsert_module_profile(
            game_profile_id=persisted["profile"].id,
            platform=overview_payload["platform"],
            victories=overview_payload["victories"],
            kills=overview_payload["kills"],
            kd=overview_payload["kd"],
            mode_breakdown=get_in(data, ["stats", "all"], default={}) or {},
        )
        return SyncStatus(
            game_slug=self.game_slug,
            handle=handle,
            provider=self.provider_slug,
            synced_at=persisted["synced_at"],
        )

    def get_overview(self, handle: str, refresh: bool = False) -> FortniteOverview:
        if refresh:
            self.sync_profile(FortniteSyncRequest(name=handle))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return FortniteOverview(**snapshot["overview"])

    def compare_players(self, left_handle: str, right_handle: str, refresh: bool = False) -> FortniteComparison:
        left = self.get_overview(left_handle, refresh=refresh)
        right = self.get_overview(right_handle, refresh=refresh)
        return FortniteComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "victories": {
                    "left": left.victories,
                    "right": right.victories,
                    "better": left_handle if left.victories >= right.victories else right_handle,
                },
                "kills": {"left": left.kills, "right": right.kills, "better": left_handle if left.kills >= right.kills else right_handle},
                "kd": {"left": left.kd, "right": right.kd, "better": left_handle if left.kd >= right.kd else right_handle},
            },
        )

    def get_reference_data(self) -> FortniteReferenceData:
        playlists = self.client.fetch_reference_data()
        return FortniteReferenceData(
            maps=["Battle Royale Island"],
            roles_or_modes=[playlist.get("name", "") for playlist in playlists.get("data", [])[:10] if playlist.get("name")],
            roster_or_characters=["Assault Rifle", "Pump Shotgun", "SMG", "Sniper"],
            ranks=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Elite", "Champion", "Unreal"],
        )

    def get_recent_history(self, handle: str, refresh: bool = False) -> list[FortniteHistoryEntry]:
        if refresh:
            self.sync_profile(FortniteSyncRequest(name=handle))
        return []

    def _upsert_module_profile(
        self,
        *,
        game_profile_id: int,
        platform: str,
        victories: int,
        kills: int,
        kd: float,
        mode_breakdown: dict,
    ) -> None:
        record = self.db.query(FortniteProfile).filter(FortniteProfile.game_profile_id == game_profile_id).first()
        if record is None:
            record = FortniteProfile(
                game_profile_id=game_profile_id,
                platform=platform,
                victories=victories,
                kills=kills,
                kd=kd,
                mode_breakdown=mode_breakdown,
            )
            self.db.add(record)
        else:
            record.platform = platform
            record.victories = victories
            record.kills = kills
            record.kd = kd
            record.mode_breakdown = mode_breakdown
        self.db.commit()
