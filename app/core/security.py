import base64
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from app.core.config import settings


ITERATIONS = 600_000


def hash_password(value: str) -> str:
    salt = secrets.token_bytes(16)

    key = hashlib.pbkdf2_hmac(
        "sha256",
        value.encode("utf-8"),
        salt,
        ITERATIONS,
    )

    return (
        f"pbkdf2_sha256${ITERATIONS}$"
        f"{base64.b64encode(salt).decode()}$"
        f"{base64.b64encode(key).decode()}"
    )


def verify_password(value: str, hashed: str) -> bool:
    try:
        algorithm, iterations, salt_b64, key_b64 = hashed.split("$")

        if algorithm != "pbkdf2_sha256":
            return False

        salt = base64.b64decode(salt_b64)
        original_key = base64.b64decode(key_b64)

        key = hashlib.pbkdf2_hmac(
            "sha256",
            value.encode("utf-8"),
            salt,
            int(iterations),
        )

        return hmac.compare_digest(key, original_key)

    except (ValueError, TypeError):
        return False


def create_token(subject: str) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(hours=12)

    return jwt.encode(
        {"sub": subject, "exp": expiry},
        settings.secret_key,
        algorithm="HS256",
    )


def read_token(token: str) -> str:
    try:
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )["sub"]

    except (JWTError, KeyError) as exc:
        raise ValueError("Invalid or expired token") from exc


def new_api_key() -> str:
    return "aura_" + secrets.token_urlsafe(32)


def fingerprint(value: str) -> str:
    return hashlib.sha256(
        value.encode()
    ).hexdigest()