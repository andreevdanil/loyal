from datetime import datetime
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
        password_id: UUID,
        email: str,
        created_at: datetime,
    ):
        query = """
            INSERT INTO users (
                id
                , first_name
                , second_name
                , email
                , password_id
                , balance
                , created_at
            ) VALUES (
                $1::UUID
                , $2::TEXT
                , $3::TEXT
                , $4::TEXT
                , $2::UUID
                , $3::FLOAT
                , $4::TIMESTAMP
            )
             ;
         """

        await self.pool.execute(
            query,
            uid,
            first_name,
            last_name,
            password_id,
            email,
            created_at,
        )

    async def find_by_id(self, uid: UUID) -> Account:
        query = """
            SELECT
                id
                , first_name
                , second_name
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

    async def find_by_email(self, email: str) -> Account:
        query = """
            SELECT
                id
                , first_name
                , second_name
                , email
                , password_id
                , balance
                , created_at
            FROM
                users
            WHERE
                users.email = $1:TEXT
            LIMIT 1
            ;
        """

        record = await self.pool.fetchrow(query, email)
        return Account(**record)
