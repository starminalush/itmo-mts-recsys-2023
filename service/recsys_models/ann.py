from rectools.tools import UserToItemAnnRecommender

from service.recsys_models.base import BaseModel
from service.recsys_models.popular_model import PopModel


class ANN(BaseModel):
    def __init__(self, backbone_model: UserToItemAnnRecommender, popular_model: PopModel):
        self._model: UserToItemAnnRecommender = backbone_model
        self._popular_model: PopModel = popular_model

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        popular_items = self._popular_model.get_reco(user_id, num_reco)
        if user_id in self._model.user_id_map.external_ids:
            result = self._model.get_item_list_for_user(user_id, num_reco)
            result = result.tolist()
        return popular_items if (user_id not in self._model.user_id_map.external_ids or len(result) == 0) else result
