from aiohttp import web

import loyal


def create_app() -> web.Application:
    config = {}

    return loyal.create_app(config)


def main() -> None:
    app = create_app()

    web.run_app(
        app,
        host="0.0.0.0",
        port=8080,
    )


if __name__ == "__main__":
    main()
