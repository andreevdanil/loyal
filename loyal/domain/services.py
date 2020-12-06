from typing import Optional
from uuid import UUID

import attr

from loyal.app.shemas import LoginCredentials, RegisterCredentials

from . import utils
from .entities import Account, LoginResponse
from .exceptions import UserLoginError, UserNotFoundError
from .repositories import PasswordRepositoryInterface, UserRepositoryInterface
from loyal.infrastructure import EthereumService

__all__ = ("AccountService",)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class AccountService:
    jwt_secret: str
    user: UserRepositoryInterface
    password: PasswordRepositoryInterface
    ethereum: EthereumService

    async def register(
        self,
        credentials: RegisterCredentials,
    ) -> Optional[UUID]:
        account = await self.user.find_by_email(credentials.email)
        if account:
            return None

        password_id = utils.generate_uuid()
        salt, hashed_password = utils.secure_password(credentials.password)
        created_at = utils.get_local_time()
        await self.password.add(
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
            credentials.email,
            credentials.eth_address,
            password_id,
            created_at,
        )
        return user_id

    async def login(self, credentials: LoginCredentials) -> LoginResponse:
        account = await self.user.find_by_email(credentials.email)
        if not account:
            raise UserLoginError

        hashed_password = await self.password.find(account.password_id)

        if not utils.is_password_valid(credentials.password, hashed_password):
            raise UserLoginError

        payload = {
            "user_id": str(account.id),
        }
        jwt = utils.generate_jwt(payload, self.jwt_secret)

        return LoginResponse(account.id, jwt)

    async def get_user_info(self, user_id: UUID) -> Account:
        account = await self.user.find_by_id(user_id)
        if not account:
            raise UserNotFoundError

        account.balance = self.ethereum.get_balance(account.eth_address)

        return account
