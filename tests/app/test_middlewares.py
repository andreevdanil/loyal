from http import HTTPStatus
from typing import Callable, Final, NoReturn

from aiohttp.test_utils import Application, TestClient
from aiohttp.web import Request

X_REQUEST_ID: Final[str] = "X-Request-ID"


async def test_request_id_handler_middleware(client: TestClient) -> None:
    url = "/ping"

    headers = {
        X_REQUEST_ID: "",
    }
    response = await client.get(url, headers=headers)
    assert response.status == HTTPStatus.BAD_REQUEST

    assert await response.json() == {
        "message": "X-Request-ID header not found",
    }


async def test_default_error_handler_middleware(
    app: Application,
    aiohttp_client: Callable,
    request_id: str,
) -> None:
    url = "/error/route"

    async def handler(_: Request) -> NoReturn:
        raise NotImplementedError

    app.router.add_get(url, handler)
    client = await aiohttp_client(app)

    headers = {
        X_REQUEST_ID: request_id,
    }
    response = await client.get(url, headers=headers)
    assert response.status == HTTPStatus.INTERNAL_SERVER_ERROR

    assert await response.json() == {
        "message": "Internal Server Error",
    }

    assert response.headers[X_REQUEST_ID] == request_id


async def test_client_error_handler(client: TestClient) -> None:
    url = "/not/found/route"

    response = await client.get(url)
    assert response.status == HTTPStatus.NOT_FOUND

    assert await response.json() == {
        "message": "Not Found",
    }
