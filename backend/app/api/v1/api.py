from fastapi import APIRouter

from app.api.v1.endpoints import users, cases, funds, players, stats, login, audit, rooms, search

api_router = APIRouter()

@api_router.get("/")
@api_router.get("")
def health_check():
    return {"status": "ok", "message": "API is running"}

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(funds.router, prefix="/funds", tags=["funds"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(rooms.router, prefix="/rooms", tags=["rooms"])
api_router.include_router(search.router, prefix="/search", tags=["search"]) 