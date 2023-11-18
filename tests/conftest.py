# pylint: disable=redefined-outer-name
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from service.api.app import create_app
from service.api.auth import bearer_auth
from service.settings import ServiceConfig, get_config

from .patches import NoAuthSimpleBearerPatch, TestSimpleBearerAuth


@pytest.fixture
def service_config() -> ServiceConfig:
    return get_config()


@pytest.fixture
def app(
    service_config: ServiceConfig,
) -> FastAPI:
    app = create_app(service_config)
    return app


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
