from http import HTTPStatus

from dotenv import load_dotenv
from fastapi.testclient import TestClient

GET_HEALTH = "/health"
load_dotenv()


def test_success_auth(client_with_auth: TestClient, test_bearer_token) -> None:
    with client_with_auth:
        response = client_with_auth.get(GET_HEALTH, headers={"Authorization": f"Bearer {test_bearer_token}"})
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "OK"


def test_no_auth(client_with_auth: TestClient) -> None:
    with client_with_auth:
        response = client_with_auth.get(GET_HEALTH)
        assert response.status_code == HTTPStatus.FORBIDDEN


def test_wrong_bearer_token_auth(client_with_auth: TestClient, fake_bearer_token) -> None:
    with client_with_auth:
        response = client_with_auth.get(GET_HEALTH, headers={"Authorization": f"Bearer {fake_bearer_token}"})
        assert response.status_code == HTTPStatus.FORBIDDEN
