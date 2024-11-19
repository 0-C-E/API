import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import jsonify, request

SECRET_KEY = os.getenv("SECRET_JWT_KEY", "SuperSecretKey")
ACCESS_TOKEN_EXPIRY = timedelta(hours=1)
REFRESH_TOKEN_EXPIRY = timedelta(days=30)


def generate_access_token(player_id: int) -> str:
    """Generate a JWT token for a user."""
    payload = {
        "player_id": player_id,
        "exp": datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRY,  # Expiration
        "iat": datetime.now(timezone.utc),  # Issued at
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def generate_refresh_token(player_id: int) -> str:
    """Generate a long-lived refresh token."""
    payload = {
        "player_id": player_id,
        "exp": datetime.now(timezone.utc) + REFRESH_TOKEN_EXPIRY,
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> dict | None:
    """Verify a JWT token and return the payload."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify(message="Token is missing"), 401

        decoded = verify_token(token)
        if not decoded:
            return jsonify(message="Token is invalid or expired"), 401

        request.player_id = decoded["player_id"]  # Attach user ID to the request
        return f(*args, **kwargs)

    return decorated
