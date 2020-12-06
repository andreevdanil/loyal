from aiohttp import hdrs, web

from loyal.app.responses import ok

from .v1 import register_api_v1

__all__ = ("register_views",)


async def ping_view(_: web.Request) -> web.Response:
    return ok(message="pong")


def register_views(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view)

    register_api_v1(app)
