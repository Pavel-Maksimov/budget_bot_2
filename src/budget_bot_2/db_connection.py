from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from settings import settings

engine = create_async_engine(settings.get_database_url(), echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False)
