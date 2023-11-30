from fastapi import APIRouter

from service.pydantic_schemas.health_status import HealthCheck

router = APIRouter()


@router.get(
    "",
    responses={200: {"model": HealthCheck}},
)
async def health() -> HealthCheck:
    return HealthCheck(status="OK")
