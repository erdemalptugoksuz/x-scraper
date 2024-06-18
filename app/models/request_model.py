from pydantic import BaseModel
from typing import List


class RequestModel(BaseModel):
    user_ids: List[int]
