from enum import unique

from aiohttp import web
from strenum import StrEnum

from loyal.domain import AccountService
from loyal.infrastructure import (
    DB,
    AsyncpgPasswordRepository,
    AsyncpgUserRepository, EthereumService,
)

__all__ = (
    "set_jwt_secret",
    "set_db",
    "get_db",
    "set_eth",
    "get_eth",
    "get_user_repository",
    "get_password_repository",
    "get_account_service",
)


@unique
class AppKeys(StrEnum):
    JWT_SECRET = "jwt_secret"
    DB = "db"
    ETH = "ethereum"


def set_jwt_secret(app: web.Application, secret: str) -> None:
    app[AppKeys.JWT_SECRET] = secret


def get_jwt_secret(app: web.Application) -> str:
    return app[AppKeys.JWT_SECRET]


def set_db(app: web.Application, db: DB) -> None:
    app[AppKeys.DB] = db


def get_db(app: web.Application) -> DB:
    return app[AppKeys.DB]


def set_eth(app: web.Application, eth: EthereumService) -> None:
    app[AppKeys.ETH] = eth


def get_eth(app: web.Application) -> EthereumService:
    return app[AppKeys.ETH]


def get_user_repository(app: web.Application) -> AsyncpgUserRepository:
    db = get_db(app)
    return AsyncpgUserRepository(db.pool)


def get_password_repository(app: web.Application) -> AsyncpgPasswordRepository:
    db = get_db(app)
    return AsyncpgPasswordRepository(db.pool)


def get_root_app(request: web.Request) -> web.Application:
    return request.match_info.apps[0]


def get_account_service(request: web.Request) -> AccountService:
    app = get_root_app(request)

    jwt_secret = get_jwt_secret(app)
    users_repository = get_user_repository(app)
    passwords_repository = get_password_repository(app)
    ethereum_repository = get_eth(app)
    return AccountService(
        jwt_secret,
        users_repository,
        passwords_repository,
        ethereum_repository,
    )
