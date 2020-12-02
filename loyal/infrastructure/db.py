from typing import Dict, TypedDict

import attr
from asyncpg.pool import Pool, create_pool
from marshmallow import EXCLUDE, Schema, fields, post_load

__all__ = (
    "AsyncpgPoolConfig",
    "AsyncpgPoolSchema",

    "DB",
    "DBConfig",
    "DBSchema",
)


class AsyncpgPoolConfig(TypedDict, total=False):
    dsn: str
    min_size: int
    max_size: int
    max_queries: int
    max_inactive_connection_lifetime: int
    timeout: float
    command_timeout: float
    statement_cache_size: int
    max_cached_statement_lifetime: int


class AsyncpgPoolSchema(Schema):
    dsn = fields.String(required=True)
    min_size = fields.Int(missing=0)
    max_size = fields.Int(missing=10)
    max_queries = fields.Int(missing=1028)
    max_inactive_connection_lifetime = fields.Int(missing=3600)
    timeout = fields.Float(missing=10)
    command_timeout = fields.Float(missing=10)
    statement_cache_size = fields.Int(missing=1024)
    max_cached_statement_lifetime = fields.Int(missing=3600)

    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_pool(self, data: Dict, **kwargs) -> Pool:
        return create_pool(**data)


class DBConfig(TypedDict):
    pool: AsyncpgPoolConfig


@attr.s(auto_attribs=True, slots=True, frozen=True)
class DB:
    pool: Pool

    async def setup(self) -> None:
        await self.pool

    async def cleanup(self) -> None:
        await self.pool.close()

    async def check_health(self) -> bool:
        return await self.pool.fetchval("select $1::bool", True)

    @classmethod
    def from_config(cls, config: DBConfig) -> "DB":
        return DBSchema().load(config)


class DBSchema(Schema):
    pool = fields.Nested(AsyncpgPoolSchema, required=True)

    @post_load
    def make_db(self, data: Dict, **kwargs) -> DB:
        return DB(**data)
