# pylint: disable=redefined-outer-name


import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from service.api.auth import bearer_auth
from service.api.exception_handlers import add_exception_handlers
from service.api.middlewares import add_middlewares
from service.api.views import add_views
from service.recsys_models import TestModel
from service.settings import ServiceConfig, get_config

from .patches import NoAuthSimpleBearerPatch, TestSimpleBearerAuth


@pytest.fixture
def service_config() -> ServiceConfig:
    return get_config()


@pytest.fixture
def app(service_config: ServiceConfig) -> FastAPI:
    new_app = FastAPI(debug=False)
    new_app.state.k_recs = service_config.k_recs
    new_app.state.models = {"test_model": TestModel()}
    add_views(new_app)
    add_middlewares(new_app)
    add_exception_handlers(new_app)
    return new_app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    app.dependency_overrides[bearer_auth] = NoAuthSimpleBearerPatch()
    return TestClient(app=app)


@pytest.fixture
def client_with_auth(app: FastAPI) -> TestClient:
    app.dependency_overrides[bearer_auth] = TestSimpleBearerAuth()
    return TestClient(app=app)


@pytest.fixture
def fake_bearer_token() -> str:
    return "testtoken"


@pytest.fixture
def test_bearer_token() -> str:
    return "supersecrettokenhere"
