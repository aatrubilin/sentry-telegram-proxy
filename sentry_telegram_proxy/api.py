import argparse
import os
from typing import Type

import uvicorn


class RestApiNamespace(argparse.Namespace):
    config: str
    host: str = "localhost"
    port: int = 8000
    workers: int = 1
    debug: int = False
    reload: bool = False
    server_header: bool = False
    log_level: str = "info"


def restapi_parse_args() -> Type[RestApiNamespace]:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Sentry-Telegram Proxy Service"
    )
    parser.add_argument(
        "--config", default="config/config.yaml", required=False, type=str
    )
    parser.add_argument("--host", default="localhost", required=False, type=str)
    parser.add_argument("--port", default=8000, type=int)
    parser.add_argument("--workers", default=1, type=int)
    parser.add_argument("--debug", default=False, action="store_true")
    parser.add_argument("--reload", default=False, action="store_true")
    parser.add_argument("--server-header", default=False, action="store_true")
    parser.add_argument(
        "--log-level",
        default="info",
        choices=["critical", "error", "warning", "info", "debug", "trace"],
    )
    return parser.parse_args(namespace=RestApiNamespace)


def restapi() -> None:
    args = restapi_parse_args()

    if not os.path.isfile(args.config) and args.debug is True:
        config = "config/config.dev.yaml"
    else:
        config = args.config
    os.environ["CONFIG"] = config

    uvicorn.run(
        "sentry_telegram_proxy.app:create",
        host=args.host,
        port=args.port,
        debug=args.debug,
        reload=args.reload,
        reload_dirs=["sentry_telegram_proxy/", "config/"] if args.reload else [],
        workers=args.workers,
        server_header=args.server_header,
        log_level=args.log_level,
        factory=True,
    )
