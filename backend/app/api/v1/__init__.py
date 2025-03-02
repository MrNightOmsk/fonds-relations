from fastapi import APIRouter

from app.api.v1.endpoints import funds, players, users, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(funds.router, prefix="/funds", tags=["funds"])
api_router.include_router(players.router, prefix="/players", tags=["players"]) 