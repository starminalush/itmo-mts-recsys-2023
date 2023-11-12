from fastapi import APIRouter, Depends, Request

from ...log import app_logger
from ...pydantic_schemas.recommendations import RecoModel, RecoResponse
from ..auth.auth_bearer import JWTBearer, jwt_bearer
from ..exceptions import ModelNotFoundError, UserNotFoundError

router = APIRouter()


@router.get(path="/", response_model=list[RecoModel], dependencies=[Depends(jwt_bearer)])
async def get_all_models(request: Request) -> list[RecoModel]:
    return [RecoModel(name=getattr(model, "MODEL_NAME")) for model in request.app.state.models]


@router.get(path="/{model_name}/{user_id}", response_model=RecoResponse, dependencies=[Depends(jwt_bearer)])
async def get_reco(request: Request, model_name: str, user_id: int) -> RecoResponse:
    app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")
    models_list = request.app.state.models
    if model_name not in [getattr(model, "MODEL_NAME") for model in models_list]:
        raise ModelNotFoundError(error_message=f"Model {model_name} not found")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    model = list(filter(lambda model: getattr(model, "MODEL_NAME") == model_name, models_list))[0]

    k_recs = request.app.state.k_recs
    reco = model.get_reco(user_id=user_id, num_reco=k_recs)
    return RecoResponse(user_id=user_id, items=reco)
