from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError

from app.core.config import get_settings

hasher = PasswordHasher()


def hash_password(password: str) -> str:
    return hasher.hash(password)


def verify_password(password: str, encoded: str) -> bool:
    try:
        return hasher.verify(encoded, password)
    except VerificationError:
        return False


def issue_token(user_id: int, version: int) -> str:
    settings = get_settings()
    now = datetime.now(UTC)
    return jwt.encode(
        {
            "sub": str(user_id),
            "ver": version,
            "jti": str(uuid4()),
            "iat": now,
            "exp": now + timedelta(minutes=settings.jwt_ttl_minutes),
            "iss": "ciclolima",
        },
        settings.jwt_secret.get_secret_value(),
        algorithm="HS256",
    )


def decode_token(token: str) -> dict:
    return jwt.decode(
        token,
        get_settings().jwt_secret.get_secret_value(),
        algorithms=["HS256"],
        issuer="ciclolima",
        options={"require": ["sub", "exp", "iat", "iss", "ver", "jti"]},
    )
