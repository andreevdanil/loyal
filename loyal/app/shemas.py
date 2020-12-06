from typing import Dict

import attr
from marshmallow import EXCLUDE, Schema, fields, post_load

__all__ = (
    "RegisterCredentials",
    "RegisterRequestSchema",
    "RegisterResponseSchema",
    "LoginCredentials",
    "LoginRequestSchema",
    "LoginResponseSchema",
    "UserResponseSchema",
)


@attr.s(auto_attribs=True, frozen=True, slots=True)
class RegisterCredentials:
    first_name: str
    last_name: str
    email: str
    eth_address: str
    password: str


class RegisterRequestSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    eth_address = fields.Str(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_credentials(self, data: Dict, **kwargs) -> RegisterCredentials:
        return RegisterCredentials(**data)


class RegisterResponseSchema(Schema):
    id = fields.UUID(required=True)

    class Meta:
        unknown = EXCLUDE


@attr.s(auto_attribs=True, frozen=True, slots=True)
class LoginCredentials:
    email: str
    password: str


class LoginRequestSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

    @post_load
    def make_credentials(self, data: Dict, **kwargs) -> LoginCredentials:
        return LoginCredentials(**data)


class LoginResponseSchema(Schema):
    id = fields.UUID(required=True)
    access_token = fields.Str(required=True)

    class Meta:
        unknown = EXCLUDE


class UserResponseSchema(Schema):
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Email(required=True)
    balance = fields.Float(required=True)
