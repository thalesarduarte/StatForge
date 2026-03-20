from datetime import datetime, timedelta, timezone

from app.modules.cs2.schemas.profile import CS2Comparison, CS2HistoryEntry, CS2Overview, CS2ReferenceData


class CS2ProfileService:
    def get_overview(self, handle: str) -> CS2Overview:
        return CS2Overview(
            handle=handle,
            region="sa",
            rank="Level 10",
            maps=["Mirage", "Inferno", "Ancient"],
            kd=1.18,
            hs_percentage=46.2,
            adr=83.5,
            weapons=["AK-47", "M4A1-S", "AWP"],
            recent_highlights=["Positive opening duel rate", "High headshot consistency", "Stable ADR"],
        )

    def compare_players(self, left_handle: str, right_handle: str) -> CS2Comparison:
        return CS2Comparison(
            left_handle=left_handle,
            right_handle=right_handle,
            metrics={
                "kd": {"left": 1.22, "right": 1.10, "better": left_handle},
                "hs_percentage": {"left": 48.0, "right": 42.5, "better": left_handle},
                "adr": {"left": 84.7, "right": 79.1, "better": left_handle},
            },
        )

    def get_reference_data(self) -> CS2ReferenceData:
        return CS2ReferenceData(
            maps=["Mirage", "Inferno", "Nuke", "Ancient"],
            roles_or_modes=["Premier", "Competitive", "Faceit", "Wingman"],
            roster_or_characters=["AK-47", "M4A1-S", "AWP", "Desert Eagle"],
            ranks=["Silver", "Gold Nova", "MG", "DMG", "LE", "LEM", "Supreme", "Global Elite"],
        )

    def get_recent_history(self, handle: str) -> list[CS2HistoryEntry]:
        now = datetime.now(timezone.utc)
        return [
            CS2HistoryEntry(
                match_id=f"{handle}-1",
                result="win",
                mode="Premier",
                map_name="Mirage",
                played_at=now - timedelta(hours=2),
                stats={"kd": 1.6, "hs_percentage": 52.0, "adr": 90.1},
            ),
            CS2HistoryEntry(
                match_id=f"{handle}-2",
                result="loss",
                mode="Competitive",
                map_name="Ancient",
                played_at=now - timedelta(hours=7),
                stats={"kd": 1.1, "hs_percentage": 44.0, "adr": 78.3},
            ),
        ]
