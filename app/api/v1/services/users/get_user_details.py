from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.api.v1.models import User, Follower
from app.api.v1.schemas import UserOutput
from app.api.exceptions import SomeError, ApiException
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")

redis_cache_time = 60 * 30


async def get_user_details(
    session: AsyncSession,
    user: User,
    redis_client: Redis
) -> User:
    """
    Ассинхронная функция получения полной информации о пользователе
    с подгруженными followers и following, с кешированием через Redis.
    """
    cache_key = f"user_details:{user.id}"
    cached = await redis_client.get(cache_key)
    if cached:
        log.debug(f"Пользователь с ID: {user.id} загружен из кеша")
        return UserOutput.model_validate_json(cached)

    log.debug(f"Получение полной информации о пользователе: {user.name}")
    try:
        result = await session.execute(
            select(User)
            .options(
                selectinload(User.followers_rel)
                .selectinload(Follower.follower),
                selectinload(User.following_rel)
                .selectinload(Follower.user),
            )
            .where(User.id == user.id)
        )
        user_with_details = result.scalar_one()

        user_output = UserOutput(
            id=user_with_details.id,
            name=user_with_details.name,
            followers=[
                {"id": u.id, "name": u.name}
                for u in user_with_details.followers
            ],
            following=[
                {"id": u.id, "name": u.name}
                for u in user_with_details.following
            ],
        )
        await redis_client.set(
            cache_key,
            user_output.model_dump_json(),
            ex=redis_cache_time
        )
        return user_output

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Ошибка при получении информации о пользователе: {e}"
        log.error(error_message)
        raise SomeError(error_message)
