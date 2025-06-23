from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Follower
from app.api.v1.services.users import get_user_by_api_key, get_user_by_id
from app.api.exceptions import (
    SomeError,
    ApiException,
    NotFoundError,
    ConflictError,
)

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def remove_follow_from_user(
    user_id: int, session: AsyncSession, api_key: str
):
    """
    Ассинхронная функция для удаления подписки пользователя.
    """
    try:
        current_user = await get_user_by_api_key(session, api_key)

        if current_user.id == user_id:
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
                Follower.follower_id == current_user.id,
            )
        )
        existing = result.scalar_one_or_none()
        if not existing:
            raise NotFoundError("Вы не подписаны на этого пользователя")

        await session.delete(existing)
        await session.commit()

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось отписаться от пользователя: {e}"
        log.error(error_message)
        raise SomeError(error_message)
