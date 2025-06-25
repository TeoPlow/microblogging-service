from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.v1.models import Follower, User
from app.api.v1.services.users.get_user_by_id import get_user_by_id
from app.api.exceptions import (
    SomeError,
    ApiException,
    NotFoundError,
    ConflictError,
)

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def remove_follow_from_user(
    user_id: int,
    user: User,
    session: AsyncSession,
    redis_client: Redis
):
    """
    Ассинхронная функция для удаления подписки пользователя.
    """
    try:
        if user.id == user_id:
            raise ConflictError("Нельзя отписаться от самого себя")

        try:
            await get_user_by_id(session, user_id)
        except NotFoundError:
            raise NotFoundError(
                "Пользователь, от которого вы хотите отписаться, не найден"
            )

        result = await session.execute(
            select(Follower).where(
                Follower.user_id == user_id,
                Follower.follower_id == user.id,
            )
        )
        existing = result.scalar_one_or_none()
        if not existing:
            raise NotFoundError("Вы не подписаны на этого пользователя")

        await session.delete(existing)
        await session.commit()

        # Очистка кеша в Redis
        log.debug(f"Очистка кеша для пользователей {user.id} и {user_id}")
        await redis_client.delete(f"user_details:{user.id}")
        await redis_client.delete(f"user_details:{user_id}")

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось отписаться от пользователя: {e}"
        log.error(error_message)
        raise SomeError(error_message)
