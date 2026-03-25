from datetime import datetime

from sqlalchemy.orm import Session

from app.models.game_match import GameMatch


class GameMatchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def replace_matches(self, game_profile_id: int, game_slug: str, matches: list[dict]) -> list[GameMatch]:
        self.db.query(GameMatch).filter(GameMatch.game_profile_id == game_profile_id).delete()
        items: list[GameMatch] = []
        for match in matches:
            item = GameMatch(
                game_profile_id=game_profile_id,
                game_slug=game_slug,
                external_match_id=match["external_match_id"],
                played_at=match["played_at"],
                payload=match["payload"],
            )
            self.db.add(item)
            items.append(item)
        self.db.commit()
        return items

    def list_recent(self, game_profile_id: int, limit: int = 10) -> list[GameMatch]:
        return (
            self.db.query(GameMatch)
            .filter(GameMatch.game_profile_id == game_profile_id)
            .order_by(GameMatch.played_at.desc())
            .limit(limit)
            .all()
        )
