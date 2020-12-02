from abc import ABC, abstractmethod
from .entities import UserID

__all__ = (
    "UserRepositoryInterface",
    "PasswordRepositoryInterface",
)


class UserRepositoryInterface(ABC):

    @abstractmethod
    async def add(self) -> UserID:
        pass

    @abstractmethod
    async def get(self) -> UserID:
        pass


class PasswordRepositoryInterface(ABC):

    @abstractmethod
    async def add(self) -> PasswordID:
        pass

    @abstractmethod
    async def update(self) -> None:
        pass
