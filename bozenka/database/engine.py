import os

from sqlalchemy import URL, create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker


def get_async_engine(url: URL | str) -> AsyncEngine:
    """
    Creates AsyncEngine, it needs to create async
    session maker by get_sessions_maker()
    :param url:
    :return:
    """
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


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
