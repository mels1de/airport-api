from passlib.context import CryptContext
from app.adapters.repositories.user import UserRepository
from app.domain.auth import UserCreate
from app.auth.pjwt import decode_token, create_access_token, create_refresh_token
# from jwt import InvalidTokenError
import logging

logger = logging.getLogger(__name__)

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, users: UserRepository):
        self.users = users

    def _hash(self, raw: str) -> str:
        return pwd.hash(raw)

    def _verify(self, raw: str, hashed: str) -> bool:
        return pwd.verify(raw, hashed)

    async def register(self, data: UserCreate) -> dict:
        email = str(data.email).lower().strip()
        if await self.users.get_by_email(email):
            raise ValueError("Email already registered")

        payload = {
            "email": email,
            "username": data.username,
            "hashed_password": self._hash(data.password),
            "role": "user",
        }
        return await self.users.create_raw(payload)

    async def login(self, email: str, password: str) -> dict:
        email = email.lower().strip()
        logger.debug("LOGIN email=%s", email)

        db_user = await self.users.get_db_user_by_email(email)
        logger.debug("LOGIN user_found=%s", bool(db_user))
        if not db_user:
            raise ValueError("Invalid credentials")

        hashed = getattr(db_user, "hashed_password", None)
        if hashed is None and isinstance(db_user, dict):
            hashed = db_user.get("hashed_password")

        logger.debug("LOGIN hashed_present=%s prefix=%s", bool(hashed), (hashed[:4] if hashed else None))
        if not hashed:
            raise ValueError("Invalid credentials")

        ok = self._verify(password, hashed)
        logger.debug("LOGIN verify=%s", ok)
        if not ok:
            raise ValueError("Invalid credentials")

        uid = str(db_user.id)

        return {
            "access_token": create_access_token(uid),
            "refresh_token": create_refresh_token(uid),
            "token_type": "bearer",
        }