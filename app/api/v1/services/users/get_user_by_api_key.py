from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database import redis_client
from app.api.v1.models import User
from app.api.exceptions import SomeError, ApiException, InvalidApiKey
from sqlalchemy import select

from app.api.utils.logger import get_logger

log = get_logger("UsersLogger")


async def get_user_by_api_key(
    session: AsyncSession, api_key: str
) -> User | None:
    """
    Ассинхронная функция получения пользователя по его api_key.
    """
    log.debug(f"Получение пользователя по API ключу: {api_key}")
    try:
        user_id = int(await redis_client.get(api_key))
        result = await session.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            error_message = f"Пользователь по API ключу '{api_key}' не найден"
            log.error(error_message)
            raise InvalidApiKey(error_message)
        log.debug(f"Пользователь по API ключу '{api_key}' найден")
        return user

    except ApiException as e:
        raise e
    except Exception as e:
        error_message = f"Ошибка при получении пользователя по API ключу: {e}"
        log.error(error_message)
        raise SomeError(error_message)
