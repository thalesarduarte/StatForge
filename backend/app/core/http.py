from collections.abc import Mapping
from typing import Any

import httpx

from app.core.config import settings
from app.core.errors import ExternalServiceError


class ExternalApiClient:
    def __init__(self, provider_name: str, base_url: str, headers: Mapping[str, str] | None = None) -> None:
        self.provider_name = provider_name
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})

    def get(self, path: str, params: Mapping[str, Any] | None = None) -> dict[str, Any] | list[Any]:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=settings.EXTERNAL_TIMEOUT_SECONDS, headers=self.headers) as client:
                response = client.get(url, params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceError(
                message=f"{self.provider_name} returned status {exc.response.status_code}",
                provider=self.provider_name,
                status_code=exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise ExternalServiceError(
                message=f"{self.provider_name} request failed",
                provider=self.provider_name,
            ) from exc
