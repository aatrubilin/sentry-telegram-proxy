from logging.config import dictConfig as loggingDictConfig

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource


class CoreContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(
        loggingDictConfig,
        config=config.logging,
    )
