import os
import pickle


class ModelUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == "UserKnn":
            from service.models.user_knn import UserKnn

            return UserKnn
        return super().find_class(module, name)


def load(path: str):
    with open(os.path.join(path), "rb") as f:
        return pickle.load(f)
