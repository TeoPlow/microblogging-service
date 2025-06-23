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
    engine, expire_on_commit=False, class_=AsyncSession
)

session = async_session()
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
