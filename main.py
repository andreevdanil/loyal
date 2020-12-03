from environs import Env
from aiohttp import web

import loyal


async def create_app() -> web.Application:
    env = Env()

    config = {
        "jwt_secret": env.str("JWT_SECRET", "secret"),
        "db": {
            "pool": {
                "dsn": env.str("DATABASE_URL", "postgres://jcvurehn:nFry4ycZcYSiQ8ZmTXL0AZjYJ-ECx_Xm@dumbo.db.elephantsql.com:5432/jcvurehn"),
                "min_size": env.int("DATABASE_POOL_MIN_SIZE", 1),
                "max_size": env.int("DATABASE_POOL_MAX_SIZE", 10),
            },
        },
    }

    return await loyal.create_app(config)


if __name__ == "__main__":
    web.run_app(create_app())
