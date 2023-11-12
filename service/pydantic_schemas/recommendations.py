from pydantic import BaseModel


class RecoResponse(BaseModel):
    user_id: int
    items: list[int]


class RecoModel(BaseModel):
    name: str
