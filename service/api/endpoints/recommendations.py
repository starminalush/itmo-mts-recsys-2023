from fastapi import APIRouter, Request

from ...log import app_logger
from ...pydantic_schemas.recomendations import RecoModel, RecoResponse
from ..exceptions import ModelNotFoundError, UserNotFoundError

router = APIRouter()


@router.get(path="/", response_model=list[RecoModel])
async def get_all_models(request: Request) -> list[RecoModel]:
    return [RecoModel(name=model.__str__()) for model in request.app.state.models]


@router.get(
    path="/{model_name}/{user_id}",
    response_model=RecoResponse,
)
async def get_reco(request: Request, model_name: str, user_id: int) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")

    if model_name not in [model.__str__() for model in request.app.state.models]:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    model = list(filter(lambda model: model.__str__() == model_name, request.app.state.models))[0]

    k_recs = request.app.state.k_recs
    reco = model.get_reco(user_id=user_id, num_reco=k_recs)
    return RecoResponse(user_id=user_id, items=reco)
