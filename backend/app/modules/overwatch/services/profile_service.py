from datetime import datetime, timedelta, timezone

from app.modules.overwatch.schemas.profile import (
    OverwatchComparison,
    OverwatchHistoryEntry,
    OverwatchOverview,
    OverwatchReferenceData,
)


class OverwatchProfileService:
    def get_overview(self, handle: str) -> OverwatchOverview:
        return OverwatchOverview(
            handle=handle,
            platform="PC",
            region="americas",
            rank="Diamond 2",
            main_hero="Tracer",
            role_stats={"tank": {"wins": 12}, "damage": {"wins": 28}, "support": {"wins": 16}},
            hero_stats={"Tracer": {"eliminations": 21, "win_rate": 58}, "Ana": {"healing": 9800, "win_rate": 54}},
            recent_highlights=["Strong damage queue", "Tracer remains the main hero", "Positive trend in ranked sessions"],
        )

    def compare_players(self, left_handle: str, right_handle: str) -> OverwatchComparison:
        return OverwatchComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "win_rate": {"left": 55.4, "right": 52.8, "better": left_handle},
                "eliminations": {"left": 18.2, "right": 16.7, "better": left_handle},
                "hero_damage": {"left": 9432, "right": 8790, "better": left_handle},
            },
        )

    def get_reference_data(self) -> OverwatchReferenceData:
        return OverwatchReferenceData(
            maps=["King's Row", "Route 66", "Circuit Royal"],
            roles_or_modes=["Tank", "Damage", "Support", "Competitive", "Quick Play"],
            roster_or_characters=["Tracer", "Ana", "Winston", "Kiriko"],
            ranks=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Master", "Grandmaster"],
        )

    def get_recent_history(self, handle: str) -> list[OverwatchHistoryEntry]:
        now = datetime.now(timezone.utc)
        return [
            OverwatchHistoryEntry(
                match_id=f"{handle}-1",
                result="win",
                mode="Competitive",
                map_name="King's Row",
                played_at=now - timedelta(hours=1),
                stats={"role": "Damage", "main_hero": "Tracer", "eliminations": 24},
            ),
            OverwatchHistoryEntry(
                match_id=f"{handle}-2",
                result="loss",
                mode="Competitive",
                map_name="Circuit Royal",
                played_at=now - timedelta(hours=4),
                stats={"role": "Support", "main_hero": "Ana", "healing": 11200},
            ),
        ]
