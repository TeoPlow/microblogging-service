from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    AsyncEngine
)
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Config
from typing import AsyncGenerator


engine: AsyncEngine = create_async_engine(
    Config.SQLALCHEMY_DATABASE_URL,
    echo=True
)

async_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор для получения сессии базы данных.
    """
    async with async_session() as session:
        yield session
