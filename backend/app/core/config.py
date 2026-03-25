from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "StatForge"
    ENVIRONMENT: str = "development"
    API_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    SECRET_KEY: str = "change-me"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str = "postgresql+psycopg://statforge:statforge@db:5432/statforge"
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl | str] = ["http://localhost:5173"]
    EXTERNAL_TIMEOUT_SECONDS: float = 20.0
    PROVIDER_CACHE_TTL_MINUTES: int = 30
    RIOT_API_KEY: str | None = None
    RIOT_BASE_URL_ACCOUNTS: str = "https://americas.api.riotgames.com"
    RIOT_BASE_URL_LOL_PLATFORM: str = "https://br1.api.riotgames.com"
    RIOT_BASE_URL_LOL_REGIONAL: str = "https://americas.api.riotgames.com"
    RIOT_DDRAGON_BASE_URL: str = "https://ddragon.leagueoflegends.com"
    HENRIK_API_KEY: str | None = None
    HENRIK_BASE_URL: str = "https://api.henrikdev.xyz"
    FACEIT_API_KEY: str | None = None
    FACEIT_BASE_URL: str = "https://open.faceit.com/data/v4"
    FORTNITE_API_KEY: str | None = None
    FORTNITE_BASE_URL: str = "https://fortnite-api.com"
    OVERFAST_BASE_URL: str = "https://overfast-api.tekrop.fr"
    VALORANT_CONTENT_BASE_URL: str = "https://valorant-api.com"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"


settings = Settings()
