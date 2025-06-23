from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Follower
from app.api.v1.services.users import get_user_by_api_key, get_user_by_id
from app.api.exceptions import (
    SomeError,
    NotFoundError,
    ConflictError,
    ApiException,
)

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def add_follow_to_user(
    user_id: int, session: AsyncSession, api_key: str
):
    """
    Ассинхронная функция для добавления подписки на пользователя.
    """
    try:
        current_user = await get_user_by_api_key(session, api_key)

        if current_user.id == user_id:
            log.warning("Попытка подписаться на самого себя")
            raise ConflictError("Нельзя подписаться на самого себя")

        try:
            await get_user_by_id(session, user_id)
        except NotFoundError:
            raise NotFoundError(
                "Пользователь, на которого вы хотите подписаться, не найден"
            )

        log.debug("Проверка существующей подписки")
        result = await session.execute(
            select(Follower).where(
                Follower.user_id == user_id,
                Follower.follower_id == current_user.id,
            )
        )
        existing = result.scalar_one_or_none()
        if existing:
            log.warning("Попытка повторной подписки")
            raise ConflictError("Вы уже подписаны на этого пользователя")

        log.debug("Создание новой подписки")
        follow = Follower(user_id=user_id, follower_id=current_user.id)
        session.add(follow)
        await session.commit()

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось подписаться на пользователя: {e}"
        log.error(error_message)
        raise SomeError(error_message)
