from http import HTTPStatus

from fastapi.testclient import TestClient

from service.settings import ServiceConfig

GET_RECO_PATH = "/reco/{model_name}/{user_id}/"
GET_RECO_MODELS_LIST_PATH = "/reco"
GET_HEALTH_PATH = "/health"


def test_health(
    client: TestClient,
) -> None:
    with client:
        response = client.get(GET_HEALTH_PATH)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] == "OK"


def test_reco_model_list(
    client: TestClient,
) -> None:
    with client:
        response = client.get(GET_RECO_MODELS_LIST_PATH)
    assert response.status_code == HTTPStatus.OK


def test_get_reco_success(
    client: TestClient,
    service_config: ServiceConfig,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(model_name="test_model", user_id=user_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["user_id"] == user_id
    assert len(response_json["items"]) == service_config.k_recs
    assert all(isinstance(item_id, int) for item_id in response_json["items"])


def test_get_reco_for_unknown_user(
    client: TestClient,
) -> None:
    user_id = 10**10
    path = GET_RECO_PATH.format(model_name="test_model", user_id=user_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


def test_get_reco_from_unknown_model(client: TestClient) -> None:
    model_name = "unknown_model"
    path = GET_RECO_PATH.format(model_name=model_name, user_id=1)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "model_not_found"


def test_get_reco_wrong_user_id_type(client: TestClient) -> None:
    user_id = "user_ud"
    path = GET_RECO_PATH.format(model_name="test_model", user_id=user_id)
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()["errors"][0]["error_key"] == "int_parsing"
