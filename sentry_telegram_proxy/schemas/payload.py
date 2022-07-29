"""sentry_telegram_proxy.schemas.payload."""
from typing import Optional

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel, HttpUrl

DEFAULT_MESSAGE_TEMPLATE = (
    "<b>[{data.level_upper}-{data.event.environment}] "
    "{data.project_name}</b>\n\n"
    "<code>{data.message}</code>"
)


class LogEntry(BaseModel):
    formatted: str
    message: Optional[str]
    type: Optional[str]


class Event(BaseModel):
    id: str
    event_id: str
    title: str
    level: str
    version: str
    environment: str
    logger: str
    timestamp: float
    received: float
    nodestore_insert: float
    culprit: str
    location: Optional[str]
    logentry: LogEntry
    modules: dict
    platform: str
    user: Optional[dict]
    request: dict
    contexts: dict
    stacktrace: Optional[dict]
    tags: list
    extra: dict
    fingerprint: list
    hashes: list
    metadata: dict
    _ref: int
    _ref_version: int
    _metrics: dict


class Payload(BaseModel):
    id: str
    project: str
    project_name: str
    project_slug: str
    logger: str | None
    level: str
    culprit: str
    message: str
    url: HttpUrl
    triggering_rules: list
    event: Event

    @property
    def level_upper(self):
        return self.level.upper()

    def get_text(self, template=DEFAULT_MESSAGE_TEMPLATE):
        return template.format(data=self)

    def get_reply_markup(self):
        reply_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"#{self.id}",
                        url=self.url,
                    ),
                ],
            ],
        )
        return reply_markup
