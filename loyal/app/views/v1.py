from aiohttp import web

from loyal.app import utils
from loyal.app.helpers import get_account_service
from loyal.app.responses import ok
from loyal.app.shemas import (
    RegisterRequestSchema,
    RegisterResponseSchema,
    LoginRequestSchema,
    LoginResponseSchema,
)

__all__ = ("register_api_v1",)


async def register_view(request: web.Request) -> web.Response:
    body = await utils.get_json(request)
    account_service = get_account_service(request.match_info.apps[0])

    register_credentials = RegisterRequestSchema().load(body)
    user = await account_service.register(register_credentials)

    response_data = RegisterResponseSchema().dump(user)
    return ok(response_data)


async def login_view(request: web.Request) -> web.Response:
    body = await utils.get_json(request)
    account_service = get_account_service(request.match_info.apps[0])

    login_credentials = LoginRequestSchema().load(body)
    token = await account_service.login(login_credentials)

    response_data = LoginResponseSchema().dump(token)
    return ok(response_data)


def register_api_v1(root: web.Application) -> None:
    v1_app = web.Application()

    v1_app.router.add_post("/users", register_view)
    v1_app.router.add_post("/tokens", login_view)

    root.add_subapp("/api/v1/", v1_app)
