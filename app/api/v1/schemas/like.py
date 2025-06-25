from pydantic import BaseModel


class LikeSchema(BaseModel):
    """
    Pydantic схема лайка.
    """
    user_id: int
    name: str
