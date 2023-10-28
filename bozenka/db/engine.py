import os

from sqlalchemy import URL, create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


def get_async_engine(url: URL | str) -> AsyncEngine:
    """
    Creates AsyncEngine
    :param url:
    :return:
    """
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


@DeprecationWarning
async def schemas(engine: AsyncEngine, metadata) -> None:
    """
    Commiting all changes & create databases
    :param engine:
    :param metadata:
    :return:
    """
    """
    async with engine.begin() as connect:
        await connect.run_sync(metadata.create_all)
    """


def get_sessions_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    Creates SessionMaker (Async!)
    :param engine:
    :return:
    """
    return async_sessionmaker(engine, class_=AsyncSession)


def generate_url() -> URL:
    """
    Generates URL for postgresql database
    :return:
    """
    return URL.create(
        "postgresql+asyncpg",
        username=os.getenv("db_username"),
        host=os.getenv("db_host"),
        password=os.getenv("db_password"),
        database=os.getenv("db_name"),
        port=os.getenv("db_port")
    )
