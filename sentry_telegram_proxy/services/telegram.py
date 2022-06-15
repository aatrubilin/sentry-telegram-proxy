"""sentry_telegram_proxy.services.telegram."""
import asyncio
import json
import logging

from aiogram import Bot
from aiogram.utils.markdown import code
from aiogram.utils.parts import MAX_MESSAGE_LENGTH, safe_split_text

from ..exceptions import WebhookNotFoundError

logger = logging.getLogger(__name__)

MESSAGE_LENGTH = MAX_MESSAGE_LENGTH - 20


class TelegramService(object):
    def __init__(self, token: str, webhooks: list[dict[str, int]]):
        assert token, "Token is empty"
        self._bot = Bot(token=token, parse_mode="Markdown")
        self._webhooks = {wh["id"]: wh["chat_ids"] for wh in webhooks}

    async def validate_webhook(self, webhook: str):
        if webhook not in self._webhooks:
            raise WebhookNotFoundError

    async def send_message(self, webhook, payload):
        logger.info(payload)
        texts = [
            code(txt)
            for txt in safe_split_text(
                json.dumps(payload, indent=4), length=MESSAGE_LENGTH
            )
        ]
        loop = asyncio.get_running_loop()
        for chat_id in self._webhooks[webhook]:
            for txt in texts:
                loop.create_task(self._bot.send_message(chat_id, txt))
