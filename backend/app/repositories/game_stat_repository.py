from sqlalchemy.orm import Session

from app.models.game_stat import GameStat


class GameStatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def replace_scopes(self, game_profile_id: int, game_slug: str, scopes: dict[str, dict]) -> list[GameStat]:
        self.db.query(GameStat).filter(GameStat.game_profile_id == game_profile_id).delete()
        items: list[GameStat] = []
        for stat_scope, payload in scopes.items():
            item = GameStat(
                game_profile_id=game_profile_id,
                game_slug=game_slug,
                stat_scope=stat_scope,
                payload=payload,
            )
            self.db.add(item)
            items.append(item)
        self.db.commit()
        return items

    def get_scope(self, game_profile_id: int, stat_scope: str) -> GameStat | None:
        return (
            self.db.query(GameStat)
            .filter(GameStat.game_profile_id == game_profile_id, GameStat.stat_scope == stat_scope)
            .first()
        )
