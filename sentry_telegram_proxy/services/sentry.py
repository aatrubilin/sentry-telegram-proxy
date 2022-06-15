"""sentry_telegram_proxy.services.sentry."""
import hashlib
import hmac

from fastapi import Request

from ..exceptions import InvalidSignatureError, NoSignatureError


class SentrySrvice(object):
    def __init__(self, secret: str):
        self.__secret = secret.encode("utf-8")

    async def validate_request(self, request: Request):
        expected_digest = request.headers.get("sentry-hook-signature")
        if not expected_digest:
            raise NoSignatureError

        body = await request.json()
        digest = hmac.new(
            key=self.__secret,
            msg=body,
            digestmod=hashlib.sha256,
        ).hexdigest()

        if digest != expected_digest:
            raise InvalidSignatureError
