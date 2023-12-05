from copy import deepcopy

import pandas as pd

from service.recsys_models.base import BaseModel


class UserKnn(BaseModel):
    def __init__(self, backbone_model, cold_user_reco_model: BaseModel):
        self._user_knn_model = deepcopy(backbone_model)
        self._popular_reco = deepcopy(cold_user_reco_model)

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        result = set()
        result.update(self._popular_reco.get_reco(user_id, num_reco))
        if user_id in self._user_knn_model.users_inv_mapping:
            internal_user_id = self._user_knn_model.users_inv_mapping[user_id]
            df = pd.DataFrame([internal_user_id], columns=["user_id"])
            user_knn_result = self._user_knn_model.predict(df, N_recs=num_reco).item_id.to_list()
            result.update(user_knn_result)
        return list(result)
