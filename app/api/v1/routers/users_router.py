from fastapi import APIRouter, Header, Path, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database import get_db, get_redis_client
from redis.asyncio import Redis
from app.api.v1.schemas import (
    UserGetMeResponse,
    BaseResponse,
    error_responses
)
from app.api.v1.models import User
from app.api.exceptions import InvalidApiKey, NotFoundError
from app.api.v1.services.users import (
    get_user_by_api_key,
    get_user_by_id,
    get_user_details,
    add_follow_to_user,
    remove_follow_from_user,
)

from app.api.utils.logger import get_logger

log = get_logger("UserRouterLogger")

router = APIRouter()


@router.get(
    "/me",
    response_model=UserGetMeResponse,
    responses=error_responses
)
async def get_current_user(
    api_key: str = Header(None, alias="api-key"),
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_client),
) -> UserGetMeResponse:
    """
    Эндпоинт для получения информации о текущем пользователе по API ключу.
    Возвращает словарь с результатом операции и данными о пользователе.
    """
    log.debug(
        "Обработка запроса на получение информации о текущем пользователе"
    )

    user: User = await get_user_by_api_key(session, redis_client, api_key)
    if not user:
        raise InvalidApiKey(f"Пользователь по API ключу '{api_key}' не найден")

    full_user: User = await get_user_details(session, user)

    return UserGetMeResponse(user=full_user)


@router.get(
    "/{user_id}",
    response_model=UserGetMeResponse,
    responses=error_responses
)
async def get_one_user_by_id(
    user_id: int = Path(...),
    session: AsyncSession = Depends(get_db),
) -> UserGetMeResponse:
    """
    Эндпоинт для получения информации о пользователе по его ID.
    Принимает ID пользователя.
    Возвращает словарь с результатом операции и данными о пользователе.
    """
    log.debug(
        "Обработка запроса на получение информации о пользователе"
    )
    user: User = await get_user_by_id(session, user_id)
    if not user:
        raise NotFoundError(f"Пользователь с ID: {user_id} не найден")

    full_user: User = await get_user_details(session, user)

    return UserGetMeResponse(user=full_user)


@router.post(
    "/{user_id}/follow",
    response_model=BaseResponse,
    responses=error_responses
)
async def post_follow(
    user_id: int,
    api_key: str = Header(None, alias="api-key"),
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_client),
) -> BaseResponse:
    """
    Эндпоинт для добавления подписки на пользователя по его ID.
    Принимает ID пользователя и добавляет подписку к нему в базе данных.
    Возвращает словарь с результатом операции.
    """
    log.debug(
        "Обработка запроса на добавление подписки на пользователя"
    )
    user = await get_user_by_api_key(session, redis_client, api_key)

    await add_follow_to_user(user_id, session, user)

    return BaseResponse()


@router.delete(
    "/{user_id}/follow",
    response_model=BaseResponse,
    responses=error_responses
)
async def delete_follow(
    user_id: int,
    api_key: str = Header(None, alias="api-key"),
    session: AsyncSession = Depends(get_db),
    redis_client: Redis = Depends(get_redis_client),
) -> BaseResponse:
    """
    Эндпоинт для удаления подписки на пользователя по его ID.
    Принимает ID пользователя и удаляет подписку к нему из базы данных.
    Возвращает словарь с результатом операции.
    """
    log.debug(
        "Обработка запроса на удаление подписки на пользователя"
    )
    user = await get_user_by_api_key(session, redis_client, api_key)

    await remove_follow_from_user(user_id, session, user)

    return BaseResponse()
