import attr
from asyncpg.pool import Pool

from loyal.domain import UserRepositoryInterface

__all__ = (
    "AsyncpgUserRepository",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class AsyncpgUserRepository(UserRepositoryInterface):
    pool: Pool

    async def add(self):
        pass

    async def get(self):
        pass
