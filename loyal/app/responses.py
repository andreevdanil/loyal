from http import HTTPStatus
from typing import Any, Dict

import ujson
from aiohttp import web

__all__ = (
    "create_response",
    "ok",
    "error",
    "unauthorized",
    "not_found",
    "conflict",
    "validation_error",
    "server_error",
)


def create_response(body: Dict, code: int) -> web.Response:
    payload = ujson.dumps(body)
    return web.json_response(text=payload, status=code)


def ok(data: Dict = None, message: str = "OK") -> web.Response:
    status = HTTPStatus.OK
    body = {
        "data": data,
        "message": message,
    }
    return create_response(body, status)


def error(code: int, message: str = None, data: Dict = None) -> web.Response:
    body = {
        "message": message or HTTPStatus(code).description,
        "data": data,
    }
    return create_response(body, code)


def unauthorized(message: str) -> web.Response:  # 401
    status = HTTPStatus.UNAUTHORIZED
    return error(status, message)


def not_found(message: str) -> web.Response:  # 404
    status = HTTPStatus.NOT_FOUND
    return error(status, message)


def conflict(message: str) -> web.Response:  # 409
    status = HTTPStatus.CONFLICT
    return error(status, message)


def validation_error(errors: Any) -> web.Response:  # 422
    status = HTTPStatus.UNPROCESSABLE_ENTITY
    message = "Input payload validation failed"
    return error(status, message, errors)


def server_error() -> web.Response:  # 500
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    return error(status, message="Internal server error. Try again later")
