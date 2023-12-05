from copy import deepcopy

import pandas as pd

from service.recsys_models.base import BaseModel


class UserKnn(BaseModel):
    def __init__(self, backbone_model):
        self._user_knn_model = deepcopy(backbone_model)

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        return self._user_knn_model.predict([user_id], num_reco)

