from aiohttp import web
from environs import Env

import loyal


async def create_app() -> web.Application:
    env = Env()

    config: loyal.AppConfig = {
        "jwt_secret": env.str("JWT_SECRET", "secret"),
        "db": {
            "pool": {
                "dsn": env.str("DATABASE_URL", "postgres://jcvurehn:nFry4ycZcYSiQ8ZmTXL0AZjYJ-ECx_Xm@dumbo.db.elephantsql.com:5432/jcvurehn"),
                "min_size": env.int("DATABASE_POOL_MIN_SIZE", 1),
                "max_size": env.int("DATABASE_POOL_MAX_SIZE", 10),
            },
        },
        "ethereum": {
            "node_url": env.str("ETH_NODE_URL", "wss://kovan.infura.io/ws/v3/776e4318c8844d01830f74bc865059ea"),
            "contract_address": "0x1AA87f0bdcDFdbBd7Be8381Ca3BD379A01e246Da",
        },
    }

    return await loyal.create_app(config)


if __name__ == "__main__":
    web.run_app(create_app())
