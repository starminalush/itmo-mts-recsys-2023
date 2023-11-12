from abc import ABCMeta, abstractmethod


class BaseModel(metaclass=ABCMeta):
    @abstractmethod
    def get_reco(self, user_id: int, num_reco: int) -> list:
        pass
