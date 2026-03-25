from app.core.config import settings
from app.core.http import ExternalApiClient


class OverwatchIntegrationClient:
    def __init__(self) -> None:
        self.client = ExternalApiClient(provider_name="overfast", base_url=settings.OVERFAST_BASE_URL)

    def fetch_summary(self, handle: str) -> dict:
        return self.client.get(f"/players/{handle}/summary")

    def fetch_stats_summary(self, handle: str) -> dict:
        return self.client.get(f"/players/{handle}/stats/summary", params={"gamemode": "competitive"})

    def fetch_reference_data(self) -> dict:
        heroes = self.client.get("/heroes")
        maps = self.client.get("/maps")
        modes = self.client.get("/gamemodes")
        roles = self.client.get("/roles")
        return {"heroes": heroes, "maps": maps, "modes": modes, "roles": roles}
