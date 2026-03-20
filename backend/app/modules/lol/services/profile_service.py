from datetime import datetime, timedelta, timezone

from app.modules.lol.schemas.profile import LolComparison, LolHistoryEntry, LolOverview, LolReferenceData


class LolProfileService:
    def get_overview(self, summoner_name: str) -> LolOverview:
        return LolOverview(
            summoner_name=summoner_name,
            server="br1",
            elo="Emerald II",
            primary_role="Mid",
            preferred_champions=["Ahri", "Orianna", "Sylas"],
            core_stats={"kda": 3.9, "winrate": 56.1, "cs_per_min": 7.4},
            recent_highlights=["Strong lane phase", "High objective impact", "Consistent champion pool"],
        )

    def compare_players(self, left_name: str, right_name: str) -> LolComparison:
        return LolComparison(
            left_name=left_name,
            right_name=right_name,
            metrics={
                "kda": {"left": 4.1, "right": 3.5, "better": left_name},
                "winrate": {"left": 57.0, "right": 54.2, "better": left_name},
                "vision_score": {"left": 32, "right": 28, "better": left_name},
            },
        )

    def get_reference_data(self) -> LolReferenceData:
        return LolReferenceData(
            maps=["Summoner's Rift", "ARAM"],
            roles_or_modes=["Top", "Jungle", "Mid", "ADC", "Support"],
            roster_or_characters=["Ahri", "Lee Sin", "Jinx", "Thresh"],
            ranks=["Iron", "Bronze", "Silver", "Gold", "Platinum", "Emerald", "Diamond", "Master+"],
        )

    def get_recent_history(self, summoner_name: str) -> list[LolHistoryEntry]:
        now = datetime.now(timezone.utc)
        return [
            LolHistoryEntry(
                match_id=f"{summoner_name}-1",
                result="win",
                mode="Ranked Solo",
                map_name="Summoner's Rift",
                played_at=now - timedelta(hours=3),
                stats={"kda": "9/2/8", "winrate_swing": 1.2, "champion": "Ahri"},
            ),
            LolHistoryEntry(
                match_id=f"{summoner_name}-2",
                result="loss",
                mode="Ranked Solo",
                map_name="Summoner's Rift",
                played_at=now - timedelta(hours=8),
                stats={"kda": "4/5/7", "winrate_swing": -0.8, "champion": "Sylas"},
            ),
        ]
