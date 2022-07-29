"""sentry_telegram_proxy.services.telegram."""
import asyncio
import io
import json
import logging
from typing import TypedDict

from aiogram import Bot
from aiogram.types import InputFile

from ..exceptions import WebhookNotFoundError
from ..schemas.payload import Payload

logger = logging.getLogger(__name__)


class Webhook(TypedDict):
    id: str
    chat_ids: list[int]


class TelegramService(object):
    def __init__(self, token: str, webhooks: list[Webhook]):
        assert token, "Token is empty"
        self._bot = Bot(token=token, parse_mode="HTML")
        self._webhooks: dict[str, list[int]] = {
            wh["id"]: wh["chat_ids"] for wh in webhooks
        }

    async def validate_webhook(self, webhook: str):
        if webhook not in self._webhooks:
            raise WebhookNotFoundError

    async def send_message(self, webhook: str, payload: Payload):
        text = payload.get_text()
        reply_markup = payload.get_reply_markup()

        loop = asyncio.get_running_loop()
        for chat_id in self._webhooks[webhook]:
            loop.create_task(
                self._bot.send_message(chat_id, text=text, reply_markup=reply_markup)
            )

    async def send_document(self, webhook: str, payload: dict):
        logger.info(payload)
        fp = io.StringIO()
        json.dump(payload, fp, indent=4)
        fp.seek(0)
        filename = (
            f"{payload.get('project_slug', 'unknown_project')}_"
            f"{payload.get('id', '0')}.json"
        )
        input_file = InputFile(fp, filename=filename)
        loop = asyncio.get_running_loop()
        for chat_id in self._webhooks[webhook]:
            loop.create_task(self._bot.send_document(chat_id, input_file))
