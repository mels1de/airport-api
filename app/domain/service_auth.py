from passlib.context import CryptContext
from app.adapters.repositories.user import UserRepository
from app.domain.auth import UserCreate

pwd = CryptContext(schemes=["bcrypt"],deprecated="auto")

class AuthService:
    def __init__(self,users:UserRepository):
        self.users = users

    def _hash(self, raw:str):
        return pwd.hash(raw)

    async def register(self, data: UserCreate):
        exists = await self.users.get_by_id(data.email)
        if exists:
            raise ValueError("User already registered")

        payload = {
            "email": data.email,
            "username": data.username,
            "hashed_password": self._hash(data.password),
            "role": "user",
        }
        user = await self.users.create_raw(payload)
        return user