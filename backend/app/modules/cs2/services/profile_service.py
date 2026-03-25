from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import ResourceNotFoundError
from app.modules.cs2.integrations.client import CS2IntegrationClient
from app.modules.cs2.models.profile import CS2Profile
from app.modules.cs2.schemas.profile import CS2Comparison, CS2HistoryEntry, CS2Overview, CS2ReferenceData, CS2SyncRequest
from app.modules.shared import SyncStatus
from app.modules.storage import GameModuleStorage
from app.utils.dicts import get_in


class CS2ProfileService:
    game_slug = "cs2"
    provider_slug = "faceit"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client = CS2IntegrationClient()
        self.storage = GameModuleStorage(db)

    def sync_profile(self, payload: CS2SyncRequest) -> SyncStatus:
        search = self.client.search_player(payload.nickname)
        player = (search.get("items") or [{}])[0]
        player_id = player.get("player_id")
        if not player_id:
            raise ResourceNotFoundError(f"No FACEIT player found for nickname {payload.nickname}")
        details = self.client.fetch_player_details(player_id)
        stats = self.client.fetch_player_stats(player_id)
        history = self.client.fetch_player_history(player_id)

        lifetime = stats.get("lifetime", {})
        overview_payload = {
            "handle": payload.nickname,
            "region": player.get("country", "global"),
            "rank": f"FACEIT Level {get_in(details, ['games', 'cs2', 'skill_level'], default='N/A')}",
            "maps": ["Mirage", "Inferno", "Ancient", "Nuke"],
            "kd": float(lifetime.get("Average K/D Ratio", 0) or 0),
            "hs_percentage": float(str(lifetime.get("Average Headshots %", 0)).replace("%", "") or 0),
            "adr": float(lifetime.get("Average ADR", 0) or 0),
            "weapons": ["AK-47", "M4A1-S", "AWP"],
            "recent_highlights": [
                f"FACEIT ELO {get_in(details, ['games', 'cs2', 'faceit_elo'], default='N/A')}",
                f"Tracked via FACEIT Data API",
                f"Lifetime winrate {lifetime.get('Win Rate %', 'N/A')}",
            ],
        }
        reference_payload = {
            "maps": ["Mirage", "Inferno", "Ancient", "Nuke", "Dust2"],
            "roles_or_modes": ["FACEIT", "Premier", "Competitive"],
            "roster_or_characters": ["AK-47", "M4A1-S", "AWP", "Desert Eagle"],
            "ranks": ["FACEIT 1", "FACEIT 2", "FACEIT 3", "FACEIT 4", "FACEIT 5", "FACEIT 6", "FACEIT 7", "FACEIT 8", "FACEIT 9", "FACEIT 10"],
        }
        normalized_matches = self._normalize_history(history)

        persisted = self.storage.persist_snapshot(
            game_slug=self.game_slug,
            handle=payload.nickname,
            display_name=details.get("nickname", payload.nickname),
            provider_slug=self.provider_slug,
            region=player.get("country"),
            external_player_id=player_id,
            metadata_json={"details": details, "stats": stats, "history": history},
            stats_scopes={"overview": overview_payload, "reference_data": reference_payload},
            matches=normalized_matches,
        )
        self._upsert_module_profile(
            game_profile_id=persisted["profile"].id,
            rank=overview_payload["rank"],
            kd=overview_payload["kd"],
            hs_percentage=overview_payload["hs_percentage"],
            weapon_stats={"weapons": overview_payload["weapons"], "adr": overview_payload["adr"]},
        )
        return SyncStatus(
            game_slug=self.game_slug,
            handle=payload.nickname,
            provider=self.provider_slug,
            synced_at=persisted["synced_at"],
        )

    def get_overview(self, handle: str, refresh: bool = False) -> CS2Overview:
        if refresh:
            self.sync_profile(CS2SyncRequest(nickname=handle))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return CS2Overview(**snapshot["overview"])

    def compare_players(self, left_handle: str, right_handle: str, refresh: bool = False) -> CS2Comparison:
        left = self.get_overview(left_handle, refresh=refresh)
        right = self.get_overview(right_handle, refresh=refresh)
        return CS2Comparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "kd": {"left": left.kd, "right": right.kd, "better": left_handle if left.kd >= right.kd else right_handle},
                "hs_percentage": {
                    "left": left.hs_percentage,
                    "right": right.hs_percentage,
                    "better": left_handle if left.hs_percentage >= right.hs_percentage else right_handle,
                },
                "adr": {"left": left.adr, "right": right.adr, "better": left_handle if left.adr >= right.adr else right_handle},
            },
        )

    def get_reference_data(self) -> CS2ReferenceData:
        return CS2ReferenceData(
            maps=["Mirage", "Inferno", "Ancient", "Nuke", "Dust2"],
            roles_or_modes=["FACEIT", "Premier", "Competitive"],
            roster_or_characters=["AK-47", "M4A1-S", "AWP", "Desert Eagle"],
            ranks=["FACEIT 1", "FACEIT 2", "FACEIT 3", "FACEIT 4", "FACEIT 5", "FACEIT 6", "FACEIT 7", "FACEIT 8", "FACEIT 9", "FACEIT 10"],
        )

    def get_recent_history(self, handle: str, refresh: bool = False) -> list[CS2HistoryEntry]:
        if refresh:
            self.sync_profile(CS2SyncRequest(nickname=handle))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return [
            CS2HistoryEntry(
                match_id=item.external_match_id,
                result=item.payload["result"],
                mode=item.payload["mode"],
                map_name=item.payload["map_name"],
                played_at=item.played_at,
                stats=item.payload["stats"],
            )
            for item in snapshot["history"]
        ]

    def _normalize_history(self, payload: dict) -> list[dict]:
        items = payload.get("items", [])
        normalized: list[dict] = []
        for item in items[:5]:
            match_id = item.get("match_id", f"faceit-{len(normalized)}")
            stats = item.get("stats", {})
            normalized.append(
                {
                    "external_match_id": match_id,
                    "played_at": datetime.now(timezone.utc),
                    "payload": {
                        "result": str(stats.get("Result", "unknown")).lower(),
                        "mode": "FACEIT",
                        "map_name": stats.get("Map", "Unknown"),
                        "stats": {
                            "kd": float(stats.get("K/D Ratio", 0) or 0),
                            "hs_percentage": float(str(stats.get("Headshots %", 0)).replace("%", "") or 0),
                            "adr": float(stats.get("ADR", 0) or 0),
                        },
                    },
                }
            )
        return normalized

    def _upsert_module_profile(
        self,
        *,
        game_profile_id: int,
        rank: str,
        kd: float,
        hs_percentage: float,
        weapon_stats: dict,
    ) -> None:
        record = self.db.query(CS2Profile).filter(CS2Profile.game_profile_id == game_profile_id).first()
        if record is None:
            record = CS2Profile(
                game_profile_id=game_profile_id,
                current_rank=rank,
                kd=kd,
                hs_percentage=hs_percentage,
                weapon_stats=weapon_stats,
            )
            self.db.add(record)
        else:
            record.current_rank = rank
            record.kd = kd
            record.hs_percentage = hs_percentage
            record.weapon_stats = weapon_stats
        self.db.commit()
