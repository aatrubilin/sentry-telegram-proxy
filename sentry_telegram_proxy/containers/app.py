import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Container, Singleton

from ..services import SentrySrvice, TelegramService
from .core import CoreContainer


class AppContainer(DeclarativeContainer):

    wiring_config = WiringConfiguration(modules=["..routers.sentry"])

    config: Configuration = Configuration(strict=True)
    config.from_yaml(os.environ["CONFIG"], required=True)

    core: Container[CoreContainer] = Container[CoreContainer](
        CoreContainer, config=config.core
    )

    telegram: Singleton[TelegramService] = Singleton[TelegramService](
        TelegramService, token=config.telegram.token, webhooks=config.telegram.webhooks
    )
    sentry: Singleton[SentrySrvice] = Singleton[SentrySrvice](
        SentrySrvice,
        secret=config.sentry.secret,
    )
