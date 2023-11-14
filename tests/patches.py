from fastapi import Request

from service.api.auth.auth_bearer import JWTBearer


class NoAuthJWTBearerPatch(JWTBearer):
    async def __call__(self, request: Request):
        return True