import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import __version__
from .containers.app import AppContainer
from .routers.sentry import router as sentry_router

logger = logging.getLogger(__name__)


def create() -> FastAPI:
    app_container: AppContainer = AppContainer()
    app_container.core.init_resources()

    app: FastAPI = FastAPI(
        version=__version__,
        description="Sentry-Telegram Proxy Service API",
        debug=app_container.config.api.debug(),
        prefix=app_container.config.api.prefix(),
        root_path=app_container.config.api.root_path(),
    )

    app.state.app_container = app_container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=app_container.config.cors.allow_origins(),
        allow_credentials=app_container.config.cors.allow_credentials(),
        allow_methods=app_container.config.cors.allow_methods(),
        allow_headers=app_container.config.cors.allow_headers(),
    )

    app.include_router(sentry_router)

    return app
