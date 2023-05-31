from asyncio import current_task

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from settings import settings

sync_engine = create_engine(settings.get_sync_test_database_url(), echo=False)

async_engine = create_async_engine(settings.get_test_database_url(), echo=False)
TestSession = async_scoped_session(
    async_sessionmaker(async_engine, expire_on_commit=False, autoflush=False),
    current_task,
)
