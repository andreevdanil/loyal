from datetime import datetime
from typing import Tuple
from uuid import UUID

import attr
from asyncpg.pool import Pool

from loyal.domain import PasswordRepositoryInterface, Password

__all__ = (
    "AsyncpgPasswordRepository",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class AsyncpgPasswordRepository(PasswordRepositoryInterface):
    pool: Pool

    async def add(
        self,
        pid: UUID,
        salt: bytes,
        password: bytes,
        created_at: datetime,
    ):
        query = """
            INSERT INTO passwords (
                id
                , salt
                , password
                , created_at
            ) VALUES (
                $1::UUID
                , $2::BYTEA
                , $3::BYTEA
                , $4::TIMESTAMP
            )
            ;
        """

        await self.pool.execute(
            query,
            pid,
            salt,
            password,
            created_at,
        )

    async def find(self, password_id: UUID) -> Password:
        query = """
            SELECT
                id
                , salt
                , password
                , created_at
            FROM
                passwords
            WHERE
                passwords.id = $1:UUID
            LIMIT 1
            ;
        """

        record = await self.pool.fetchrow(query, password_id)
        return Password(**record)
