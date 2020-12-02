from enum import unique

from aiohttp import web
from strenum import StrEnum
from loyal.infrastructure import DB

__all__ = (
    "set_db",
    "get_db",
    "get_user_repository",
    "get_password_repository",
    "get_account_service",
)


@unique
class AppKeys(StrEnum):
    DB = "db"


def set_db(app: web.Application, db: DB) -> None:
    app[AppKeys.DB] = db


def get_db(app: web.Application) -> DB:
    return app[AppKeys.DB]


def get_user_repository(app: web.Application) -> UserRepository:
    db = get_db(app)
    return UserRepository(db.pool)


def get_password_repository(app: web.Application) -> PasswordRepository:
    db = get_db(app)
    return PasswordRepository(db.pool)


def get_account_service(app: web.Application) -> AccountService:
    users_repository = get_user_repository(app)
    passwords_repository = get_password_repository(app)
    return AccountService(users_repository, passwords_repository)
