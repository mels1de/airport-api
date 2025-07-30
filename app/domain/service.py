from typing import List
from uuid import UUID
from app.domain.models import Airport,AirportCreate
from app.adapters.repositories.airport import AirportRepository

class AirportService:

    def __init__(self,repo: AirportRepository):
        self._repo = repo

    async def list_airports(self,limit: int = 100, offset:int = 0):
        records = await self._repo.list(limit=limit,offset=offset)
        return [Airport(**r) for r in records]

    async def get_airport(self, airport_id:UUID):
        data = await self._repo.get(airport_id)
        if data is None:
            raise ValueError(f"Airport {airport_id} not found")
        return Airport(**data)

    async def create_airport(self, payload: AirportCreate):
        created = await self._repo.create(payload.dict())
        return Airport(**created)

    async def update_airport(self,airport_id: UUID,payload: dict):
        updated = await self._repo.update(airport_id, payload)
        if updated is None:
            raise ValueError(f"Airport {airport_id} not found")
        return Airport(**updated)

    async def delete_airport(self,airport_id: UUID):
        success = await self._repo.delete(airport_id)
        if not success:
            raise ValueError(f"Airport {airport_id} not found")

