import os

from service.recsys_models import BaseModel, TestModel, UserKnn
from service.utils.unpickler import load


def load_models() -> dict[str, BaseModel]:
    user_knn: BaseModel = UserKnn(
        backbone_model=load(os.getenv("USER_KNN_MODEL_PATH")),
    )
    test_model: BaseModel = TestModel()
    models: dict[str, BaseModel] = {"test_model": test_model, "userknn_tfidf": user_knn}
    return models
