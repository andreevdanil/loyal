import asyncio
import logging
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Dict, TypedDict

import uvloop
from aiohttp import web

from loyal.infrastructure import DB, DBConfig, EthConfig, make_eth_client
from loyal.log import setup_logging

from .helpers import set_db, set_jwt_secret, set_eth
from .middlewares import register_middlewares
from .views import register_views

logger = logging.getLogger("app")


class AppConfig(TypedDict):
    jwt_secret: str
    db: DBConfig
    ethereum: EthConfig


def register_db(app: web.Application, db_config: DBConfig) -> None:
    db = DB.from_config(db_config)
    set_db(app, db)

    app.on_startup.append(lambda _: db.setup())
    app.on_cleanup.append(lambda _: db.cleanup())


def register_eth(app: web.Application, eth_config: EthConfig) -> None:
    eth = make_eth_client(eth_config)
    set_eth(app, eth)


def asyncio_exception_handler(_, context: Dict) -> None:
    message = "Caught asyncio exception: {message}".format_map(context)
    logger.warning(message)


def setup_asyncio() -> None:
    uvloop.install()
    loop = asyncio.get_event_loop()

    executor = ThreadPoolExecutor(thread_name_prefix="loyal")
    loop.set_default_executor(executor)

    loop.set_exception_handler(asyncio_exception_handler)


async def create_app(config: AppConfig) -> web.Application:
    setup_logging()
    setup_asyncio()

    app = web.Application(logger=logger)
    register_views(app)
    register_middlewares(app)

    set_jwt_secret(app, config["jwt_secret"])
    register_db(app, config["db"])
    register_eth(app, config["ethereum"])

    return app
