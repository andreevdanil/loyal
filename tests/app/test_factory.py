import asyncio
from http import HTTPStatus
from typing import Final
from unittest.mock import patch

import aiohttp
from aiohttp.test_utils import TestClient
from yarl import URL

import loyal

X_REQUEST_ID: Final[str] = "X-Request-ID"


async def test_loyal_tcp_server_fixture(
    loyal_tcp_server: URL,
    request_id: str,
) -> None:
    url = loyal_tcp_server.with_path("ping")

    async with aiohttp.ClientSession() as session:
        headers = {
            X_REQUEST_ID: request_id,
        }
        async with session.get(url, headers=headers) as response:
            assert response.status == HTTPStatus.OK

            assert await response.json() == {
                "data": {},
                "message": "OK",
            }

            assert response.headers[X_REQUEST_ID] == request_id


async def test_asyncio_error_handler(
    client: TestClient,
    loop: asyncio.AbstractEventLoop,
) -> None:
    assert client.app.frozen

    with patch.object(loyal.app.factory.logger, "warning") as warning:
        context = {
            "message": "Something goes wrong",
        }
        loop.call_exception_handler(context)

        message = "Caught asyncio exception: {message}".format_map(context)
        warning.assert_called_with(message)
