from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import User
from sqlalchemy.future import select
from app.api.exceptions import SomeError, ApiException, NotFoundError

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def get_user_by_id(session: AsyncSession, user_id: str) -> User:
    """
    Ассинхронная функция получения пользователя по его user_id
    """
    try:
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            error_message = f"Пользователь с id={user_id} не найден"
            log.error(error_message)
            raise NotFoundError(error_message)
        log.debug(f"Пользователь с id={user_id} найден")
        return user

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Ошибка при получении пользователя по id: {e}"
        log.error(error_message)
        raise SomeError(error_message)
