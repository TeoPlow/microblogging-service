from pydantic import BaseModel
from typing import Any


class BaseErrorResponse(BaseModel):
    """
    Базовый класс для возвращения форматированного ответа об ошибке.
    """
    result: bool = False
    error_type: str
    error_message: str


class BaseResponse(BaseModel):
    """
    Базовый класс для возвращения форматированного ответа об успешной операции.
    """
    result: bool = True


error_responses: dict[int | str, dict[str, Any]] | None = {
    400: {"model": BaseErrorResponse},
    422: {"model": BaseErrorResponse},
    500: {"model": BaseErrorResponse},
}
