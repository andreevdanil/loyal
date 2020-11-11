from aiohttp import web, hdrs
from .responses import ok

__all__ = ("register_views",)


async def ping_view(_: web.Request) -> web.Response:
    return ok(message="pong")


async def register_v1_view(_: web.Request) -> web.Response:
    return ok(message="register")


async def login_v1_view(_: web.Request) -> web.Response:
    return ok(message="login")


def register_api_v1(root: web.Application) -> None:
    v1_app = web.Application()
    v1_app.router.add_post("/register", register_v1_view)
    v1_app.router.add_post("/login", login_v1_view)

    root.add_subapp("/api/v1/", v1_app)


def register_views(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view)

    register_api_v1(app)
