from abc import ABC,abstractmethod
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update as sa_update,delete as sa_delete
from app.adapters.db.models import Airport as DBAirport

class AirportRepository(ABC):
    @abstractmethod
    async def list(self,limit: int, offset: int) -> List[dict]:
        ...

    @abstractmethod
    async def get(self, airport_id: UUID) -> Optional[dict]:
        ...

    @abstractmethod
    async def create(self, data: dict) -> dict:
        ...

    @abstractmethod
    async def update(self, airport_id: UUID, data: dict) -> Optional[dict]:
        ...

    @abstractmethod
    async def delete(self, airport_id: UUID) -> bool:
        ...

class SQLAlchemyAirportRepository(AirportRepository):
    def __init__(self,session: AsyncSession):
        self.session = session

    async def list(self,limit: int = 100, offset: int = 0) -> List[dict]:
        result = await self.session.execute(
            select(DBAirport).limit(limit).offset(offset)
        )
        rows = result.scalars().all()
        return [row.to_dict() for row in rows]

    async def get(self, airport_id: UUID) -> Optional[dict]:
        obj = await self.session.get(DBAirport, airport_id)
        return obj.to_dict() if obj else None

    async def create(self, data: dict) -> dict:
        obj = DBAirport(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj.to_dict()

    async def update(self, airport_id: UUID, data: dict) -> Optional[dict]:
        await self.session.execute(
            sa_update(DBAirport)
            .where(DBAirport.id == airport_id)
            .values(**data)
            .execution_options(synchronize_session="fetch")
        )
        await self.session.commit()
        return await self.get(airport_id)

    async def delete(self, airport_id: UUID) -> bool:
        result = await self.session.execute(
            sa_delete(DBAirport).where(DBAirport.id == airport_id)
        )
        await self.session.commit()
        return result.rowcount > 0