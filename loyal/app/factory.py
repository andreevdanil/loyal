import logging
from typing import Dict
import uvloop
from aiohttp import web

from .middlewares import register_middlewares
from .views import register_views
from loyal.log import install_log

logger = logging.getLogger("app")


def create_app(config: Dict) -> web.Application:
    install_log()
    uvloop.install()

    app = web.Application(logger=logger)
    app["config"] = config

    register_middlewares(app)
    register_views(app)

    return app
