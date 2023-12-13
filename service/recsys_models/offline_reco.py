import json
from pathlib import Path

from service.recsys_models.base import BaseModel
from service.recsys_models.popular_model import PopModel


class OfflineReco(BaseModel):
    def __init__(self, recos_path: Path | str, popular_model: PopModel):
        self._recos = self._load_recos(recos_path)
        self._pop_model = popular_model

    def _load_recos(self, recos_path: Path | str):
        with open(recos_path) as jf:
            return json.load(jf)

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        if str(user_id) in self._recos:
            return self._recos[str(user_id)][:num_reco]
        return self._pop_model.get_reco(user_id, num_reco)
