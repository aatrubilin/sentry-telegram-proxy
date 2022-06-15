from .base import APIError


class InvalidSignatureError(APIError):
    status_code: int = 401
    detail: str = "InvalidSignature"


class NoSignatureError(APIError):
    status_code: int = 401
    detail: str = "NoSignature"
