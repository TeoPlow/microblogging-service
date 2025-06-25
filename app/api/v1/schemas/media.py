from pydantic import BaseModel


class MediaResponse(BaseModel):
    """
    Pydantic схема для ответа о медиа-файле.
    """
    result: bool = True
    media_id: int
