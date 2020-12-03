from enum import unique

from aiohttp import web
from strenum import StrEnum

from loyal.domain import AccountService
from loyal.infrastructure import (
    DB,
    AsyncpgUserRepository,
    AsyncpgPasswordRepository,
)

__all__ = (
    "set_jwt_secret",
    "set_db",
    "get_db",
    "get_user_repository",
    "get_password_repository",
    "get_account_service",
)


@unique
class AppKeys(StrEnum):
    JWT_SECRET = "jwt_secret"
    DB = "db"


def set_jwt_secret(app: web.Application, secret: str) -> None:
    app[AppKeys.JWT_SECRET] = secret


def get_jwt_secret(app: web.Application) -> str:
    return app[AppKeys.JWT_SECRET]


def set_db(app: web.Application, db: DB) -> None:
    app[AppKeys.DB] = db


def get_db(app: web.Application) -> DB:
    return app[AppKeys.DB]


def get_user_repository(app: web.Application) -> AsyncpgUserRepository:
    db = get_db(app)
    return AsyncpgUserRepository(db.pool)


def get_password_repository(app: web.Application) -> AsyncpgPasswordRepository:
    db = get_db(app)
    return AsyncpgPasswordRepository(db.pool)


def get_account_service(app: web.Application) -> AccountService:
    jwt_secret = get_jwt_secret(app)
    users_repository = get_user_repository(app)
    passwords_repository = get_password_repository(app)
    return AccountService(jwt_secret, users_repository, passwords_repository)
