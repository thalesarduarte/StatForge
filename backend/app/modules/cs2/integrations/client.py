from app.core.config import settings
from app.core.errors import ConfigurationError
from app.core.http import ExternalApiClient


class CS2IntegrationClient:
    def __init__(self) -> None:
        if not settings.FACEIT_API_KEY:
            raise ConfigurationError("FACEIT_API_KEY is required for CS2 integration")
        headers = {"Authorization": f"Bearer {settings.FACEIT_API_KEY}"}
        self.client = ExternalApiClient(provider_name="faceit", base_url=settings.FACEIT_BASE_URL, headers=headers)

    def search_player(self, nickname: str) -> dict:
        return self.client.get("/search/players", params={"nickname": nickname, "game": "cs2", "limit": 1})

    def fetch_player_details(self, player_id: str) -> dict:
        return self.client.get(f"/players/{player_id}")

    def fetch_player_stats(self, player_id: str) -> dict:
        return self.client.get(f"/players/{player_id}/stats/cs2")

    def fetch_player_history(self, player_id: str) -> dict:
        return self.client.get(f"/players/{player_id}/history", params={"game": "cs2", "limit": 5})
