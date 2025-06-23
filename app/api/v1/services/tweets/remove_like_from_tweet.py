from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.v1.models import Tweet, Like
from app.api.v1.services.users import get_user_by_api_key
from app.api.exceptions import SomeError, ApiException, NotFoundError

from app.api.utils.logger import get_logger

log = get_logger("TweetRouterLogger")


async def remove_like_from_tweet(
    tweet_id: int, session: AsyncSession, api_key: str
):
    """
    Ассинхронная функция для удаления лайка из твита.
    """
    try:
        current_user = await get_user_by_api_key(session, api_key)

        tweet_result = await session.execute(
            select(Tweet).where(Tweet.id == tweet_id)
        )
        tweet = tweet_result.scalar_one_or_none()
        if tweet is None:
            raise NotFoundError(f"Твит с id {tweet_id} не найден")

        like_result = await session.execute(
            select(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == current_user.id
            )
        )
        like = like_result.scalar_one_or_none()
        if like is None:
            raise SomeError(
                f"Лайк от пользователя {current_user.id} не найден"
            )

        await session.execute(
            delete(Like).where(
                Like.tweet_id == tweet_id, Like.user_id == current_user.id
            )
        )
        await session.commit()

        log.debug(
            f"Пользователь {current_user.id} удалил лайк с твита {tweet_id}"
        )

    except ApiException as e:
        raise e
    except Exception as e:
        await session.rollback()
        error_message = f"Не удалось удалить лайк: {e}"
        log.error(error_message)
        raise SomeError(error_message)
