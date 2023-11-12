from fastapi import APIRouter, Depends

from service.api.auth.auth_bearer import JWTBearer, jwt_bearer
from service.pydantic_schemas.health import HealthCheck

router = APIRouter()


@router.get("/", dependencies=[Depends(jwt_bearer)])
async def health() -> HealthCheck:
    return HealthCheck(status="OK")
