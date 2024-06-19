from pydantic import BaseModel
from typing import List


class IdRequestModel(BaseModel):
    user_ids: List[int]


class UrlRequestModel(BaseModel):
    users: List[object]
