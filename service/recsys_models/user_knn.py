from copy import deepcopy

from service.models.user_knn import UserKnn as UserKnnModel
from service.recsys_models.base import BaseModel


class UserKnn(BaseModel):
    def __init__(self, backbone_model: UserKnnModel):
        self._user_knn_model = deepcopy(backbone_model)

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        return self._user_knn_model.recommend(user_id, num_reco)
