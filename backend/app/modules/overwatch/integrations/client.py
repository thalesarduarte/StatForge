class OverwatchIntegrationClient:
    """Adapter placeholder for external Overwatch data providers."""

    def fetch_profile(self, external_player_id: str) -> dict[str, str]:
        return {"external_player_id": external_player_id, "provider": "stub"}
