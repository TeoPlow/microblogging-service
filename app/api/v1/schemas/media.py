from pydantic import BaseModel


class MediaResponse(BaseModel):
    result: bool = True
    media_id: int
