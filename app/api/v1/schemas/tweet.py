from pydantic import BaseModel
from typing import List
from .user import SimpleUser
from .like import LikeSchema
from app.api.utils.base_responses import BaseResponse


class TweetSendRequest(BaseModel):
    tweet_data: str
    tweet_media_ids: List[int]


class TweetResponse(BaseModel):
    id: int
    content: str
    attachments: List[str]
    author: SimpleUser
    likes: List[LikeSchema]


class TweetListResponse(BaseResponse):
    tweets: List[TweetResponse]


class TweetSendResponse(BaseResponse):
    tweet_id: int
