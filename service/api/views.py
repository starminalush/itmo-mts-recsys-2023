from fastapi import APIRouter, FastAPI

from .endpoints import health, recommendations

router = APIRouter()


def add_views(app: FastAPI) -> None:
    router.include_router(health.router, prefix="/health", tags=["health"])
    router.include_router(recommendations.router, prefix="/reco", tags=["recommendations"])
    app.include_router(router)
