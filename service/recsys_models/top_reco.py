from .base import BaseModel


class TopRecoModel(BaseModel):
    def __str__(self):
        return "top_reco"

    def get_reco(self, user_id: int, num_reco: int) -> list:
        # возвращаем самые популярные среди всего датасета
        return list(range(1, num_reco + 1))
