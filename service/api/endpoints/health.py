from fastapi import APIRouter

from service.pydantic_schemas.health import HealthCheck

router = APIRouter()


@router.get("/")
async def health() -> HealthCheck:
    return HealthCheck(status="OK")
