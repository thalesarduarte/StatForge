from app.core.config import settings
from app.core.errors import ConfigurationError
from app.core.http import ExternalApiClient


class LolIntegrationClient:
    def __init__(self) -> None:
        if not settings.RIOT_API_KEY:
            raise ConfigurationError("RIOT_API_KEY is required for LoL integration")

        headers = {"X-Riot-Token": settings.RIOT_API_KEY}
        self.account_client = ExternalApiClient(
            provider_name="riot-account",
            base_url=settings.RIOT_BASE_URL_ACCOUNTS,
            headers=headers,
        )
        self.platform_client = ExternalApiClient(
            provider_name="riot-lol-platform",
            base_url=settings.RIOT_BASE_URL_LOL_PLATFORM,
            headers=headers,
        )
        self.regional_client = ExternalApiClient(
            provider_name="riot-lol-regional",
            base_url=settings.RIOT_BASE_URL_LOL_REGIONAL,
            headers=headers,
        )
        self.ddragon_client = ExternalApiClient(
            provider_name="riot-ddragon",
            base_url=settings.RIOT_DDRAGON_BASE_URL,
        )

    def fetch_account(self, game_name: str, tag_line: str) -> dict:
        return self.account_client.get(f"/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}")

    def fetch_summoner(self, puuid: str) -> dict:
        return self.platform_client.get(f"/lol/summoner/v4/summoners/by-puuid/{puuid}")

    def fetch_league_entries(self, summoner_id: str) -> list:
        return self.platform_client.get(f"/lol/league/v4/entries/by-summoner/{summoner_id}")

    def fetch_match_ids(self, puuid: str) -> list:
        return self.regional_client.get(f"/lol/match/v5/matches/by-puuid/{puuid}/ids", params={"start": 0, "count": 5})

    def fetch_match(self, match_id: str) -> dict:
        return self.regional_client.get(f"/lol/match/v5/matches/{match_id}")

    def fetch_reference_data(self) -> dict:
        versions = self.ddragon_client.get("/api/versions.json")
        version = versions[0] if isinstance(versions, list) and versions else "14.1.1"
        champions = self.ddragon_client.get(f"/cdn/{version}/data/en_US/champion.json")
        return {"version": version, "champions": champions}
