from .base import APIError


class WebhookNotFoundError(APIError):
    status_code: int = 404
    detail: str = "WebhookNotFound"
