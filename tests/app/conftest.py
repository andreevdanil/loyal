# pylint: disable=W0621

from typing import Callable

import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

import loyal


@pytest.fixture
async def app(
    loyal_db_url: str,
    loyal_app_factory: Callable,
) -> web.Application:
    config: loyal.AppConfig = {
        "db": {
            "pool": {
                "dsn": loyal_db_url,
                "min_size": 1,
                "max_size": 5,
            },
        },
    }
    return await loyal_app_factory(config)


@pytest.fixture
async def client(
    aiohttp_client: Callable,
    app: web.Application,
    request_id: str,
) -> TestClient:
    headers = {
        "X-Request-Id": request_id,
    }
    return await aiohttp_client(app, headers=headers)
