"""sentry_telegram_proxy.services.telegram."""
import asyncio
import io
import json
import logging

from aiogram import Bot
from aiogram.types import InputFile

from ..exceptions import WebhookNotFoundError

logger = logging.getLogger(__name__)


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
        fp = io.StringIO()
        json.dump(payload, fp)
        fp.seek(0)
        input_file = InputFile(fp, filename="sentry-data.json")
        loop = asyncio.get_running_loop()
        for chat_id in self._webhooks[webhook]:
            loop.create_task(self._bot.send_document(chat_id, input_file))
