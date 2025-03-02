from fastapi import APIRouter

from app.api.v1.endpoints import login, users, players, cases, audit, funds

api_router = APIRouter()

@api_router.get("/")
def health_check():
    return {"status": "ok", "message": "API is running"}

api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(players.router, prefix="/players", tags=["players"])
api_router.include_router(cases.router, prefix="/cases", tags=["cases"])
api_router.include_router(audit.router, prefix="/audit", tags=["audit"])
api_router.include_router(funds.router, prefix="/funds", tags=["funds"]) 