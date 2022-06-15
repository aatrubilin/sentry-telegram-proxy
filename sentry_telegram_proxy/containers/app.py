import os

from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Configuration, Container, Singleton

from ..services import TelegramService
from .core import CoreContainer


class AppContainer(DeclarativeContainer):

    wiring_config = WiringConfiguration(modules=["..routers.sentry"])

    config: Configuration = Configuration(strict=True)
    config.from_yaml(os.environ["CONFIG"], required=True)

    core: Container[CoreContainer] = Container(CoreContainer, config=config.core)

    telegram: Singleton[TelegramService] = Singleton(
        TelegramService, token=config.telegram.token
    )
