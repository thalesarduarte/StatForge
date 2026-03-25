from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.errors import ResourceNotFoundError
from app.modules.shared import SyncStatus
from app.modules.storage import GameModuleStorage
from app.modules.valorant.integrations.client import ValorantIntegrationClient
from app.modules.valorant.models.profile import ValorantProfile
from app.modules.valorant.schemas.profile import (
    ValorantComparison,
    ValorantHistoryEntry,
    ValorantOverview,
    ValorantReferenceData,
    ValorantSyncRequest,
)
from app.utils.dicts import get_in


class ValorantProfileService:
    game_slug = "valorant"
    provider_slug = "henrikdev"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client = ValorantIntegrationClient()
        self.storage = GameModuleStorage(db)

    def sync_profile(self, payload: ValorantSyncRequest) -> SyncStatus:
        account = self.client.fetch_account(payload.name, payload.tag)
        mmr = self.client.fetch_mmr(payload.region, payload.name, payload.tag)
        matches = self.client.fetch_matches(payload.region, get_in(account, ["data", "puuid"], default=""))
        reference = self.client.fetch_reference_data()

        handle = f"{payload.name}#{payload.tag}"
        normalized_matches = self._normalize_matches(matches, handle)
        metrics = self._aggregate_match_metrics(normalized_matches)
        overview_payload = {
            "handle": handle,
            "region": payload.region,
            "rank": get_in(mmr, ["data", "current", "tier", "name"], default="Unrated"),
            "agents": metrics["agents"],
            "weapons": [weapon.get("displayName", "") for weapon in get_in(reference, ["weapons", "data"], default=[])[:5]],
            "core_stats": {
                "hs_percentage": metrics["hs_percentage"],
                "kda": metrics["kda"],
                "winrate": metrics["winrate"],
            },
            "recent_highlights": [
                f"Current rank: {get_in(mmr, ['data', 'current', 'tier', 'name'], default='Unrated')}",
                f"Recent winrate: {metrics['winrate']}%",
                f"Tracked from HenrikDev + Valorant-API",
            ],
        }
        reference_payload = {
            "maps": [item.get("displayName", "") for item in get_in(reference, ["maps", "data"], default=[]) if item.get("displayName")],
            "roles_or_modes": ["Competitive", "Unrated", "Swiftplay", "Deathmatch"],
            "roster_or_characters": [
                item.get("displayName", "")
                for item in get_in(reference, ["agents", "data"], default=[])
                if item.get("displayName")
            ],
            "ranks": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ascendant", "Immortal", "Radiant"],
        }

        persisted = self.storage.persist_snapshot(
            game_slug=self.game_slug,
            handle=handle,
            display_name=handle,
            provider_slug=self.provider_slug,
            region=payload.region,
            external_player_id=get_in(account, ["data", "puuid"], default=None),
            metadata_json={"account": account, "mmr": mmr, "matches": matches},
            stats_scopes={"overview": overview_payload, "reference_data": reference_payload},
            matches=normalized_matches,
        )
        self._upsert_module_profile(
            game_profile_id=persisted["profile"].id,
            rank=overview_payload["rank"],
            agents=overview_payload["agents"],
            core_stats=overview_payload["core_stats"],
            weapon_stats={"top_weapons": overview_payload["weapons"]},
        )
        return SyncStatus(
            game_slug=self.game_slug,
            handle=handle,
            provider=self.provider_slug,
            synced_at=persisted["synced_at"],
        )

    def get_overview(self, handle: str, refresh: bool = False) -> ValorantOverview:
        if refresh:
            name, tag = handle.split("#", maxsplit=1)
            self.sync_profile(ValorantSyncRequest(name=name, tag=tag, region="br"))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return ValorantOverview(**snapshot["overview"])

    def compare_players(self, left_handle: str, right_handle: str, refresh: bool = False) -> ValorantComparison:
        left = self.get_overview(left_handle, refresh=refresh)
        right = self.get_overview(right_handle, refresh=refresh)
        return ValorantComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "hs_percentage": {
                    "left": left.core_stats["hs_percentage"],
                    "right": right.core_stats["hs_percentage"],
                    "better": left_handle if left.core_stats["hs_percentage"] >= right.core_stats["hs_percentage"] else right_handle,
                },
                "kda": {
                    "left": left.core_stats["kda"],
                    "right": right.core_stats["kda"],
                    "better": left_handle if left.core_stats["kda"] >= right.core_stats["kda"] else right_handle,
                },
                "winrate": {
                    "left": left.core_stats["winrate"],
                    "right": right.core_stats["winrate"],
                    "better": left_handle if left.core_stats["winrate"] >= right.core_stats["winrate"] else right_handle,
                },
            },
        )

    def get_reference_data(self) -> ValorantReferenceData:
        reference = self.client.fetch_reference_data()
        return ValorantReferenceData(
            maps=[item.get("displayName", "") for item in get_in(reference, ["maps", "data"], default=[]) if item.get("displayName")],
            roles_or_modes=["Competitive", "Unrated", "Swiftplay", "Deathmatch"],
            roster_or_characters=[
                item.get("displayName", "")
                for item in get_in(reference, ["agents", "data"], default=[])
                if item.get("displayName")
            ],
            ranks=["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ascendant", "Immortal", "Radiant"],
        )

    def get_recent_history(self, handle: str, refresh: bool = False) -> list[ValorantHistoryEntry]:
        if refresh:
            name, tag = handle.split("#", maxsplit=1)
            self.sync_profile(ValorantSyncRequest(name=name, tag=tag, region="br"))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return [
            ValorantHistoryEntry(
                match_id=item.external_match_id,
                result=item.payload["result"],
                mode=item.payload["mode"],
                map_name=item.payload["map_name"],
                played_at=item.played_at,
                stats=item.payload["stats"],
            )
            for item in snapshot["history"]
        ]

    def _normalize_matches(self, payload: dict, handle: str) -> list[dict]:
        items = payload.get("data", []) if isinstance(payload.get("data"), list) else []
        normalized: list[dict] = []
        for entry in items[:5]:
            metadata = entry.get("metadata", {})
            players = get_in(entry, ["players", "all_players"], default=[]) or []
            player = next(
                (
                    item
                    for item in players
                    if f"{item.get('name', '')}#{item.get('tag', '')}".lower() == handle.lower()
                ),
                {},
            )
            stats = player.get("stats", {})
            kills = float(stats.get("kills", 0) or 0)
            deaths = float(stats.get("deaths", 1) or 1)
            assists = float(stats.get("assists", 0) or 0)
            hs = float(stats.get("headshots", 0) or 0)
            shots = max(float(stats.get("bodyshots", 0) or 0) + float(stats.get("legshots", 0) or 0) + hs, 1.0)
            kda = round((kills + assists) / deaths, 2)
            teams = entry.get("teams", {})
            player_team = str(player.get("team", "")).lower()
            won = False
            if isinstance(teams, dict):
                for team_name, team_payload in teams.items():
                    if str(team_name).lower() == player_team and team_payload.get("has_won"):
                        won = True
                        break
            played_at = datetime.now(timezone.utc)
            raw_started_at = metadata.get("started_at")
            if isinstance(raw_started_at, str) and "T" in raw_started_at:
                played_at = datetime.fromisoformat(raw_started_at.replace("Z", "+00:00"))
            elif metadata.get("game_start"):
                played_at = datetime.fromtimestamp(int(metadata["game_start"]), tz=timezone.utc)
            normalized.append(
                {
                    "external_match_id": metadata.get("matchid") or metadata.get("match_id") or f"{handle}-{len(normalized)}",
                    "played_at": played_at,
                    "payload": {
                        "result": "win" if won else "loss",
                        "mode": metadata.get("mode") or get_in(metadata, ["queue", "name"], default="Competitive"),
                        "map_name": metadata.get("map") or get_in(metadata, ["map", "name"], default="Unknown"),
                        "stats": {
                            "agent": player.get("character", "Unknown"),
                            "hs_percentage": round((hs / shots) * 100, 2),
                            "kda": kda,
                        },
                    },
                }
            )
        if not normalized and items:
            raise ResourceNotFoundError(f"Unable to map Valorant matches for {handle}")
        return normalized

    def _aggregate_match_metrics(self, matches: list[dict]) -> dict:
        if not matches:
            return {"hs_percentage": 0.0, "kda": 0.0, "winrate": 0.0, "agents": []}
        hs_values = [float(match["payload"]["stats"].get("hs_percentage", 0)) for match in matches]
        kda_values = [float(match["payload"]["stats"].get("kda", 0)) for match in matches]
        wins = sum(1 for match in matches if match["payload"]["result"] == "win")
        agents = list(
            dict.fromkeys(str(match["payload"]["stats"].get("agent", "Unknown")) for match in matches if match["payload"]["stats"].get("agent"))
        )
        return {
            "hs_percentage": round(sum(hs_values) / len(hs_values), 2),
            "kda": round(sum(kda_values) / len(kda_values), 2),
            "winrate": round((wins / len(matches)) * 100, 2),
            "agents": agents[:5],
        }

    def _upsert_module_profile(
        self,
        *,
        game_profile_id: int,
        rank: str,
        agents: list[str],
        core_stats: dict,
        weapon_stats: dict,
    ) -> None:
        record = self.db.query(ValorantProfile).filter(ValorantProfile.game_profile_id == game_profile_id).first()
        if record is None:
            record = ValorantProfile(
                game_profile_id=game_profile_id,
                current_rank=rank,
                favorite_agents=agents,
                core_stats=core_stats,
                weapon_stats=weapon_stats,
            )
            self.db.add(record)
        else:
            record.current_rank = rank
            record.favorite_agents = agents
            record.core_stats = core_stats
            record.weapon_stats = weapon_stats
        self.db.commit()
