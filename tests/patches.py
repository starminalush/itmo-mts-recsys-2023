from fastapi import Request

from service.api.auth import SimpleBearerAuth


class NoAuthSimpleBearerPatch(SimpleBearerAuth):
    async def __call__(self, request: Request):
        return True


class TestSimpleBearerAuth(SimpleBearerAuth):
    def _validate_token(self, token: str) -> bool:
        return token == "supersecrettokenhere"
