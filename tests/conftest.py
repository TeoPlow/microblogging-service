import sys
import os
import pytest_asyncio
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Заставляю pytest увидеть app.main
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
print(f"Корень проекта: {project_root}")
if project_root not in sys.path:
    print("Добавляем корень проекта в sys.path")
    sys.path.insert(0, project_root)
else:
    print("Корень проекта уже в sys.path")

print("Успешно импортирован app.main")

from app.api.database.redis import get_redis_client  # noqa: E402
from app.api.v1.models import User  # noqa: E402
from app.main import app  # noqa: E402

images_dir = "tests/images"


# Основная фикстура асинхронного клиента
@pytest_asyncio.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


# Фикстура для создания тестового engine
@pytest_asyncio.fixture
async def test_db_engine():
    from app.config import Config

    engine = create_async_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)
    yield engine
    await engine.dispose()


# Фикстура для создания отдельной сессии для каждого теста
@pytest_asyncio.fixture
async def test_db_session(test_db_engine):
    async with test_db_engine.connect() as conn:
        transaction = await conn.begin()
        async_session = sessionmaker(
            bind=conn, expire_on_commit=False, class_=AsyncSession
        )
        async with async_session() as session:
            # Создаём тестовых пользователей
            users = await session.execute(
                select(User).where(
                    User.name.in_(["testuser1", "testuser2", "testuser3"])
                )
            )
            users = users.scalars().all()
            if len(users) < 3:
                user1 = User(name="testuser1")
                user2 = User(name="testuser2")
                user3 = User(name="testuser3")
                session.add_all([user1, user2, user3])
                await session.commit()
                users = [user1, user2, user3]

            # Устанавливаем значения в Redis
            redis = await get_redis_client()
            name_to_key = {
                "testuser1": "test1",
                "testuser2": "test2",
                "testuser3": "test3",
            }
            for user in users:
                key = name_to_key.get(user.name)
                if key:
                    await redis.set(key, str(user.id))

            yield session
        await transaction.rollback()


# Фикстура для подмены get_db на тестовую сессию в каждом тесте
@pytest_asyncio.fixture(autouse=True)
async def override_db_dependency(test_db_session):
    from app.api.database.db import get_db

    # Тестовая зависимость, возвращающая тестовую сессию
    async def _get_test_db():
        async with test_db_session as session:
            yield session

    app.dependency_overrides[get_db] = _get_test_db
    yield
    app.dependency_overrides.pop(get_db, None)
