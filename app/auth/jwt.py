from time import time
import uuid
import jwt
from app.config.config import settings
from typing import Optional, Dict, Any

def _create_token(sub: str, ttl: int, typ:str):
    now = int(time())
    payload: Dict[str, Any] = {
        "jti": str(uuid.uuid4()),
        "sub": sub,
        "typ": typ,
        "iat": now,
        "exp": now + ttl
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)

def create_access_token(user_id: str):
    return _create_token(user_id,settings.jwt_access_expires,"access")

def create_refresh_token(user_id: str) -> str:
    return _create_token(user_id, settings.jwt_refresh_expires, "refresh")

def decode_token(token: str) -> Dict[str, Any]:
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
