from aiohttp import web

from loyal.app import responses, utils
from loyal.app.helpers import get_account_service
from loyal.app.shemas import (
    LoginRequestSchema,
    LoginResponseSchema,
    RegisterRequestSchema,
    UserResponseSchema,
)

__all__ = ("register_api_v1",)


async def register_view(request: web.Request) -> web.Response:
    body = await utils.get_json(request)
    account_service = get_account_service(request)

    credentials = RegisterRequestSchema().load(body)
    user_id = await account_service.register(credentials)

    if user_id is None:
        return responses.conflict("Account already exist")

    data = {
        "user_id": str(user_id),
    }
    return responses.ok(data)


async def user_view(request: web.Request) -> web.Response:
    account_service = get_account_service(request)
    user_id = request.match_info["user_id"]

    user = await account_service.get_user_info(user_id)

    if user is None:
        responses.not_found("User not found")

    data = UserResponseSchema().dump(user)
    return responses.ok(data)


async def login_view(request: web.Request) -> web.Response:
    body = await utils.get_json(request)
    account_service = get_account_service(request)

    credentials = LoginRequestSchema().load(body)
    result = await account_service.login(credentials)

    response_data = LoginResponseSchema().dump(result)
    return responses.ok(response_data)


def register_api_v1(root: web.Application) -> None:
    v1_app = web.Application()

    v1_app.router.add_post("/users", register_view)
    v1_app.router.add_get("/users/{user_id}", user_view)

    v1_app.router.add_post("/tokens", login_view)

    root.add_subapp("/api/v1/", v1_app)
