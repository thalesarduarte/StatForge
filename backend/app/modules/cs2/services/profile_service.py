class CS2ProfileService:
    """Coordinates CS2-specific profile sync and transforms."""

    def sync_profile(self, handle: str) -> dict[str, str]:
        return {"handle": handle, "status": "queued"}
