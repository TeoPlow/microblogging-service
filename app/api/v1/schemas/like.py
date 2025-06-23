from pydantic import BaseModel


class LikeSchema(BaseModel):
    user_id: int
    name: str
