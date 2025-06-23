from fastapi import APIRouter, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.database import get_db
from app.api.v1.schemas import (
    TweetSendRequest,
    TweetListResponse,
    TweetSendResponse,
    BaseResponse,
    error_responses
)

from app.api.v1.services.tweets import (
    send_tweet,
    get_tweets_from_follow,
    delete_tweet_by_id,
    add_like_to_tweet,
    remove_like_from_tweet,
)

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")

router = APIRouter()


@router.post(
    "",
    response_model=TweetSendResponse,
    responses=error_responses
)
async def post_tweet(
    data: TweetSendRequest,
    api_key: str = Header(None, alias="api-key"),
    session: AsyncSession = Depends(get_db),
) -> TweetSendResponse:
    """
    Эндпоинт для отправки нового твита.
    Принимает данные твита и сохраняет его в базе данных.
    Возвращает словарь с результатом операции и ID сохраненного твита.
    """
    log.debug(f"Обработка запроса на отправку твита - {data}")

    tweet_id = await send_tweet(data, api_key, session)

    return TweetSendResponse(tweet_id=tweet_id)


@router.get(
    "",
    response_model=TweetListResponse,
    responses=error_responses
)
async def get_tweets(
    session: AsyncSession = Depends(get_db),
    api_key: str = Header(None, alias="api-key"),
) -> TweetListResponse:
    """
    Эндпоинт для получения списка твитов по подпискам.
    Возвращает словарь с результатом операции и списком твитов.
    """
    log.debug("Обработка запроса на получение списка твитов по подпискам")

    tweet_list = await get_tweets_from_follow(session, api_key)

    return TweetListResponse(tweets=tweet_list)


@router.delete(
    "/{tweet_id}",
    response_model=BaseResponse,
    responses=error_responses
)
async def delete_tweet(
    tweet_id: int,
    session: AsyncSession = Depends(get_db),
    api_key: str = Header(None, alias="api-key"),
) -> BaseResponse:
    """
    Эндпоинт для удаления твита по его ID.
    Принимает ID твита и удаляет его из базы данных.
    Возвращает словарь с результатом операции.
    """
    log.debug(f"Обработка запроса на удаление твита - {tweet_id}")

    await delete_tweet_by_id(tweet_id, session, api_key)
    return BaseResponse()


@router.post(
    "/{tweet_id}/likes",
    response_model=BaseResponse,
    responses=error_responses
)
async def post_like(
    tweet_id: int,
    session: AsyncSession = Depends(get_db),
    api_key: str = Header(None, alias="api-key"),
) -> BaseResponse:
    """
    Эндпоинт для добавления лайка к твиту по его ID.
    Принимает ID твита и добавляет лайк к нему в базе данных.
    Возвращает словарь с результатом операции.
    """
    log.debug(f"Обработка запроса на добавление лайка к твиту - {tweet_id}")

    await add_like_to_tweet(tweet_id, session, api_key)

    return BaseResponse()


@router.delete(
    "/{tweet_id}/likes",
    response_model=BaseResponse,
    responses=error_responses
)
async def delete_like(
    tweet_id: int,
    session: AsyncSession = Depends(get_db),
    api_key: str = Header(None, alias="api-key"),
) -> BaseResponse:
    """
    Эндпоинт для удаления лайка из твита по его ID.
    Принимает ID твита и удаляет лайк из него в базе данных.
    Возвращает словарь с результатом операции.
    """
    log.debug(f"Обработка запроса на удаление лайка из твита - {tweet_id}")

    await remove_like_from_tweet(tweet_id, session, api_key)

    return BaseResponse()
