class FortniteIntegrationClient:
    """Placeholder adapter for Fortnite trackers/providers."""

    def fetch_profile(self, handle: str) -> dict[str, str]:
        return {"handle": handle, "provider": "stub"}
