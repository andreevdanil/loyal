import logging
from typing import Callable, Awaitable

from aiohttp import web
from aiohttp.web_exceptions import HTTPClientError
from marshmallow import ValidationError
from loyal.domain.exceptions import UserLoginError
from .responses import server_error, error, validation_error, unauthorized

__all__ = ("register_middlewares",)

Handler = Callable[[web.Request], Awaitable[web.StreamResponse]]


@web.middleware
async def default_handler_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except Exception as e:
        message = f"Caught unhandled exception - {e.__class__.__name__}: {e}"
        request.app.logger.error(message)
        return server_error()


@web.middleware
async def validation_error_handler_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except ValidationError as e:
        return validation_error(e.messages)


@web.middleware
async def client_error_handler_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except HTTPClientError as e:
        message = f"Client error - {e.status}: {e.reason}"
        request.app.logger.error(message)
        return error(e.status, e.reason)


@web.middleware
async def account_error_handler_middleware(
    request: web.Request,
    handler: Handler,
) -> web.StreamResponse:
    try:
        return await handler(request)
    except UserLoginError as e:
        return unauthorized(e.message)


def register_middlewares(app: web.Application) -> None:
    app.middlewares.append(default_handler_middleware)
    app.middlewares.append(validation_error_handler_middleware)
    app.middlewares.append(client_error_handler_middleware)
    app.middlewares.append(account_error_handler_middleware)
