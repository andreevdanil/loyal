import uuid

from aiohttp import web, hdrs
from .responses import ok

__all__ = ("register_views",)

ID = 10


async def ping_view(_: web.Request) -> web.Response:
    return ok(message="pong")


async def register_user_view(_: web.Request) -> web.Response:
    global ID
    data = {
        "user_id": ID,
        "access_token": str(uuid.uuid4())
    }
    ID = ID + 1
    return ok(data=data)


async def login_user_view(_: web.Request) -> web.Response:
    global ID
    data = {
        "user_id": ID,
        "access_token": str(uuid.uuid4())
    }
    ID = ID + 1
    return ok(data=data)


def register_api_v1(root: web.Application) -> None:
    v1_app = web.Application()

    v1_app.router.add_post("/users", register_user_view)
    v1_app.router.add_post("/tokens", login_user_view)

    root.add_subapp("/api/v1/", v1_app)


def register_views(app: web.Application) -> None:
    app.router.add_route(hdrs.METH_ANY, "/ping", ping_view)

    register_api_v1(app)
