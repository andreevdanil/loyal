from environs import Env
from aiohttp import web

import loyal


def create_app() -> web.Application:
    env = Env()

    config = {
        "db": {
            "pool": {
                "dsn": env.str("DATABASE_URL"),
                "min_size": env.int("DATABASE_POOL_MIN_SIZE", 1),
                "max_size": env.int("DATABASE_POOL_MAX_SIZE", 10),
            },
        },
    }

    return await loyal.create_app(config)
