from pydantic import BaseModel


class BaseErrorResponse(BaseModel):
    result: bool = False
    error_type: str
    error_message: str


class BaseResponse(BaseModel):
    result: bool = True


error_responses = {
    400: {"model": BaseErrorResponse},
    422: {"model": BaseErrorResponse},
    500: {"model": BaseErrorResponse},
}
