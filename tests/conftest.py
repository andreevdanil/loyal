# pylint: disable=W0621

import asyncio
from typing import AsyncIterator, Final, List

import asyncpg
import pytest
from asyncpg.pool import Pool

from loyal.domain import (
    PassportRepositoryInterface,
    PersonRepositoryInterface,
)
from loyal.infrastructure import (
    AsyncpgPassportRepository,
    AsyncpgPersonRepository,
)

pytest_plugins: Final[List[str]] = ["loyal.pytest_plugin"]


@pytest.fixture
async def asyncpg_pool(
    loop: asyncio.AbstractEventLoop,
    loyal_db_url: str,
) -> AsyncIterator[Pool]:
    assert loop.is_running()

    pool = await asyncpg.create_pool(loyal_db_url, timeout=1)
    try:
        yield pool
    finally:
        await pool.close()


@pytest.fixture
async def asyncpg_passport_repository(
    asyncpg_pool: Pool,
) -> PassportRepositoryInterface:
    return AsyncpgPassportRepository(asyncpg_pool)


@pytest.fixture
async def asyncpg_person_repository(
    asyncpg_pool: Pool,
) -> PersonRepositoryInterface:
    return AsyncpgPersonRepository(asyncpg_pool)
