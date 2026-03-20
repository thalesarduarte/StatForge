from fastapi import APIRouter

from app.api.routes import activity, admin, auth, badges, comment_likes, comments, favorites, follows, profiles, teams, tournaments, users
from app.modules.cs2.api.router import router as cs2_router
from app.modules.fortnite.api.router import router as fortnite_router
from app.modules.lol.api.router import router as lol_router
from app.modules.overwatch.api.router import router as overwatch_router
from app.modules.valorant.api.router import router as valorant_router

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(comment_likes.router, prefix="/comment-likes", tags=["comment-likes"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
api_router.include_router(follows.router, prefix="/follows", tags=["follows"])
api_router.include_router(teams.router, prefix="/teams", tags=["teams"])
api_router.include_router(tournaments.router, prefix="/tournaments", tags=["tournaments"])
api_router.include_router(badges.router, prefix="/badges", tags=["badges"])
api_router.include_router(activity.router, prefix="/activity", tags=["activity"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(overwatch_router, prefix="/modules/overwatch", tags=["overwatch"])
api_router.include_router(valorant_router, prefix="/modules/valorant", tags=["valorant"])
api_router.include_router(cs2_router, prefix="/modules/cs2", tags=["cs2"])
api_router.include_router(lol_router, prefix="/modules/lol", tags=["lol"])
api_router.include_router(fortnite_router, prefix="/modules/fortnite", tags=["fortnite"])
