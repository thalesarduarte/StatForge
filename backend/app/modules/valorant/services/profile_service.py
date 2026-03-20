from datetime import datetime, timedelta, timezone

from app.modules.valorant.schemas.profile import (
    ValorantComparison,
    ValorantHistoryEntry,
    ValorantOverview,
    ValorantReferenceData,
)


class ValorantProfileService:
    def get_overview(self, handle: str) -> ValorantOverview:
        return ValorantOverview(
            handle=handle,
            region="br",
            rank="Ascendant 3",
            agents=["Jett", "Sova", "Omen"],
            weapons=["Vandal", "Operator", "Sheriff"],
            core_stats={"hs_percentage": 27.8, "kda": 1.42, "winrate": 54.6},
            recent_highlights=["High entry frag impact", "Stable headshot percentage", "Positive ranked trend"],
        )

    def compare_players(self, left_handle: str, right_handle: str) -> ValorantComparison:
        return ValorantComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "hs_percentage": {"left": 27.8, "right": 24.1, "better": left_handle},
                "kda": {"left": 1.42, "right": 1.29, "better": left_handle},
                "winrate": {"left": 54.6, "right": 52.0, "better": left_handle},
            },
        )

    def get_reference_data(self) -> ValorantReferenceData:
        return ValorantReferenceData(
            maps=["Ascent", "Bind", "Lotus", "Sunset"],
            roles_or_modes=["Duelist", "Initiator", "Sentinel", "Controller", "Competitive"],
            roster_or_characters=["Jett", "Sova", "Omen", "Killjoy"],
            ranks=["Iron", "Bronze", "Silver", "Gold", "Platinum", "Diamond", "Ascendant", "Immortal", "Radiant"],
        )

    def get_recent_history(self, handle: str) -> list[ValorantHistoryEntry]:
        now = datetime.now(timezone.utc)
        return [
            ValorantHistoryEntry(
                match_id=f"{handle}-1",
                result="win",
                mode="Competitive",
                map_name="Ascent",
                played_at=now - timedelta(hours=2),
                stats={"agent": "Jett", "hs_percentage": 31.2, "kda": 1.8},
            ),
            ValorantHistoryEntry(
                match_id=f"{handle}-2",
                result="loss",
                mode="Competitive",
                map_name="Lotus",
                played_at=now - timedelta(hours=6),
                stats={"agent": "Omen", "hs_percentage": 23.5, "kda": 1.1},
            ),
        ]
