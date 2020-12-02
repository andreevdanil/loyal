import attr
from asyncpg.pool import Pool

from loyal.domain import PasswordRepositoryInterface

__all__ = (
    "AsyncpgPasswordRepository",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class AsyncpgPasswordRepository(PasswordRepositoryInterface):
    pool: Pool

    async def add(self):
        pass

    async def update(self):
        pass
