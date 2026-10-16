from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_SECRET_KEY,
)

ALGORITHM = "HS256"


def create_access_token(
    username: str,
    role: str,
) -> str:
    """Create a signed JWT access token."""
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not configured.")

    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "role": role,
        "iat": now,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_access_token(token: str) -> dict:
    """Verify a JWT signature and its expiration."""
    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is not configured.")

    return jwt.decode(
        token,
        JWT_SECRET_KEY,
        algorithms=[ALGORITHM],
        options={"require": ["sub", "exp"]},
    )