from http import HTTPStatus

from fastapi.testclient import TestClient

GET_RECO_MODEL_LIST_PATH = "/reco"


def test_success_auth(client_with_auth: TestClient, test_bearer_token: str) -> None:
    with client_with_auth:
        response = client_with_auth.get(
            GET_RECO_MODEL_LIST_PATH, headers={"Authorization": f"Bearer {test_bearer_token}"}
        )
    assert response.status_code == HTTPStatus.OK
    assert (
        all(
            isinstance(model, dict)
            and all(isinstance(key, str) and isinstance(value, str) for key, value in model.items())
            for model in response.json()
        )
        is True
    )


def test_no_auth(client_with_auth: TestClient) -> None:
    with client_with_auth:
        response = client_with_auth.get(GET_RECO_MODEL_LIST_PATH)
        assert response.status_code == HTTPStatus.FORBIDDEN


def test_wrong_bearer_token_auth(client_with_auth: TestClient, fake_bearer_token: str) -> None:
    with client_with_auth:
        response = client_with_auth.get(
            GET_RECO_MODEL_LIST_PATH, headers={"Authorization": f"Bearer {fake_bearer_token}"}
        )
        assert response.status_code == HTTPStatus.FORBIDDEN
