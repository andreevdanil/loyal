from uuid import UUID

import attr
from loyal.app import RegisterCredentials, LoginCredentials
from .entities import Balance, LoginResponse, UserID
from .repositories import (
    UserRepositoryInterface,
    PasswordRepositoryInterface,
)

__all__ = ("AccountService",)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class AccountService:
    user: UserRepositoryInterface
    password: PasswordRepositoryInterface

    async def register(self, credentials: RegisterCredentials) -> UserID:
        pass

    async def login(self, credentials: LoginCredentials) -> LoginResponse:
        pass

    async def get_balance(self, user_id: UUID) -> Balance:
        pass
