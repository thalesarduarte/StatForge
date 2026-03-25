from app.core.config import settings
from app.core.errors import ConfigurationError
from app.core.http import ExternalApiClient


class ValorantIntegrationClient:
    def __init__(self) -> None:
        if not settings.HENRIK_API_KEY:
            raise ConfigurationError("HENRIK_API_KEY is required for Valorant integration")

        headers = {"Authorization": settings.HENRIK_API_KEY}
        self.henrik_client = ExternalApiClient(
            provider_name="henrikdev",
            base_url=settings.HENRIK_BASE_URL,
            headers=headers,
        )
        self.content_client = ExternalApiClient(
            provider_name="valorant-api",
            base_url=settings.VALORANT_CONTENT_BASE_URL,
        )

    def fetch_account(self, name: str, tag: str) -> dict:
        return self.henrik_client.get(f"/valorant/v1/account/{name}/{tag}")

    def fetch_mmr(self, region: str, name: str, tag: str) -> dict:
        return self.henrik_client.get(f"/valorant/v3/mmr/{region}/pc/{name}/{tag}")

    def fetch_matches(self, region: str, puuid: str) -> dict:
        return self.henrik_client.get(f"/valorant/v3/by-puuid/matches/{region}/{puuid}")

    def fetch_reference_data(self) -> dict:
        return {
            "agents": self.content_client.get("/v1/agents", params={"isPlayableCharacter": "true"}),
            "maps": self.content_client.get("/v1/maps"),
            "weapons": self.content_client.get("/v1/weapons"),
        }
