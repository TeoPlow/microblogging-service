from pydantic import BaseModel, Field
from app.api.utils.base_responses import BaseResponse


class SimpleUser(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class UserOutput(BaseModel):
    name: str
    id: int
    followers: list[SimpleUser] = Field(..., alias="followers_users")
    following: list[SimpleUser] = Field(..., alias="following_users")

    model_config = {
        "from_attributes": True,
        "populate_by_name": True,
    }


class UserGetMeResponse(BaseResponse):
    user: UserOutput
