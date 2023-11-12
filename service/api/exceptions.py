from http import HTTPStatus
from typing import Sequence


class AppException(Exception):
    def __init__(
        self,
        status_code: int,
        error_key: str,
        error_message: str = "",
        error_loc: Sequence[str] | None = None,
    ) -> None:
        self.error_key = error_key
        self.error_message = error_message
        self.error_loc = error_loc
        self.status_code = status_code
        super().__init__()


class UnauthorizedUserError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.UNAUTHORIZED,
        error_key: str = "invalid_jwt_token",
        error_message: str = "Invalid JWT token",
        error_loc: Sequence[str] | None = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)


class UserNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "user_not_found",
        error_message: str = "User is unknown",
        error_loc: Sequence[str] | None = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)


class ModelNotFoundError(AppException):
    def __init__(
        self,
        status_code: int = HTTPStatus.NOT_FOUND,
        error_key: str = "model_not_found",
        error_message: str = "Model is unknown",
        error_loc: Sequence[str] | None = None,
    ):
        super().__init__(status_code, error_key, error_message, error_loc)
