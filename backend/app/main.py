from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.version import API_VERSION, LAST_UPDATE, RELEASE_NOTES
from app.core.health import get_health_status
from app.services.search import search_service

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version=API_VERSION,
    redirect_slashes=True
)

# Настройка шаблонов
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Главная страница API с информацией о статусе и версии
    """
    status = await get_health_status()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "project_name": settings.PROJECT_NAME,
            "api_version": API_VERSION,
            "last_update": LAST_UPDATE,
            "release_notes": RELEASE_NOTES,
            "api_status": status["api_status"],
            "db_status": status["db_status"]
        }
    )

@app.on_event("startup")
async def startup_event():
    """
    Инициализация сервисов при запуске приложения
    """
    try:
        # Инициализация индекса Elasticsearch
        await search_service.create_index()
        print("Elasticsearch index initialized successfully")
    except Exception as e:
        print(f"Error initializing Elasticsearch index: {str(e)}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Закрытие соединений при остановке приложения
    """
    await search_service.close()

app.include_router(api_router, prefix=settings.API_V1_STR) 