import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

# Подключаем проект в PYTHONPATH
sys.path.append(os.getcwd())

# Подгружаем .env и Settings
from dotenv import load_dotenv
load_dotenv(".env")
from app.config.config import settings

# Импортируем Base.metadata
from app.adapters.db.models import Base

# Конфиг Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata для autogenerate
target_metadata = Base.metadata

# URL из настроек
ASYNC_DATABASE_URL = settings.db_dsn

# Создаём асинхронный движок
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    poolclass=pool.NullPool,
    echo=settings.debug,
)

def run_migrations_offline() -> None:
    """Генерация SQL миграций без подключения к БД."""
    context.configure(
        url=ASYNC_DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    """Выполнение миграций в синхронном API на заданном connection."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,  # чтобы autogenerate видел изменения типов
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    """Подключаемся асинхронно и внутри запускаем синхронный блок."""
    async with async_engine.connect() as connection:
        await connection.run_sync(do_run_migrations)

def run_migrations_online() -> None:
    """Запуск миграций через асинхронный engine."""
    import asyncio
    asyncio.run(run_async_migrations())

# Выбор режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
