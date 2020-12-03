from uuid import UUID

import attr
from loyal.app import RegisterCredentials, LoginCredentials
from . import utils
from .entities import LoginResponse
from .exceptions import UserNotFoundError, IncorrectPasswordError
from .repositories import (
    UserRepositoryInterface,
    PasswordRepositoryInterface,
)

__all__ = ("AccountService",)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class AccountService:
    jwt_secret: str
    user: UserRepositoryInterface
    password: PasswordRepositoryInterface

    async def register(self, credentials: RegisterCredentials) -> UUID:
        account = await self.user.find_by_email(credentials.email)
        if account:
            return account.id

        password_id = utils.generate_uuid()
        salt, hashed_password = utils.secure_password(credentials.password)
        created_at = utils.get_local_time()
        password_id = await self.password.add(
            password_id,
            salt,
            hashed_password,
            created_at,
        )

        user_id = utils.generate_uuid()
        created_at = utils.get_local_time()
        await self.user.add(
            user_id,
            credentials.first_name,
            credentials.last_name,
            password_id,
            credentials.email,
            created_at,
        )
        return user_id

    async def login(self, credentials: LoginCredentials) -> LoginResponse:
        account = await self.user.find_by_email(credentials.email)
        if not account:
            raise UserNotFoundError

        salt, hashed_password = await self.password.find(account.password_id)

        if not utils.is_password_valid(
            credentials.password,
            salt,
            hashed_password,
        ):
            raise IncorrectPasswordError

        jwt_payload = {
            "user_id": account.id,
        }
        jwt = utils.generate_jwt(jwt_payload, self.jwt_secret)

        return LoginResponse(account.id, jwt)

    async def get_balance(self, user_id: UUID) -> int:
        account = await self.user.find_by_id(user_id)
        if not account:
            raise UserNotFoundError

        return account.balance
