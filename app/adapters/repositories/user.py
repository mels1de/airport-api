from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from app.adapters.db.models import User as DBUser

class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email:str):
        ...
    @abstractmethod
    async def get_by_id(self, user_id:UUID):
        ...
    @abstractmethod
    async def create_raw(self, data:dict):
        ...

class SQLAlchemyUserRepository(UserRepository):

    def __init__(self, session:AsyncSession):
        self.session = session

    async def get_by_email(self, email:str):
        res = await self.session.execute(select(DBUser).where(DBUser.email == email))
        obj = res.scalar_one_or_none()
        return obj.to_public_dict() if obj else None

    async def get_by_id(self, user_id:UUID):
        obj = await self.session.get(DBUser, user_id)
        return obj.to_public_dict() if obj else None

    async def create_raw(self, data:dict):
        obj = DBUser(**data)
        self.session.add(obj)
        try:
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()

            raise ValueError("Email or username already registered")
        await self.session.refresh(obj)
        return obj.to_public_dict()