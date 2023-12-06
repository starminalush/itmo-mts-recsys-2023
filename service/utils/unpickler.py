import os
import pickle


class ModelUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        return super().find_class(module, name)


def load(path: str):
    with open(os.path.join(path), "rb") as f:
        return pickle.load(f)
