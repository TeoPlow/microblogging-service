from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.api.v1.models import User, Follower
from app.api.exceptions import SomeError, ApiException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def get_user_details(session: AsyncSession, user: User) -> User:
    """
    Ассинхронная функция получения полной информации о пользователе
    с подгруженными followers и following.
    """
    log.debug(f"Получение полной информации о пользователе: {user.name}")
    try:
        result = await session.execute(
            select(User)
            .options(
                selectinload(User.followers).selectinload(Follower.follower),
                selectinload(User.following).selectinload(Follower.user),
            )
            .where(User.id == user.id)
        )
        user_with_details = result.scalar_one()
        return user_with_details

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Ошибка при получении информации о пользователе: {e}"
        log.error(error_message)
        raise SomeError(error_message)
