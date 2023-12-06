from fastapi import Request

from service.api.auth import SimpleBearerAuth
from service.recsys_models.base import BaseModel
from service.recsys_models.test import TestModel


class NoAuthSimpleBearerPatch(SimpleBearerAuth):
    async def __call__(self, request: Request):
        return True


class TestSimpleBearerAuth(SimpleBearerAuth):
    def _validate_token(self, token: str) -> bool:
        return token == "supersecrettokenhere"


def monkey_patched_get_test_models() -> dict[str, BaseModel]:
    return {"test_model": TestModel()}
