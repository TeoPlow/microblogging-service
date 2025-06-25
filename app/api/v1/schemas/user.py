from pydantic import BaseModel
from app.api.utils.base_responses import BaseResponse


class SimpleUser(BaseModel):
    """
    Pydantic схема простого пользователя.
    """
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class UserOutput(BaseModel):
    """
    Pydantic схема для вывода полной информации о пользователе.
    """
    id: int
    name: str
    followers: list[SimpleUser]
    following: list[SimpleUser]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class UserGetMeResponse(BaseResponse):
    user: UserOutput
