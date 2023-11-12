from fastapi import APIRouter

from .endpoints import health, recommendations

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["health"])
router.include_router(recommendations.router, prefix="/reco", tags=["recommendations"])
