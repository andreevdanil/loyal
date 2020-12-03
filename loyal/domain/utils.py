import hashlib
import os
import uuid
from datetime import datetime
from typing import Tuple, Dict
import jwt
from loyal.domain import Password

__all__ = (
    "generate_uuid",
    "get_local_time",
    "hash_password",
    "secure_password",
    "is_password_valid",
)


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def get_local_time() -> datetime:
    return datetime.now()


def hash_password(salt: bytes, password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000,
    )


def secure_password(password: str) -> Tuple[bytes, bytes]:
    salt = os.urandom(32)
    return salt, hash_password(salt, password)


def is_password_valid(
    password: str,
    hashed_password: Password,
) -> bool:
    return hash_password(
        hashed_password.salt,
        password,
    ) == hashed_password.password


def generate_jwt(payload: Dict, secret: str) -> str:
    return jwt.encode(payload, secret, algorithm="HS256")
