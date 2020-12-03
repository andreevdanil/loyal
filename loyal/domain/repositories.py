from abc import ABC, abstractmethod

__all__ = (
    "UserRepositoryInterface",
    "PasswordRepositoryInterface",
)

from datetime import datetime
from typing import Tuple

from uuid import UUID

from .entities import Account


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def find_by_id(self, uid: UUID) -> Account:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Account:
        pass

    @abstractmethod
    async def add(
        self,
        uid: UUID,
        first_name: str,
        last_name: str,
        password_id: UUID,
        email: str,
        created_at: datetime,
    ) -> Account:
        pass


class PasswordRepositoryInterface(ABC):

    @abstractmethod
    async def add(self, salt: bytes, password: bytes) -> UUID:
        pass

    @abstractmethod
    async def get(self, password_id: UUID) -> Tuple[bytes, bytes]:
        pass
