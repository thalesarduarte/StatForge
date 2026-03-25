from app.core.config import settings
from app.core.errors import ConfigurationError
from app.core.http import ExternalApiClient


class FortniteIntegrationClient:
    def __init__(self) -> None:
        if not settings.FORTNITE_API_KEY:
            raise ConfigurationError("FORTNITE_API_KEY is required for Fortnite integration")
        headers = {"Authorization": settings.FORTNITE_API_KEY}
        self.client = ExternalApiClient(provider_name="fortnite-api", base_url=settings.FORTNITE_BASE_URL, headers=headers)

    def fetch_stats(self, name: str, account_type: str) -> dict:
        return self.client.get(
            "/v2/stats/br/v2",
            params={"name": name, "accountType": account_type, "timeWindow": "lifetime"},
        )

    def fetch_reference_data(self) -> dict:
        return self.client.get("/v1/playlists")
