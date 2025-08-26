from fastapi import Depends
from app.adapters.db.session import get_db
from app.adapters.repositories.airport import SQLAlchemyAirportRepository
from app.adapters.repositories.user import SQLAlchemyUserRepository
from app.domain.service import AirportService
from app.domain.service_auth import AuthService


async def get_airport_service(db = Depends(get_db)):
    repo = SQLAlchemyAirportRepository(db)
    return AirportService(repo)

async def get_auth_service(db = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    return AuthService(repo)