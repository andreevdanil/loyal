import pytest
from asyncpg.pool import Pool

from loyal.domain import MatchingService
from loyal.infrastructure import (
    AsyncpgPassportRepository,
    AsyncpgPersonRepository,
)


@pytest.fixture
async def matching_service(asyncpg_pool: Pool) -> MatchingService:
    passports = AsyncpgPassportRepository(asyncpg_pool)
    persons = AsyncpgPersonRepository(asyncpg_pool)
    return MatchingService(passports, persons)
