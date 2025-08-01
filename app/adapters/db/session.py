from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config.config import settings

engine = create_async_engine(settings.db_dsn, echo=settings.debug)
AsyncSessionLocal = sessionmaker(engine,class_ = AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session