from app.api.utils.base_responses import BaseErrorResponse


class ApiException(Exception):
    """Базовое исключение для всех ошибок API"""

    def to_dict(self):
        return BaseErrorResponse(
            error_message=self.error_message,
            error_type=self.error_type
        ).model_dump()


class SomeError(ApiException):
    """Какая-то ошибка"""

    def __init__(
        self, error_message="Возникла какая-то ошибка", error_type="SomeError"
    ):
        self.error_message = error_message
        self.error_type = error_type


class NotFoundError(ApiException):
    """Не найдено"""

    def __init__(
        self,
        error_message="Возникла ошибка 'Не найдено'",
        error_type="NotFoundError",
    ):
        self.error_message = error_message
        self.error_type = error_type


class InvalidApiKey(ApiException):
    """Исключение при неверном API ключе"""

    def __init__(
        self,
        error_message="API ключ не найден или некорректен",
        error_type="InvalidApiKey",
    ):
        self.error_message = error_message
        self.error_type = error_type


class ConflictError(ApiException):
    """Исключение при конфликте"""

    def __init__(
        self, error_message="Возник некий конфликт", error_type="ConflictError"
    ):
        self.error_message = error_message
        self.error_type = error_type
