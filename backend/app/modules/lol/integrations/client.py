class LolIntegrationClient:
    """Placeholder adapter for Riot or other LoL data providers."""

    def fetch_profile(self, summoner_name: str) -> dict[str, str]:
        return {"summoner_name": summoner_name, "provider": "stub"}
