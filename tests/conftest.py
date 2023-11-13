# pylint: disable=redefined-outer-name
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from service.api.app import create_app
from service.api.auth.auth_bearer import jwt_bearer
from service.settings import ServiceConfig, get_config

from .patches import NoAuthJWTBearerPatch


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
    app.dependency_overrides[jwt_bearer] = NoAuthJWTBearerPatch()
    return TestClient(app=app)


@pytest.fixture
def client_with_auth(app: FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture
def fake_bearer_token() -> str:
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.pj0NmBjKT7cpC8NU35eGYJHbrNoSAfkAVdF20Aijlb8.123"
