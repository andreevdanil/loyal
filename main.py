from environs import Env
from aiohttp import web

import loyal

env = Env()


def create_app() -> web.Application:
    config = {}

    return loyal.create_app(config)


def main() -> None:
    app = create_app()
    port = env.int("PORT", 8080)

    web.run_app(
        app,
        host="0.0.0.0",
        port=port,
    )


if __name__ == "__main__":
    main()
