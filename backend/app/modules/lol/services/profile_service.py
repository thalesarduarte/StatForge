from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.modules.lol.integrations.client import LolIntegrationClient
from app.modules.lol.models.profile import LolProfile
from app.modules.lol.schemas.profile import LolComparison, LolHistoryEntry, LolOverview, LolReferenceData, LolSyncRequest
from app.modules.shared import SyncStatus
from app.modules.storage import GameModuleStorage
from app.utils.dicts import get_in


class LolProfileService:
    game_slug = "lol"
    provider_slug = "riot"

    def __init__(self, db: Session) -> None:
        self.db = db
        self.client = LolIntegrationClient()
        self.storage = GameModuleStorage(db)

    def sync_profile(self, payload: LolSyncRequest) -> SyncStatus:
        account = self.client.fetch_account(payload.game_name, payload.tag_line)
        summoner = self.client.fetch_summoner(account["puuid"])
        league_entries = self.client.fetch_league_entries(summoner["id"])
        match_ids = self.client.fetch_match_ids(account["puuid"])
        matches = [self.client.fetch_match(match_id) for match_id in match_ids]
        reference = self.client.fetch_reference_data()

        handle = f"{payload.game_name}#{payload.tag_line}"
        normalized_matches = self._normalize_matches(matches, account["puuid"])
        metrics = self._aggregate(normalized_matches, league_entries)
        overview_payload = {
            "summoner_name": handle,
            "server": payload.region,
            "elo": metrics["elo"],
            "primary_role": metrics["primary_role"],
            "preferred_champions": metrics["preferred_champions"],
            "core_stats": metrics["core_stats"],
            "recent_highlights": [
                f"Current queue tier: {metrics['elo']}",
                f"Recent winrate: {metrics['core_stats']['winrate']}%",
                "Tracked via Riot API",
            ],
        }
        reference_payload = {
            "maps": ["Summoner's Rift", "ARAM"],
            "roles_or_modes": ["Top", "Jungle", "Mid", "ADC", "Support"],
            "roster_or_characters": list((reference.get("champions", {}).get("data") or {}).keys())[:20],
            "ranks": ["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"],
        }
        persisted = self.storage.persist_snapshot(
            game_slug=self.game_slug,
            handle=handle,
            display_name=payload.game_name,
            provider_slug=self.provider_slug,
            region=payload.region,
            external_player_id=account["puuid"],
            metadata_json={"account": account, "summoner": summoner, "league": league_entries, "matches": matches},
            stats_scopes={"overview": overview_payload, "reference_data": reference_payload},
            matches=normalized_matches,
        )
        self._upsert_module_profile(
            game_profile_id=persisted["profile"].id,
            elo=metrics["elo"],
            primary_role=metrics["primary_role"],
            champions=metrics["preferred_champions"],
            core_stats=metrics["core_stats"],
        )
        return SyncStatus(
            game_slug=self.game_slug,
            handle=handle,
            provider=self.provider_slug,
            synced_at=persisted["synced_at"],
        )

    def get_overview(self, handle: str, refresh: bool = False) -> LolOverview:
        if refresh:
            game_name, tag_line = handle.split("#", maxsplit=1)
            self.sync_profile(LolSyncRequest(game_name=game_name, tag_line=tag_line, region="br1"))
        snapshot = self.storage.load_snapshot(self.game_slug, handle)
        return LolOverview(**snapshot["overview"])

    def compare_players(self, left_name: str, right_name: str, refresh: bool = False) -> LolComparison:
        left = self.get_overview(left_name, refresh=refresh)
        right = self.get_overview(right_name, refresh=refresh)
        return LolComparison(
            left_name=left_name,
            right_name=right_name,
            metrics={
                "kda": {
                    "left": left.core_stats["kda"],
                    "right": right.core_stats["kda"],
                    "better": left_name if left.core_stats["kda"] >= right.core_stats["kda"] else right_name,
                },
                "winrate": {
                    "left": left.core_stats["winrate"],
                    "right": right.core_stats["winrate"],
                    "better": left_name if left.core_stats["winrate"] >= right.core_stats["winrate"] else right_name,
                },
            },
        )

    def get_reference_data(self) -> LolReferenceData:
        reference = self.client.fetch_reference_data()
        return LolReferenceData(
            maps=["Summoner's Rift", "ARAM"],
            roles_or_modes=["Top", "Jungle", "Mid", "ADC", "Support"],
            roster_or_characters=list((reference.get("champions", {}).get("data") or {}).keys())[:20],
            ranks=["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master", "Grandmaster", "Challenger"],
        )

    def get_recent_history(self, summoner_name: str, refresh: bool = False) -> list[LolHistoryEntry]:
        if refresh:
            game_name, tag_line = summoner_name.split("#", maxsplit=1)
            self.sync_profile(LolSyncRequest(game_name=game_name, tag_line=tag_line, region="br1"))
        snapshot = self.storage.load_snapshot(self.game_slug, summoner_name)
        return [
            LolHistoryEntry(
                match_id=item.external_match_id,
                result=item.payload["result"],
                mode=item.payload["mode"],
                map_name=item.payload["map_name"],
                played_at=item.played_at,
                stats=item.payload["stats"],
            )
            for item in snapshot["history"]
        ]

    def _normalize_matches(self, matches: list[dict], puuid: str) -> list[dict]:
        normalized: list[dict] = []
        for match in matches[:5]:
            info = match.get("info", {})
            participant = next((item for item in info.get("participants", []) if item.get("puuid") == puuid), {})
            normalized.append(
                {
                    "external_match_id": match.get("metadata", {}).get("matchId", f"lol-{len(normalized)}"),
                    "played_at": datetime.fromtimestamp(info.get("gameCreation", 0) / 1000, tz=timezone.utc),
                    "payload": {
                        "result": "win" if participant.get("win") else "loss",
                        "mode": info.get("queueId", "Ranked"),
                        "map_name": "Summoner's Rift",
                        "stats": {
                            "champion": participant.get("championName", "Unknown"),
                            "kda": f"{participant.get('kills', 0)}/{participant.get('deaths', 0)}/{participant.get('assists', 0)}",
                            "role": participant.get("individualPosition", "Unknown"),
                        },
                    },
                }
            )
        return normalized

    def _aggregate(self, matches: list[dict], league_entries: list[dict]) -> dict:
        if matches:
            wins = sum(1 for match in matches if match["payload"]["result"] == "win")
            champions = list(dict.fromkeys(str(match["payload"]["stats"]["champion"]) for match in matches))
            roles = [str(match["payload"]["stats"]["role"]) for match in matches if match["payload"]["stats"]["role"]]
            kda_values: list[float] = []
            for match in matches:
                kills, deaths, assists = [float(value) for value in str(match["payload"]["stats"]["kda"]).split("/")]
                kda_values.append(round((kills + assists) / max(deaths, 1.0), 2))
            primary_role = max(set(roles), key=roles.count) if roles else "Unknown"
            winrate = round((wins / len(matches)) * 100, 2)
            kda = round(sum(kda_values) / len(kda_values), 2)
        else:
            champions = []
            primary_role = "Unknown"
            winrate = 0.0
            kda = 0.0
        solo_queue = next((entry for entry in league_entries if entry.get("queueType") == "RANKED_SOLO_5x5"), None)
        elo = f"{solo_queue.get('tier', 'UNRANKED')} {solo_queue.get('rank', '')}".strip() if solo_queue else "UNRANKED"
        return {
            "elo": elo,
            "primary_role": primary_role,
            "preferred_champions": champions[:5],
            "core_stats": {"kda": kda, "winrate": winrate, "cs_per_min": 0.0},
        }

    def _upsert_module_profile(
        self,
        *,
        game_profile_id: int,
        elo: str,
        primary_role: str,
        champions: list[str],
        core_stats: dict,
    ) -> None:
        record = self.db.query(LolProfile).filter(LolProfile.game_profile_id == game_profile_id).first()
        if record is None:
            record = LolProfile(
                game_profile_id=game_profile_id,
                current_elo=elo,
                primary_role=primary_role,
                champion_pool=champions,
                core_stats=core_stats,
            )
            self.db.add(record)
        else:
            record.current_elo = elo
            record.primary_role = primary_role
            record.champion_pool = champions
            record.core_stats = core_stats
        self.db.commit()
