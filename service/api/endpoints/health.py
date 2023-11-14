from fastapi import APIRouter, Depends

from service.api.auth import bearer_auth
from service.pydantic_schemas.health_status import HealthCheck

router = APIRouter()


@router.get(
    "",
    dependencies=[Depends(bearer_auth)],
    responses={200: {"model": HealthCheck}},
)
async def health() -> HealthCheck:
    return HealthCheck(status="OK")
