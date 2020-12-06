from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from uuid import UUID

from .entities import Account, Password

__all__ = (
    "UserRepositoryInterface",
    "PasswordRepositoryInterface",
)


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def add(
        self,
        uid: UUID,
        first_name: str,
        last_name: str,
        email: str,
        eth_address: str,
        password_id: UUID,
        created_at: datetime,
    ) -> None:
        pass

    @abstractmethod
    async def find_by_id(self, uid: UUID) -> Optional[Account]:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Account]:
        pass


class PasswordRepositoryInterface(ABC):

    @abstractmethod
    async def add(
        self,
        pid: UUID,
        salt: bytes,
        password: bytes,
        created_at: datetime,
    ):
        pass

    @abstractmethod
    async def find(self, password_id: UUID) -> Password:
        pass
