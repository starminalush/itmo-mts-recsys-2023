from fastapi import APIRouter, Depends

from service.api.auth.auth_bearer import jwt_bearer
from service.pydantic_schemas.error import Error
from service.pydantic_schemas.health import HealthCheck

router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(jwt_bearer)],
    responses={
        200: {"model": HealthCheck},
        401: {
            "model": Error,
            "description": "Authentication error",
        },
        404: {
            "model": Error,
            "description": "Not Found Error",
        },
    },
)
async def health() -> HealthCheck:
    return HealthCheck(status="OK")
