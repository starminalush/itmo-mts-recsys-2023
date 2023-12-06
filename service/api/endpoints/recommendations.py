import logging

from fastapi import APIRouter, Depends, Request

from service.api.auth import bearer_auth
from service.api.exceptions import ModelNotFoundError, UserNotFoundError
from service.log import app_logger
from service.pydantic_schemas.error import Error
from service.pydantic_schemas.reco import RecoModel, RecoResponse

router = APIRouter()


@router.get(
    path="",
    dependencies=[Depends(bearer_auth)],
    responses={
        200: {"model": list[RecoModel]},
        401: {
            "model": Error,
            "description": "Authentication error",
        },
    },
)
async def get_all_models(request: Request) -> list[RecoModel]:
    return [RecoModel(name=model_name) for model_name in request.app.state.models.keys()]


@router.get(
    path="/{model_name}/{user_id}",
    dependencies=[Depends(bearer_auth)],
    responses={
        200: {"model": RecoResponse},
        401: {
            "model": Error,
            "description": "Authentication error",
        },
        404: {
            "model": Error,
            "description": "Not Found Error",
        },
    },
)
async def get_reco(request: Request, model_name: str, user_id: int) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")
    models_list = request.app.state.models
    model = models_list.get(model_name, None)
    if not model:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    k_recs = request.app.state.k_recs
    try:
        reco = model.get_reco(user_id=user_id, num_reco=k_recs)
    except ValueError as err:
        logging.error(err)
        raise UserNotFoundError(error_message=f"User {user_id} not found")
    return RecoResponse(user_id=user_id, items=reco)
