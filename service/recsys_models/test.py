from service.recsys_models.base import BaseModel


class TestModel(BaseModel):
    MODEL_NAME: str = "test_model"

    def get_reco(self, user_id: int, num_reco: int) -> list[int]:
        return list(range(1, num_reco + 1))
