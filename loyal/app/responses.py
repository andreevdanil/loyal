from http import HTTPStatus
from typing import Dict, Any
import ujson
from aiohttp import web

__all__ = (
    "create_response",
    "ok",
    "error",
    "validation_error",
    "server_error",
)


def create_response(body: Dict, status: HTTPStatus) -> web.Response:
    payload = ujson.dumps(body)
    return web.json_response(text=payload, status=status)


def ok(data: Dict = None, message: str = "OK") -> web.Response:
    status = HTTPStatus.OK
    body = {
        "data": data,
        "message": message,
    }
    return create_response(body, status)


def error(
    status: HTTPStatus,
    message: str = None,
    data: Dict = None,
) -> web.Response:
    body = {
        "message": message or status.description,
        "data": data,
    }
    return create_response(body, status)


def validation_error(errors: Any) -> web.Response:  # 422
    status = HTTPStatus.UNPROCESSABLE_ENTITY
    message = "Input payload validation failed"
    return error(status, message, errors)


def server_error() -> web.Response:  # 500
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    return error(status, message="Internal server error. Try again later")
