from fastapi import Depends
from app.adapters.db.session import get_db
from app.adapters.repositories.airport import SQLAlchemyAirportRepository
from app.domain.service import AirportService

async def get_airport_service(db = Depends(get_db)):
    repo = SQLAlchemyAirportRepository(db)
    return AirportService(repo)
