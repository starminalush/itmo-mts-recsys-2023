import jwt
from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ..exceptions import UnauthorizedUserError
from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise UnauthorizedUserError(error_message="Invalid authentication scheme")
            if not self.verify_jwt(credentials.credentials):
                raise UnauthorizedUserError(error_message="Invalid token or expired token")
            return credentials.credentials
        else:
            raise UnauthorizedUserError(error_message="Invalid authorization code")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except (jwt.InvalidSignatureError, jwt.InvalidAlgorithmError):
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


jwt_bearer = JWTBearer()
