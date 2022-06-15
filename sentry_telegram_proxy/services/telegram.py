"""sentry_telegram_proxy.services.telegram."""
import logging

logger = logging.getLogger(__name__)


class TelegramService(object):
    def __init__(self, token: str):
        assert token, "Token is empty"
        self.token: str = token

    async def send_message(self, *args, **kwargs):
        logger.info(*args)
