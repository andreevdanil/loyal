from uuid import UUID

import attr

__all__ = (
    "UserID",
    "LoginResponse",
    "Balance",
)


@attr.s(auto_attribs=True, slots=True, frozen=True)
class UserID:
    id: UUID


@attr.s(auto_attribs=True, slots=True, frozen=True)
class LoginResponse:
    id: UserID
    token: str


@attr.s(auto_attribs=True, slots=True, frozen=True)
class Balance:
    value: int
