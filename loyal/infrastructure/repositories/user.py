from datetime import datetime
from typing import Optional
from uuid import UUID

import attr
from asyncpg.pool import Pool

from loyal.domain import UserRepositoryInterface, Account

__all__ = (
    "AsyncpgUserRepository",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class AsyncpgUserRepository(UserRepositoryInterface):
    pool: Pool

    async def add(
        self,
        uid: UUID,
        first_name: str,
        last_name: str,
        email: str,
        password_id: UUID,
        balance: float,
        created_at: datetime,
    ):
        query = """
            INSERT INTO users (
                id
                , first_name
                , last_name
                , email
                , password_id
                , balance
                , created_at
            ) VALUES (
                $1::UUID
                , $2::TEXT
                , $3::TEXT
                , $4::TEXT
                , $5::UUID
                , $6::FLOAT
                , $7::TIMESTAMP
            )
            ;
         """

        await self.pool.fetch(
            query,
            uid,
            first_name,
            last_name,
            email,
            password_id,
            balance,
            created_at,
        )

    async def find_by_id(self, uid: UUID) -> Optional[Account]:
        query = """
            SELECT
                id
                , first_name
                , last_name
                , email
                , password_id
                , balance
                , created_at
            FROM
                users
            WHERE
                users.id = $1:UUID
            LIMIT 1
            ;
        """

        record = await self.pool.fetchrow(query, uid)
        return Account(**record)

    async def find_by_email(self, email: str) -> Optional[Account]:
        query = """
            SELECT
                id
                , first_name
                , last_name
                , email
                , password_id
                , balance
                , created_at
            FROM
                users
            WHERE
                users.email = $1::TEXT
            LIMIT 1
            ;
        """

        record = await self.pool.fetchrow(query, email)
        return Account(**record) if record else None
