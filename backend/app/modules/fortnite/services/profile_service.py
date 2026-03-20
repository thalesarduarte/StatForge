from datetime import datetime, timedelta, timezone

from app.modules.fortnite.schemas.profile import (
    FortniteComparison,
    FortniteHistoryEntry,
    FortniteOverview,
    FortniteReferenceData,
)


class FortniteProfileService:
    def get_overview(self, handle: str) -> FortniteOverview:
        return FortniteOverview(
            handle=handle,
            platform="Epic",
            victories=112,
            kills=1843,
            kd=3.14,
            preferred_modes=["Battle Royale", "Zero Build Duos", "Ranked Solos"],
            recent_highlights=["Victory-heavy session", "Strong endgame placement", "High elimination output"],
        )

    def compare_players(self, left_handle: str, right_handle: str) -> FortniteComparison:
        return FortniteComparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "victories": {"left": 112, "right": 98, "better": left_handle},
                "kills": {"left": 1843, "right": 1762, "better": left_handle},
                "kd": {"left": 3.14, "right": 2.81, "better": left_handle},
            },
        )

    def get_reference_data(self) -> FortniteReferenceData:
        return FortniteReferenceData(
            maps=["Apollo Reloaded", "Battle Royale Island"],
            roles_or_modes=["Solos", "Duos", "Trios", "Squads", "Zero Build"],
            roster_or_characters=["Assault Rifle", "Pump Shotgun", "SMG", "Sniper"],
            ranks=["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Elite", "Champion", "Unreal"],
        )

    def get_recent_history(self, handle: str) -> list[FortniteHistoryEntry]:
        now = datetime.now(timezone.utc)
        return [
            FortniteHistoryEntry(
                match_id=f"{handle}-1",
                result="win",
                mode="Zero Build Duos",
                map_name="Battle Royale Island",
                played_at=now - timedelta(hours=2),
                stats={"placement": 1, "kills": 9, "kd_session": 3.2},
            ),
            FortniteHistoryEntry(
                match_id=f"{handle}-2",
                result="top-5",
                mode="Ranked Solos",
                map_name="Battle Royale Island",
                played_at=now - timedelta(hours=5),
                stats={"placement": 4, "kills": 6, "kd_session": 2.6},
            ),
        ]
